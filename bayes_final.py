from manim import *
import math
import numpy as np
from math import erf, sqrt, pi
from pi_creature_scene import *
from manim.utils.space_ops import midpoint

class Person(SVGMobject):
    def __init__(
        self,
        file_name="assets/person.svg",
        height=1.5,
        stroke_width=0,
        fill_opacity=1,
        fill_color=GREY_B,
        **kwargs
    ):
        super().__init__(
            file_name=file_name,
            stroke_width=stroke_width,
            fill_opacity=fill_opacity,
            fill_color=fill_color,
            **kwargs
        )

        self.set_height(height)
def give_pop_plusses(pop):
            for icon in pop:
                plus = Text("+", weight=BOLD, color=YELLOW)
                plus.set_width(icon.get_width())
                plus.move_to(icon.get_corner(UR))
                icon.add(plus)
def get_positive_symbol():
        circle = Circle(
            radius=1,
            color=WHITE,
            fill_opacity=0.3,
            stroke_width=4
        )

        vertical = Line(
            start=UP,
            end=DOWN,
            stroke_width=6
        )
        horizontal = Line(
            start=LEFT,
            end=RIGHT,
            stroke_width=6
        )

        plus = VGroup(vertical, horizontal).set_color(YELLOW).scale(0.5)

        plus.move_to(circle.get_center())
        return VGroup(circle, plus)
class SportsBettingCond(Scene):
    def construct(self):
        self.add_sound("voiceovers/SportsBettingCond_part1.mp3")
        # 1. Title
        title = Text("Cá cược thể thao trực tiếp", font="Noto Sans", font_size=36).to_edge(UP)
        title[:6].set_color(YELLOW)
        self.play(Write(title))
        ball = ImageMobject("assets/ball.png").scale(0.05).move_to(title[0])
        self.play(FadeIn(ball, shift=DOWN), title.animate.next_to(ball, RIGHT))
        foolball_field = ImageMobject("assets/foolball-field.png").scale(0.6)
        label_a = Label(
            label=Text('Team A', font='sans-serif'),
            box_config = {
                "color" : BLUE,
                "fill_opacity" : 0.75
            }
        )
        label_a.scale(0.6)
        label_b = Label(
            label=Text('Team B', font='sans-serif'),
            box_config = {
                "color" : RED,
                "fill_opacity" : 0.75
            }
        )
        label_b.scale(0.6)
        Group(label_a, label_b).arrange(RIGHT, LARGE_BUFF)
        self.play(FadeIn(foolball_field))
        self.play(FadeIn(label_a))
        self.play(FadeIn(label_b))
        question = Text("?", font_size=96, weight=BOLD).shift(UP)
        self.play(FadeIn(question, shift=UP), run_time=2)
        self.wait(2)
        self.play(FadeOut(question, label_a, label_b, foolball_field))

        # 2. Setup the Odds Gauge
        gauge_box = Rectangle(width=8, height=1, color=WHITE)
        team_a_fill = Rectangle(width=4, height=1, color=BLUE, fill_opacity=0.6).align_to(gauge_box, LEFT)
        team_b_fill = Rectangle(width=4, height=1, color=RED, fill_opacity=0.6).align_to(gauge_box, RIGHT)
        
        text_a = Text("Team A (50%)", font="Noto Sans", font_size=24).next_to(team_a_fill, UP)
        text_b = Text("Team B (50%)", font="Noto Sans", font_size=24).next_to(team_b_fill, UP)
        
        self.play(Create(gauge_box), FadeIn(team_a_fill, team_b_fill), Write(text_a), Write(text_b))
        self.wait(2)
        football = ImageMobject("assets/footbal.png").scale(0.3).to_corner(UR)
        self.play(FadeIn(football))
        self.wait(2)

        # 3. The Condition: A Key Event
        event_text = Text("VÀO! Team A ghi bàn", font="Noto Sans", font_size=32, color=YELLOW).shift(DOWN * 1.5)
        self.add_sound("voiceovers/victory_sound.mp3")
        self.play(Write(event_text), Flash(event_text, color=YELLOW))
        
        # 4. Updating the Probability (The Shift)
        # New Probability: Team A 80%, Team B 20%
        new_label_a = Text("Team A (80%)", font="Noto Sans", font_size=24, color=BLUE).move_to(text_a)
        new_label_b = Text("Team B (20%)", font="Noto Sans", font_size=24, color=RED).move_to(text_b)
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(
            team_a_fill.animate.stretch_to_fit_width(6.4, about_edge=LEFT),
            team_b_fill.animate.stretch_to_fit_width(1.6, about_edge=RIGHT),
            Transform(text_a, new_label_a),
            Transform(text_b, new_label_b),
            run_time=2
        )
        self.wait(3)
        new_label_a_strong = Text("Team A (90%)", font="Noto Sans", font_size=24, color=BLUE).move_to(text_a)
        new_label_b_strong = Text("Team B (10%)", font="Noto Sans", font_size=24, color=RED).move_to(text_b)
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(
            team_a_fill.animate.stretch_to_fit_width(7.2, about_edge=LEFT),
            team_b_fill.animate.stretch_to_fit_width(0.8, about_edge=RIGHT),
            Transform(text_a, new_label_a_strong),
            Transform(text_b, new_label_b_strong),
            run_time=2
        )
        self.wait()

        new_label_a_weak = Text("Team A (60%)", font="Noto Sans", font_size=24, color=BLUE).move_to(text_a)
        new_label_b_weak = Text("Team B (40%)", font="Noto Sans", font_size=24, color=RED).move_to(text_b)
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(
            team_a_fill.animate.stretch_to_fit_width(4.8, about_edge=LEFT),
            team_b_fill.animate.stretch_to_fit_width(3.2, about_edge=RIGHT),
            Transform(text_a, new_label_a_weak),
            Transform(text_b, new_label_b_weak),
            run_time=2
        )
        self.wait(4)

        self.play(FadeOut(ball, title, text_a, text_b, gauge_box, team_a_fill, team_b_fill, event_text))

        # Conceptual rule (no name yet)
        rule = Text(
            "Niềm tin được cập nhật \n= Niềm tin trước đó + Bằng chứng mới",
            font_size=36, font="Noto Sans"
        )
        rule[:18].set_color(GREEN)
        rule[19:33].set_color(BLUE)
        rule[34:].set_color(YELLOW)
        ball.scale(2).next_to(rule, UP).shift(UP * 3)

        self.play(Write(rule), run_time=3)
        self.wait(4)
        educated = ImageMobject("assets/educated.png").scale(0.3).to_corner(UL)
        self.play(FadeIn(educated))
        self.wait(2)
        self.play(Indicate(rule[34:]))
        emotion = Text("Cảm xúc", font="Noto Sans").scale(0.7)
        heuristics = Text("Phán đoán", font="Noto Sans").scale(0.7)
        VGroup(emotion, heuristics).arrange(RIGHT, LARGE_BUFF).to_edge(UP, LARGE_BUFF)
        cross1 = Cross(emotion)
        self.play(FadeIn(emotion), Create(cross1))
        cross2 = Cross(heuristics)
        self.play(FadeIn(heuristics), Create(cross2))
        self.wait(3)
        news = ImageMobject("assets/news.png").scale(0.3).to_edge(UP)
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(FadeOut(emotion, heuristics, cross1, cross2),
                  FadeIn(news, shift=DOWN))
        self.wait()
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(FadeOut(news, shift=UP),
                  ball.animate.shift(DOWN * 3).rotate(PI),
                  rate_func=rate_functions.ease_out_bounce, run_time=2)
        self.wait()
        
        self.play(FadeOut(ball, football, educated))

        # Transform into formal idea
        formal = Text(
            "Một quy tắc để cập nhật niềm tin \nkhi có thông tin mới",
            font_size=36, font="Noto Sans"
        )
        self.add_sound("voiceovers/SportsBettingCond_part2.mp3")
        self.play(Transform(rule, formal))
        self.wait(2)

        # Final reveal
        bayes = Text(
            "Định lý Bayes",
            font_size=48,
            weight=BOLD, font="Noto Sans"
        )
        self.add_sound("voiceovers/shine2.mp3")
        self.play(
            FadeOut(rule),
            FadeIn(bayes)
        )
        self.wait(3)
