"""3Blue1Brown-style math scene (Manim CE): binary search halves the range each step.

Built with the 3brown1blue skill rules: Write() for text, ReplacementTransform for range changes,
dim-and-reveal for discarded items, white background to match the lesson UI.
Render: manim -qh --fps 30 -r 1920,1080 halving.py HalvingSearch
"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from common import ACC, BAD, FONT, HL, OK  # noqa: E402
from manim import *


class HalvingSearch(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        vals = list(range(1, 33, 2))  # 16 sorted values: 1,3,...,31
        target = 23

        boxes = VGroup(*[
            Square(side_length=0.62, color=BLACK, stroke_width=3).set_fill(WHITE, opacity=1)
            for _ in vals
        ]).arrange(RIGHT, buff=0.1).shift(DOWN * 0.2)
        labels = VGroup(*[
            Text(font=FONT, text=str(v), font_size=26, color=BLACK).move_to(b) for v, b in zip(vals, boxes)
        ])

        caption = Text(font=FONT, text="Sorted list, looking for 23", font_size=30, color=GREY_D)
        caption.next_to(boxes, DOWN, buff=1.1)

        self.play(
            LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.06),
            LaggedStart(*[Write(l) for l in labels], lag_ratio=0.06),
            run_time=2,
        )
        self.play(FadeIn(caption))

        def range_box(lo, hi):
            return SurroundingRectangle(VGroup(*boxes[lo:hi + 1]), color=ACC, buff=0.14, stroke_width=6)

        def mid_arrow(idx):
            top = boxes[idx].get_top()
            return Arrow(top + UP * 1.0, top + UP * 0.08, color=HL, buff=0, stroke_width=6)

        # Step 1: full range, check the middle (index 7 -> value 15)
        rng = range_box(0, 15)
        arrow = mid_arrow(7)
        self.play(Create(rng), GrowArrow(arrow))
        self.wait(1.0)

        new_caption = Text(font=FONT, text="Middle is 15. 15 < 23, so 23 must be on the right", font_size=28, color=BLACK)
        new_caption.move_to(caption)
        self.play(ReplacementTransform(caption, new_caption))
        self.wait(0.6)

        # Step 2: discard the left half (dim it)
        dim = [m.animate.set_opacity(0.2) for m in list(boxes[0:8]) + list(labels[0:8])]
        self.play(*dim, run_time=1.2)
        rng2 = range_box(8, 15)
        arrow2 = mid_arrow(11)
        self.play(ReplacementTransform(rng, rng2), arrow.animate.become(arrow2))
        self.wait(0.8)

        # Step 3: middle is 23 -> found
        found_caption = Text(font=FONT, text="Middle is 23. Found it in 2 checks, not 16", font_size=30, color=BLACK)
        found_caption.move_to(new_caption)
        self.play(ReplacementTransform(new_caption, found_caption))
        self.play(boxes[11].animate.set_fill(HL, opacity=1), run_time=0.8)
        self.wait(2.0)
