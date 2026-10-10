"""Binary search tree insert (3b1b style): insert 15, 7, 23, 11 and show the path each time.
Sections: 0 root 15, 1 insert 7 (go left), 2 insert 23 (go right), 3 insert 11 (left, then right).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from common import ACC, BAD, FONT, HL, OK, beats, section  # noqa: E402
from manim import *  # noqa: E402


def node(val, pos, color):
    c = Circle(radius=0.42, color=color, stroke_width=4).set_fill(WHITE, 1).move_to(pos)
    t = Text(font=FONT, text=str(val), font_size=30, color=BLACK).move_to(pos)
    return VGroup(c, t)


class BSTInsert(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        d = beats(4)
        ink = BLACK

        P = {15: UP * 2.0, 7: LEFT * 3.2 + UP * 0.4, 23: RIGHT * 3.2 + UP * 0.4, 11: LEFT * 1.6 + DOWN * 1.6}

        cap = Text(font=FONT, text="Insert 15 first. It becomes the root.", font_size=30, color=GREY_D).to_edge(DOWN, buff=0.6)
        n15 = node(15, P[15], ACC)
        section(self, d[0], ([FadeIn(cap), FadeIn(n15)], 1.4))

        # Section 1: 7 < 15, go left
        cap1 = Text(font=FONT, text="7 is smaller than 15, so go left.", font_size=30, color=GREY_D).to_edge(DOWN, buff=0.6)
        e1 = Line(P[15], P[7], color=ink, stroke_width=4, buff=0.45)
        n7 = node(7, P[7], ACC)
        section(self, d[1],
                ([FadeOut(cap), FadeIn(cap1), Create(e1)], 1.0),
                ([FadeIn(n7)], 0.8))

        # Section 2: 23 > 15, go right
        cap2 = Text(font=FONT, text="23 is bigger than 15, so go right.", font_size=30, color=GREY_D).to_edge(DOWN, buff=0.6)
        e2 = Line(P[15], P[23], color=ink, stroke_width=4, buff=0.45)
        n23 = node(23, P[23], ACC)
        section(self, d[2],
                ([FadeOut(cap1), FadeIn(cap2), Create(e2)], 1.0),
                ([FadeIn(n23)], 0.8))

        # Section 3: 11 < 15 -> left, 11 > 7 -> right of 7
        cap3 = Text(font=FONT, text="11 goes left of 15, then right of 7. Two comparisons.", font_size=30, color=GREY_D).to_edge(DOWN, buff=0.6)
        e3 = Line(P[7], P[11], color=ink, stroke_width=4, buff=0.45)
        n11 = node(11, P[11], HL)
        section(self, d[3],
                ([FadeOut(cap2), FadeIn(cap3), Create(e3)], 1.0),
                ([FadeIn(n11)], 0.8))
