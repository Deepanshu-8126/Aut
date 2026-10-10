// Pre-render code (Shiki syntax highlight, vdo-style) and formulas (KaTeX) for each scene.
// Input (stdin): JSON array of { id, code, code_lang, diff, formula }
// Output (stdout): JSON array of { id, code_spans, formula_html }
import { createHighlighter } from "shiki";
import katex from "katex";

const chunks = [];
for await (const c of process.stdin) chunks.push(c);
const scenes = JSON.parse(Buffer.concat(chunks).toString("utf8"));

const highlighter = await createHighlighter({
  themes: ["github-light"],
  langs: ["python", "javascript", "typescript", "java", "cpp", "text"],
});

function escapeHtml(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

// Returns html lines; each token is a span with its color, so typing can reveal char spans.
function highlightLines(code, lang, isDiff) {
  const langs = ["python", "javascript", "typescript", "java", "cpp"];
  const useLang = langs.includes(lang) ? lang : "text";
  const lines = code.split("\n");
  const lineHtml = lines.map((raw) => {
    let line = raw;
    let mark = "";
    if (isDiff && /^\+ /.test(line)) { mark = "add"; line = line.slice(2); }
    else if (isDiff && /^- /.test(line)) { mark = "del"; line = line.slice(2); }
    const tokens = highlighter.codeToTokens(line === "" ? " " : line, { lang: useLang, theme: "github-light" }).tokens[0] || [];
    const chars = tokens.map((t) => {
      const color = t.color || "#24292f";
      return [...t.content].map((ch) => `<span class="ch" style="color:${color}">${escapeHtml(ch)}</span>`).join("");
    }).join("");
    return { mark, html: chars || "&nbsp;" };
  });
  return lineHtml.map((l) => {
    const cls = l.mark ? `line ${l.mark}` : "line";
    const prefix = l.mark === "add" ? "+" : l.mark === "del" ? "-" : " ";
    return `<div class="${cls}"><span class="gutter">${prefix}</span>${l.html}</div>`;
  }).join("");
}

const out = scenes.map((s) => {
  const res = { id: s.id };
  if (s.code) {
    res.code_html = highlightLines(s.code, (s.code_lang || "python").toLowerCase(), !!s.diff);
    res.code_chars = [...s.code].length;
  }
  if (s.formula) {
    try {
      res.formula_html = katex.renderToString(s.formula, { throwOnError: false, displayMode: true });
    } catch (e) {
      res.formula_html = escapeHtml(s.formula);
    }
  }
  return res;
});

process.stdout.write(JSON.stringify(out));