class DiceScene(Scene):
    def construct(self):
        self.wait()
        
        gauge_box = Rectangle(width=8, height=1, color=WHITE)
        left_part = Rectangle(width=3.5, height=1, color=GREEN, fill_opacity=0.6).align_to(gauge_box, LEFT)
        right_part = Rectangle(width=4.5, height=1, color=GRAY, fill_opacity=0.6).align_to(gauge_box, RIGHT)
        VGroup(gauge_box, left_part, right_part).shift(2*UP)
        text_belief = Text("Niềm tin", font="Noto Sans", color=GREEN, font_size=36).next_to(gauge_box, UP, aligned_edge=LEFT)
        understood = SVGMobject("assets/46.svg").to_edge(LEFT, LARGE_BUFF).set_z_index(3)

        self.play(FadeIn(understood), Create(gauge_box), FadeIn(left_part, right_part), Write(text_belief))
        self.wait()
        self.add_sound("voiceovers/DiceScene1.mp3")
        evidence = Text("bằng chứng", color=YELLOW, font="Noto Sans", font_size=24)
        evidence.move_to(understood).to_edge(RIGHT)
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(
            left_part.animate.stretch_to_fit_width(4.5, about_edge=LEFT),
            right_part.animate.stretch_to_fit_width(3.5, about_edge=RIGHT),
            FadeOut(evidence, target_position=understood),
            run_time=2
        )
        self.wait()
        evidence.move_to(understood).to_edge(RIGHT)
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(
            left_part.animate.stretch_to_fit_width(3, about_edge=LEFT),
            right_part.animate.stretch_to_fit_width(5, about_edge=RIGHT),
            FadeOut(evidence, target_position=understood),
            run_time=2
        )
        self.wait()
        evidence.move_to(understood).to_edge(RIGHT)
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(
            left_part.animate.stretch_to_fit_width(4, about_edge=LEFT),
            right_part.animate.stretch_to_fit_width(4, about_edge=RIGHT),
            FadeOut(evidence, target_position=understood),
            run_time=2
        )
        self.wait()
        self.play(FadeOut(understood, left_part, right_part, gauge_box, text_belief))
        cond_prob_text = Text(
            "Xác suất có điều kiện", gradient=[RED, YELLOW],
            font_size=36, font="Noto Sans"
        )
        self.play(Write(cond_prob_text))
        self.wait()
        self.play(FadeOut(cond_prob_text))
        
        dices = VGroup(*[SVGMobject(f"assets/dice_{i}.svg").scale(0.4) for i in range(1, 7)]).arrange(RIGHT)
        dices[5].set_fill(RED)
        six_prob = MathTex("P(6)=\\frac{1}{6}")
        six_prob[0][2].set_color(RED)
        even_prob = MathTex("P(so chan)=\\frac{1}{2}")
        cond_prob = MathTex(r"P(6 \mid so chan)=\frac{1}{3}")
        cond_prob[0][2].set_color(RED)
        VGroup(dices, six_prob, even_prob, cond_prob).arrange(DOWN)
       
        even_number = Text("số chẵn", color=YELLOW, font="Noto Sans").scale(0.65)
        even_number.move_to(even_prob[0][2:8])
        even_prob[0][2:8].set_opacity(0)

        even_number_condition = even_number.copy()
        even_number_condition.move_to(cond_prob[0][4:10])
        cond_prob[0][4:10].set_opacity(0)
        self.add_sound("voiceovers/shine2.mp3")
        self.play(*[FadeIn(dice) for dice in dices])
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(FadeIn(six_prob[0][:2]),
                  Transform(dices[5].copy(), six_prob[0][2:3]))
        self.play(Write(six_prob[0][3:]))
        self.wait(4)
        
        self.play(FadeIn(even_prob[0][:2], even_prob[0][8]), Write(even_number))
        self.play(FadeIn(even_prob[0][9:]))
        self.wait()
        boxes = VGroup()
        for i in [1, 3, 5]:
            box = SurroundingRectangle(dices[i], buff=0.1, color=YELLOW, corner_radius=0.2)
            boxes.add(box)
        self.play(*[Create(box) for box in boxes])
        self.wait()
        self.play(*[FadeOut(box) for box in boxes])
        self.wait()
        self.play(Circumscribe(six_prob, color=BLUE), run_time=2)
        self.play(Circumscribe(even_prob, color=BLUE), run_time=2)
        self.wait(2)
        self.play(Write(cond_prob[0][:3]))
        self.wait()
        self.play(FadeIn(cond_prob[0][3]))
        self.play(Write(even_number_condition), FadeIn(cond_prob[0][10]))
        self.wait()
        self.add_sound("voiceovers/wiggle.mp3")
        self.play(Wiggle(dices[5]), run_time=2)
        self.wait(3.5)
        self.play(LaggedStartMap(Create, boxes, lag_ratio=1.5))
        self.wait(4)
        self.play(Write(cond_prob[0][11:]))
        self.wait(2.5)

        prob_one = MathTex("1").move_to(cond_prob[0][12:]).shift(0.6*LEFT)
        self.play(Swap(even_number_condition, cond_prob[0][2]),
                  cond_prob[0][:2].animate.shift(0.65*LEFT),
                  cond_prob[0][3].animate.shift(0.6*RIGHT),
                  cond_prob[0][4:12].animate.shift(0.6*LEFT)
                  )
        self.play(cond_prob[0][12:].animate.set_color(GRAY_E))
        self.wait()
        self.play(Circumscribe(even_number_condition, color=BLUE))
        self.play(Circumscribe(cond_prob[0][2], color=BLUE))
        self.add_sound("voiceovers/click.wav")
        self.play(Transform(cond_prob[0][12:], prob_one))
        self.wait(5)
