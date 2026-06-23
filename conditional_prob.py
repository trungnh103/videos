from manim import *
import numpy as np
import random
from manim.utils.space_ops import midpoint

class Intro(Scene):
    def construct(self):
        self.add_sound("voiceovers/Intro.mp3")
        independent_events = Text("Sự kiện độc lập", font="Noto Sans", color=YELLOW)
        self.play(Write(independent_events))
        self.wait()
        self.play(independent_events.animate.to_corner(UL))
        # Dice body
        dice1 = RoundedRectangle(
            width=2,
            height=2,
            corner_radius=0.2,
            fill_opacity=1,
            fill_color=GREEN,
            stroke_width=3,
            stroke_color=BLACK
        )

        dice1.shift(UP * 3)

        # Six pips (top face)
        pip_positions = [
            [-0.5,  0.5, 0], [0.5,  0.5, 0],
            [-0.5,  0.0, 0], [0.5,  0.0, 0],
            [-0.5, -0.5, 0], [0.5, -0.5, 0]
        ]

        pips = VGroup(*[
            Dot(point=pos, radius=0.12, color=BLACK)
            for pos in pip_positions
        ])

        pips.move_to(dice1.get_center())

        dice_group = VGroup(dice1, pips)
        self.play(FadeIn(dice_group))

        # Landing animation
        self.add_sound("voiceovers/dice19shuffle.flac")
        self.play(
            dice_group.animate.shift(DOWN * 3).rotate(PI),
            rate_func=rate_functions.ease_out_bounce,  # fixed
            run_time=3
        )
        self.wait()
        self.play(FadeOut(dice_group))
        dice_group_second = dice_group.copy().shift(UP * 3)
        self.play(FadeIn(dice_group_second))

        # Landing animation
        self.add_sound("voiceovers/dice19shuffle.flac")
        self.play(
            dice_group_second.animate.shift(DOWN * 3).rotate(PI),
            rate_func=rate_functions.ease_out_bounce,  # fixed
            run_time=3
        )
        self.wait()
        self.play(FadeOut(independent_events), FadeOut(dice_group_second))
        title = Text("Conditional Probability", font="Noto Sans", font_size=56)
        subtitle = Text("Xác suất có điều kiện", font="Noto Sans", font_size=36, color=YELLOW)

        subtitle.next_to(title, DOWN)

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))
        self.wait(2)
