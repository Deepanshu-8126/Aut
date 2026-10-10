"""Hindi TTS with Indic Parler-TTS (ai4bharat, Apache 2.0, free, commercial safe).

Pipeline contract (same as tts_words.synth_with_words):
    dur, words = synth_with_words(text, out_path)
    words = [{"word", "start", "end"}, ...]  -> popup/typing sync ke liye.

Notes:
- Parler word timestamps nahi deta. Har sentence alag generate hota hai, aur
  sentence ke andar words ko characters ke hisaab se time diya jaata hai.
  Agar faster-whisper installed hai to USE_WHISPER_ALIGN=1 se exact word timing
  milti hai (audio ko transcribe karke word timestamps).
- GPU (CUDA) par fast chalega. CPU par chalega, lekin slow (~RTF 3-4).
- Model ~0.9B params: GPU ~4-6 GB VRAM, CPU ~8 GB RAM.
- Output WAV 44.1 kHz (model ka sampling rate).

Usage (test): python3 pipeline/tts_parler_hi.py "Hindi text" out.wav
"""
import json
import os
import re
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

MODEL_ID = "ai4bharat/indic-parler-tts"
# Female Hindi voice. Caption ka tone pacing/clarity control karta hai.
SPEAKER = "Divya"
DESCRIPTION = (
    f"{SPEAKER} speaks in a clear, moderately paced and friendly teaching tone. "
    "The recording is of very high quality, with no background noise and the voice "
    "sounds close and clear."
)
GAP_SEC = 0.25          # sentences ke beech pause
USE_WHISPER_ALIGN = os.environ.get("USE_WHISPER_ALIGN", "0") == "1"

_model = None
_tok = None
_desc_tok = None
_device = None


def _load():
    global _model, _tok, _desc_tok, _device
    if _model is not None:
        return
    import torch
    from parler_tts import ParlerTTSForConditionalGeneration
    from transformers import AutoTokenizer

    _device = "cuda:0" if torch.cuda.is_available() else "cpu"
    _model = ParlerTTSForConditionalGeneration.from_pretrained(MODEL_ID).to(_device)
    _tok = AutoTokenizer.from_pretrained(MODEL_ID)
    _desc_tok = AutoTokenizer.from_pretrained(_model.config.text_encoder._name_or_path)


def release() -> None:
    global _model, _tok, _desc_tok
    _model = _tok = _desc_tok = None


def _sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[।.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def _gen(sentence: str) -> np.ndarray:
    d = _desc_tok(DESCRIPTION, return_tensors="pt").to(_device)
    p = _tok(sentence, return_tensors="pt").to(_device)
    out = _model.generate(
        input_ids=d.input_ids, attention_mask=d.attention_mask,
        prompt_input_ids=p.input_ids, prompt_attention_mask=p.attention_mask,
    )
    return out.cpu().numpy().squeeze().astype(np.float32)


def _split_words_by_chars(tokens: list[str], start: float, end: float) -> list[dict]:
    total = sum(max(1, len(t)) for t in tokens) or 1
    res, t = [], start
    span = end - start
    for tok in tokens:
        d = span * max(1, len(tok)) / total
        res.append({"word": tok, "start": round(t, 3), "end": round(t + d, 3)})
        t += d
    return res


def _whisper_align(wav: np.ndarray, sr: int, tokens: list[str]) -> list[dict] | None:
    """Optional: faster-whisper se word timestamps (sirf agar installed ho)."""
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        return None
    import tempfile
    model = WhisperModel("small", device="auto", compute_type="int8")
    with tempfile.NamedTemporaryFile(suffix=".wav") as f:
        sf.write(f.name, wav, sr)
        segs, _ = model.transcribe(f.name, language="hi", word_timestamps=True)
        ws = [w for s in segs for w in (s.words or [])]
    if not ws:
        return None
    return [{"word": tok, "start": round(w.start, 3), "end": round(w.end, 3)}
            for tok, w in zip(tokens, ws)] if len(ws) >= len(tokens) else None


def synth_with_words(text: str, out: Path) -> tuple[float, list[dict]]:
    _load()
    sr = _model.config.sampling_rate
    gap = np.zeros(int(sr * GAP_SEC), dtype=np.float32)
    chunks, words, t = [], [], 0.0
    all_tokens: list[str] = []
    for sent in _sentences(text):
        wav = _gen(sent)
        dur = len(wav) / sr
        tokens = sent.split()
        all_tokens += tokens
        words += _split_words_by_chars(tokens, t, t + dur)
        chunks += [wav, gap]
        t += dur + GAP_SEC
    full = np.concatenate(chunks) if chunks else np.zeros(sr, dtype=np.float32)
    if USE_WHISPER_ALIGN:
        exact = _whisper_align(full, sr, all_tokens)
        if exact:
            words = exact
    out = Path(out).with_suffix(".wav")
    out.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(out), full, sr)
    return round(len(full) / sr, 3), words


if __name__ == "__main__":
    text, out = sys.argv[1], Path(sys.argv[2])
    dur, words = synth_with_words(text, out)
    print(json.dumps({"duration": dur, "words": words}, ensure_ascii=False))