class ConditionalProbability(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/ConditionalProbability_part1.mp3")
        equation = MathTex(
            r"P(A \mid B)",
            "=",
            r"\frac{P(B \mid A)P(A)}{P(B)}"
        )
        equation[0][2].set_color(RED)
        equation[0][-2].set_color(YELLOW)
        equation[2][2].set_color(YELLOW)
        equation[2][4].set_color(RED)
        equation[2][8].set_color(RED)
        equation[2][-2].set_color(YELLOW)
        given = equation[0][3]

        equation.scale(1.2)
        equation.move_to(ORIGIN)

        self.play(Write(equation))
        self.add_sound("voiceovers/shine2.mp3")
        self.play(Flash(equation, line_length=1, flash_radius=equation.width/2, 
                        run_time=2, num_lines=20, rate_func=rush_from))
        # box_given = SurroundingRectangle(given, color=GREEN)
        # self.play(Create(box_given))
        self.add_sound("voiceovers/line.mp3")
        self.play(given.animate.scale(2), run_time=5, rate_func=there_and_back)
        self.wait(3)
        self.play(Circumscribe(equation[0][2], color=BLUE))
        self.play(Circumscribe(equation[0][-2], color=BLUE))
        self.wait()
        self.play(Circumscribe(equation, color=BLUE))
        self.wait()
        self.play(Circumscribe(equation[0], color=BLUE))
        self.wait()
        self.play(Circumscribe(equation[2][:6], color=BLUE))
        self.wait()
        self.play(Circumscribe(equation[2][6:10], color=BLUE))
        self.wait()
        self.play(Circumscribe(equation[2][11:], color=BLUE))
        self.wait()
        box = SurroundingRectangle(equation, buff=MED_LARGE_BUFF, color=BLUE)
        self.play(Create(box))
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(VGroup(box, equation).animate.scale(0.8).to_edge(UP))
        # First equation (Bayes' theorem form)
        eq1 = MathTex(
            r"P(\text{so chan}\mid 6)",
            "=",
            r"\frac{P(6\mid \text{so chan})\,P(\text{so chan})}{P(6)}"
        )
        eq1[0][-2].set_color(YELLOW)
        eq1[2][2].set_color(YELLOW)
        eq1[2][-2].set_color(YELLOW)

        # Second equation (substitution of values)
        eq2 = MathTex(
            r"P(\text{so chan}\mid 6)",
            "=",
            r"\frac{\frac{1}{3}\times\frac{1}{2}}{\frac{1}{6}}",
            "=",
            r"1"
        )
        eq2[0][-2].set_color(YELLOW)

        # Positioning
        # eq1.to_edge(UP)
        eq2.next_to(eq1, DOWN, buff=1)

        even_number = Text("số chẵn", color=RED, font="Noto Sans").scale(0.65)
        even_number.move_to(eq1[0][2:8])
        eq1[0][2:8].set_opacity(0)
        even_number2 = even_number.copy()
        even_number2.move_to(eq1[2][4:10])
        eq1[2][4:10].set_opacity(0)
        even_number3 = even_number.copy()
        even_number3.move_to(eq1[2][13:19])
        eq1[2][13:19].set_opacity(0)
        even_number4 = even_number.copy()
        even_number4.move_to(eq2[0][2:8])
        eq2[0][2:8].set_opacity(0)

        # Animations
        self.play(Write(eq1), Write(even_number),
                  Write(even_number2), Write(even_number3))
        self.wait()
        even_number_copy = even_number.copy()
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(TransformMatchingTex(eq1.copy(), eq2),
                  Transform(even_number_copy, even_number4))
        self.wait()
        self.add_sound("voiceovers/ConditionalProbability_part2.mp3")
        penguin = ImageMobject("assets/penguin.png").scale(0.25)
        self.wait()
        self.play(FadeOut(eq1, eq2, even_number, even_number2, even_number3, even_number_copy))
        self.wait()
        self.add_sound("voiceovers/win.mp3")
        self.play(FadeIn(penguin))
        self.wait(5)
class BayesTheoremMedical(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/BayesTheoremMedical.mp3")
        title = Text("Xét nghiệm y tế", font="Noto Sans", weight=BOLD, font_size=40).to_edge(UP)
        subtitle = Text("Tỷ lệ mắc bệnh: 1% | Độ nhạy: 99%, Độ đặc hiệu: 95%", font="Noto Sans", font_size=24, color=BLUE).next_to(title, DOWN)
        sensitive = subtitle[22:25]
        specific = subtitle[36:]
        self.play(Write(title))
        self.add_sound("voiceovers/disintegration-into-small-particles.mp3")
        self.wait(3)
        positive_symbol = get_positive_symbol()
        circle, plus = positive_symbol
        self.play(Create(circle))
        self.add_sound("voiceovers/aww.mp3")
        self.play(Create(plus))
        self.wait()
        question = Text("Xác suất bạn thật sự bị bệnh là bao nhiêu?", font="Noto Sans", font_size=24, color=YELLOW).next_to(title, DOWN)
        self.play(Write(question))
        self.wait(2)
        arrow = MathTex(r"\rightarrow").next_to(positive_symbol, RIGHT)
        certain = Text("Gần như chắc chắn", color=RED, font="Noto Sans")
        certain.scale(0.7).next_to(arrow, RIGHT)
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(FadeIn(arrow), Write(certain))
        self.wait()
        self.play(certain.animate.set_color(GRAY))
        self.play(FadeOut(positive_symbol, question, certain, arrow))
        self.play(Write(subtitle), run_time=4)
        self.wait(4)
        sensitivity = MathTex(
            "P(+ | D) = 99\%", 
            font_size=42, 
            tex_to_color_map={
                "D": RED,
            },
            substrings_to_isolate=list("P(|)=")
        )
        sensitivity[2].set_color(YELLOW)
        D = sensitivity.get_parts_by_tex("D")[0]
        index = sensitivity.submobjects.index(D)
        sick = Person()
        sick.set_color(RED)
        sick.replace(D)
        sensitivity.submobjects[index] = sick
        sick.set_height(0.5)

        specificity = MathTex(
            "P(- | N) = 95\%", 
            font_size=42, 
            tex_to_color_map={
                "N": BLUE,
            },
            substrings_to_isolate=list("P(|)=")
        )
        specificity[2].set_color(PURPLE)
        N = specificity.get_parts_by_tex("N")[0]
        index = specificity.submobjects.index(N)
        normal = Person()
        normal.set_color(BLUE)
        normal.replace(N)
        specificity.submobjects[index] = normal
        normal.set_height(0.5)
        accuracy_group = VGroup(sensitivity, specificity).arrange(DOWN, LARGE_BUFF)
        self.play(Write(sensitivity))
        self.wait(3)
        self.play(Write(specificity))
        # Legend
        legend = VGroup(
            Person(fill_color=RED, height=0.5), Text("Mắc bệnh", font="Noto Sans", font_size=22),
            Person(fill_color=BLUE, height=0.5), Text("Không mắc bệnh", font="Noto Sans", font_size=22),
        ).arrange_in_grid(rows=2, cols=4, buff=0.4)

        legend.to_corner(DR)
        self.play(FadeIn(legend))
        self.wait(3)
        self.play(accuracy_group.animate.next_to(positive_symbol, LEFT, LARGE_BUFF))
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(FadeIn(positive_symbol, shift=UP))
        self.wait(2)
        correct_prob  = Text("16.7%", color=GREEN, font="Noto Sans").next_to(arrow, RIGHT)
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(FadeIn(arrow), Write(correct_prob))
        self.wait(2)
        question = Text("?", font_size=40, weight=BOLD).next_to(arrow, UP)
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(FadeIn(question, shift=UP))
        self.wait()
        self.add_sound("voiceovers/wobble.mp3")
        self.play(FadeOut(accuracy_group, question, positive_symbol, arrow, correct_prob))

        population = VGroup(*[Person().set_height(0.5).set_fill(BLUE, opacity=1) for _ in range(100)]).arrange_in_grid(rows=5, cols=20, buff=0.2)
        population.shift(LEFT*3 + DOWN)
        self.play(ShowIncreasingSubsets(population), run_time=5)
        self.wait(2)

        sick_person = population[50]
        label_sick = Text("1 người mắc bệnh", font="Noto Sans", font_size=20, color=RED).next_to(population, UP)
        self.play(Write(label_sick), sick_person.animate.set_fill(RED, opacity=1), run_time=2)
        self.wait()
        self.play(Indicate(sensitive))
        self.wait()

        false_positives = VGroup(population[2], population[18], population[11],
                                 population[72], population[96]) # Picking a random healthy square
        self.add_sound("voiceovers/click.wav")
        give_pop_plusses(VGroup(sick_person))
        self.play(FocusOn(sick_person))
        self.wait(4)
        self.add_sound("voiceovers/click.wav")
        give_pop_plusses(false_positives)
        self.wait(2)
        self.play(Indicate(specific))
        self.wait(2)

        positives_group = VGroup(sick_person.copy(), *[false_positive.copy() for false_positive in false_positives]).arrange(RIGHT, buff=0.5).center()
        
        explanation = Text("Nếu kết quả xét nghiệm dương tính, bạn là một trong 6 người này:", font="Noto Sans", font_size=24).next_to(positives_group, UP, buff=1)
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(
            *[FadeOut(person) for person in population],
            FadeOut(label_sick),
            Transform(VGroup(sick_person.copy(), false_positives.copy()), positives_group),
            Write(explanation)
        )
        self.wait(3)
        
        math = MathTex(
            "P(D | +) = \\frac{1}{1 + 5} = 16.7\%", 
            font_size=42, 
            tex_to_color_map={
                "D": RED,
            },
            substrings_to_isolate=list("P(|)=")
        ).next_to(positives_group, DOWN, buff=1)
        math[5].set_color(YELLOW)
        D = math.get_parts_by_tex("D")[0]
        index = math.submobjects.index(D)
        sick = Person()
        sick.set_color(RED)
        sick.replace(D)
        math.submobjects[index] = sick
        sick.set_height(0.5)
        
        self.play(Write(math))
        self.add_sound("voiceovers/bad-to-the-bone.mp3")
        self.wait(4)

class DiseaseBayes(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/DiseaseBayes1.mp3")
        formula = MathTex(
            r"P(D \mid +) = {P(+ \mid D) P(D) \over P(+ \mid D) P(D) + P(+ \mid N) P(N)}",
            tex_to_color_map={
                "D": RED,
                "N": BLUE,
                "+": YELLOW,
            },
            substrings_to_isolate=list("P(|)=")
        )
        all_positive = MathTex(r"P(+)",
                               tex_to_color_map={
                                    "+": YELLOW,
                                },
                               substrings_to_isolate=list("P()"))
        over_part = formula.get_part_by_tex(r"\over")
        Ns = formula.get_parts_by_tex("N")
        Ds = formula.get_parts_by_tex("D")
        
        for N in Ns:
            index = formula.submobjects.index(N)
            normal_person = Person()
            normal_person.set_color(BLUE)
            normal_person.replace(N)
            formula.submobjects[index] = normal_person
            normal_person.set_height(0.5)

        for D in Ds:
            index = formula.submobjects.index(D)
            sick_person = Person()
            sick_person.set_color(RED)
            sick_person.replace(D)
            formula.submobjects[index] = sick_person
            sick_person.set_height(0.5)
        eq = formula[7]
        lhs = formula[:6]
        lhs.save_state()
        lhs.center()

        sicky = lhs[2]
        sick_words = Text("Bạn bị bệnh", font="Noto Sans").scale(0.65)
        sick_words[-4:].set_color(RED)
        sick_words.next_to(sicky, UP, 2 * LARGE_BUFF)

        positive_words = Text("Kết quả xét nghiệm dương tính", font="Noto Sans").scale(0.65)
        positive_words.set_color(YELLOW)
        positive_words.next_to(lhs[4], DOWN, 2 * LARGE_BUFF)

        sick_arrow = Arrow(sicky.get_top(), sick_words.get_bottom())
        positive_arrow = Arrow(lhs[4].get_bottom(), positive_words.get_top())

        arrow_groups = VGroup(
            sick_words, sick_arrow,
            positive_words, positive_arrow,
        )

        sicky.save_state()
        sicky.set_color(YELLOW)
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(lhs, shift=DOWN))
        self.wait()
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(
            Restore(sicky),
            GrowArrow(sick_arrow),
            FadeIn(sick_words, shift=DOWN),
        )
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(
            GrowArrow(positive_arrow),
            FadeIn(positive_words, shift=UP),
        )
        self.wait(2)
        over_part.scale(0.5)
        eq.save_state()
        eq.next_to(over_part, LEFT)
        self.add_sound("voiceovers/DiseaseBayes2.mp3")
        self.play(
            lhs.animate.next_to(eq, LEFT),
            MaintainPositionRelativeTo(arrow_groups, lhs),
            FadeIn(eq),
        )

        def get_formula_slice(*indices):
            return VGroup(*[formula[i] for i in indices])
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(
            TransformFromCopy(
                get_formula_slice(0, 1, 2, 5),
                get_formula_slice(16, 17, 18, 19),
            ),
        )

        lhs_copy = formula[:6].copy()
        likelihood = formula[9:14]
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(lhs_copy.animate.next_to(likelihood, UP))
        self.play(Swap(lhs_copy[2], lhs_copy[4]))
        self.play(lhs_copy.animate.move_to(likelihood))
        all_positive.move_to(formula[21:])
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(
            Create(over_part),
            TransformFromCopy(
                get_formula_slice(9, 10, 11, 14),
                all_positive,
            ),
        )
        self.wait()
        formula[33].set_color(WHITE)
        
        test_info = Text("Tỷ lệ mắc bệnh: 1% | Độ nhạy: 99%, Độ đặc hiệu: 95%", font="Noto Sans", font_size=24, color=BLUE).to_corner(UR)
        prevalance = test_info[:14]
        sensitive = test_info[15:25]
        specific = test_info[26:]
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(test_info))
        self.wait(2)
        prior_brace = Brace(formula[16:20], UP)
        prior_val = prior_brace.get_tex("0.01")
        likelihood_brace = Brace(likelihood, UP)
        likelihood_val = likelihood_brace.get_tex("0.99")

        sick_positive_brace = Brace(formula[21:27], DOWN)
        sick_positive_val = sick_positive_brace.get_tex("0.99")
        sick_brace = Brace(formula[27:32], DOWN)
        sick_val = sick_brace.get_tex("0.01")
        normal_positive_brace = Brace(formula[34:42], DOWN)
        normal_positive_val = normal_positive_brace.get_tex("0.05")
        normal_brace = Brace(formula[42:], DOWN)
        normal_val = normal_brace.get_tex("0.99")
        brace_group = VGroup(prior_brace, prior_val, likelihood_brace, likelihood_val,
                             sick_positive_brace, sick_positive_val, sick_brace, sick_val,
                             normal_positive_brace, normal_positive_val, normal_brace, normal_val)
        self.play(FadeIn(prior_brace))
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(prior_val))
        self.play(Indicate(prevalance))
        self.wait(2)
        self.play(FadeIn(likelihood_brace))
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(likelihood_val))
        self.wait()
        self.play(Indicate(sensitive))
        self.wait()
        self.play(Circumscribe(all_positive, color=GREEN))
        self.wait()
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(Restore(lhs), Restore(eq),
                  over_part.animate.scale(2),
                  MaintainPositionRelativeTo(arrow_groups, lhs),
                  Transform(all_positive, formula[21:]))
        self.wait(2)
        self.play(FadeIn(sick_brace))
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(sick_val))
        self.play(FadeIn(sick_positive_brace))
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(sick_positive_val))    
        self.wait()      
        self.play(Indicate(prevalance))
        self.wait()
        self.play(Indicate(sensitive))
        self.wait()
        self.play(FadeIn(normal_brace))
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(normal_val))
        self.play(FadeIn(normal_positive_brace))
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(normal_positive_val))  
        self.wait(2)      
        self.play(Indicate(prevalance))
        self.wait(2)
        self.play(Indicate(specific))
        self.wait()
        self.wait(2)
        final_numbers = MathTex(
            "\\frac{0.99 \\times 0.01}{(0.99 \\times 0.01) + (0.05 \\times 0.99)}",
            font_size=34).next_to(eq, RIGHT)
        
        result = MathTex("\\approx 16.7\%", font_size=40, color=GREEN).next_to(final_numbers, RIGHT)
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(FadeOut(brace_group),
                  Transform(VGroup(formula[8:], lhs_copy, all_positive), final_numbers))
        self.wait()
        self.add_sound("voiceovers/DiseaseBayes3.mp3")
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(result))
        self.wait(2)
        self.play(Flash(result))
        self.wait()
        hand = ImageMobject("assets/hand.png").scale(0.15).next_to(result, UP)
        self.add_sound("voiceovers/drum-roll.mp3")
        self.play(FadeIn(hand))
        self.wait(4)