class CardConditional(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/CardConditional.mp3")
        # 1. Title and Setup
        title = Text("Xác suất có điều kiện: Rút bài", font="Noto Sans", font_size=36, color=YELLOW).to_edge(UP)
        self.play(FadeIn(title))

        # 2. Create a simplified deck (e.g., 20 cards to keep screen clean)
        # In reality 52, but 20 is better for visualization
        deck = VGroup(*[
            Rectangle(height=0.8, width=0.6, color=WHITE, fill_opacity=0.2) 
            for _ in range(52)
        ]).arrange_in_grid(rows=4, cols=13, buff=0.2).shift(LEFT * 2)

        # Label 4 of them as Aces
        aces_indices = [0, 5, 10, 15]
        ace_cards = ["assets/ace-spade.svg", "assets/Ace_of_diamonds.svg", "assets/Ace_of_hearts.svg", "assets/ace-club.svg"]
        for idx, card in zip(aces_indices, ace_cards):
            deck[idx].set_color(GOLD).set_fill(GOLD, opacity=0.5)
            # ace_label = Text("A", font_size=20).move_to(deck[idx].get_center())
            ace_label = SVGMobject(card).stretch_to_fit_height(deck[idx].height).stretch_to_fit_width(deck[idx].width)
            ace_label.move_to(deck[idx].get_center())
            deck[idx].add(ace_label)
        self.add_sound("voiceovers/magic-dark-teleport.wav")
        self.play(Create(deck))
        self.wait(2)
        for idx in aces_indices:
            self.play(Wiggle(deck[idx]), run_time=0.5)
        
        # 3. First Draw Calculation
        prob_text1 = MathTex("P(A_1) = \\frac{4}{52}", font_size=36).to_edge(RIGHT, buff=1).shift(UP)
        self.play(Write(prob_text1[0][:5]))
        self.wait()
        self.add_sound("voiceovers/correct-choice.wav")
        self.play(Write(prob_text1[0][5:]))
        self.wait()
        self.play(*[Indicate(deck[idx], color=GOLD) for idx in aces_indices], run_time=2)
        self.wait()
        # 4. The "Condition" - Remove one Ace
        removed_card = deck[0]
        explanation = Text("1 quân Át bị loại bỏ...", font="Noto Sans", font_size=20, color=GOLD).next_to(prob_text1, DOWN, buff=0.5)
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(
            removed_card.animate.shift(UP * 2 + RIGHT * 2).set_opacity(0),
            Write(explanation)
        )
        self.wait(2)

        # 5. Second Draw Calculation (The Conditional Part)
        # Update the visual: highlight remaining Aces
        remaining_aces = VGroup(deck[5], deck[10], deck[15])
        
        prob_text2 = MathTex(
            "P(A_2 | A_1) = ?", 
            font_size=42, 
            color=YELLOW
        ).next_to(explanation, DOWN, buff=0.5)

        self.play(Write(prob_text2))
        self.wait()
        wrong_prob  = MathTex("\\frac{4}{52}", font_size=42).next_to(prob_text2, DOWN)
        self.play(FadeIn(wrong_prob))
        cross = Cross(wrong_prob)
        self.add_sound("voiceovers/error.wav") 
        self.play(Create(cross))
        self.wait()
        self.play(FadeOut(wrong_prob, cross))
        self.wait()
        # Highlight the logic
        rect_target = SurroundingRectangle(remaining_aces, color=YELLOW)
        self.play(Create(rect_target))  
        self.wait(3)
        self.play(Indicate(prob_text2[0][2:4], color=GREEN))
        self.wait(0.5)
        self.play(Indicate(prob_text2[0][5:7], color=GREEN))
        self.wait(0.5)
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(Circumscribe(prob_text2))
        self.wait(3)
        self.play(Circumscribe(prob_text1))
        self.wait(3)
class Define(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/Define.mp3")
        title = Text("Xác suất có điều kiện", font="Noto Sans", color=YELLOW, font_size=42)
        explain = Text("Xác suất để một sự kiện A xảy ra khi một sự kiện B đã xảy ra", font="Noto Sans")
        explain.scale(0.65)
        explain[18].set_color(BLUE)
        explain[-8].set_color(RED)
        self.play(Write(title))
        self.wait(0.5)
        self.play(title.animate.to_corner(UL))
        self.play(Write(explain), run_time=3)
        self.wait(2)
        text = MathTex("P(A|B)").scale(1.4)
        text[0][2].set_color(BLUE)
        text[0][4].set_color(RED)
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(Transform(explain, text))
        self.wait()
        read  = Text("Xác suất của A khi biết B", font="Noto Sans")
        read[10].set_color(BLUE)
        read[-1].set_color(RED)
        read.scale(0.65).next_to(text, DOWN, LARGE_BUFF)
        self.play(Write(read))
        self.wait(3)
class Formula(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/Formula.mp3")
        title = Text("Công thức", font="Noto Sans", color=YELLOW, font_size=42)
        self.play(Write(title))
        self.wait()
        self.play(title.animate.to_corner(UL))
        formula = MathTex(
            "P(A|B)", "=", "{P(A \\cap B)", "\\over", "P(B)}"
        ).scale(1.4)
        formula[0][2].set_color(BLUE)
        formula[0][4].set_color(RED)

        self.play(Write(formula[0]))
        self.wait(0.5)
        self.play(FadeIn(formula[1]))
        self.wait(0.5)
        self.play(FadeIn(formula[2]))
        self.play(FadeIn(formula[3]), FadeIn(formula[4]))
        self.wait()

        self.play(formula[2].animate.set_color(PURPLE))
        self.wait()
        self.play(Circumscribe(formula[2]))
        self.wait()
        self.play(formula[4].animate.set_color(RED))
        self.play(Circumscribe(formula[4]))
        self.wait(1.5)
        self.play(Circumscribe(formula[0]))
        self.wait(3)

        self.play(FadeOut(formula))
        self.wait(2)
class ExplainFormula(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/ExplainFormula1.mp3")
        title = Text("Sơ đồ Venn", font="Noto Sans", color=YELLOW).scale(0.7).to_corner(UL)
        self.play(FadeIn(title))
        self.wait()
        # 1. Setup the Universe
        universe = Rectangle(width=6, height=4, color=WHITE)
        universe_label = Text("Không gian mẫu (S)", font="Noto Sans", font_size=20).next_to(universe, UP)
        self.play(Create(universe), Write(universe_label), run_time=3)
        self.wait(2)

        # 2. Create Sets A and B
        circle_a = Circle(radius=1.2, color=BLUE, fill_opacity=0.3).shift(LEFT * 0.7)
        circle_b = Circle(radius=1.2, color=RED, fill_opacity=0.3).shift(RIGHT * 0.7)
        
        label_a = Text("A", color=BLUE).next_to(circle_a, LEFT)
        label_b = Text("B", color=RED).next_to(circle_b, RIGHT)

        self.play(FadeIn(circle_a))
        self.play(Write(label_a))
        self.wait()
        self.play(FadeIn(circle_b))
        self.play(Write(label_b))
        self.wait()
        
        # 3. Highlight the Intersection (A and B)
        intersection = Intersection(circle_a, circle_b, color=PURPLE, fill_opacity=0.7)
        int_label = MathTex("A \\cap B", font_size=30).move_to(intersection)
        
        self.play(FadeIn(intersection), Write(int_label))
        self.wait()
        self.add_sound("voiceovers/ExplainFormula2.mp3")

        # 4. Show the "Condition" (Given B)
        # We darken everything that is NOT B to show the new sample space
        not_b_mask = Difference(universe, circle_b).set_fill(BLACK, opacity=0.7)
        
        formula = MathTex(
            "P(A|B) = ", "{P(A \\cap B)", "\\over", "P(B)}",
            font_size=48
        ).to_edge(DOWN, buff=0.5)
        formula[0][2].set_color(BLUE)
        formula[0][4].set_color(RED)
        formula[1].set_color(PURPLE)
        formula[3].set_color(RED)
        self.wait()
        self.play(FadeIn(not_b_mask), run_time=2)
        self.wait()
        self.play(circle_b.animate.set_stroke(YELLOW, width=8), run_time=2)
        self.wait(3)
        self.play(Indicate(circle_b, color=RED), run_time=2)
        self.wait()
        self.play(Indicate(intersection, color=PURPLE), run_time=2)
        self.wait()
        self.play( Write(formula[0]))
        self.wait(2)

        # 5. Link Visuals to Formula
        # Numerator: The purple part
        self.play(
            intersection.animate.scale(1.2).set_opacity(1),
            Write(formula[1]) # Write P(A intersection B)
        )
        self.play(intersection.animate.scale(1/1.2))
        self.wait()
        
        # Denominator: The Blue circle (the only thing that matters now)
        self.play(Write(formula[2]), Write(formula[3])) # Write / P(B)
        self.wait(3)

class NumericalExam(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/NumericalExam.mp3")
        title = Text("Ví dụ đơn giản", font="Noto Sans", color=YELLOW).scale(0.7).to_corner(UL)
        self.play(FadeIn(title))
        self.wait()
        # 1. Setup the Venn Diagram
        circle_a = Circle(radius=1.5, color=BLUE, fill_opacity=0.3).shift(LEFT * 0.8)
        circle_b = Circle(radius=1.5, color=RED, fill_opacity=0.3).shift(RIGHT * 0.8)
        intersection = Intersection(circle_a, circle_b, fill_opacity=0.5)
        total_b = circle_b.copy()
        
        # Labels for the circles
        label_a = Text("A", color=BLUE).next_to(circle_a, LEFT)
        label_b = Text("B", color=RED).next_to(circle_b, RIGHT)
        
        self.play(FadeIn(circle_a, circle_b, label_a, label_b))

        # 2. Add Numerical Values to regions
        # Area only in B (excluding intersection)
        val_b = MathTex("0.40", font_size=34).shift(RIGHT)
        val_b_only = MathTex("0.30", font_size=34).shift(RIGHT * 1.5)
        # Intersection area
        val_inter = MathTex("0.10", font_size=34).move_to(ORIGIN)
        # Area only in A
        val_a_only = MathTex("0.20", font_size=34).shift(LEFT * 1.5)

        self.play(Write(val_b))
        self.wait()
        self.play(Write(val_a_only), Transform(val_b, VGroup(val_inter, val_b_only)))

        # 3. The "Focus" Shift
        # Darken A and emphasize B
        not_b = FullScreenRectangle().set_fill(BLACK, opacity=0.8)
        mask = Cutout(not_b, circle_b).set_fill(BLACK, opacity=0.8)
        
        explanation = Text("Với điều kiện B đã cho: Chúng ta bỏ qua mọi thứ khác", font="Noto Sans", font_size=24, color=YELLOW).to_edge(UP)

        self.play(
            FadeIn(mask),
            FadeOut(val_a_only),
            FadeIn(explanation),
            circle_b.animate.set_stroke(YELLOW, width=6)
        )

        # 4. Construct the Calculation
        
        formula = MathTex(
            "P(A|B) = \\frac{\\text{Overlap}}{\\text{Total } B}",
            font_size=40
        ).shift(DOWN * 2.5)
        formula[0][2].set_color(BLUE)
        formula[0][4].set_color(RED)
        
        step_1 = MathTex(
            " = \\frac{0.10}{0.10 + 0.30}",
            font_size=40
        ).next_to(formula, RIGHT)

        step_2 = MathTex(
            " = \\frac{0.10}{0.40}",
            font_size=40
        ).next_to(formula, RIGHT)

        final = MathTex(
            " = 0.25",
            font_size=48, color=GREEN
        ).next_to(formula, RIGHT)

        # 5. Animate the Math
        self.play(Write(formula[0][:7]), Write(formula[0][14]), 
                  intersection.animate.scale(0.2).next_to(formula[0][14], UP, SMALL_BUFF),
                  total_b.animate.scale(0.2).next_to(formula[0][14], DOWN, SMALL_BUFF))
        self.play(Write(step_1), Indicate(val_inter), Indicate(val_b_only))
        self.play(Transform(step_1, step_2))
        self.play(Transform(step_1, final))
        self.wait(3)
        self.play(Circumscribe(step_1))
        self.wait(3)
class DiceExam(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/DiceExam1.mp3")
        title = Text("Hai con xúc xắc", font="Noto Sans").scale(0.7).to_corner(UL)
        self.play(FadeIn(title))
        self.wait()
        self.add_sound("voiceovers/dice19shuffle.flac")
        self.wait()
        problem = Text("Xác suất để giá trị mặt ngửa của con xúc xắc đầu tiên là 2, \nbiết rằng tổng của chúng không lớn hơn 5", font="Noto Sans", color=YELLOW)
        problem.scale(0.65).next_to(title, DOWN, aligned_edge=LEFT)
        self.play(Write(problem), run_time=5)
        self.wait()
        diagram = self.get_dice_diagram()
        x1_label = MathTex(r"X_1").next_to(diagram, LEFT)
        x2_label = MathTex(r"X_2").next_to(diagram, UP)
        VGroup(x1_label, diagram, x2_label).to_corner(DL)

        grid = diagram[0]
        result_two = MathTex("P(X_1 = 2) = \\frac{6}{36} = \\frac{1}{6}").scale(0.75)
        result_five = MathTex("P(X_1 + X_2 \\le 5) = \\frac{10}{36}").scale(0.75)
        result_condition = MathTex("P(X_1 = 2 | X_1 + X_2 \\le 5) = \\frac{3}{10} = 0.3").scale(0.75)
        VGroup(result_two, result_five, result_condition).arrange(DOWN, aligned_edge=LEFT).next_to(grid, RIGHT, LARGE_BUFF).to_edge(UP, LARGE_BUFF)
        prob_line = Line(LEFT, RIGHT).next_to(grid, RIGHT, LARGE_BUFF).shift(2*UP)
        arrow_two = MathTex(r"\downarrow").next_to(result_two[0][4], DOWN)
        arrow_five = MathTex(r"\downarrow").next_to(result_five[0][4], DOWN)
        arrow_condition = MathTex(r"\downarrow").next_to(result_condition[0][4], DOWN)
        
        five_part_origin = VGroup(*[
            square
            for i, row in enumerate(grid)
            for j, square in enumerate(row)
            if i + j <= 3
        ])
        two_part_origin = VGroup(*[
            square
            for i, row in enumerate(grid)
            for square in row
            if i == 1
        ])
        condition_part_origin = VGroup(*[
            square
            for i, row in enumerate(grid)
            for j, square in enumerate(row)
            if i + j <= 3 and i == 1
        ])
        self.add_sound("voiceovers/magic-dark-teleport.wav")
        self.play(FadeOut(problem), FadeIn(diagram, x1_label, x2_label))
        self.play(Indicate(x1_label), run_time=2)
        self.wait()
        self.play(Indicate(x2_label), run_time=2)
        self.wait()
        self.play(Circumscribe(grid), run_time=2)
        prob_of_each_num = MathTex("\\frac{1}{36}").scale(1.3).shift(3*RIGHT)
        self.play(FadeIn(prob_of_each_num[0][-2:]), Flash(prob_of_each_num[0][-2:]))
        self.wait(3)
        self.play(FadeIn(prob_of_each_num[0][:-2]))
        self.play(Circumscribe(prob_of_each_num))
        self.wait(1.5)
        sum_text = MathTex("X_1+X_2").next_to(prob_of_each_num, UP, LARGE_BUFF)
        self.play(FadeIn(sum_text))
        self.wait()
        self.play(FadeOut(prob_of_each_num, sum_text))
        self.wait()

        # Probability that X1 = 2
        self.add_sound("voiceovers/DiceExam2.mp3")
        result_two[0][2:6].set_color(YELLOW)
        self.add_sound("voiceovers/popchat.wav")
        self.play(FadeIn(result_two[0][2:6]))
        self.play(*[square.animate.set_fill(YELLOW, opacity=0.5) for square in two_part_origin])
        self.wait(3)
        
        grid_copy_two = grid.copy()
        
        self.add(grid_copy_two, diagram[1])
        self.play(
            FadeIn(result_two[0][:2], result_two[0][6])
        )
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(
            FadeIn(arrow_two, prob_line),
            grid_copy_two.animate.scale(0.35).next_to(prob_line, DOWN),
        )
        two_part = VGroup(*[
            square
            for i, row in enumerate(grid_copy_two)
            for square in row
            if i == 1
        ]).copy()
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(two_part.animate.next_to(prob_line, UP))
        self.play(Transform(two_part, MathTex("6").next_to(prob_line, UP)), Transform(grid_copy_two, MathTex("36").next_to(prob_line, DOWN)))
        self.play(Transform(VGroup(two_part, grid_copy_two), result_two[0][7:]),
                  FadeOut(arrow_two), FadeOut(prob_line))
        self.add_sound("voiceovers/correct-choice.wav")
        self.play(Flash(result_two[0][-2]))
        self.wait()

        # Probability that X1 + X2 ≤ 5
        self.add_sound("voiceovers/DiceExam3.mp3")
        result_five[0][2:9].set_color(BLUE)
        self.add_sound("voiceovers/popchat.wav")
        self.play(FadeIn(result_five[0][2:9]))
        self.wait()
        prob_line.shift(2*DOWN)
        self.play(*[square.animate.set_fill(BLUE, opacity=0.5) for square in five_part_origin])       
        self.wait(3)
        
        grid_copy_five = grid.copy()
        self.add(grid_copy_five)
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(
            FadeIn(result_five[0][:2], result_five[0][9]),
            FadeIn(arrow_five, prob_line),
            grid_copy_five.animate.scale(0.35).next_to(prob_line, DOWN),
        )
        five_part = VGroup(*[
            square
            for i, row in enumerate(grid_copy_five)
            for j, square in enumerate(row)
            if i + j <= 3
        ]).copy()    
        self.add_sound("voiceovers/sword-swing.wav") 
        self.play(five_part.animate.next_to(prob_line, UP))
        self.play(Transform(five_part, MathTex("10").next_to(prob_line, UP)), Transform(grid_copy_five, MathTex("36").next_to(prob_line, DOWN)))
        self.play(Transform(VGroup(five_part, grid_copy_five), result_five[0][10:]),
                  FadeOut(arrow_five), FadeOut(prob_line))
        self.add_sound("voiceovers/correct-choice.wav")
        self.play(Flash(result_five[0][11:]))
        self.wait()

        # Probability that X1 = 2 given that X1 + X2 ≤ 5
        self.add_sound("voiceovers/DiceExam4.mp3")
        prob_line.shift(0.5*DOWN)
        self.play(*[square.animate.set_fill(GREEN, opacity=0.5) for square in condition_part_origin],
                  Circumscribe(condition_part_origin)) 
        result_condition[0][2:14].set_color(GREEN)
        self.add_sound("voiceovers/popchat.wav")
        self.play(FadeIn(result_condition[0][2:14]))
        self.wait()
        grid_copy_condition = five_part_origin.copy()
        self.add(grid_copy_condition)
        self.play(FadeIn(result_condition[0][:2], result_condition[0][14]))
        self.wait(2)
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(
            FadeIn(arrow_condition, prob_line),
            grid_copy_condition.animate.scale(0.35).next_to(prob_line, DOWN),
        )
        condition_part = VGroup(*[
            square
            for i, square in enumerate(grid_copy_condition)
            if i in (4, 5, 6)
        ]).copy()     
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(condition_part.animate.next_to(prob_line, UP))
        self.play(Transform(condition_part, MathTex("3").next_to(prob_line, UP)), Transform(grid_copy_condition, MathTex("10").next_to(prob_line, DOWN)))
        self.play(Transform(VGroup(condition_part, grid_copy_condition), result_condition[0][15:]),
                  FadeOut(arrow_condition), FadeOut(prob_line))
        self.add_sound("voiceovers/correct-choice.wav")
        self.play(Flash(result_condition[0][-3:]))
        self.wait()

        self.add_sound("voiceovers/DiceExam5.mp3")
        self.wait(4)
        brace_A = Brace(result_condition[0][2:6])
        brace_A_text = brace_A.get_tex("A")
        brace_B = Brace(result_condition[0][7:14])
        brace_B_text = brace_B.get_tex("B")
        result_formula = MathTex("P(A|B) = \\frac{P(A \\cap B)}{P(B)} = \\frac{3/36}{10/36} = \\frac{3}{10}").scale(0.75)
        result_formula.next_to(brace_B, DOWN)
        A_text = result_formula[0][2].set_color(YELLOW)
        B_text = result_formula[0][4].set_color(BLUE)
        A_text.target, B_text.target = brace_A_text, brace_B_text
        for mob in (A_text, B_text):
            mob.save_state()
            mob.move_to(mob.target)
        self.play(FadeIn(B_text))
        self.play(FadeIn(brace_B))
        self.wait()
        self.play(FadeIn(A_text))
        self.play(FadeIn(brace_A))
        self.wait()
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(FadeIn(result_formula[0][:2], result_formula[0][3], result_formula[0][5]),
                  *[mob.animate.restore() for mob in (A_text, B_text)],
                  FadeOut(brace_A, brace_B))
        self.wait(0.5)
        result_formula[0][9:12].set_color(GREEN)
        self.play(FadeIn(result_formula[0][6:13]))
        result_formula[0][16].set_color(BLUE)
        self.play(FadeIn(result_formula[0][13:18]))
        self.wait(0.5)
        self.play(FadeIn(result_formula[0][18:29]))
        self.wait(1.5)
        self.play(FadeIn(result_formula[0][29:]))
        self.add_sound("voiceovers/correct-choice.wav")
        self.play(Flash(result_formula[0][-4:]))
        self.wait(4)

    def get_die_faces(self):
        dot = Dot(radius=0.075, color=BLUE_B)

        square = Square()
        square.round_corners(0.25)
        square.set_stroke(WHITE, 2)
        square.set_fill(GREY_E, 1)
        square.set_width(0.6)

        edge_groups = [
            (ORIGIN,),
            (UL, DR),
            (UL, ORIGIN, DR),
            (UL, UR, DL, DR),
            (UL, UR, ORIGIN, DL, DR),
            (UL, UR, LEFT, RIGHT, DL, DR),
        ]

        arrangements = VGroup(*[
            VGroup(*[
                dot.copy().move_to(square.get_critical_point(ec))
                for ec in edge_group
            ])
            for edge_group in edge_groups
        ])


        square.set_width(1)

        faces = VGroup(*[
            VGroup(square.copy(), arrangement)
            for arrangement in arrangements
        ])
        faces.arrange(RIGHT)

        return faces

    def get_random_dice(self):
        faces = list(self.get_die_faces())

        def get_random_pair():
            result = VGroup(*random.sample(faces, 2)).copy()
            result.arrange(RIGHT)
            for mob in result:
                mob.shift(random.random() * RIGHT * MED_SMALL_BUFF)
                mob.shift(random.random() * UP * MED_SMALL_BUFF)
            return result

        result = VGroup(*get_random_pair())
        result.time = 0
        result.iter_count = 0

        def update_result(group, dt):
            group.time += dt
            group.iter_count += 1

            if int(group.time) % 3 == 2:
                group.set_stroke(YELLOW)
            elif group.iter_count % 3 == 0:
                pair = get_random_pair()
                pair.move_to(group)
                group.submobjects = [*pair]

        result.add_updater(update_result)
        result.update()
        return result

    def get_dice_diagram(self):
        grid = VGroup(*[
            VGroup(*[
                Square() for _ in range(6)
            ]).arrange(RIGHT, buff=0)
            for _ in range(6)
        ]).arrange(DOWN, buff=0)

        grid.set_stroke(WHITE, 1)
        grid.set_height(5)

        numbers = VGroup()
        for i, row in enumerate(grid):
            for j, square in enumerate(row):
                num = Integer(i + j + 2)
                num.set_height(square.get_height() - MED_LARGE_BUFF)
                num.move_to(square)
                num.set_fill(GREY_D)
                numbers.add(num)

        faces = VGroup()
        face_templates = self.get_die_faces()
        face_templates.scale(0.5)

        for face, row in zip(face_templates, grid):
            face.next_to(row, LEFT, MED_SMALL_BUFF)
            faces.add(face)

        for face, square in zip(faces.copy(), grid[0]):
            face.next_to(square, UP, MED_SMALL_BUFF)
            faces.add(face)

        return VGroup(grid, numbers, faces)
class Summary(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/Summary.mp3")
        title = Text("Tóm lại", color=YELLOW, font="Noto Sans", font_size=48).to_edge(UP)
        formula = MathTex("P(A|B) = \\frac{P(A\\cap B)}{P(B)}")
        formula[0][2].set_color(BLUE)
        formula[0][4].set_color(RED)
        formula[0][9:12].set_color(PURPLE)
        formula[0][16].set_color(RED)
        bullets = VGroup(
            Text("• Xác suất khi đã biết một thông tin mới", font="Noto Sans"),
            Text("• Không gian bị thu hẹp", font="Noto Sans"),
            formula,
            Text("• Cơ sở của định lý Bayes và Machine Learning", font="Noto Sans")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).scale(0.9)

        bullets.next_to(title, DOWN, buff=0.7)

        self.play(Write(title))
        for line in bullets:
            self.play(FadeIn(line, shift=RIGHT), run_time=3)
            self.wait()
        self.wait(2)
        self.add_sound("voiceovers/thankyou.wav")
        self.wait(2)
        self.play(FadeOut(title, bullets))
class ConditionalProbability(Scene):

    def construct(self):
        self.scene_intro()
        self.scene_definition()
        self.scene_formula()
        self.scene_dice_example()
        self.scene_sample_space_shrink()
        self.scene_bayes_bridge()
        self.scene_summary()

    # ----------------------------------------------------
    # Scene 1 — Intro & Hook
    # ----------------------------------------------------
    def scene_intro(self):
        title = Text("Conditional Probability", font="Noto Sans", font_size=56)
        subtitle = Text("Xác suất có điều kiện", font="Noto Sans", font_size=36, color=YELLOW)

        subtitle.next_to(title, DOWN)

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle))

    # ----------------------------------------------------
    # Scene 2 — Intuition with Venn Diagram
    # ----------------------------------------------------
    def scene_definition(self):
        title = Text("Intuition", font="Noto Sans", font_size=42).to_edge(UP)

        circle_A = Circle(radius=2, color=BLUE).shift(LEFT * 1.5)
        circle_B = Circle(radius=2, color=RED).shift(RIGHT * 1.5)

        label_A = MathTex("A").next_to(circle_A, LEFT)
        label_B = MathTex("B").next_to(circle_B, RIGHT)

        inter = Intersection(circle_A, circle_B, color=PURPLE, fill_opacity=0.6)

        text = MathTex("P(A|B)").next_to(inter, DOWN)

        self.play(Write(title))
        self.play(Create(circle_A), Create(circle_B))
        self.play(Write(label_A), Write(label_B))
        self.wait(0.5)

        self.play(FadeIn(inter))
        self.play(Write(text))
        self.wait(2)

        self.play(FadeOut(title), FadeOut(circle_A), FadeOut(circle_B),
                  FadeOut(label_A), FadeOut(label_B), FadeOut(inter), FadeOut(text))

    # ----------------------------------------------------
    # Scene 3 — Formula
    # ----------------------------------------------------
    def scene_formula(self):
        formula = MathTex(
            "P(A|B)", "=", "{P(A \\cap B)", "\\over", "P(B)}"
        ).scale(1.4)

        self.play(Write(formula))
        self.wait(1)

        self.play(formula[2].animate.set_color(PURPLE))
        self.play(formula[4].animate.set_color(RED))
        self.wait(2)

        self.play(FadeOut(formula))

    # ----------------------------------------------------
    # Scene 4 — Dice Example
    # ----------------------------------------------------
    def scene_dice_example(self):
        title = Text("Dice Example", font="Noto Sans", font_size=42).to_edge(UP)

        nums = VGroup(*[
            Text(str(i), font_size=48).move_to(LEFT*3 + RIGHT*i)
            for i in range(1, 7)
        ])

        A_text = MathTex("A = \\{2,4,6\\}", color=BLUE).to_edge(LEFT).shift(DOWN)
        B_text = MathTex("B = \\{4,5,6\\}", color=RED).next_to(A_text, DOWN)
        inter_text = MathTex("A \\cap B = \\{4,6\\}", color=PURPLE).next_to(B_text, DOWN)

        self.play(Write(title))
        self.play(FadeIn(nums, shift=UP))
        self.wait(0.5)

        self.play(Write(A_text))
        self.play(nums[1].animate.set_color(BLUE),
                  nums[3].animate.set_color(BLUE),
                  nums[5].animate.set_color(BLUE))

        self.play(Write(B_text))
        self.play(nums[3].animate.set_color(PURPLE),
                  nums[4].animate.set_color(RED),
                  nums[5].animate.set_color(PURPLE))

        self.play(Write(inter_text))
        self.wait(1.5)

        result = MathTex("P(A|B) = {2 \\over 3}", color=YELLOW).scale(1.3).to_edge(DOWN)
        self.play(Write(result))
        self.wait(2)

        self.play(FadeOut(title), FadeOut(nums), FadeOut(A_text),
                  FadeOut(B_text), FadeOut(inter_text), FadeOut(result))

    # ----------------------------------------------------
    # Scene 5 — Sample Space Shrinks
    # ----------------------------------------------------
    def scene_sample_space_shrink(self):
        title = Text("Shrinking Sample Space", font="Noto Sans", font_size=42).to_edge(UP)

        omega = Rectangle(width=6, height=4, color=WHITE)
        label_omega = MathTex("\\Omega").next_to(omega, UP)

        B_box = Rectangle(width=3, height=2, color=RED)
        B_label = MathTex("B").move_to(B_box)

        self.play(Write(title))
        self.play(Create(omega), Write(label_omega))
        self.wait(0.5)

        self.play(Transform(omega, B_box), Transform(label_omega, B_label))
        self.wait(2)

        self.play(FadeOut(title), FadeOut(omega), FadeOut(label_omega))

    # ----------------------------------------------------
    # Scene 6 — Bridge to Bayes
    # ----------------------------------------------------
    def scene_bayes_bridge(self):
        title = Text("Bridge to Bayes", font="Noto Sans", font_size=42).to_edge(UP)

        bayes = MathTex(
            "P(A|B) = {P(B|A)P(A) \\over P(B)}"
        ).scale(1.3)

        self.play(Write(title))
        self.play(Write(bayes))
        self.wait(2)

        label = Text("Bayes' Theorem", font="Noto Sans", font_size=36, color=YELLOW).next_to(bayes, DOWN)
        self.play(Write(label))
        self.wait(2)

        self.play(FadeOut(title), FadeOut(bayes), FadeOut(label))

    # ----------------------------------------------------
    # Scene 7 — Summary
    # ----------------------------------------------------
    def scene_summary(self):
        title = Text("Summary", font="Noto Sans", font_size=48).to_edge(UP)

        bullets = VGroup(
            Text("• Probability given information", font="Noto Sans"),
            Text("• Reduced sample space", font="Noto Sans"),
            MathTex("P(A|B) = \\frac{P(A\\cap B)}{P(B)}"),
            Text("• Foundation of Bayes & Machine Learning", font="Noto Sans")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).scale(0.9)

        bullets.next_to(title, DOWN, buff=0.7)

        self.play(Write(title))
        for line in bullets:
            self.play(FadeIn(line, shift=RIGHT))
            self.wait(0.4)

        self.wait(3)

class ThumbnailConditional(Scene):
    def construct(self):
        # --- Title ---
        title = Text(
            "Conditional Probability",
            font_size=72,
            weight=BOLD
        ).to_edge(UP)

        subtitle = Text(
            "XÁC SUẤT CÓ ĐIỀU KIỆN", font="Noto Sans",
            font_size=42,
            color=YELLOW
        ).next_to(title, DOWN, buff=0.25)

        # --- Venn Diagram ---
        A = Circle(radius=1.3, color=BLUE, stroke_width=6).shift(LEFT*3.5 + DOWN*0.5)
        B = Circle(radius=1.3, color=RED, stroke_width=6).shift(LEFT*2 + DOWN*0.5)

        label_A = Text("A", font_size=48, color=BLUE).next_to(A, LEFT).shift(RIGHT)
        label_B = Text("B", font_size=48, color=RED).next_to(B, RIGHT).shift(LEFT)

        inter = Intersection(A, B, color=PURPLE, fill_opacity=0.8)

        # --- Formula ---
        formula = MathTex(
            "P(A|B) = \\frac{P(A \\cap B)}{P(B)}",
            font_size=64
        ).shift(RIGHT*3 + DOWN*0.5)

        # --- ML Tag ---
        ml_tag = Text(
            "Cơ sở của định lý Bayes và Machine Learning",
            font_size=34, font="Noto Sans",
            color=GREEN
        ).to_edge(DOWN)

        # --- Composition ---
        self.add(A, B, inter, label_A, label_B)
        self.add(formula)
        self.add(title, subtitle, ml_tag)
        self.wait(0.5)
