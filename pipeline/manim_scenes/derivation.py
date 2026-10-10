"""Equation derivation (3b1b style): sum of 1..n, step by step with dim-and-reveal.
Sections: 0 setup, 1 pair the terms, 2 simplify, 3 final result boxed.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from common import ACC, BAD, FONT, HL, OK, beats, section  # noqa: E402
from manim import *  # noqa: E402


class EquationDerivation(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        d = beats(4)
        ink = BLACK

        s1 = MathTex(r"S = 1 + 2 + 3 + \cdots + n", font_size=60, color=ink).shift(UP * 1.2)
        cap = Text(font=FONT, text="Write the sum, then add it to itself, reversed.", font_size=30, color=GREY_D).to_edge(DOWN, buff=1.0)

        s2 = MathTex(r"2S = (n+1) + (n+1) + \cdots + (n+1)", font_size=60, color=ink).shift(DOWN * 0.2)
        cap2 = Text(font=FONT, text="Each pair adds to n+1, and there are n pairs.", font_size=30, color=GREY_D).to_edge(DOWN, buff=1.0)

        s3 = MathTex(r"2S = n(n+1)", font_size=60, color=ink).shift(DOWN * 0.2)
        cap3 = Text(font=FONT, text="Divide both sides by 2.", font_size=30, color=GREY_D).to_edge(DOWN, buff=1.0)

        s4 = MathTex(r"S = \frac{n(n+1)}{2}", font_size=72, color=ACC).shift(DOWN * 1.6)
        box = SurroundingRectangle(s4, color=HL, buff=0.25, stroke_width=6)

        section(self, d[0],
                ([Write(s1)], 1.6),
                ([FadeIn(cap)], 0.6))

        section(self, d[1],
                ([FadeOut(cap)], 0.4),
                ([FadeIn(cap2), TransformMatchingTex(s1, s2)], 1.4))

        section(self, d[2],
                ([FadeOut(cap2)], 0.4),
                ([FadeIn(cap3), TransformMatchingTex(s2, s3)], 1.4))

        section(self, d[3],
                ([FadeOut(cap3)], 0.4),
                ([Write(s4), Create(box)], 1.6))