class DiseaseBayesSecond(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/DiseaseBayesSecond1.mp3")
        title = Text("Xét nghiệm lần hai", font_size=40, font="Noto Sans")
        self.play(Write(title))
        self.wait()     
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(title.animate.to_edge(UP))
        subtitle = Text("Tỷ lệ mắc bệnh: 1% | Độ nhạy: 99%, Độ đặc hiệu: 95%", font="Noto Sans", font_size=24, color=BLUE).next_to(title, DOWN)
        self.play(FadeIn(subtitle))

        positive_symbol = get_positive_symbol()
        circle, plus = positive_symbol
        self.play(Create(circle))
        self.add_sound("voiceovers/aww.mp3")
        self.play(Create(plus))
        self.wait()
        self.play(FadeOut(positive_symbol))
        genaral_formula = MathTex(
            "P(A|B) = \\frac{P(B|A)P(A)}{P(B)}",
            font_size=60
        )
        genaral_formula[0][2].set_color(RED)
        genaral_formula[0][4].set_color(YELLOW)
        genaral_formula[0][9].set_color(YELLOW)
        genaral_formula[0][11].set_color(RED)
        genaral_formula[0][15].set_color(RED)
        genaral_formula[0][-2].set_color(YELLOW)
        self.add_sound("voiceovers/shine2.mp3")
        self.play(Write(genaral_formula))
        self.wait()
        self.play(genaral_formula.animate.shift(DOWN))
        posterior_brace = Brace(genaral_formula[0][:6], UP)
        prior_brace = Brace(genaral_formula[0][13:17], UP)

        prior = prior_brace.get_tex("16,7\%")
        posterior = posterior_brace.get_tex("16,7\%")
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(GrowFromCenter(posterior_brace), Write(posterior))
        self.wait()

        loop = CurvedArrow(
            posterior.get_top(),
            prior.get_top(),
            angle=-TAU / 4
        )
        posterior_copy = posterior.copy()
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(Create(loop), GrowFromCenter(prior_brace), posterior_copy.animate.move_to(prior))    
        self.wait()  
        self.play(FadeOut(loop, prior, prior_brace, posterior, posterior_brace, genaral_formula, posterior_copy)) 
        positive_person = Person()
        plus = Text("+", weight=BOLD, color=YELLOW)
        plus.set_width(positive_person.get_width())
        plus.move_to(positive_person.get_corner(UR))
        self.play(FadeIn(positive_person))
        self.wait(2)
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(plus))
        self.wait()
        self.play(FadeOut(positive_person, plus))
        formula = MathTex(
            r"P(D \mid +_1,+_2) = {P(+ \mid D) P(D \mid +_1) \over P(+ \mid D) P(D \mid +_1) + P(+ \mid N) P(N \mid +_1)}",
            tex_to_color_map={
                "D": RED,
                "N": BLUE,
                "+": YELLOW,
            },
            substrings_to_isolate=list("P(|)=")
        )
        formula[42].set_color(WHITE)
        eq = formula[10]
        Ns = formula.get_parts_by_tex("N")
        Ds = formula.get_parts_by_tex("D")
        
        for N in Ns:
            index = formula.submobjects.index(N)
            normal_person = Person()
            normal_person.set_color(BLUE)
            normal_person.replace(N)
            formula.submobjects[index] = normal_person
            normal_person.set_height(0.5)

        for D in Ds:
            index = formula.submobjects.index(D)
            sick_person = Person()
            sick_person.set_color(RED)
            sick_person.replace(D)
            formula.submobjects[index] = sick_person
            sick_person.set_height(0.5)
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(formula))
        self.wait(3)
        prior_brace = Brace(formula[19:26], UP)
        prior_val = prior_brace.get_tex("16,7\%")
        prior_text = Tex("0,167").move_to(prior_val)
        likelihood_brace = Brace(formula[12:19], UP)
        likelihood_val = likelihood_brace.get_tex("0.99")

        sick_positive_brace = Brace(formula[27:34], DOWN)
        sick_positive_val = sick_positive_brace.get_tex("0.99")
        sick_brace = Brace(formula[34:41], DOWN)
        sick_val = sick_brace.get_tex("0.167")
        normal_positive_brace = Brace(formula[43:50], DOWN)
        normal_positive_val = normal_positive_brace.get_tex("0.05")
        normal_brace = Brace(formula[50:], DOWN)
        normal_val = normal_brace.get_tex("0.833")
        brace_group = VGroup(prior_brace, prior_val, likelihood_brace, likelihood_val,
                             sick_positive_brace, sick_positive_val, sick_brace, sick_val,
                             normal_positive_brace, normal_positive_val, normal_brace, normal_val)
        self.play(FadeIn(prior_brace))
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(prior_val))
        self.wait()
        self.add_sound("voiceovers/click.wav")
        self.play(Transform(prior_val, prior_text))
        self.wait(2)
        self.play(FadeIn(likelihood_brace))
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(likelihood_val))
        self.wait(2)
        self.play(Circumscribe(formula[27:], color=GREEN))
        self.wait()
        self.play(Circumscribe(formula[27:41], color=GREEN))
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(sick_brace, sick_val))
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(sick_positive_brace, sick_positive_val))             
        self.wait()
        self.play(Circumscribe(formula[49:], color=GREEN))
        
        arrow = MathTex(r"\downarrow").next_to(normal_val, DOWN)
        normal_val_explain = MathTex("1-0.167").next_to(arrow, DOWN)
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(normal_brace, normal_val, arrow, normal_val_explain))
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(normal_positive_brace, normal_positive_val))
        self.wait()
        
        final_numbers = MathTex(
            "\\frac{0.99 \\times 0.167}{(0.99 \\times 0.167) + (0.05 \\times 0.833)}",
            font_size=34).next_to(eq, RIGHT)
        
        result = MathTex("\\approx 0.80", font_size=40, color=GREEN).next_to(final_numbers, RIGHT)
        self.add_sound("voiceovers/click.wav")
        self.play(FadeOut(brace_group, arrow, normal_val_explain),
                  Transform(formula[12:], final_numbers))
        self.add_sound("voiceovers/drum-roll.mp3")
        self.play(FadeIn(result))
        self.wait()
        self.add_sound("voiceovers/DiseaseBayesSecond2.mp3")
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        # 1. Create the Meter Frame
        meter_height = 5
        meter_width = 0.5
        frame = Rectangle(height=meter_height, width=meter_width, stroke_color=WHITE)
        frame.to_edge(RIGHT, buff=1.5)
        
        # Percentage Markers
        ticks = VGroup(*[
            Line(LEFT, RIGHT, color=GRAY).scale(0.1).move_to(frame.get_bottom() + UP * (meter_height * i/10))
            for i in range(11)
        ])
        labels = VGroup(
            Text("100%", font_size=16).next_to(ticks[10], RIGHT),
            Text("50%", font_size=16).next_to(ticks[5], RIGHT),
            Text("0%", font_size=16).next_to(ticks[0], RIGHT)
        )

        # 2. The Liquid (The Probability)
        # We use a ValueTracker to animate the level smoothly
        level_tracker = ValueTracker(0.01) # Start at 1%
        
        # Define the filling rectangle based on the tracker value
        liquid = always_redraw(lambda: 
            Rectangle(
                width=meter_width, 
                height=level_tracker.get_value() * meter_height,
                fill_color=YELLOW, 
                fill_opacity=0.8,
                stroke_width=0
            ).align_to(frame, DOWN)
        )

        percent_label = always_redraw(lambda:
            Text(f"{level_tracker.get_value()*100:.1f}%", font_size=24, color=YELLOW)
            .next_to(liquid, LEFT)
        )

        self.add(frame, ticks, labels, liquid, percent_label)
        self.wait(1)

        # --- ANIMATION SEQUENCE ---
        
        # Test 1 Result
        self.play(
            level_tracker.animate.set_value(0.167), 
            run_time=3, 
            rate_func=bezier([0, 0, 1, 1])
        )
        self.add_sound("voiceovers/ding.wav")
        self.play(Indicate(percent_label))
        self.wait()

        # Test 2 Result
        self.play(
            level_tracker.animate.set_value(0.80), 
            run_time=4, 
            rate_func=smooth
        )
        self.add_sound("voiceovers/ding.wav")
        self.play(Indicate(percent_label, scale_factor=1.2))

        # Test 3 Result
        self.play(
            level_tracker.animate.set_value(0.987), 
            run_time=6, 
            rate_func=smooth
        )
        self.add_sound("voiceovers/ding.wav")
        self.wait(3)

class BaseRatesLecture(Scene):
    def create_population(self, prevalence, sensitivity, specificity, total=100):
        population = VGroup()

        infected = int(total * prevalence)
        healthy = total - infected

        true_pos = infected * sensitivity
        true_pos = math.ceil(true_pos)
        false_neg = infected - true_pos
        false_pos = healthy * (1 - specificity)
        false_pos = math.ceil(false_pos)
        true_neg = healthy - false_pos

        for _ in range(true_pos):
            person = Person(height=0.5, fill_color=RED).set_stroke(YELLOW, width=0)
            plus = Text("+", weight=BOLD, color=YELLOW)
            plus.set_width(person.get_width())
            plus.move_to(person.get_corner(UR))
            person.add(plus)
            population.add(person)
        for _ in range(false_pos):
            person = Person(height=0.5, fill_color=BLUE).set_stroke(YELLOW, width=0)
            plus = Text("+", weight=BOLD, color=YELLOW)
            plus.set_width(person.get_width())
            plus.move_to(person.get_corner(UR))
            person.add(plus)
            population.add(person)
        for _ in range(false_neg):
            population.add(Person(height=0.5, fill_color=PURPLE))
        for _ in range(true_neg):
            population.add(Person(height=0.5, fill_color=BLUE))

        population.arrange_in_grid(rows=5, cols=20, buff=0.15)
        return population, true_pos, false_pos

    def isolate_and_explain(self, dots, tp, fp, headline, color):
        positives = VGroup(*[
            d for d in dots if d.get_stroke_color() in [YELLOW]
        ])
        negatives = VGroup(*[
            d for d in dots if d.get_stroke_color() not in [YELLOW]
        ])

        total_pos = tp + fp
        ppv = 100 * tp / total_pos

        # Fade out negatives
        self.play(FadeOut(negatives))
        self.wait(0.5)

        # Gather positives
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(
            positives.animate.arrange(RIGHT, buff=0.15).move_to(ORIGIN)
        )
        self.wait(0.5)

        # Count text
        count_text = Text(
            f"{tp} trường hợp mắc bệnh thực sự trong số {total_pos} ca dương tính",
            font="Noto Sans", font_size=32
        )
        count_text.next_to(positives, DOWN)
        self.play(Write(count_text))
        self.wait(4)

        ppv_label = MathTex(
            r"P(D \mid +) \approx ",
            tex_to_color_map={
                "D": RED,
                "+": YELLOW,
            },
            substrings_to_isolate=list("P(|)=")
        )

        D = ppv_label.get_parts_by_tex("D")[0]        
        index = ppv_label.submobjects.index(D)
        sick_person = Person()
        sick_person.set_color(RED)
        sick_person.replace(D)
        ppv_label.submobjects[index] = sick_person
        sick_person.set_height(0.5)

        ppv_value = DecimalNumber(
            0,
            num_decimal_places=0,
            font_size=36,
            color=color
        )
        percent = MathTex(r"\%").scale(0.8).set_color(color)

        ppv_group = VGroup(ppv_label, ppv_value, percent)
        ppv_group.arrange(RIGHT, buff=0.15)
        ppv_group.next_to(count_text, DOWN)
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(ppv_group))
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(
            ppv_value.animate.set_value(ppv),
            run_time=3,
            rate_func=smooth
        )
        self.wait(2)
        self.play(
            FadeOut(positives),
            FadeOut(count_text),
            FadeOut(ppv_group)
        )

    def construct(self):
        self.wait()
        self.add_sound("voiceovers/BaseRatesLecture1.mp3")
        # title = Text("Mức độ phổ biến của bệnh", font="Noto Sans", font_size=48).to_edge(UP)
        subtitle = Text(
            "Cùng một xét nghiệm • Mức độ phổ biến khác nhau • Ý nghĩa khác nhau",
            font_size=28, font="Noto Sans"
        )
        subtitle.to_edge(UP)

        self.play(FadeIn(subtitle))
        self.wait()

        accuracy = Text("Độ nhạy: 99%, Độ đặc hiệu: 95%", font="Noto Sans", font_size=24, color=BLUE)
        accuracy.next_to(subtitle, DOWN)
        self.play(FadeIn(accuracy))
        self.wait(2)

        rare_dots, rare_tp, rare_fp = self.create_population(
            prevalence=0.01,
            sensitivity=0.90,
            specificity=0.95
        )
        rare_dots.to_edge(LEFT, buff=1).shift(DOWN)
        rare_label = Text("Bệnh hiếm gặp (1%)", font="Noto Sans", font_size=32)
        rare_label.next_to(rare_dots, UP)
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(FadeIn(rare_dots), Write(rare_label))
        self.wait()

        self.isolate_and_explain(
            rare_dots,
            rare_tp,
            rare_fp,
            "Đa số các kết quả xét nghiệm dương tính đều là dương tính giả",
            color=RED
        )
        self.wait()

        # Common disease
        self.add_sound("voiceovers/BaseRatesLecture2.mp3")
        common_dots, common_tp, common_fp = self.create_population(
            prevalence=0.30,
            sensitivity=0.99,
            specificity=0.95
        )
        common_dots.to_edge(RIGHT, buff=1).shift(DOWN)
        common_label = Text("Bệnh phổ biến (30%)", font="Noto Sans", font_size=32)
        common_label.next_to(common_dots, UP)
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(FadeIn(common_dots), Write(common_label), FadeOut(rare_label))
        self.wait()

        self.isolate_and_explain(
            common_dots,
            common_tp,
            common_fp,
            "Đa số các kết quả xét nghiệm dương tính đều là dương tính thật",
            color=GREEN
        )
        self.play(FadeOut(common_label))
        self.wait()
        self.play(FadeOut(subtitle, accuracy))
        self.wait(2)
