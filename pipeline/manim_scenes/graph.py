"""Graph / curve (3b1b style): f(x)=x^2, a tangent line, and the area under the curve.
Sections: 0 axes+curve, 1 tangent slope at x=1, 2 area from 0 to 2, 3 conclusion.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from common import ACC, BAD, FONT, HL, OK, beats, section  # noqa: E402
from manim import *  # noqa: E402


class GraphCurve(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        d = beats(4)
        ink = BLACK

        axes = Axes(x_range=[-3, 3, 1], y_range=[-1, 9, 2], x_length=9, y_length=5.2,
                    axis_config={"color": ink, "include_numbers": False, "include_tip": True},
                    tips=True).shift(DOWN * 0.4)
        graph = axes.plot(lambda x: x ** 2, x_range=[-2.2, 2.2], color=ACC)
        label = MathTex(r"f(x) = x^2", color=ACC, font_size=48).next_to(graph, UP, buff=0.2).shift(RIGHT * 1.2)
        cap = Text(font=FONT, text="Start with a simple curve.", font_size=30, color=GREY_D).to_edge(DOWN, buff=0.6)

        # tangent at x = 1: slope f'(1) = 2
        x0 = 1.0
        tangent = Line(axes.c2p(x0 - 0.9, 2 * (x0 - 0.9) - 1), axes.c2p(x0 + 0.9, 2 * (x0 + 0.9) - 1),
                       color=HL, stroke_width=6)
        dot = Dot(axes.c2p(x0, x0 ** 2), color=HL, radius=0.09)
        slope_txt = MathTex(r"f'(1) = 2", color=HL, font_size=44).next_to(tangent, RIGHT, buff=0.3).shift(UP * 0.4)
        cap2 = Text(font=FONT, text="The slope at x = 1 is 2. That is the derivative.", font_size=30, color=GREY_D).to_edge(DOWN, buff=0.6)

        area = axes.get_area(graph, x_range=[0, 2], color=HL, opacity=0.55)
        area_lbl = MathTex(r"\int_0^2 x^2\,dx = \frac{8}{3}", color=BLACK, font_size=44).move_to(axes.c2p(1.0, 0.8))
        cap3 = Text(font=FONT, text="The area under the curve from 0 to 2 is 8/3.", font_size=30, color=GREY_D).to_edge(DOWN, buff=0.6)

        cap4 = Text(font=FONT, text="Slope tells how fast it changes. Area tells how much it adds up.", font_size=30,
                    color=GREY_D).to_edge(DOWN, buff=0.6)

        section(self, d[0],
                ([Create(axes)], 1.4),
                ([Create(graph), Write(label)], 1.6),
                ([FadeIn(cap)], 0.5))

        section(self, d[1],
                ([FadeOut(cap)], 0.4),
                ([FadeIn(cap2), FadeIn(dot), Create(tangent), Write(slope_txt)], 1.6))

        section(self, d[2],
                ([FadeOut(cap2), FadeOut(tangent), FadeOut(slope_txt), FadeOut(dot)], 0.8),
                ([FadeIn(area), FadeIn(cap3)], 1.4),
                ([Write(area_lbl)], 0.8))

        section(self, d[3],
                ([FadeOut(cap3)], 0.4),
                ([FadeIn(cap4)], 0.8))