class BayesTheoremProof(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/BayesTheoremProof1.mp3")
        # 1. Define the formulas
        title = Text("Chứng minh định lý Bayes", font="Noto Sans")
        title.to_edge(UP)
        
        h_line = Line(LEFT, RIGHT).scale(4) 
        h_line.next_to(title, DOWN)
        
        # Step 1: Definition
        def_prob_ab = MathTex(
            "P(A|B) = \\frac{P(A \\cap B)}{P(B)}", 
            font_size=42
        )
        def_prob_ab[0][2].set_color(RED)
        def_prob_ab[0][4].set_color(YELLOW)
        def_prob_ab[0][9].set_color(RED)
        def_prob_ab[0][11].set_color(YELLOW)
        def_prob_ab[0][-2].set_color(YELLOW)

        def_prob_ba = MathTex(
            "P(B|A) = \\frac{P(A \\cap B)}{P(A)}", 
            font_size=42
        )
        def_prob_ba[0][2].set_color(YELLOW)
        def_prob_ba[0][4].set_color(RED)
        def_prob_ba[0][9].set_color(RED)
        def_prob_ba[0][11].set_color(YELLOW)
        def_prob_ba[0][-2].set_color(RED)

        VGroup(def_prob_ab, def_prob_ba).arrange(DOWN, LARGE_BUFF)
        
        # Step 2: Multiply by P(B)
        product_rule_1 = MathTex(
            "P(A \\cap B) = P(A|B)P(B)",
            font_size=42
        )
        product_rule_1[0][2].set_color(RED)
        product_rule_1[0][4].set_color(YELLOW)
        product_rule_1[0][9].set_color(RED)
        product_rule_1[0][11].set_color(YELLOW)
        product_rule_1[0][-2].set_color(YELLOW)
        # Step 3: Symmetric side
        product_rule_2 = MathTex(
            "P(A \\cap B) = P(B|A)P(A)",
            font_size=42
        )
        product_rule_2[0][2].set_color(RED)
        product_rule_2[0][4].set_color(YELLOW)
        product_rule_2[0][9].set_color(YELLOW)
        product_rule_2[0][11].set_color(RED)
        product_rule_2[0][-2].set_color(RED)
        VGroup(product_rule_1, product_rule_2).arrange(DOWN, LARGE_BUFF)
        # Step 4: Set them equal
        equality = MathTex(
            "P(A|B)P(B) = P(B|A)P(A)",
            font_size=42
        )
        equality[0][2].set_color(RED)
        equality[0][4].set_color(YELLOW)
        equality[0][8].set_color(YELLOW)
        equality[0][13].set_color(YELLOW)
        equality[0][15].set_color(RED)
        equality[0][-2].set_color(RED)
        
        # Step 5: Final Theorem
        final_formula = MathTex(
            "P(A|B) = \\frac{P(B|A)P(A)}{P(B)}",
            font_size=60
        )
        final_formula[0][2].set_color(RED)
        final_formula[0][4].set_color(YELLOW)
        final_formula[0][9].set_color(YELLOW)
        final_formula[0][11].set_color(RED)
        final_formula[0][15].set_color(RED)
        final_formula[0][-2].set_color(YELLOW)

        # --- ANIMATION SEQUENCE ---

        # Show Title
        self.play(Write(title), GrowFromCenter(h_line))
        self.wait(2)

        # Show definition
        self.add_sound("voiceovers/BayesTheoremProof2.mp3")
        self.add_sound("voiceovers/click.wav")
        self.play(Write(def_prob_ab))
        self.wait()
        self.add_sound("voiceovers/BayesTheoremProof3.mp3")
        self.add_sound("voiceovers/click.wav")
        self.play(Write(def_prob_ba))
        self.wait(2)

        # Transform to product rule
        self.add_sound("voiceovers/BayesTheoremProof4.mp3")
        self.wait()
        self.play(Indicate(def_prob_ab[0][7:13], color=ORANGE),
                  Indicate(def_prob_ba[0][7:13], color=ORANGE), run_time=4)
        self.wait(2)
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(Transform(def_prob_ab, product_rule_1))
        self.wait()

        # Show the second product rule
        self.add_sound("voiceovers/BayesTheoremProof5.mp3")
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(Transform(def_prob_ba, product_rule_2))
        self.wait()

        # Highlight that they are both equal to P(A and B)
        box = SurroundingRectangle(VGroup(def_prob_ab, def_prob_ba), color=GREEN)
        self.play(Create(box))
        self.wait()

        # Move to equality
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(
            FadeOut(box),
            ReplacementTransform(VGroup(def_prob_ab, def_prob_ba), equality)
        )
        self.wait(2)

        # Final rearrangement to Bayes' Theorem
        self.add_sound("voiceovers/BayesTheoremProof6.mp3")
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(ReplacementTransform(equality, final_formula))
        self.play(final_formula.animate.scale(1.2))
        self.wait(2)
        
        # Draw a box around the final result
        final_box = SurroundingRectangle(final_formula, color=GREEN, buff=MED_LARGE_BUFF)
        self.add_sound("voiceovers/shine2.mp3")
        self.play(Create(final_box))      
        self.wait(4)

class BayesVennProof(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/BayesVennProof.mp3")
        title = Text("Minh họa trực quan cho \nđịnh lý Bayes", font="Noto Sans").scale(0.7).to_corner(UL)
        title[18:].set_color_by_gradient(RED, YELLOW)
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(FadeIn(title))
        omega = Rectangle(width=8, height=4, fill_opacity=0.3, color=WHITE)
        omega_label = MathTex(r"\Omega").next_to(omega, UP)
        self.add_sound("voiceovers/click.wav")
        self.play(Create(omega), Write(omega_label))
        self.wait(1)
        circle_a = Circle(radius=1.5, color=RED, fill_opacity=0.3).shift(LEFT)
        circle_b = Circle(radius=1.5, color=YELLOW, fill_opacity=0.3).shift(RIGHT)
        
        label_a = Text("A", color=RED).next_to(circle_a, LEFT, buff=0.5)
        label_b = Text("B", color=YELLOW).next_to(circle_b, RIGHT, buff=0.5)
        
        intersection = Intersection(circle_a, circle_b, color=ORANGE, fill_opacity=0.7)
        self.add_sound("voiceovers/click.wav")
        self.play(Create(circle_a), Write(label_a))
        self.add_sound("voiceovers/click.wav")
        self.play(Create(circle_b), Write(label_b))
        self.wait(1)
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(intersection))
        self.wait()
        venn_group = VGroup(omega, omega_label, 
                            circle_a, label_a, circle_b, label_b, intersection)
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(venn_group.animate.scale(0.5).to_edge(LEFT))
        self.wait()
        p_a = VGroup(MathTex(r"P(A) =").scale(0.7),
                     Line(LEFT, RIGHT).scale(0.7)
                     ).arrange(RIGHT).next_to(omega, RIGHT, 1.5*LARGE_BUFF).shift(2.5*UP)
        p_a[0][0][2].set_color(RED)
        p_ba = VGroup(MathTex(r"P(B|A) =").scale(0.7),
                     Line(LEFT, RIGHT).scale(0.7)
                     ).arrange(RIGHT).next_to(p_a, RIGHT, LARGE_BUFF)
        p_ba[0][0][2].set_color(YELLOW)
        p_ba[0][0][4].set_color(RED)
        p_b = VGroup(MathTex(r"P(B) =").scale(0.7),
                     Line(LEFT, RIGHT).scale(0.7)
                     ).arrange(RIGHT).next_to(p_a, DOWN, 1.5*LARGE_BUFF)
        p_b[0][0][2].set_color(YELLOW)
        p_ab = VGroup(MathTex(r"P(A|B) =").scale(0.7),
                     Line(LEFT, RIGHT).scale(0.7)
                     ).arrange(RIGHT).next_to(p_b, RIGHT, LARGE_BUFF)
        p_ab[0][0][2].set_color(RED)
        p_ab[0][0][4].set_color(YELLOW)
        p_a_ba = MathTex(r"P(A) P(B|A) =").scale(0.7).next_to(p_b, DOWN, 1.5*LARGE_BUFF)
        p_a_ba[0][2].set_color(RED)
        p_a_ba[0][6].set_color(YELLOW)
        p_a_ba[0][8].set_color(RED)
        p_b_ab = MathTex(r"P(B) P(A|B) =").scale(0.7).next_to(p_a_ba, DOWN, 1.5*LARGE_BUFF)
        p_b_ab[0][2].set_color(YELLOW)
        p_b_ab[0][6].set_color(RED)
        p_b_ab[0][8].set_color(YELLOW)
        
        circle_a_copy1 = circle_a.copy()
        circle_b_copy1 = circle_b.copy()
        intersection_copy1 = intersection.copy()
        omega_copy1 = omega.copy()
        circle_a_copy2 = circle_a.copy()
        circle_b_copy2 = circle_b.copy()
        intersection_copy2 = intersection.copy()
        omega_copy2 = omega.copy()
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(p_a))
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(circle_a_copy1.animate.scale(0.3).next_to(p_a[1], UP),
                  omega_copy1.animate.scale(0.3).next_to(p_a[1], DOWN))
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(p_ba))
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(intersection_copy1.animate.scale(0.3).next_to(p_ba[1], UP),
                  circle_a_copy2.animate.scale(0.3).next_to(p_ba[1], DOWN))
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(p_b))
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(circle_b_copy1.animate.scale(0.3).next_to(p_b[1], UP),
                  omega_copy2.animate.scale(0.3).next_to(p_b[1], DOWN))
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(p_ab))
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(intersection_copy2.animate.scale(0.3).next_to(p_ab[1], UP),
                  circle_b_copy2.animate.scale(0.3).next_to(p_ab[1], DOWN))
        
        p_a_copy = VGroup(circle_a_copy1.copy(), p_a[1].copy(), omega_copy1.copy()
                          ).arrange(DOWN).move_to(p_a[1])
        p_ba_copy = VGroup(intersection_copy1.copy(), p_ba[1].copy(), circle_a_copy2.copy()
                           ).arrange(DOWN).move_to(p_ba[1])
        p_b_copy = VGroup(circle_b_copy1.copy(), p_b[1].copy(), omega_copy2.copy()
                          ).arrange(DOWN).move_to(p_b[1])
        p_ab_copy = VGroup(intersection_copy2.copy(), p_ab[1].copy(), circle_b_copy2.copy()
                           ).arrange(DOWN).move_to(p_ab[1])
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(p_a_ba))
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(p_a_copy.animate.next_to(p_a_ba, RIGHT))
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(p_ba_copy.animate.next_to(p_a_copy, RIGHT))
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(p_b_ab))
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(p_b_copy.animate.next_to(p_b_ab, RIGHT))
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(p_ab_copy.animate.next_to(p_b_copy, RIGHT))
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(FadeOut(p_a_copy[0], p_ba_copy[1:]),
                  p_ba_copy[0].animate.next_to(p_a_copy[1], UP))
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(FadeOut(p_b_copy[0], p_ab_copy[1:]),
                  p_ab_copy[0].animate.next_to(p_b_copy[1], UP))
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(FadeOut(p_ab_copy[0], p_b_copy[1:], p_b_ab[0][-1],
                          p_ba_copy[0], p_a_copy[1:]),
                  p_b_ab[0][:-1].animate.next_to(p_a_ba, RIGHT))
        prob_line = Line(LEFT, RIGHT).next_to(p_a_ba, RIGHT)
        
        self.wait()
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(p_b_ab[0][:-1].animate.next_to(prob_line, UP),
                  FadeIn(prob_line),
                  p_a_ba[0][:4].animate.next_to(prob_line, DOWN))
        p_ab_bayes = p_b_ab[0][4:-1].copy()
        prob_line_bayes = prob_line.copy()
        p_b_bayes = p_b_ab[0][:4].copy()
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(p_ab_bayes.animate.next_to(p_a_ba[0][4:-1], DOWN, 1.3*LARGE_BUFF))
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(VGroup(p_a_ba[0][-1].copy(), prob_line_bayes).animate.next_to(p_ab_bayes, RIGHT))
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(p_b_bayes.animate.next_to(prob_line_bayes, DOWN),
                  VGroup(p_a_ba[0][:4].copy(), p_a_ba[0][4:-1].copy()).animate.arrange(RIGHT, buff=0.05).next_to(prob_line_bayes, UP))
        box = SurroundingRectangle(VGroup(p_a_ba, p_b_ab, p_ab_bayes, prob_line_bayes, p_b_bayes), color=GREEN, stroke_width=2)
        self.add_sound("voiceovers/shine2.mp3")
        self.play(Create(box))
        self.wait(3)

class BayesianSpamFilter(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/BayesianSpamFilter1.mp3")
        # 1. Title and Formula
        title = Text("Lọc thư rác bằng phương pháp Bayes", font="Noto Sans", font_size=40).to_edge(UP)
        formula = MathTex(
            "P(S|W) = \\frac{P(W|S)P(S)}{P(W)}",
            font_size=36
        )
        formula[0][2].set_color(RED)
        formula[0][4].set_color(YELLOW)
        formula[0][9].set_color(YELLOW)
        formula[0][11].set_color(RED)
        formula[0][15].set_color(RED)
        formula[0][-2].set_color(YELLOW)
        
        self.play(Write(title))
        email1 = SVGMobject("assets/email.svg").scale(0.6).set_color(BLUE)
        email2 = SVGMobject("assets/email.svg").scale(0.6).set_color(BLUE)

        email1_text = Text("Email:\n\"Kiếm tiền ngay bây giờ\"", font="Noto Sans").scale(0.4)
        email2_text = Text("Email:\n\"Họp lúc 3 giờ chiều\"", font="Noto Sans").scale(0.4)

        email1_group = VGroup(email1, email1_text).arrange(DOWN, buff=0.1)
        email2_group = VGroup(email2, email2_text).arrange(DOWN, buff=0.1)

        emails = VGroup(email1_group, email2_group).arrange(DOWN, buff=0.5)
        emails.to_edge(LEFT)
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(email1, email1_text))
        self.play(Flash(email1_text))
        self.wait()
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(email2, email2_text))
        self.wait()

        classifier = Rectangle(width=3.5, height=1.5).set_color(YELLOW)
        classifier_text = Text("Spam Filter", font="Noto Sans").scale(0.5)

        classifier_group = VGroup(classifier, classifier_text).arrange(DOWN, buff=0.1)
        classifier_group.next_to(emails, RIGHT, 2*LARGE_BUFF)

        arrows_to_features = VGroup(
            Arrow(email1_group.get_right(), classifier.get_left()),
            Arrow(email2_group.get_right(), classifier.get_left())
        )
        formula.save_state()
        formula.scale(0.8).move_to(classifier)
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(classifier_group, formula))
        self.wait()
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(Create(arrows_to_features))
        
        spam_box = Rectangle(width=2.8, height=1).set_color(RED)
        spam_text = Text("SPAM", font="Noto Sans").scale(0.5).set_color(RED)
        spam_group = VGroup(spam_box, spam_text).arrange(DOWN, buff=0.1)
        spam_group.to_edge(RIGHT).shift(UP)

        inbox_box = Rectangle(width=2.8, height=1).set_color(GREEN)
        inbox_text = Text("INBOX", font="Noto Sans").scale(0.5).set_color(GREEN)
        inbox_group = VGroup(inbox_box, inbox_text).arrange(DOWN, buff=0.1)
        inbox_group.to_edge(RIGHT).shift(DOWN)
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(spam_group))
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(inbox_group))
        self.wait()

        # Decision arrows
        spam_arrow = Arrow(classifier.get_right(), spam_group.get_left())
        inbox_arrow = Arrow(classifier.get_right(), inbox_group.get_left())
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(Create(spam_arrow))
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(Create(inbox_arrow))
        self.wait()

        # Highlight classification
        self.add_sound("voiceovers/error.wav")
        self.play(
            email1_group.animate.set_color(RED),
            Flash(spam_group, color=RED)
        )
        self.wait()

        self.play(
            email2_group.animate.set_color(GREEN),
            Flash(inbox_group, color=GREEN)
        )
        self.wait()
        self.play(FadeOut(emails, arrows_to_features, classifier_group,
                          spam_group, inbox_group, spam_arrow, inbox_arrow))
        
        self.wait()
        self.play(formula.animate.restore())
        self.wait()

        posterior = formula[0][:6]
        likelihood = formula[0][7:13]
        prior = formula[0][13:17]
        evidence = formula[0][18:]
        def focus_on(target):
            return [
                m.animate.set_opacity(1 if m in target else 0.2)
                for m in formula[0]
            ]
        explanation = Text("", font_size=32).next_to(formula, DOWN)

        # 1. Posterior
        explanation.become(
            Text("Xác suất email là thư rác khi biết rằng nó chứa từ khóa", 
                 font="Noto Sans", font_size=32).next_to(formula, DOWN)
        )
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(
            *focus_on(posterior),
            Write(explanation)
        )
        self.wait(3)

        # 2. Likelihood
        explanation.become(
            Text("Xác suất từ ​​khóa xuất hiện trong email thư rác", 
                 font="Noto Sans", font_size=32).next_to(formula, DOWN)
        )
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(
            *focus_on(likelihood),
            Transform(explanation, explanation)
        )
        self.wait(3)
        letter = ImageMobject("assets/letter.png").scale(0.2).next_to(likelihood, UP)
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(letter))
        self.wait()

        # 3. Prior
        explanation.become(
            Text("Xác suất tổng thể của bất kỳ email nào là thư rác", 
                 font="Noto Sans", font_size=32).next_to(formula, DOWN)
        )
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(
            FadeOut(letter),
            *focus_on(prior),
            Transform(explanation, explanation)
        )
        self.wait(2)
        prior_exam = Text("80% email là thư rác", 
                 font="Noto Sans", font_size=32).next_to(prior, UP, LARGE_BUFF)
        prior_exam_arrow = MathTex(r"\rightarrow").next_to(prior_exam, RIGHT)
        prior_exam_prob= MathTex("P(S) = 0.8}", font_size=36).next_to(prior_exam_arrow, RIGHT)
        prior_exam_prob[0][2].set_color(RED)
        self.play(Write(prior_exam))
        self.play(Write(prior_exam_arrow))
        self.play(Write(prior_exam_prob))
        self.wait()
        self.play(FadeOut(prior_exam, prior_exam_arrow, prior_exam_prob))

        # 4. Evidence
        explanation.become(
            Text("Xác suất tổng thể của từ khóa xuất hiện trong bất kỳ email nào", 
                 font="Noto Sans", font_size=32).next_to(formula, DOWN)
        )
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(
            *focus_on(evidence),
            Transform(explanation, explanation)
        )
        self.wait(4)

        # Restore full visibility
        self.play(
            *[m.animate.set_opacity(1) for m in formula],
            FadeOut(explanation)
        )
        self.wait()
        self.add_sound("voiceovers/BayesianSpamFilter2.mp3")
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(formula.animate.next_to(title, DOWN))

        # 2. Setup Training Data Boxes
        spam_box = Rectangle(color=RED, height=3, width=2).shift(LEFT * 3)
        ham_box = Rectangle(color=BLUE, height=3, width=2).shift(RIGHT * 3)
        
        spam_label = Text("Thư rác (40)", font="Noto Sans", color=RED, font_size=24).next_to(spam_box, UP)
        ham_label = Text("Thư hợp lệ (60)", font="Noto Sans", color=BLUE, font_size=24).next_to(ham_box, UP)
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(Create(spam_box), Write(spam_label))
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(Create(ham_box), Write(ham_label))
        self.wait()

        # 3. Representing the word "Prize"
        prize_text = Text("'Prize'", font="Noto Sans", color=YELLOW, font_size=30).set_z_index(3).move_to(ORIGIN + UP * 0.5)
        
        # Dots representing occurrences
        spam_dots = VGroup(*[Dot(color=RED, radius=0.05) for _ in range(20)]).arrange_in_grid(5, 4).move_to(spam_box)
        ham_dots = VGroup(*[Dot(color=BLUE, radius=0.05) for _ in range(3)]).arrange_in_grid(1, 3).move_to(ham_box)
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(ShowIncreasingSubsets(spam_dots))
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(ShowIncreasingSubsets(ham_dots))
        self.wait(2)
        new_email = SVGMobject("assets/email.svg")
        new_email.scale(0.3).set_color(WHITE).set_opacity(0.6).move_to(prize_text)
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(new_email, shift=UP))
        self.wait(2)
        prize_text.save_state()
        prize_text.set_color(WHITE)
        words = VGroup(
            Text("'Họp'", font="Noto Sans", font_size=30).set_z_index(3),
            prize_text,
            Text("'Thanks'", font="Noto Sans", font_size=30).set_z_index(3),
            Text("'Người chiến thắng'", font="Noto Sans", font_size=30).set_z_index(3),
        ).scale(0.6).arrange_in_grid(2*LARGE_BUFF)
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(ShowIncreasingSubsets(words), run_time=3)
        self.wait(3)
        self.play(words[0].animate.set_color(BLUE), run_time=2)
        self.wait(1.5)
        self.play(words[3].animate.set_color(RED), run_time=2)
        self.wait(3)
        self.play(FadeOut(new_email, words[0], words[2:]),
                  prize_text.animate.restore())
        self.wait(2)

        # 4. The Calculation Step
        calc_title = Text("Tính toán cho từ \n'Prize'", font="Noto Sans", font_size=30).shift(DOWN * 1.5)
        
        # Step-by-step math
        step1 = MathTex("P(S|Prize) = \\frac{0.5 \\times 0.4}{(0.5 \\times 0.4) + (0.05 \\times 0.6)}", font_size=32)
        step1[0][2].set_color(RED)
        step1[0][4:9].set_color(YELLOW)
        step1[0][11:14].set_color(ORANGE)
        step1[0][15:18].set_color(RED)
        step1[0][20:23].set_color(ORANGE)
        step1[0][24:27].set_color(RED)
        step1[0][30:34].set_color(GREEN)
        step1[0][35:].set_color(BLUE)
        step1.shift(DOWN * 2.5)
        
        self.play(Write(calc_title))
        self.play(Write(step1))
        # 5. Result
        result = MathTex("\\approx 0.87", color=RED).next_to(step1, RIGHT)
        self.play(Write(result))
        self.wait(0.5)
        threshold = MathTex("0.85").next_to(prize_text, DOWN)
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(threshold), Indicate(result))
        
        # Highlight Spam Box as it's the winner
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(
            spam_box.animate.scale(1.2).set_fill(RED, opacity=0.3),
            ham_box.animate.set_stroke(opacity=0.2),
            prize_text.animate.move_to(spam_box.get_center())
        )
        self.add_sound("voiceovers/bad-to-the-bone.mp3")
        self.wait(5)
class BayesianScience(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/BayesianScience1.mp3")
        title = Text("Khám phá khoa học", weight=BOLD, font="Noto Sans")
        self.play(Write(title))
        self.wait()
        self.play(FadeOut(title))
        
        look_closely = SVGMobject("assets/look_closely.svg").to_corner(UR)
        capsule = ImageMobject("assets/capsule.png").scale(0.2)
        atom = ImageMobject("assets/atom.png").scale(0.2)
        Group(atom, capsule).arrange(RIGHT, 2*LARGE_BUFF)
        self.play(FadeIn(look_closely))
        self.add_sound("voiceovers/disintegration-into-small-particles.mp3")
        self.play(FadeIn(atom))
        self.play(FadeIn(capsule))
        self.wait()
        self.play(FadeOut(look_closely, atom, capsule))
        efficancy = Text("Bước đột phá thực sự \nhay chỉ là sự trùng hợp ngẫu nhiên", weight=BOLD, font="Noto Sans")
        self.play(Write(efficancy))
        self.wait()
        self.play(FadeOut(efficancy))
        radius = 1.5
        center = ORIGIN

        arc = Arc(
            radius=radius,
            start_angle=5 * PI / 4,
            angle=3 * PI / 2,
            color=GREY
        )

        ticks = VGroup()
        labels = VGroup()

        for i, value in enumerate(range(0, 101, 10)):
            alpha = i / 10  # 0 → 1
            angle = 5 * PI / 4 + alpha * (3 * PI / 2)

            # Major tick
            start = center + radius * np.array([np.cos(angle), np.sin(angle), 0])
            end = center + (radius - 0.3) * np.array([np.cos(angle), np.sin(angle), 0])
            tick = Line(start, end, stroke_width=3)
            ticks.add(tick)

            # Label
            label_pos = center + (radius - 0.4) * np.array([np.cos(angle), np.sin(angle), 0])
            label = Text(str(value), font_size=12).move_to(label_pos)
            labels.add(label)

        # Needle (starts at 0)
        needle = Line(
            start=center,
            end=center + RIGHT,
            color=RED,
            stroke_width=6
        )
        needle.rotate(5 * PI / 4, about_point=center)

        # Pivot
        pivot = Dot(center, radius=0.1)

        # Titles
        title = Text("Thay đổi quan điểm", font="Noto Sans", font_size=40).to_edge(UP)
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(Create(arc))
        self.play(LaggedStartMap(Create, ticks), FadeIn(labels))
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(pivot), FadeIn(needle))
        self.add_sound("voiceovers/BayesianScience2.mp3")
        self.wait(0.5)

        # Shift the needle (0 → ~75%)
        self.add_sound("voiceovers/wobble.mp3")
        self.play(
            Write(title),
            Rotate(
                needle,
                angle=PI * 0.75,
                about_point=center,
                rate_func=smooth
            ),
            run_time=2
        )
        self.wait()
        self.play(FadeOut(title, arc, ticks, labels, pivot, needle))
        # 1. SETUP: The Hypothesis
        title = Text("Suy luận Bayes trong khoa học", font="Noto Sans", font_size=40).to_edge(UP)
        hypothesis = Text("Giả thuyết: Thuốc X chữa khỏi bệnh.", font="Noto Sans", font_size=28, color=BLUE).next_to(title, DOWN)
        
        self.play(Write(title))
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(hypothesis, shift=UP))
        self.wait(1)
        self.add_sound("voiceovers/BayesianScience3.mp3")

        # 2. THE PRIOR (Skepticism)
        # Most new drugs fail, so a scientist starts with a low prior.
        prior_gauge = VGroup()
        prior_box = Square(side_length=2, color=GRAY)
        prior_fill = Rectangle(width=2, height=0.2, fill_color=RED, fill_opacity=0.8, stroke_width=0).align_to(prior_box, DOWN)
        prior_label = Text("Hoài nghi ban đầu: 10%", font="Noto Sans", font_size=20, color=RED).next_to(prior_box, DOWN)
        
        prior_gauge.add(prior_box, prior_fill, prior_label).to_edge(LEFT, buff=1.5)
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(Create(prior_box), FadeIn(prior_fill), Write(prior_label))
        self.wait(1)

        # 3. THE EVIDENCE (Clinical Trial)
        evidence_text = Text("Bằng chứng: Thử nghiệm thành công (p < 0.05)", font="Noto Sans", font_size=24, color=GREEN).shift(UP*1.5)
        likelihood_math = MathTex(
            "P(Thanh cong. | Hieu qua.) = 0.80", 
            "P(Thanh cong. | Khong hieu qua..) = 0.05",
            font_size=30
        ).arrange(DOWN).next_to(evidence_text, DOWN)
        success = Text("Thành công", font="Noto Sans").scale(0.45)
        success.move_to(likelihood_math[0][2:12])
        likelihood_math[0][2:12].set_opacity(0)
        effective = Text("Hiệu quả", font="Noto Sans").scale(0.45)
        effective.move_to(likelihood_math[0][13:21])
        likelihood_math[0][13:21].set_opacity(0)
        success2 = success.copy()
        success2.move_to(likelihood_math[1][2:12])
        likelihood_math[1][2:12].set_opacity(0)
        ineffective = Text("Không hiệu quả", font="Noto Sans").scale(0.45)
        ineffective.move_to(likelihood_math[1][13:27])
        likelihood_math[1][13:27].set_opacity(0)

        self.play(Write(evidence_text))
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(likelihood_math, success, effective, success2, ineffective, shift=RIGHT))
        self.wait(2)

        # 4. THE POSTERIOR (The Update)
        # Using Bayes: (0.8 * 0.1) / [(0.8 * 0.1) + (0.05 * 0.9)] = 0.64
        post_gauge = VGroup()
        post_box = Square(side_length=2, color=GRAY)
        post_fill = Rectangle(width=2, height=1.28, fill_color=GREEN, fill_opacity=0.8, stroke_width=0).align_to(post_box, DOWN)
        post_label = Text("Xác suất hậu nghiệm: 64%", font="Noto Sans", font_size=20, color=GREEN).next_to(post_box, DOWN)
        
        post_gauge.add(post_box, post_fill, post_label).to_edge(RIGHT, buff=1.5)

        arrow = Arrow(prior_box.get_right(), post_box.get_left(), color=WHITE)
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(Create(arrow))
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(Create(post_box), FadeIn(post_fill), Write(post_label))
        self.wait(2)

        # 5. CONCLUSION
        conclusion = Text(
            "Trong khoa học, một nghiên cứu hiếm khi là đủ.\nChúng ta cập nhật độ tin cậy của mình sau mỗi lần thử nghiệm.",
            font="Noto Sans", font_size=24, line_spacing=1.5
        ).to_edge(DOWN, buff=0.5)
        self.add_sound("voiceovers/drum-roll.mp3")
        self.play(Write(conclusion))
        self.wait(4)
class BayesUpdate(Scene):
    def construct(self):
        self.wait()
        formula = MathTex(
            "P(A|B) = \\frac{P(B|A)P(A)}{P(B)}",
            font_size=60
        )
        formula[0][2].set_color(RED)
        formula[0][4].set_color(YELLOW)
        formula[0][9].set_color(YELLOW)
        formula[0][11].set_color(RED)
        formula[0][15].set_color(RED)
        formula[0][-2].set_color(YELLOW)
        self.add_sound("voiceovers/click.wav")
        self.play(Write(formula))
        posterior_brace = Brace(formula[0][:6], UP)
        prior_brace = Brace(formula[0][13:17], UP)

        prior = prior_brace.get_tex("Prior")
        posterior = posterior_brace.get_tex("Posterior")
        self.add_sound("voiceovers/BayesUpdate.mp3")
        self.play(GrowFromCenter(prior_brace), Write(prior))
        self.play(GrowFromCenter(posterior_brace), Write(posterior))
        explain = Text("* Prior: Xác suất tiên nghiệm, Posterior: Xác suất hậu nghiệm", font="Noto Sans", font_size=20).to_edge(DOWN)
        self.play(FadeIn(explain))

        loop = CurvedArrow(
            posterior.get_top(),
            prior.get_top(),
            angle=-TAU / 4
        )
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(Create(loop))     
        self.wait()  
        self.play(FadeOut(loop, explain, prior, prior_brace, posterior, posterior_brace, formula)) 
        # ---------- Initial ratio 6:4 ----------
        sunny_r1 = 1.5
        rain_r1 = 1

        sunny_circle = Circle(
            radius=sunny_r1,
            color=YELLOW,
            fill_opacity=0.3
        ).shift(LEFT * 3)

        rain_circle = Circle(
            radius=rain_r1,
            color=BLUE,
            fill_opacity=0.3
        ).shift(RIGHT * 3)

        # Background images
        sun_bg = ImageMobject("assets/sunny.png") \
            .scale(0.13) \
            .move_to(sunny_circle.get_center()) \
            .set_opacity(0.6)

        rain_bg = ImageMobject("assets/rain.png") \
            .scale(0.13) \
            .move_to(rain_circle.get_center()) \
            .set_opacity(0.6)

        sunny_label = Text("60%", font_size=28).move_to(sunny_circle)
        rain_label = Text("40%", font_size=28).move_to(rain_circle)
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(
            FadeIn(sun_bg),
            FadeIn(rain_bg),
            Create(sunny_circle),
            Create(rain_circle)
        )
        self.play(Write(sunny_label), Write(rain_label))
        self.wait()
        self.add_sound("voiceovers/loud-thunder.mp3")
        cloud = ImageMobject("assets/cloud.png").scale(0.5).to_edge(UP).shift(LEFT)
        self.play(FadeIn(cloud, shift=DOWN))

        # ---------- Target ratio 2:8 ----------
        sunny_r2 = 1
        rain_r2 = 2.5

        sunny_circle_new = Circle(
            radius=sunny_r2,
            color=YELLOW,
            fill_opacity=0.3
        ).move_to(sunny_circle.get_center())

        rain_circle_new = Circle(
            radius=rain_r2,
            color=BLUE,
            fill_opacity=0.3
        ).move_to(rain_circle.get_center())

        # Resize background images to match new circles
        sun_bg_new = sun_bg.copy() \
            .scale(sunny_r2 / sunny_r1)

        rain_bg_new = rain_bg.copy() \
            .scale(rain_r2 / rain_r1)

        sunny_label_new = Text("20%", font_size=28).move_to(sunny_circle_new)
        rain_label_new = Text("80%", font_size=28).move_to(rain_circle_new)

        # Animate transition
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(
            Transform(sunny_circle, sunny_circle_new),
            Transform(rain_circle, rain_circle_new),
            Transform(sun_bg, sun_bg_new),
            Transform(rain_bg, rain_bg_new),
            Transform(sunny_label, sunny_label_new),
            Transform(rain_label, rain_label_new),
            run_time=2
        )

        self.wait(4)
class BayesConclusion(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/BayesConclusion1.mp3")
        title = Text("Kết luận",  font="Noto Sans", weight=BOLD).to_edge(UP)
        self.play(Write(title))
        self.wait()
        formula = MathTex(
            "P(A|B) = \\frac{P(B|A)P(A)}{P(B)}",
            font_size=60
        )
        formula[0][2].set_color(RED)
        formula[0][4].set_color(YELLOW)
        formula[0][9].set_color(YELLOW)
        formula[0][11].set_color(RED)
        formula[0][15].set_color(RED)
        formula[0][-2].set_color(YELLOW)
        self.add_sound("voiceovers/click.wav")
        self.play(Write(formula))
        self.wait()
        self.play(FadeOut(formula))
        text = Text(
            "Định lý Bayes dạy chúng ta cách \ncập nhật niềm tin trong một thế giới bất định.",
            font="Noto Sans", line_spacing=1.2
        )

        # Define the center of the orbits, off-screen at the bottom right
        orbit_center = RIGHT * 7 + DOWN * 4

        # Lists of mathematical symbols
        symbols_tex = [
            r"\alpha", r"\beta", r"\gamma", r"\delta", r"\epsilon", r"\zeta", r"\eta",
            r"\theta", r"\iota", r"\kappa", r"\lambda", r"\mu", r"\nu", r"\xi",
            r"+", r"-", r"\times", r"\div", r"=", r"\neq", r"<", r">",
            r"\sqrt{2}", r"\int", r"\sum", r"\lim", r"\infty", r"\partial",
            r"\mathbb{N}", r"\mathbb{Z}", r"\mathbb{Q}", r"\mathbb{R}", r"\mathbb{C}",
            r"\forall", r"\exists", r"\in", r"\notin", r"\subset", r"\supset",
            r"\wedge", r"\vee", r"\neg", r"\implies", r"\iff", r"\bot", r"\top"
        ]

        # Parameters for 8 orbits
        num_orbits = 8
        radii = [2 + i * 0.8 for i in range(num_orbits)]
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK]
        speeds = [0.1 + i * 0.05 for i in range(num_orbits)] # Different rotation speeds
        spin_speeds = [0.5 + i * 0.2 for i in range(num_orbits)] # Different self-spin speeds
        # Outer orbits have more symbols, are slower, and spin slower
        num_symbols_per_orbit = [3, 4, 5, 8, 11, 14, 17, 23] # Total must match len(symbols_tex)
        speeds = [0.2 - i * 0.02 for i in range(num_orbits)] # Slower for outer orbits
        spin_speeds = [1.0 - i * 0.1 for i in range(num_orbits)] # Slower spin for outer orbits

        # Shuffle symbols to randomize their distribution
        random.shuffle(symbols_tex)

        # Assign symbols to orbits based on num_symbols_per_orbit
        symbols_by_orbit = []
        start_index = 0
        for num in num_symbols_per_orbit:
            end_index = start_index + num
            symbols_by_orbit.append(symbols_tex[start_index:end_index])
            start_index = end_index
        # Create and animate symbols for each orbit
        all_symbols = VGroup()
        for i in range(num_orbits):
            orbit_symbols = VGroup()
            # Distribute a subset of symbols on this orbit
            symbols_on_this_orbit = symbols_tex[i::num_orbits]
            num_symbols_on_orbit = len(symbols_on_this_orbit)
            
            for j, tex in enumerate(symbols_on_this_orbit):
                symbol = MathTex(tex, color=colors[i % len(colors)]).scale(0.8)
                # Set initial position
                angle = 2 * PI * j / num_symbols_on_orbit
                symbol.move_to(orbit_center + radii[i] * (np.cos(angle) * RIGHT + np.sin(angle) * UP))
                # Set initial orientation to face away from the center
                symbol.rotate(angle)
                orbit_symbols.add(symbol)

            # Add an updater to the group of symbols for this orbit
            def create_updater(orbit_group, radius, speed, spin_speed):
                def updater(mob, dt):
                    # Orbit rotation
                    mob.rotate(speed * dt, about_point=orbit_center)
                    # Keep symbols oriented relative to the center
                    for submob in mob:
                        # Counter-rotate to nullify the orbit's rotation effect on the symbol's orientation
                        submob.rotate(-speed * dt)
                        # Add the independent spin
                        submob.rotate(spin_speed * dt)
                return updater

            orbit_symbols.add_updater(create_updater(orbit_symbols, radii[i], speeds[i], spin_speeds[i]))
            all_symbols.add(orbit_symbols)        
        self.add(all_symbols)
        self.add_sound("voiceovers/click.wav")
        self.play(Write(text), run_time=3)
        self.wait(2)
        self.play(FadeOut(text, title))
        self.add_sound("voiceovers/BayesConclusion2.mp3")
        trophy = ImageMobject("assets/trophy.png").scale(0.6).to_corner(UL, LARGE_BUFF)
        self.play(FadeIn(trophy))
        self.wait(20)
class BayesMLThumbnail2(Scene):
    def construct(self):

        # Background
        bg = Rectangle(
            width=14,
            height=8,
            fill_color=BLACK,
            fill_opacity=1
        )
        self.add(bg)

        # Title (KEEP)
        title = Text(
            "ĐỊNH LÝ BAYES",
            font_size=96, font="Noto Sans",
            weight=BOLD
        ).set_color(YELLOW)
        title.to_edge(UP, buff=0.45)

        # Subtitle (KEEP)
        subtitle = Text(
            "Machine Learning",
            font_size=42
        ).set_color(GREY_B)
        subtitle.next_to(title, DOWN, buff=0.25)

        formula = MathTex(
            "P(S|W) = \\frac{P(W|S)P(S)}{P(W)}",
            font_size=72
        )
        formula[0][2].set_color(RED)
        formula[0][4].set_color(YELLOW)
        formula[0][9].set_color(YELLOW)
        formula[0][11].set_color(RED)
        formula[0][15].set_color(RED)
        formula[0][-2].set_color(YELLOW)

        formula.move_to(ORIGIN + DOWN * 0.5)

        # Add all
        self.add(
            title,
            subtitle,
            formula
        )