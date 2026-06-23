from manim import *
import random
from Bubble import *
from pi_creature_scene import *
import math
from math import erf, sqrt, pi

class HookScene(Scene):
    def construct(self):
        self.add_sound("voiceovers/HookScene.mp3")
        title = Text("Mỗi ngày, chúng ta đều phải đưa ra quyết định \n mà không biết chắc điều gì sẽ xảy ra.", 
                     font="Noto Sans")

        self.play(Write(title), run_time=3)
        self.wait()
        self.play(FadeOut(title))
        question = Text("???", font_size=96, weight=BOLD)
        
        rain = SVGMobject("assets/43.svg").to_edge(LEFT, LARGE_BUFF).scale(1.2).set_z_index(3)
        
        dice = SVGMobject("assets/dice.svg").to_edge(DOWN, LARGE_BUFF).set_z_index(3)
        dice.set_color(GREEN)
        
        youtube = SVGMobject("assets/youtube.svg").to_edge(RIGHT, LARGE_BUFF).scale(0.8).set_z_index(3)
        youtube.set_fill(RED, opacity=.7)
        self.add_sound("voiceovers/popchat.wav")
        self.play(FadeIn(rain), FadeIn(question[0], shift=UP))
        self.wait(0.5)
        self.add_sound("voiceovers/popchat.wav")
        self.play(FadeIn(youtube, shift=LEFT), FadeIn(question[1], shift=UP))
        self.wait(0.5)
        self.add_sound("voiceovers/popchat.wav")
        self.play(FadeIn(dice, shift=DOWN), FadeIn(question[2], shift=UP))
        self.wait(0.5)
        uncertain = Text("Bất định", font="Noto Sans", color=YELLOW)
        group = VGroup(title, rain, dice, youtube, question)
        self.play(Transform(group, uncertain))
        self.wait()
        self.play(FadeOut(group))
        prob = Text("Xác suất", font="Noto Sans", color=BLUE).to_edge(LEFT, LARGE_BUFF)
        stats = Text("Thống kê", font="Noto Sans", color=GREEN).to_edge(RIGHT, LARGE_BUFF)
        and_text = Text("&")
        self.play(Write(prob))
        self.wait(2)
        self.play(Write(stats))
        self.wait(2.5)
        self.play(Write(and_text), 
                  prob.animate.next_to(and_text, LEFT),
                  stats.animate.next_to(and_text, RIGHT))
        self.wait()
        self.play(Circumscribe(VGroup(prob, and_text, stats)))
        self.wait(5)
class IntroScene(Scene):
    def construct(self):
        self.add_sound("voiceovers/HookScene_part1.mp3")
        title = Text("Mỗi ngày, chúng ta đều phải đưa ra quyết định \n mà không biết chắc điều gì sẽ xảy ra.", 
                     font="Noto Sans")

        self.play(Write(title), run_time=3)
        self.wait()
        self.add_sound("voiceovers/rain-rumble.wav")
        self.play(FadeOut(title))
        question = Text("???", font="Noto Sans", font_size=96, weight=BOLD).to_edge(UP)
        # Cloud parts
        cloud_color = LIGHT_GREY

        c1 = Circle(radius=0.6, fill_opacity=1, color=cloud_color).shift(LEFT * 0.8)
        c2 = Circle(radius=0.8, fill_opacity=1, color=cloud_color)
        c3 = Circle(radius=0.6, fill_opacity=1, color=cloud_color).shift(RIGHT * 0.8)

        cloud_base = RoundedRectangle(
            width=3,
            height=0.9,
            corner_radius=0.4,
            fill_opacity=1,
            color=cloud_color
        ).shift(DOWN * 0.4)

        cloud = VGroup(c1, c2, c3, cloud_base).shift(UP * 1.5).to_edge(LEFT, LARGE_BUFF)
        self.add(cloud)

        # Raindrops
        drops = VGroup()
        for x in [-0.8, -0.3, 0.3, 0.8]:
            drop = Line(
                start=UP * 0.3,
                end=DOWN * 0.3,
                stroke_width=4,
                color=BLUE
            ).shift(np.array([x, 0, 0]))
            drops.add(drop)

        drops.next_to(cloud, DOWN, buff=0.2)
        self.add(drops)

        # Animate rain falling
        drops.add_updater(
            lambda m, dt: m.shift(DOWN * dt * 2)
        )
        self.play(FadeIn(question[0], shift=UP))
        self.wait(2)
        drops.clear_updaters()
        # Screen body
        screen = RoundedRectangle(
            width=4,
            height=2.5,
            corner_radius=0.3,
            stroke_width=3
        )

        # Play button (triangle)
        play_button = Polygon(
            LEFT * 0.4 + UP * 0.5,
            LEFT * 0.4 + DOWN * 0.5,
            RIGHT * 0.6,
            fill_color=RED_E,
            color=RED_E,
            fill_opacity=1
        )

        # Group and center
        icon = VGroup(screen, play_button)
        play_button.move_to(screen.get_center())

        # self.add(icon)

        # Optional simple animation
        self.add_sound("voiceovers/HookScene_part2.mp3")
        self.add_sound("voiceovers/popchat.wav")
        self.play(
            FadeIn(screen),
            GrowFromCenter(play_button),
            FadeIn(question[1], shift=UP),
            run_time=1
        )
        self.wait(2)
        # Dice body
        dice = RoundedRectangle(
            width=2,
            height=2,
            corner_radius=0.2,
            fill_opacity=1,
            fill_color=GREEN,
            stroke_width=3,
            stroke_color=BLACK
        )

        dice.shift(UP * 3)

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

        pips.move_to(dice.get_center())

        dice_group = VGroup(dice, pips).to_edge(RIGHT, LARGE_BUFF)
        self.add_sound("voiceovers/HookScene_part3.mp3")
        self.play(FadeIn(dice_group))

        # Landing animation
        self.add_sound("voiceovers/dice19shuffle.flac")
        self.play(
            dice_group.animate.shift(DOWN * 3).rotate(PI),
            FadeIn(question[2], shift=UP),
            rate_func=rate_functions.ease_out_bounce,  # fixed
            run_time=2
        )

        self.wait()
        self.add_sound("voiceovers/HookScene_part4.mp3")
        uncertain = Text("Bất định", font="Noto Sans", color=YELLOW)
        group = VGroup(cloud, drops, dice_group, icon, question)
        self.play(Transform(group, uncertain))
        self.wait()
        prob = Text("Xác suất", font="Noto Sans", color=YELLOW).to_edge(LEFT, LARGE_BUFF)
        stats = Text("Thống kê", font="Noto Sans", color=BLUE).to_edge(RIGHT, LARGE_BUFF)
        and_text = Text("&")
        self.play(FadeOut(group), Write(prob))
        self.wait(2)
        self.play(Write(stats))
        self.wait(2.5)
        self.play(Write(and_text), 
                  prob.animate.next_to(and_text, LEFT),
                  stats.animate.next_to(and_text, RIGHT))
        self.wait()
        self.play(Circumscribe(VGroup(prob, and_text, stats)))
        self.wait(2)
        hand = ImageMobject("assets/hand.png").scale(0.3).to_corner(UL)
        self.play(FadeIn(hand))
        self.wait(3)

class ProbabilityDefinition(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/ProbabilityDefinition.mp3")
        doors = VGroup(*[SVGMobject("assets/door-575567.svg").set_z_index(3).set_height(3) for _ in range(3)])
        doors.arrange(RIGHT, LARGE_BUFF).to_corner(UR, LARGE_BUFF).shift(LEFT)
        monster = SVGMobject("assets/1.svg")
        three_eyes = SVGMobject("assets/41.svg")
        girl = SVGMobject("assets/23.svg")
        outcomes = VGroup(monster, three_eyes, girl).arrange(RIGHT, LARGE_BUFF).to_corner(UR, LARGE_BUFF)

        confused = SVGMobject("assets/17.svg").to_edge(DOWN, LARGE_BUFF)
        understood = SVGMobject("assets/46.svg").to_edge(DOWN, LARGE_BUFF)
        self.play(LaggedStartMap(FadeIn, doors, lag_ratio=1.5))
        self.wait(3)
        self.play(FadeIn(confused))
        self.wait(2)
        self.play(FadeOut(confused), FadeIn(understood), LaggedStartMap(FadeIn, outcomes, lag_ratio=1.0))
        self.wait()
        self.play(Circumscribe(monster))
        self.play(Circumscribe(three_eyes))
        self.play(Circumscribe(girl))
        self.wait(2)
        self.play(FadeOut(doors), FadeOut(understood),
                  FadeOut(monster), FadeOut(three_eyes), FadeOut(girl))
        self.wait()
        formula = MathTex(r"P(A) = \frac{11111111111111111111}{2}")
        formula[0][0].set_color(YELLOW)
        formula[0][2].set_color(GREEN)
        eq = formula[0][4:5]
        numerator = formula[0][5:25]
        denominator = formula[0][-1:]
        favorable = Text("Số kết quả thuận lợi", font="Noto Sans", color=GREEN)
        favorable.scale(0.65).move_to(numerator)
        total = Text("Tổng số kết quả", font="Noto Sans", color=BLUE)
        total.scale(0.65).move_to(denominator)
        prob_text = Text("* P: Xác suất, A: Kết quả thuận lợi", font="Noto Sans", slant=ITALIC)
        prob_text[1].set_color(YELLOW)
        prob_text[11].set_color(GREEN)
        prob_text.scale(0.65).to_edge(DOWN, LARGE_BUFF)
        
        self.play(Write(formula[0][:4]), FadeIn(prob_text))
        self.play(Write(eq), Write(favorable))
        self.play(Write(formula[0][-2:-1]), Write(total))
        self.play(Circumscribe(VGroup(formula)))
        self.wait(3)

class ProbabilityLineBasic(Scene):
    def construct(self):
        self.wait()
        title = Text("Trục xác suất từ 0 → 1", font="Noto Sans", color=YELLOW, font_size=42).to_edge(UP)
        self.play(FadeIn(title))
        line = NumberLine(
            x_range=[0, 1, 0.1],
            length=8,
            include_numbers=True
        )
        arrows = VGroup(
            Arrow(0.5*UP, 0.5*DOWN, color=YELLOW).next_to(line.n2p(0), UP),
            Arrow(0.5*UP, 0.5*DOWN, color=YELLOW).next_to(line.n2p(0.5), UP),
            Arrow(0.5*UP, 0.5*DOWN, color=YELLOW).next_to(line.n2p(1), UP),
        )

        labels = VGroup(
            Text("Không thể xảy ra", color=RED_D, font="Noto Sans").scale(0.5).next_to(arrows[0], UP),
            Text("Không chắc chắn", font="Noto Sans").set_color_by_gradient(RED_D, BLUE).scale(0.5).next_to(arrows[1], UP),
            Text("Chắc chắn", color=BLUE, font="Noto Sans").scale(0.5).next_to(arrows[2], UP),
        )

        self.add_sound("voiceovers/ProbabilityLineBasic.mp3")
        self.play(Create(line), run_time=1.5)
        self.add_sound("voiceovers/ui_pop_up.mp3")
        self.play(FadeIn(arrows[0]))
        self.wait()
        self.add_sound("voiceovers/slidecard03.wav")
        self.play(Transform(arrows[0], arrows[2]), run_time=1.5)

        self.play(FadeIn(labels[0]))
        self.wait()
        self.play(FadeIn(labels[2]))
        self.wait(2)
        self.add_sound("voiceovers/slidecard03.wav")
        self.play(FadeIn(labels[1]), Transform(arrows[0], arrows[1]))
        
        self.play(FadeOut(arrows[0], shift=2*LEFT, run_time=2))
        self.wait()
class CoinDiceScene(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/CoinDiceScene.mp3")
        coins = VGroup(SVGMobject("assets/bitcoin.svg").scale(0.4), SVGMobject("assets/Bitcoin-Currency.svg").scale(0.4)).arrange(RIGHT)
        dices = VGroup(*[SVGMobject(f"assets/dice_{i}.svg").set_fill(BLUE).scale(0.4) for i in range(1, 7)]).arrange(RIGHT)

        head = Text("P(Mặt ngửa)", font="Noto Sans").scale(0.65)
        head[0].set_color(YELLOW)
        coin_prob = MathTex("=\\frac{1}{2}")
        eq_coin = coin_prob[0][0]
        coin_label = VGroup(head, coin_prob).arrange(RIGHT)
        dice_label = MathTex("P(6)=\\frac{1}{6}")
        dice_label[0][0].set_color(YELLOW)
        eq_dice = dice_label[0][4]

        coin_group = VGroup(coins, coin_label).arrange(DOWN)
        die_group = VGroup(dices, dice_label).arrange(DOWN)

        VGroup(coin_group, die_group).arrange(RIGHT, 2*LARGE_BUFF)

        self.play(*[FadeIn(coin) for coin in coins], run_time=1.5)
        self.play(Wiggle(coins[0]), run_time=0.5)
        self.play(Wiggle(coins[1]))
        self.wait(2)
        self.play(FadeIn(head[:2]),
                  Transform(coins[0].copy(), head[2:9]),
                  FadeIn(head[9:]))
        self.play(Write(coin_prob))
        self.wait()
        self.play(*[DrawBorderThenFill(dice) for dice in dices], run_time=2)
        self.wait()
        self.play(FadeIn(dice_label[0][:2]),
                  Transform(dices[5].copy(), dice_label[0][2:3]))
        self.play(Write(dice_label[0][3:]))
        definition = Text("Xác suất cổ điển", font="Noto Sans", color=YELLOW).scale(0.7).to_edge(UP)
        self.play(Write(definition))
        self.wait(3)
        question_coin = MathTex("?").set_color(RED).move_to(eq_coin)
        question_dice = MathTex("?").set_color(RED).move_to(eq_dice)
        self.play(FadeIn(question_coin), FadeIn(question_dice))
        self.play(question_coin.animate.scale(1.5),
                  question_dice.animate.scale(1.5))
        self.wait(4)
class ProbabilityLineExamples(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/prob_line2.mp3")
        coins = VGroup(SVGMobject("assets/bitcoin.svg").scale(0.4), SVGMobject("assets/Bitcoin-Currency.svg").scale(0.4)).arrange(RIGHT)
        coins.to_edge(UP)
        dices = VGroup(*[SVGMobject(f"assets/dice_{i}.svg").set_fill(BLUE).scale(0.4) for i in range(1, 7)]).arrange_in_grid(2, 3)
        dices.to_edge(UP)

        line = NumberLine(
            x_range=[0, 1, 0.1],
            length=8,
            include_numbers=True
        ).shift(DOWN)

        coin_dot = Dot(color=BLUE).move_to(line.n2p(0.5))
        dice_dot = Dot(color=RED).move_to(line.n2p(1/6))
        arrow_coin = Arrow(0.5*UP, 0.5*DOWN, color=YELLOW).next_to(coin_dot, UP)
        arrow_dice = Arrow(0.5*UP, 0.5*DOWN, color=YELLOW).next_to(dice_dot, UP)
        head = Text("P(Mặt ngửa)", font="Noto Sans").scale(0.65)
        head[0].set_color(YELLOW)
        coin_prob = MathTex("=\\frac{1}{2}")
        coin_label = VGroup(head, coin_prob).arrange(RIGHT).next_to(arrow_coin, UP)
        dice_label = MathTex("P(6)=\\frac{1}{6}").next_to(arrow_dice, UP)
        dice_label[0][0].set_color(YELLOW)

        self.play(Create(line), *[FadeIn(coin) for coin in coins], run_time=1.5)
        self.add_sound("voiceovers/ui_pop_up.mp3")
        self.play(FadeIn(coin_dot), FadeIn(arrow_coin, shift=RIGHT), FadeIn(coin_label))
        self.wait()
        self.play(FadeOut(coin_dot), FadeOut(coin_label),FadeOut(coins))
        self.play(*[FadeIn(dice) for dice in dices])
        self.play(Circumscribe(dices[5]))
        self.add_sound("voiceovers/slidecard03.wav")
        self.play(Transform(arrow_coin, arrow_dice), FadeIn(dice_dot), FadeIn(dice_label))
        self.wait(4)

class CoinTosses(Scene):
    def construct(self):
        self.wait()      
        random.seed(3)  # reproducible results
        # Title
        title = Text("Thí nghiệm tung đồng xu", font_size=44, font="Noto Sans")
        title.to_edge(UP)

        # Counters
        heads_count = 0
        tails_count = 0

        heads_no = Text("#", font_size=32, font="Noto Sans")     
        heads_text = Text(": 0", font_size=32, font="Noto Sans")
        heads_group = VGroup(heads_no, SVGMobject("assets/bitcoin.svg").scale(0.2), heads_text).arrange(RIGHT)
        tails_no = Text("#", font_size=32, font="Noto Sans")
        tails_text = Text(": 0", font_size=32, font="Noto Sans")
        tails_group = VGroup(tails_no, SVGMobject("assets/Bitcoin-Currency.svg").scale(0.2), tails_text).arrange(RIGHT)

        counters = VGroup(heads_group, tails_group).arrange(
            DOWN, aligned_edge=LEFT
        ).to_corner(LEFT + DOWN)

        self.play(Write(title), FadeIn(counters))
        self.add_sound("voiceovers/CoinTosses.mp3")

        # Toss display area
        toss_group = VGroup()
        toss_group.next_to(title, DOWN, buff=1)

        n_tosses = 40

        for i in range(n_tosses):
            outcome = random.choice(["H", "T"])

            if outcome == "H":
                coin = SVGMobject("assets/bitcoin.svg").scale(0.3).rotate(PI)
            else:
                coin = SVGMobject("assets/Bitcoin-Currency.svg").scale(0.3).rotate(PI)

            # Add coin to row
            toss_group.add(coin)
            # toss_group.arrange(RIGHT, buff=0.5)
            toss_group.arrange_in_grid(cols=10, buff=0.1)

            # Animate coin flip appearance
            # self.play(
            #     coin.animate.rotate(PI).fade(),
            #     run_time=0.5
            # )
            anims = [coin.animate.rotate(PI).fade()]
            if outcome == "H":
                heads_count += 1
                new_heads = Text(f": {heads_count}", font_size=32, font="Noto Sans")
                new_heads.move_to(heads_text)
                # self.play(Transform(heads_text, new_heads))
                anims.append(Transform(heads_text, new_heads))
            else:
                tails_count += 1
                new_tails = Text(f": {tails_count}", font_size=32, font="Noto Sans")
                new_tails.move_to(tails_text)
                # self.play(Transform(tails_text, new_tails))
                anims.append(Transform(tails_text, new_tails))
            self.play(*anims, run_time=0.3)

        # Empirical probability
        head_text = Text("P(")
        probability = VGroup(head_text, SVGMobject("assets/bitcoin.svg").scale(0.3), Text(")"),
                             MathTex(r" \approx",rf"\frac{{{heads_count}}}{{{n_tosses}}}")
                             .scale(1.3)).arrange(RIGHT)

        probability.next_to(toss_group, DOWN, buff=1)

        self.play(Write(probability))
        self.play(Circumscribe(probability))
        self.wait()     
        self.play(FadeOut(toss_group), FadeOut(title), FadeOut(counters), FadeOut(probability))
        self.add_sound("voiceovers/CoinTosses_part2.mp3")
        large_number_rule_title = Text("Luật số lớn", font="Noto Sans", color=YELLOW)
        large_number_rule_title.scale(0.7).to_edge(UP)
        large_number_rule = Text("Xác suất là thứ mà \n tần suất dài hạn sẽ hội tụ về.", font="Noto Sans").scale(0.65)
        self.play(Write(large_number_rule_title))
        self.wait()
        self.play(Write(large_number_rule), run_time=3)
        self.wait(3)
class ProbabilityLineConvergence(Scene):
    def construct(self):
        self.wait()
        title = Text("Trục xác suất với đồng xu", font="Noto Sans", color=YELLOW, font_size=42).to_edge(UP)
        line = NumberLine(
            x_range=[0, 1, 0.1],
            length=8,
            include_numbers=True
        )

        dot = Dot(color=YELLOW)
        dot.move_to(line.n2p(0.2))

        self.play(FadeIn(title), Create(line))
        self.add_sound("voiceovers/ProbabilityLineConvergence.mp3")
        self.play(FadeIn(dot))

        positions = [0.2, 0.7, 0.4, 0.55, 0.48, 0.51, 0.5]
        for p in positions:
            self.add_sound("voiceovers/sword-swing.wav")
            self.play(dot.animate.move_to(line.n2p(p)))
        self.add_sound("voiceovers/ding.wav")
        self.play(Flash(dot))
        self.wait(2)
class RandomVariableScene(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/RandomVariableScene.mp3")
        coins = VGroup(SVGMobject("assets/bitcoin.svg").scale(0.4), SVGMobject("assets/Bitcoin-Currency.svg").scale(0.4)).arrange(RIGHT)
        dices = VGroup(*[SVGMobject(f"assets/dice_{i}.svg").set_fill(BLUE).scale(0.4) for i in range(1, 7)]).arrange_in_grid(2, 3)
        dice_variables = Text("🎲 → X = {1,2,3,4,5,6}", font_size=48)
        coin_variables = Text("🪙 → X = {0,1}", font_size=48)
        dice_group = VGroup(dices, dice_variables).arrange(RIGHT)
        coin_group = VGroup(coins, coin_variables).arrange(RIGHT)

        VGroup(coin_group, dice_group).arrange(DOWN, buff=1)
        coin_group.shift(0.7*LEFT)
        title = Text("Biến ngẫu nhiên", font="Noto Sans", color=YELLOW, font_size=42)
        self.play(SpinInFromNothing(title), run_time=1.5)       
        self.wait()
        self.play(Circumscribe(title))
        self.wait()
        self.play(title.animate.to_corner(UL))
        self.wait(2)
        self.play(*[FadeIn(coin) for coin in coins])
        self.wait(0.5)
        self.play(Write(coin_variables))
        self.wait()
        self.play(*[FadeIn(dice) for dice in dices])
        self.wait(0.5)
        self.play(Write(dice_variables))
        self.wait(0.5)
        uncertain = Text("Bất định", font="Noto Sans").scale(0.65).to_corner(UR, LARGE_BUFF)
        arrow = Arrow(0.5*UP, 0.5*DOWN).next_to(uncertain, DOWN)
        analyze = Text("Phân tích", font="Noto Sans").scale(0.65).next_to(arrow, DOWN)
        self.play(FadeIn(uncertain))
        self.play(GrowArrow(arrow), FadeIn(analyze))
        self.wait(2)

class DiceGridWithBarChart(Scene):
    def construct(self):
        self.wait()
        colors = [BLUE, RED, PURPLE, YELLOW, GREEN, TEAL]
        random.seed(6)

        title = Text("Thí nghiệm gieo xúc xắc", font_size=40, font="Noto Sans")
        title.to_edge(UP)
        self.play(Write(title))
        dices = VGroup(*[SVGMobject(f"assets/dice_{i}.svg").set_color(colors[i-1]).scale(0.2) for i in range(1, 7)])
        dices.arrange(RIGHT).next_to(title, DOWN)

        n_rolls = 120

        # Counters
        counts = [0] * 6
        heights = [0] * 6

        barchart = BarChart(
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
            y_range=[0, 15, 3],
            x_length=6,
            y_length=4,
            bar_colors=colors,
            # bar_names=faces
        )
        self.add(barchart)
        self.play(FadeIn(dices))
        self.add_sound("voiceovers/prob_distribute1.mp3")
        for die, bar in zip(dices, barchart.bars):
            self.play(die.animate.next_to(bar, DOWN), run_time=0.3)

        dice_group = VGroup()
        die = SVGMobject("assets/dice_1.svg").scale(0.6)
        die.next_to(title, DOWN).to_edge(RIGHT, LARGE_BUFF)
        for i in range(n_rolls):
            roll = random.randint(1, 6)
            counts[roll - 1] += 1

            new_die = SVGMobject(f"assets/dice_{roll}.svg").scale(0.6)

            new_die.next_to(title, DOWN).to_edge(RIGHT, LARGE_BUFF)
            
            new_die.set_color(colors[roll - 1])
            dice_group.add(die)

            heights[roll - 1] = counts[roll - 1] * 0.25
            
            self.play(
                Transform(die, new_die),
                barchart.animate.change_bar_values(heights),
                run_time=0.1
            )
        self.wait(2)
        prob_distri = Text("Phân phối xác suất", font="Noto Sans", color=YELLOW).scale(0.7).to_edge(RIGHT, LARGE_BUFF)
        self.play(Write(prob_distri))
        self.wait(3)

class BiasedDiceDistribution(ZoomedScene):
    def construct(self):
        self.wait()
        title = Text("Phân bố xác suất của Biến rời rạc", font="Noto Sans", font_size=42)
        title.to_edge(UP)
        colors = [BLUE, RED, PURPLE, YELLOW, GREEN, TEAL]

        fair_probs = [1/6] * 6
        biased_probs = [0.05, 0.10, 0.15, 0.20, 0.25, 0.25]

        # Fair die bar chart
        fair_chart = BarChart(
            fair_probs,
            y_range=[0, 0.35, 0.1],
            x_length=5,
            y_length=3,
            bar_colors=colors,
            # bar_names=faces
        ).shift(LEFT * 3)

        fair_bar_lbls = VGroup()
        for bar, color in zip(fair_chart.bars, colors):
            label = MathTex("1/6")
            label.scale(0.6).set_color(color)
            label.next_to(bar, UP)
            fair_bar_lbls.add(label)

        fair_label = Text("Xúc xắc công bằng", font="Noto Sans", font_size=28).next_to(fair_chart, UP)
        discrete_text = Text("Biến ngẫu nhiên rời rạc", font="Noto Sans", font_size=28).next_to(fair_chart, UP)
        fair_one = Text("1", font_size=96, weight=BOLD).next_to(fair_label, DOWN)
        fair_dices = VGroup(*[SVGMobject(f"assets/dice_{i}.svg").set_color(colors[i-1]).scale(0.2) for i in range(1, 7)])
        fair_dices.arrange(RIGHT).next_to(fair_label, DOWN)

        # Biased die bar chart
        biased_chart = BarChart(
            biased_probs,
            y_range=[0, 0.35, 0.1],
            x_length=5,
            y_length=3,
            bar_colors=colors,
            # bar_names=faces
        ).shift(RIGHT * 3)
        biased_dices = VGroup(*[SVGMobject(f"assets/dice_{i}.svg").set_color(colors[i-1]).scale(0.2) for i in range(1, 7)])
        for die, bar in zip(biased_dices, biased_chart.bars):
            die.next_to(bar, DOWN)
        biased_bar_lbls = biased_chart.get_bar_labels(font_size=28)

        biased_label = Text("Xúc xắc bị lệch", font="Noto Sans", font_size=28).next_to(biased_chart, UP)
        biased_one = Text("1", font_size=96, weight=BOLD).next_to(biased_label, DOWN)
        self.play(self.camera.frame.animate.move_to(fair_chart.get_center())
                  .set(width=fair_chart.width*1.5), run_time=1)
        self.add_sound("voiceovers/prob_distribute2.mp3")
        self.play(Write(discrete_text))
        self.play(ApplyWave(discrete_text))
        self.wait()
        for die in fair_dices:
            self.add_sound("voiceovers/popchat.wav")
            self.play(FadeIn(die), run_time=0.3)    
        self.wait()
        self.play(Create(fair_chart), 
                  *[die.animate.next_to(bar, DOWN) for die, bar in zip(fair_dices, fair_chart.bars)],
                  run_time=2)
        pmf_label = MathTex("Probability Mass Function(PMF)")
        pmf_label.scale(0.5).next_to(fair_label, DOWN).shift(RIGHT)
        self.play(Write(pmf_label))
        self.wait()
        pmf_prob = MathTex("P(X = x)").next_to(fair_label, DOWN)
        self.play(Transform(pmf_label, pmf_prob))
        for die_lbl in fair_bar_lbls:
            self.add_sound("voiceovers/popchat.wav")
            self.play(FadeIn(die_lbl), run_time=0.5)  
        self.wait(2)
        self.add_sound("voiceovers/prob_distribute3.mp3")
        self.play(Transform(discrete_text, title), pmf_label.animate.next_to(title, DOWN),
                  self.camera.frame.animate.move_to(ORIGIN).set(width=14), run_time=1)
        
        self.play(
            Write(fair_label), 
            Create(biased_chart), FadeIn(biased_bar_lbls), 
            FadeIn(biased_dices), Write(biased_label)
        )
        self.wait()
        self.play(Indicate(fair_label))
        self.wait()
        self.play(fair_bar_lbls.animate(run_time=1, lag_ratio=0.1).shift(0.5*UP))
        self.play(fair_bar_lbls.animate(run_time=1, lag_ratio=0.1).shift(0.5*DOWN))
        self.play(Indicate(biased_label))
        self.wait()
        self.play(biased_bar_lbls.animate(run_time=1, lag_ratio=0.1).shift(0.5*UP))
        self.play(biased_bar_lbls.animate(run_time=1, lag_ratio=0.1).shift(0.5*DOWN))
        fair_bar_lbls_copy = fair_bar_lbls.copy()
        biased_bar_lbls_copy = biased_bar_lbls.copy()
        self.play(Transform(fair_bar_lbls_copy, fair_one))
        self.play(Transform(biased_bar_lbls_copy, biased_one))
        self.wait()
        self.play(FadeOut(fair_bar_lbls_copy))
        self.play(FadeOut(biased_bar_lbls_copy))
        self.play(*[Flash(bar) for bar in fair_chart.bars])
        self.play(*[Flash(bar) for bar in biased_chart.bars])
        self.wait()
        self.play(Circumscribe(title))
        self.wait(3)
class ContinuousVariables(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/continuous1.mp3")
        time_title = Text("Thời gian", font="Noto Sans").scale(0.7)
        # Clock face
        radius = 1  # smaller radius
        shift_left = LEFT * 4  # shift entire clock

        center = shift_left

        # Clock face
        clock_face = Circle(radius=radius, color=WHITE).move_to(center)
        time_title.move_to(center).to_edge(UP, LARGE_BUFF)
        self.add(clock_face, time_title)

        # Hour marks
        hour_marks = VGroup()
        for i in range(12):
            angle = i * 2 * np.pi / 12
            start = center + radius * 0.85 * np.array([np.cos(angle), np.sin(angle), 0])
            end = center + radius * np.array([np.cos(angle), np.sin(angle), 0])
            mark = Line(start, end, color=WHITE, stroke_width=2)
            hour_marks.add(mark)
        self.add(hour_marks)

        # Clock hands
        hour_hand = Line(center, center + UP * radius * 0.5, color=WHITE, stroke_width=4)
        minute_hand = Line(center, center + UP * radius * 0.7, color=WHITE, stroke_width=3)
        second_hand = Line(center, center + UP * radius * 0.9, color=YELLOW, stroke_width=2)

        hands = VGroup(hour_hand, minute_hand, second_hand)
        self.add(hands)

        second_hand.add_updater(
            lambda m, dt: m.rotate(-TAU * dt, about_point=center)
        )

        minute_hand.add_updater(
            lambda m, dt: m.rotate(-TAU * dt / 60, about_point=center)
        )

        hour_hand.add_updater(
            lambda m, dt: m.rotate(-TAU * dt / 720, about_point=center)
        )

        height_title = Text("Chiều cao", font="Noto Sans").scale(0.7).to_edge(UP, LARGE_BUFF)
        # Ruler body
        ruler_height = 3
        ruler = Rectangle(
            height=ruler_height,
            width=0.3,
            stroke_width=2
        )

        self.add(height_title)

        # Tick marks
        ticks = VGroup()

        major_divisions = 10      # long ticks
        minor_per_major = 4       # short ticks between long ones

        for i in range(major_divisions + 1):
            y_major = np.interp(
                i,
                [0, major_divisions],
                [-ruler_height / 2, ruler_height / 2]
            )

            # Long tick
            long_tick = Line(
                start=LEFT * 0.18,
                end=RIGHT * 0.18,
                stroke_width=2
            ).move_to(ruler.get_center() + UP * y_major)
            ticks.add(long_tick)

            # Short ticks between majors
            if i < major_divisions:
                for j in range(1, minor_per_major + 1):
                    y_minor = y_major + (
                        j / (minor_per_major + 1)
                    ) * (ruler_height / major_divisions)

                    short_tick = Line(
                        start=LEFT * 0.1,
                        end=RIGHT * 0.1,
                        stroke_width=1
                    ).move_to(ruler.get_center() + UP * y_minor)
                    ticks.add(short_tick)

        self.add(ticks)

        # Triangle measuring indicator (arrow)
        measure_bar = Polygon(
            [0, 0.15, 0],
            [0, -0.15, 0],
            [0.4, 0, 0],
            color=BLUE,
            fill_opacity=1
        )

        measure_bar.move_to(ruler.get_bottom())

        self.add(measure_bar)

        # Height tracker
        height_value = ValueTracker(0)

        # Height label
        height_text = always_redraw(
            lambda: Text(
                f"{height_value.get_value():.1f} cm",
                font_size=36
            ).next_to(measure_bar, 1.5*RIGHT)
        )
        self.add(height_text)

        # Updater to move triangle
        def update_bar(mob):
            h = height_value.get_value()  # 0–200 cm
            y_pos = np.interp(
                h,
                [0, 200],
                [ruler.get_bottom()[1], ruler.get_top()[1]]
            )
            mob.move_to([ruler.get_left()[0], y_pos, 0], aligned_edge=RIGHT)

        measure_bar.add_updater(update_bar)

        temp_title = Text("Nhiệt độ", font="Noto Sans").scale(0.7)
        # Smaller shift and scaling
        shift_right = RIGHT * 4
        tube_height = 2        # smaller tube
        tube_width = 0.25      # smaller width
        bulb_radius = 0.25     # smaller bulb

        # Thermometer outline
        bulb = Circle(radius=bulb_radius, fill_opacity=0, color=WHITE).shift(DOWN + shift_right)
        tube = RoundedRectangle(
            width=tube_width,
            height=tube_height,
            corner_radius=0.15,
            fill_opacity=0,
            color=WHITE
        ).shift(shift_right)
        # un = Union(bulb, tube, fill_opacity=1)
        # un = Intersection(bulb, tube)

        temp_title.shift(shift_right).to_edge(UP, LARGE_BUFF)
        self.add(bulb, tube, temp_title)

        # Liquid inside thermometer
        liquid_bulb = Circle(radius=bulb_radius*0.8, color=RED, fill_opacity=1).shift(DOWN + shift_right)
        liquid_tube = Rectangle(
            width=tube_width*0.8,
            height=0.01,  # start small
            color=RED,
            fill_opacity=1
        ).align_to(liquid_bulb, DOWN)

        liquid_tube.shift(shift_right)
        self.add(liquid_bulb, liquid_tube)

        # Temperature label
        temp_value = ValueTracker(0)
        temp_text = always_redraw(
            lambda: Text(
                f"{int(temp_value.get_value())} °C",
                font_size=28  # smaller font
            ).next_to(tube, RIGHT, buff=0.3)
        )
        self.add(temp_text)

        # Updater for liquid level
        def update_liquid(mob):
            temp = temp_value.get_value()
            height = 0.1 + 0.03 * temp
            height = np.clip(height, 0.1, tube_height-0.4)
            mob.become(
                Rectangle(
                    width=tube_width*0.8,
                    height=height,
                    color=RED,
                    fill_opacity=1
                ).align_to(liquid_bulb, DOWN).shift(shift_right)
            )

        liquid_tube.add_updater(update_liquid)

        # Animate temperature continuously
        self.play(
            height_value.animate.set_value(200),
            temp_value.animate.set_value(100),
            rate_func=there_and_back,
            run_time=8
        )
        self.wait(2)
class ProbabilityAsArea(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/continuous2.mp3")
        title = Text("Phân phối xác suất liên tục (PDF)", font="Noto Sans", font_size=48).to_edge(UP)
        # Axes
        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[0, 1.2, 0.2],
            x_length=8,
            y_length=4,
            axis_config={"include_tip": False},
        )

        labels = axes.get_axis_labels(
            x_label=MathTex("x"),
            y_label=MathTex("f(x)")
        )

        # Probability density function (Gaussian-like)
        pdf = axes.plot(
            lambda x: np.exp(-0.5 * (x - 2)**2),
            # lambda x: 0.5 * x * np.exp(-0.5 * x), # Gamma-like
            color=BLUE,
        )

        # pdf_label = MathTex("f(x)").next_to(pdf, UP)
        self.play(Write(title))
        self.play(ApplyWave(title))
        self.play(Create(axes), FadeIn(labels), Create(pdf))
        self.wait()
        
        # Interval [a, b]
        a, b = 1, 3

        area = axes.get_area(
            pdf,
            x_range=(a, b),
            color=BLUE,
            opacity=0.4,
        )
        # prob_text = MathTex("P(a \\le X \\le b)").next_to(title, DOWN).shift(3*RIGHT)
        prob_text = MathTex(r"P(a \le X \le b) = \int_a^b f(x)\,dx").next_to(title, DOWN).shift(3*RIGHT)
        prob_text[0][0].set_color(YELLOW)
        arrow_prob = Arrow(prob_text[0][3], area.get_center())
        total_area = axes.get_area(pdf, x_range=(-1, 5), color=YELLOW)
        
        vertical_lines = axes.get_vertical_lines_to_graph(pdf, x_range=[a, b], num_lines=3, color=RED)

        line_a = vertical_lines[0]
        line_b = vertical_lines[2]
        line_x = vertical_lines[1]
        a_label = MathTex("a").next_to(line_a, DOWN)
        b_label = MathTex("b").next_to(line_b, DOWN)

        self.play(Create(line_x))
        pmf_label = MathTex("P(X = x)=0").next_to(prob_text, DOWN)
        pmf_label[0][0].set_color(YELLOW)
        arrow_pmf = Arrow(pmf_label, line_x.get_center())
        self.play(FadeIn(pmf_label), GrowArrow(arrow_pmf))
        
        self.play(FadeOut(arrow_pmf), FadeOut(line_x))
        self.play(FadeIn(area), Write(prob_text), GrowArrow(arrow_prob), FadeIn(a_label), FadeIn(b_label))
        self.play(Indicate(prob_text[0][:8]), run_time=4)
        self.wait()
        self.play(Indicate(prob_text[0][9:]), Indicate(area), run_time=4)
        self.wait(1.5)
        one = Text("1", font_size=96, weight=BOLD).move_to(area)
        self.play(FadeOut(area), FadeOut(arrow_prob),
                  FadeIn(total_area), run_time=1.5)
        self.play(FadeIn(one), run_time=0.5)
        self.play(Wiggle(pdf))
        self.play(ApplyWave(title))

        self.wait(2)

class PDFandCDF(Scene):
    def construct(self):
        self.wait()
        title = Text("PDF và CDF", font="Noto Sans").scale(0.7)
        title[:3].set_color(BLUE)
        title[-3:].set_color(GREEN)
        title.to_corner(UL)
        self.play(Write(title))
        self.add_sound("voiceovers/continuous3.mp3")

        # --- Common functions ---
        def normal_pdf(x):
            return (1 / sqrt(2 * pi)) * np.exp(-x**2 / 2)

        def normal_cdf(x):
            return 0.5 * (1 + erf(x / sqrt(2)))

        # --- PDF Axes ---
        pdf_axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 0.4, 0.2],
            x_length=5,
            y_length=3,
            tips=False,
            axis_config={"include_numbers": True}
        ).shift(DOWN+LEFT * 3)

        pdf_label = MathTex(r"\text{PDF } f_X(x)")
        pdf_label[0][:4].set_color(BLUE)
        pdf_label.next_to(pdf_axes, UP)

        # --- CDF Axes ---
        cdf_axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 1.05, 0.5],
            x_length=5,
            y_length=3,
            tips=False,
            axis_config={"include_numbers": True}
        ).shift(DOWN+RIGHT * 3)

        cdf_label = MathTex(r"\text{CDF } F_X(x)")
        cdf_label[0][:4].set_color(GREEN)
        cdf_label.next_to(cdf_axes, UP)

        self.play(
            Create(pdf_axes),
            Write(pdf_label),
        )

        # --- PDF Curve ---
        pdf_curve = pdf_axes.plot(
            lambda x: normal_pdf(x),
            x_range=[-4, 4],
            color=BLUE
        )

        # --- CDF Curve ---
        cdf_curve = cdf_axes.plot(
            lambda x: normal_cdf(x),
            x_range=[-4, 4],
            color=GREEN
        )
        self.play(
            Create(pdf_curve), run_time=3
        )
        self.wait(3)
        self.play(
            Create(cdf_axes),
            Write(cdf_label)
        )
        self.play(
            Create(cdf_curve), run_time=3
        )
        relation = MathTex(
            r"F_X(x) = \int_{-\infty}^{x} f_X(t)\,dt"
        )
        relation[0][:1].set_color(GREEN)
        relation[0][-7:-6].set_color(BLUE)
        relation.shift(2.5*UP)
        self.play(Write(relation))
        self.play(Create(pdf_curve), Create(cdf_curve), run_time=4)
        self.wait(2)
class BernoulliDistribution(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/continuous4_part1.mp3")
        # Parameter
        p = 0.7

        # Title
        title = Text("Phân phối Bernoulli", font="Noto Sans", color=YELLOW)
        title.scale(0.7).to_edge(UP)
        self.play(FadeIn(title))
        self.wait()
        self.play(ApplyWave(title))

        # PMF definition
        pmf_formula = MathTex(
            r"P(X = 1) = p,\quad P(X = 0) = 1 - p"
        )
        pmf_formula[0][0].set_color(YELLOW)
        pmf_formula[0][9].set_color(YELLOW)
        pmf_formula.next_to(title, DOWN)

        # Bar chart
        bernoulli_chart = BarChart(
            values=[1 - p, p],
            bar_names=["0", "1"],
            y_range=[0, 1, 0.2],
            x_length=4,
            y_length=3,
            bar_colors=[BLUE, GREEN],
            bar_width=0.8
        )

        bernoulli_chart.to_edge(DOWN)

        labels = VGroup(
            MathTex(r"1-p").next_to(bernoulli_chart.bars[0], UP),
            MathTex(r"p").next_to(bernoulli_chart.bars[1], UP)
        )

        self.play(FadeIn(pmf_formula), Create(bernoulli_chart))
        self.play(FadeIn(labels))
        self.wait(2)

class BinomialDistribution(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/continuous4_part2.mp3")
        # Parameters
        n = 10
        p = 0.4

        # Title
        title = Text("Phân phối nhị thức", color=YELLOW, font="Noto Sans")
        title.scale(0.7).to_edge(UP)
        self.play(FadeIn(title))

        # PMF formula
        pmf_formula = MathTex(
            r"P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}"
        )
        pmf_formula[0][0].set_color(YELLOW)
        pmf_formula.next_to(title, DOWN)

        # Compute PMF values
        pmf_values = [
            math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k))
            for k in range(n + 1)
        ]

        # Bar chart
        binomial_chart = BarChart(
            values=pmf_values,
            bar_names=[str(k) for k in range(n + 1)],
            y_range=[0, max(pmf_values) * 1.3, 0.05],
            x_length=8,
            y_length=4,
            bar_colors=[BLUE],
            bar_width=0.6
        )

        binomial_chart.to_edge(DOWN)

        self.play(FadeIn(pmf_formula), Create(binomial_chart))

        # Parameter labels
        params = MathTex(
            rf"n = {n},\quad p = {p}"
        )
        params.next_to(binomial_chart, UP)

        self.play(FadeIn(params))
        self.wait(2)

class HeightDistribution(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/continuous4_part3.mp3")
        # Parameters
        mu = 170      # mean height (cm)
        sigma = 7     # standard deviation

        # Title
        title = Text("Phân phối chuẩn (phân phối Gauss)", color=YELLOW, font="Noto Sans")
        title.scale(0.7).to_edge(UP)
        self.play(Write(title))

        # Axes
        axes = Axes(
            x_range=[150, 190, 5],
            y_range=[0, 0.08, 0.02],
            x_length=9,
            y_length=4,
            axis_config={"include_numbers": True},
            tips=False
        ).shift(DOWN * 0.5)

        x_label = axes.get_x_axis_label(Text("Chiều cao (cm)", font="Noto Sans", font_size=24))
        y_label = axes.get_y_axis_label(Text("Mật độ xác suất", font="Noto Sans", font_size=24))

        self.play(Create(axes), Write(x_label), Write(y_label))

        # Normal distribution function
        def normal_pdf(x):
            return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(
                -0.5 * ((x - mu) / sigma) ** 2
            )

        # Curve
        graph = axes.plot(
            normal_pdf,
            x_range=[150, 190],
            color=BLUE,
        )

        self.play(Create(graph))
        bell = SVGMobject("assets/bell.svg").move_to(graph)
        self.play(FadeIn(bell))
        self.wait()
        self.play(FadeOut(bell))

        # Mean line
        mean_line = DashedLine(
            start=axes.c2p(mu, 0),
            end=axes.c2p(mu, normal_pdf(mu)),
            color=YELLOW,
        )

        mean_label = MathTex(r"\mu = 170").next_to(mean_line, UP)

        self.play(Create(mean_line), Write(mean_label))
        arrow_left = Arrow(0.5*LEFT, 0.5*RIGHT).next_to(mean_line, LEFT)
        arrow_right = Arrow(0.5*RIGHT, 0.5*LEFT).next_to(mean_line, RIGHT)
        self.play(FadeIn(arrow_left, shift=RIGHT), 
                  FadeIn(arrow_right, shift=LEFT))
        self.wait(5)
        tree = ImageMobject("assets/tree.png").scale(0.3).to_corner(UR, LARGE_BUFF)
        calliper = ImageMobject("assets/calliper.png").scale(0.3).to_corner(UR, LARGE_BUFF)
        self.play(FadeIn(calliper))
        self.play(FadeOut(calliper), FadeIn(tree))
        self.wait(3)

class TimeDistribution(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/continuous4_part4.mp3")
        # Parameter
        lam = 0.5  # rate parameter

        # Title
        title = Text("Phân phối mũ", font="Noto Sans", color=YELLOW).scale(0.7)
        title.to_edge(UP)
        self.play(Write(title))

        # Axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 0.6, 0.1],
            x_length=9,
            y_length=4,
            axis_config={"include_numbers": True},
            tips=False
        ).shift(DOWN * 0.5)

        x_label = axes.get_x_axis_label(Text("Thời gian", font="Noto Sans", font_size=24))
        y_label = axes.get_y_axis_label(Text("Mật độ xác suất", font="Noto Sans", font_size=24))

        self.play(Create(axes), Write(x_label), Write(y_label))

        # Exponential PDF
        def exponential_pdf(t):
            return lam * np.exp(-lam * t)

        # Curve
        graph = axes.plot(
            exponential_pdf,
            x_range=[0, 10],
            color=BLUE,
        )

        self.play(Create(graph))

        # Lambda indicator at t=0
        lambda_label = MathTex(r"\lambda = 0.5")
        lambda_label.next_to(axes.c2p(1, exponential_pdf(1)), UP)

        self.play(Write(lambda_label))

        self.wait(3)

class MeanMedianModeDefine(Scene):
    def construct(self):
        self.wait()
        
        look_closely = SVGMobject("assets/look_closely.svg").to_corner(UR)
        test_tube = ImageMobject("assets/test-tube.png").scale(0.2)
        petri_dish = ImageMobject("assets/petri-dish.png").scale(0.2)
        checklist = ImageMobject("assets/checklist.png").scale(0.2)
        data_collection = Group(test_tube, petri_dish, checklist).arrange(RIGHT, LARGE_BUFF)
        self.play(FadeIn(look_closely))
        self.add_sound("voiceovers/mmm1.mp3")
        for mob in (test_tube, petri_dish, checklist):
            self.play(FadeIn(mob))
        title = Text("Trung bình, trung vị và mode", font="Noto Sans")
        title[:9].set_color(YELLOW)
        title[10:17].set_color(GREEN)
        title[-4:].set_color(RED)
        title.scale(0.7).to_edge(UP)
        self.play(FadeOut(look_closely), FadeOut(data_collection), Write(title))

        # Parameters
        mu = 0          # mean
        sigma = 1       # standard deviation
        samples = 5000
        bins = 30

        # Generate normal distribution samples
        data = np.random.normal(mu, sigma, samples)

        # Compute histogram
        counts, bin_edges = np.histogram(data, bins=bins, density=True)
        bin_width = bin_edges[1] - bin_edges[0]

        # Axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, max(counts) * 1.2, 0.1],
            x_length=10,
            y_length=5,
            y_axis_config={"stroke_opacity": 0},
            x_axis_config={"include_ticks": False, "stroke_opacity": 0},
            tips=False
        )

        bars = VGroup()
        for count, left_edge in zip(counts, bin_edges[:-1]):
            bar = Rectangle(
                width=axes.x_axis.unit_size * bin_width,
                height=axes.y_axis.unit_size * count,
                fill_color=BLUE,
                fill_opacity=0.8,
                stroke_width=0
            )
            bar.move_to(
                axes.c2p(
                    left_edge + bin_width / 2,
                    count / 2
                )
            )
            bars.add(bar)

        arrow_left = Arrow(LEFT, RIGHT).shift(3*LEFT)
        arrow_right = Arrow(RIGHT, LEFT).shift(3*RIGHT)

        self.add(axes)
        self.play(*[LaggedStart(GrowFromEdge(bar, edge=DOWN, lag_ratio=0.1) for bar in bars)])
        for _ in range(3):
            self.play(FadeIn(arrow_left, shift=RIGHT), 
                      FadeIn(arrow_right, shift=LEFT))        
        self.wait(3)
        self.play(VGroup(axes, bars, arrow_left, arrow_right).animate.to_edge(DOWN))
        mean_def = VGroup(
            Text("Trung bình", font="Noto Sans", font_size=32, color=YELLOW),
            Text(
                "Giá trị trung bình cộng", font="Noto Sans",
                font_size=24
            )
        ).arrange(DOWN, aligned_edge=LEFT)

        median_def = VGroup(
            Text("Trung vị", font="Noto Sans", font_size=32, color=GREEN),
            Text(
                "Giá trị ở giữa", font="Noto Sans",
                font_size=24
            )
        ).arrange(DOWN, aligned_edge=LEFT)

        mode_def = VGroup(
            Text("Mode", font_size=32, color=RED),
            Text(
                "Giá trị xuất hiện \nthường xuyên nhất", font="Noto Sans",
                font_size=24
            )
        ).arrange(DOWN, aligned_edge=LEFT)

        # Positioning
        mean_def.shift(LEFT * 4)
        mode_def.shift(RIGHT * 4)
        VGroup(mean_def, median_def, mode_def).shift(2*UP)

        self.play(FadeIn(mean_def, shift=DOWN))
        self.wait(4)

        self.play(FadeIn(median_def, shift=DOWN))
        self.wait(4.5)

        self.play(FadeIn(mode_def, shift=DOWN))
        self.wait(5)
class NormalDistribution(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/mmm2.mp3")
        # Parameters
        mu = 0
        sigma = 1

        # Title
        title = Text("Phân phối chuẩn", font="Noto Sans")
        title.scale(0.7).to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 0.45, 0.1],
            x_length=8,
            y_length=4,
            y_axis_config={"stroke_opacity": 0},
            x_axis_config={"include_ticks": False},
            tips=False
        )

        self.add(axes)

        # Normal PDF
        def normal_pdf(x):
            return (1 / (sigma * sqrt(2 * pi))) * np.exp(
                -((x - mu) ** 2) / (2 * sigma ** 2)
            )

        pdf_curve = axes.plot(
            lambda x: normal_pdf(x),
            x_range=[-4, 4],
            color=BLUE
        )

        self.play(Create(pdf_curve))

        # Mean line
        mean_line = axes.get_vertical_line(
            axes.c2p(mu, normal_pdf(mu)),
            line_func=Line,
            color=YELLOW
        )
        mean_label = Text("Trung bình = Trung vị = Mode", font="Noto Sans", font_size=20).next_to(mean_line, UP)
        mean_label[:9].set_color(YELLOW)
        mean_label[10:17].set_color(GREEN)
        mean_label[-4:].set_color(RED)
        mode_bar = Line(
            0.5*LEFT,
            0.5*RIGHT,
            color=YELLOW
        ).move_to(axes.c2p(mu, normal_pdf(mu)))

        self.play(Create(mean_line), Create(mode_bar), Write(mean_label))
        self.play(Circumscribe(mean_label))
        self.wait(2)

class LogNormalMeanMedianMode(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/mmm3.mp3")
        # Parameters of log-normal
        mu = 0
        sigma = 1

        title = Text("Phân phối lệch", font="Noto Sans", font_size=40)
        title.to_edge(UP)

        # Axes
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 0.8, 0.1],
            x_length=10,
            y_length=4,
            y_axis_config={"include_numbers": False, "stroke_opacity": 0},
            x_axis_config={"include_ticks": False},
            tips=False
        )

        def lognormal_pdf(x):
            if x <= 0:
                return 0
            return (1 / (x * sigma * math.sqrt(2 * math.pi))) * \
                   math.exp(-(math.log(x) - mu) ** 2 / (2 * sigma ** 2))

        pdf_curve = axes.plot(
            lognormal_pdf,
            x_range=[0.01, 6],
            color=BLUE
        )

        self.play(Write(title), Create(axes), Create(pdf_curve))

        # Mean, Median, Mode
        mean = math.exp(mu + sigma**2 / 2)
        median = math.exp(mu)
        mode = math.exp(mu - sigma**2)

        # Vertical lines
        mean_line = DashedLine(
            axes.c2p(mean, 0),
            axes.c2p(mean, lognormal_pdf(mean)),
            color=YELLOW
        )

        median_line = Line(
            axes.c2p(median, 0),
            axes.c2p(median, lognormal_pdf(median)),
            color=GREEN
        )
        area_left = axes.get_area(pdf_curve, x_range=[0.01, median], color=YELLOW, opacity=0.4)
        area_left_text = Text("50%").scale(0.65).next_to(median_line, LEFT).shift(0.5*DOWN)
        area_right = axes.get_area(pdf_curve, x_range=[median, 6], color=BLUE, opacity=0.4)
        area_left_right = Text("50%").scale(0.65).next_to(median_line, RIGHT).shift(0.5*DOWN)

        mode_line = Line(
            axes.c2p(mode, 0),
            axes.c2p(mode, lognormal_pdf(mode)),
            color=RED
        )
        mode_bar = Line(
            0.5*LEFT,
            0.5*RIGHT,
            color=ORANGE
        ).move_to(axes.c2p(mode, lognormal_pdf(mode)))

        # Labels
        mean_label = Text("Trung bình", font="Noto Sans", color=YELLOW).scale(0.7)
        median_label = Text("Trung vị", font="Noto Sans", color=GREEN).scale(0.7)
        mode_label = Text("Mode", font="Noto Sans", color=RED).scale(0.7)

        triangle = Triangle(color=YELLOW).set_fill(YELLOW, 1).scale(0.2).next_to(mean_line, DOWN, SMALL_BUFF)
        mean_label.next_to(triangle, DOWN)
        median_label.next_to(median_line, DOWN)
        mode_label.next_to(mode_line, DOWN)

        self.play(FadeIn(triangle, shift=RIGHT), FadeIn(mean_label, shift=RIGHT))
        self.wait()
        self.play(FadeOut(triangle), FadeOut(mean_label),
                  Create(mode_line), FadeIn(mode_bar), FadeIn(mode_label))
        self.wait()      
        self.play(FadeOut(mode_line), FadeOut(mode_bar), FadeOut(mode_label),
                  Create(median_line), FadeIn(area_left), FadeIn(area_right), 
                  FadeIn(area_left_text), FadeIn(area_left_right), FadeIn(median_label))
        self.wait()
        self.play(FadeOut(median_line), FadeOut(area_left), FadeOut(area_right), 
                  FadeOut(median_label), FadeOut(area_left_text), FadeOut(area_left_right),
                  FadeOut(pdf_curve), FadeOut(axes), FadeOut(title))       
        self.wait(2)
        
class CoffeeSalesScenario(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/m3_coffeesales1.mp3")
        long_text = Text("Hãy cùng xem xét một tập dữ liệu mẫu " \
        "\n để thấy sự khác biệt giữa các thước đo này trong thực tế," \
        "\n đặc biệt là khi dữ liệu không hoàn toàn đối xứng.", font="Noto Sans")
        long_text.scale(0.7)
        self.play(Write(long_text), run_time=5)
        self.wait()
        self.play(FadeOut(long_text))
        
        # 1. Data Setup
        data = [15, 18, 18, 22, 25, 29, 88]
        labels = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
        
        mean_val = sum(data) / len(data)  # 30.7
        median_val = 22
        mode_val = 18

        # 2. Create Bar Chart
        chart = BarChart(
            values=data,
            # label_y_axis=True,
            y_range=[0, 100, 20],
            x_length=10,
            y_length=6,
            axis_config={"font_size": 24},
            bar_names=labels,
            bar_colors=[BLUE_B, BLUE_B, BLUE_B, BLUE_B, BLUE_B, BLUE_B, GOLD_E] # Highlight outlier
        ).scale(0.8).to_edge(DOWN)

        # Labels for the bars
        bar_labels = chart.get_bar_labels(font_size=24)
        
        # 3. Create Measure Lines
        mean_line = chart.get_horizontal_line(chart.c2p(7, mean_val), color=YELLOW, line_func=Line)
        mean_text = Text(f"Trung bình: {mean_val:.1f}", font="Noto Sans", color=YELLOW, font_size=20).next_to(mean_line, RIGHT)

        median_line = chart.get_horizontal_line(chart.c2p(7, median_val), color=GREEN, line_func=Line)
        median_text = Text(f"Trung vị: {median_val}", font="Noto Sans", color=GREEN, font_size=20).next_to(median_line, RIGHT)

        mode_line = chart.get_horizontal_line(chart.c2p(7, mode_val), color=RED, line_func=Line)
        mode_text = Text(f"Mode: {mode_val}", font="Noto Sans", color=RED, font_size=20).next_to(mode_line, RIGHT).shift(0.1*DOWN)

        # 4. Animation Sequence
        title = Text("Doanh số bán cà phê", font="Noto Sans", font_size=36).to_edge(UP)
        self.play(Write(title))
        self.wait()
        cafe = ImageMobject("assets/cafe.png").scale(0.2).to_corner(UR)
        self.play(FadeIn(cafe))
        self.wait()
        festival = ImageMobject("assets/festival.png").scale(0.2).next_to(title, DOWN)

        self.play(Create(chart), run_time=2)
        for lbl in bar_labels:
            self.add_sound("voiceovers/cash-register-purchase.wav")
            self.play(FadeIn(lbl, shift=DOWN))
        self.wait()

        outlier_box = SurroundingRectangle(chart.bars[6], color=YELLOW)
        outlier_text = Text("Ngoại lệ!", font="Noto Sans", color=YELLOW, font_size=24).next_to(outlier_box, UP)
        self.play(Create(outlier_box), Write(outlier_text))
        self.wait()
        self.play(FadeIn(festival))
        self.wait()
        self.play(FadeOut(festival), FadeOut(outlier_box), FadeOut(outlier_text))
        self.wait(4)
        self.add_sound("voiceovers/m3_coffeesales5.mp3")
        self.play(Create(mean_line), Write(mean_text))
        self.wait(0.5)
        self.play(Create(median_line), Write(median_text))
        self.wait()
        self.play(Create(mode_line), Write(mode_text))
        
        self.wait(3)
class CalculateMean(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/m3_coffeesales2_part1.mp3")
        find_mean = Text("Tìm giá trị trung bình", font="Noto Sans", color=YELLOW)
        self.play(SpinInFromNothing(find_mean))
        self.play(FadeOut(find_mean))
        # 1. The Dataset
        numbers = [15, 18, 18, 22, 25, 29, 88]
        data_tex = VGroup(*[MathTex(str(n)) for n in numbers]).arrange(RIGHT, buff=0.5)
        data_tex.to_edge(UP, buff=1.5)

        title = Text("Bước 1: Cộng các giá trị", font="Noto Sans", font_size=32).to_edge(UP, buff=0.5)

        # 2. Summation Visual
        plus_signs = VGroup(*[MathTex("+") for _ in range(len(numbers)-1)])
        for i, sign in enumerate(plus_signs):
            sign.move_to((data_tex[i].get_right() + data_tex[i+1].get_left()) / 2)
        self.add_sound("voiceovers/m3_coffeesales2_part2.mp3")
        self.play(Write(title), Write(data_tex))
        self.wait(1)
        self.add_sound("voiceovers/click.wav")
        self.play(Write(plus_signs))
        self.wait(1)

        # Transform sum to result
        total_sum = sum(numbers)
        sum_result = MathTex(str(total_sum)).scale(1.5).move_to(ORIGIN)
        self.add_sound("voiceovers/m3_coffeesales2_part3.mp3")
        self.play(
            ReplacementTransform(VGroup(data_tex, plus_signs), sum_result),
            title.animate.become(Text("Bước 2: Chia cho Số lượng (n=7)", font="Noto Sans", font_size=32).to_edge(UP, buff=0.5))
        )
        self.wait(1)

        # 3. Division Visual
        division_line = Line(LEFT, RIGHT, stroke_width=2).next_to(sum_result, DOWN, buff=0.2)
        denominator = MathTex("7").scale(1.5).next_to(division_line, DOWN, buff=0.2)
        self.add_sound("voiceovers/click.wav")
        self.play(Create(division_line), Write(denominator))
        self.wait(1)

        # 4. Final Result
        mean_val = total_sum / len(numbers)
        final_formula = MathTex(r"\bar{x} = ", f"{mean_val:.1f}").scale(1.5).move_to(ORIGIN)
        final_formula[0][:2].set_color(YELLOW)
        self.add_sound("voiceovers/m3_coffeesales2_part4.mp3")
        self.play(
            FadeOut(sum_result, division_line, denominator),
            Write(final_formula),
            title.animate.become(Text("Giá trị trung bình cuối cùng", color=YELLOW, font="Noto Sans", font_size=32).to_edge(UP, buff=0.5))
        )
        self.add_sound("voiceovers/completed.wav")
        self.play(Flash(final_formula))
        
        self.wait(2)

class CalculateMedian(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/m3_coffeesales3_part1.mp3")
        # 1. The Dataset (Unsorted to show the importance of sorting)
        raw_data = [29, 18, 15, 88, 22, 18, 25]
        numbers = VGroup(*[MathTex(str(n)) for n in raw_data]).arrange(RIGHT, buff=0.6)
        
        title = Text("Tìm giá trị trung vị", font="Noto Sans", color=GREEN, font_size=36).to_edge(UP, buff=0.5)
        step_text = Text("Bước 1: Sắp xếp từ nhỏ nhất đến lớn nhất", font="Noto Sans", font_size=28, color=YELLOW).next_to(title, DOWN)

        self.play(Write(title), Write(numbers))
        self.wait()
        self.add_sound("voiceovers/m3_coffeesales3_part2.mp3")
        self.play(Write(step_text))
        self.wait(0.5)

        # 2. Sorting Animation
        sorted_data = sorted(raw_data)
        sorted_numbers = VGroup(*[MathTex(str(n)) for n in sorted_data]).arrange(RIGHT, buff=0.6)
        
        # Move numbers to their sorted positions
        self.add_sound("voiceovers/click.wav")
        self.play(
            *[ReplacementTransform(numbers[i], sorted_numbers[i]) # Handles duplicate 18s
              for i in range(len(raw_data))],
            run_time=2
        )
        self.wait()

        # 3. Identify Middle
        self.add_sound("voiceovers/m3_coffeesales3_part3.mp3")
        self.play(step_text.animate.become(Text("Bước 2: Tìm giá trị ở giữa", font="Noto Sans", font_size=28, color=YELLOW).next_to(title, DOWN)))
        
        # Elimination pairs (fading out outer numbers)
        pairs = [(0, 6), (1, 5), (2, 4)]
        for left, right in pairs:
            self.add_sound("voiceovers/click.wav")
            indicator = VGroup(
                SurroundingRectangle(sorted_numbers[left], color=RED),
                SurroundingRectangle(sorted_numbers[right], color=RED)
            )
            self.play(Create(indicator))
            self.play(FadeOut(indicator), sorted_numbers[left].animate.set_opacity(0.3), sorted_numbers[right].animate.set_opacity(0.3))
            self.wait(0.5)

        # 4. Highlight Result
        median_val = sorted_numbers[3] # The 22
        final_box = SurroundingRectangle(median_val, color=GREEN)
        median_label = Text("Trung vị = 22", font="Noto Sans", color=GREEN).scale(1.2).move_to(ORIGIN).shift(DOWN*1.5)
        self.add_sound("voiceovers/click.wav")
        self.play(Create(final_box), median_val.animate.set_opacity(1))
        self.add_sound("voiceovers/m3_coffeesales3_part4.mp3")
        self.play(Write(median_label), median_val.animate.scale(1.5), FadeOut(final_box))
        self.add_sound("voiceovers/completed.wav")
        self.play(Flash(median_label))
        self.wait(2)

class CalculateMode(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/m3_coffeesales4_part1.mp3")
        # 1. Setup Data
        raw_data = [15, 18, 18, 22, 25, 29, 88]
        numbers = VGroup(*[MathTex(str(n)) for n in raw_data]).arrange(RIGHT, buff=0.6)
        
        title = Text("Tìm giá trị Mode", font="Noto Sans", font_size=36).to_edge(UP, buff=0.5)
        step_text = Text("Bước 1: Nhóm các giá trị giống nhau", font="Noto Sans", font_size=28, color=YELLOW).next_to(title, DOWN)
        
        self.play(Write(title), Write(numbers))
        self.wait(1)

        # 2. Grouping Animation
        # We'll move the two 18s together to show they are a pair
        self.add_sound("voiceovers/m3_coffeesales4_part2.mp3")
        self.play(Write(step_text))
        
        # Target positions for grouping
        grouped_positions = VGroup(
            MathTex("15"), 
            VGroup(MathTex("18"), MathTex("18")).arrange(DOWN, buff=0.2),
            MathTex("22"), MathTex("25"), MathTex("29"), MathTex("88")
        ).arrange(RIGHT, buff=0.8).move_to(ORIGIN)
        self.add_sound("voiceovers/click.wav")
        self.play(
            ReplacementTransform(numbers[0], grouped_positions[0]),
            ReplacementTransform(VGroup(numbers[1], numbers[2]), grouped_positions[1]),
            ReplacementTransform(numbers[3], grouped_positions[2]),
            ReplacementTransform(numbers[4], grouped_positions[3]),
            ReplacementTransform(numbers[5], grouped_positions[4]),
            ReplacementTransform(numbers[6], grouped_positions[5]),
            run_time=2
        )
        self.wait()

        # 3. Tallying / Counting
        self.add_sound("voiceovers/m3_coffeesales4_part3.mp3")
        self.play(step_text.animate.become(Text("Bước 2: Đếm tần suất", font="Noto Sans", font_size=28, color=YELLOW).next_to(title, DOWN)))
        
        counts = VGroup(
            Text("count: 1", font_size=20).next_to(grouped_positions[0], DOWN),
            Text("count: 2", font_size=20, color=RED).next_to(grouped_positions[1], DOWN),
            Text("count: 1", font_size=20).next_to(grouped_positions[2], DOWN),
            Text("count: 1", font_size=20).next_to(grouped_positions[3], DOWN),
            Text("count: 1", font_size=20).next_to(grouped_positions[4], DOWN),
            Text("count: 1", font_size=20).next_to(grouped_positions[5], DOWN),
        )
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(counts, shift=UP))
        self.wait()

        # 4. Highlight the Winner
        mode_box = SurroundingRectangle(VGroup(grouped_positions[1], counts[1]), color=RED, buff=0.2)
        mode_label = Text("Mode = 18", color=RED).scale(1.2).next_to(mode_box, UP, buff=0.5)
        self.add_sound("voiceovers/click.wav")
        self.play(Create(mode_box))
        self.add_sound("voiceovers/m3_coffeesales4_part4.mp3")
        self.play(Write(mode_label), grouped_positions[1].animate.scale(1.2))
        self.add_sound("voiceovers/completed.wav")
        self.play(Flash(mode_label))
        
        # Dim the others
        others = VGroup(grouped_positions[0], grouped_positions[2:], counts[0], counts[2:])
        self.play(others.animate.set_opacity(0.3))
        
        self.wait(2)

class SamplingScene(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/SamplingScene_part1.mp3")
        population = VGroup(*[PiCreature().scale(0.2).set_color(random_bright_color()) for _ in range(50)])
        population.arrange_in_grid(5, 10).to_corner(UL, LARGE_BUFF)
        sample = VGroup(*population[:10]).copy().to_edge(DOWN, LARGE_BUFF)

        for cup in population:
            self.add_sound("voiceovers/ui_pop_up.mp3")
            self.play(FadeIn(cup), run_time=0.1)
        self.add_sound("voiceovers/SamplingScene_part2.mp3")
        copy = population[:10].copy()
        self.play(Transform(copy, sample), run_time=3)
        self.wait(0.5)
        self.play(copy.animate(run_time=1, lag_ratio=0.3).shift(0.4*UP))
        self.wait()
        self.play(copy.animate(run_time=1, lag_ratio=0.3).shift(0.4*DOWN))
        self.wait(4)

class CorrelationCausation(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/CorrelationCausation.mp3")
        # 1. Setup Axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            axis_config={"include_tip": False}
        ).scale(0.8)
        
        x_label = axes.get_x_axis_label("Ice Cream Sales")
        y_label = axes.get_y_axis_label("Sunburns")
        ice_cream_label = Text("Doanh số bán kem", font="Noto Sans", slant=ITALIC)
        ice_cream_label.scale(0.65).move_to(x_label)
        sunburn_label = Text("Cháy nắng", font="Noto Sans", slant=ITALIC)
        sunburn_label.scale(0.65).move_to(y_label)
        labels = VGroup(ice_cream_label, sunburn_label)

        # 2. Generate Correlated Data Points
        # Points that follow a general upward trend
        np.random.seed(42)
        x_vals = np.linspace(1, 9, 15)
        y_vals = x_vals + np.random.normal(0, 1, 15)
        
        points = VGroup(*[
            Dot(axes.c2p(x, y), color=BLUE) for x, y in zip(x_vals, y_vals)
        ])

        # 3. Animation Sequence
        title = Text("Mối tương quan: Kem và cháy nắng", font="Noto Sans", font_size=32).to_edge(UP)
        sunburn = SVGMobject("assets/40.svg").next_to(axes.get_y_axis(), LEFT)
        ice_cream = ImageMobject("assets/ice_cream.png").scale(0.2).next_to(axes.get_x_axis(), DOWN)
        self.play(Write(title), Create(axes), Write(labels),
                  FadeIn(sunburn), FadeIn(ice_cream))
        self.play(Create(points), run_time=4)
        self.wait(1)

        # Draw a trend line
        trend_line = Line(axes.c2p(1, 1), axes.c2p(9, 9), color=YELLOW)
        self.play(Create(trend_line))
        self.wait(2)

        # 4. Reveal the Hidden Variable (The "Sun")
        mystery_text = Text("Ăn kem có gây cháy nắng không?", font="Noto Sans", font_size=24, color=RED).add_background_rectangle().next_to(trend_line, DOWN)
        self.play(Write(mystery_text))
        self.wait(1)

        sun = ImageMobject("assets/sun.png").scale(0.2).to_corner(UR) # Assuming an SVG or just use a Circle
        if not sun: # Fallback if no SVG
            sun = Circle(radius=0.5, color=YELLOW, fill_opacity=1).to_corner(UR)
        
        sun_label = Text("Mặt Trời (Biến ẩn)", font="Noto Sans", font_size=24, color=YELLOW).next_to(sun, DOWN)
        
        # Arrows from Sun to both variables
        arrow_to_x = Arrow(sun.get_left(), axes.c2p(5, 0), color=YELLOW)
        arrow_to_y = Arrow(sun.get_left(), axes.c2p(0, 5), color=YELLOW)
        self.add_sound("voiceovers/shine.mp3")
        self.play(
            FadeIn(sun), Write(sun_label),
            FadeOut(mystery_text),
            Create(arrow_to_x), Create(arrow_to_y)
        )
        self.add_sound("voiceovers/CorrelationCausation_2.mp3")
        conclusion = Text("Kết luận: Tương quan không đồng nghĩa với nhân quả.", font="Noto Sans", font_size=32).to_edge(UP)
        self.play(Transform(title, conclusion))
        self.wait(3)

class ApplicationsScene(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/ApplicationsScene.mp3")
        title = Text("Xác suất & Thống kê có mặt ở khắp mọi nơi.", font="Noto Sans")
        title[:7].set_color(YELLOW)
        title[8:15].set_color(BLUE)
        self.play(Write(title))
        self.play(FadeOut(title), run_time=0.5)
        apps = [
            ("assets/weather.png", "Dự báo thời tiết", 0.3),
            ("assets/brain.png", "Học máy", 0.2), 
            ("assets/questionnaire.png", "Thăm dò dư luận", 0.2),
            ("assets/ds.png", "Khoa học dữ liệu", 0.2)
        ]
        app_group = Group()
        for name, title, ratio in apps:
            image = ImageMobject(name).scale(ratio)
            title = Text(title, font="Noto Sans").scale(0.6).next_to(image, DOWN)
            image.add(title)
            app_group.add(image)
        app_group.arrange_in_grid(2, 2, 1.5*LARGE_BUFF)
        for app in app_group:
            self.add_sound("voiceovers/ui_pop_up.mp3")
            self.play(FadeIn(app, shift=UP))
        self.wait(2)
        data_and_uncertain = Text("Dữ liệu và sự bất định", font="Noto Sans")
        self.play(FadeOut(app_group), Write(data_and_uncertain))
        self.wait(4)

class Final(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/final.mp3")
        functions = self.get_functions("dự đoán", "giải thích")
        top_arc, bottom_arc = arcs = self.get_arcs(functions)
        top, bottom = self.get_arc_labels(arcs)

        self.play(FadeIn(top), Create(top_arc), FadeIn(functions), run_time=0.5)
        self.play(
            Create(bottom_arc),
            FadeIn(bottom)
        )
        self.wait(2)
        self.play(Indicate(functions[0]))
        self.wait()
        self.play(Indicate(functions[1]))
        self.wait(2)
        self.play(FadeOut(top), FadeOut(top_arc), FadeOut(functions), FadeOut(bottom_arc), FadeOut(bottom))
        world = ImageMobject("assets/world-159267_1280.png").scale(0.4) 
        self.play(FadeIn(world))
        title = Text("Trong video tiếp theo", font="Noto Sans", color=YELLOW).scale(0.8)
        point = ImageMobject("assets/point.png").scale(0.4).to_edge(LEFT)
        self.play(FadeOut(world), Write(title))
        self.play(title.animate.to_corner(UL))
        
        bayes = Text("Định lý Bayes", color=BLUE, font="Noto Sans").scale(0.8).shift(UP)
        
        self.play(FadeIn(point), Write(bayes))
        self.wait(3)
        self.play(FadeOut(title), FadeOut(bayes), FadeOut(point))
        self.wait()

    def get_functions(self, left_tex, right_tex):
        left = Text(left_tex, font="Noto Sans").scale(0.5)
        left.shift(2 * LEFT)
        left.set_color(MAROON_B)

        right = Text(right_tex, font="Noto Sans").scale(0.5)
        right.shift(2 * RIGHT)
        right.set_color(GREEN)

        result = VGroup(left, right)
        result.shift(UP)
        return result

    def get_arcs(self, functions):
        f1, f2 = functions

        top_line = Line(f1.get_corner(UP + RIGHT), f2.get_corner(UP + LEFT))
        bottom_line = Line(f1.get_corner(DOWN + RIGHT), f2.get_corner(DOWN + LEFT))

        top_arc = Arc(start_angle=5 * np.pi / 6, angle=-2 * np.pi / 3)
        bottom_arc = top_arc.copy()
        bottom_arc.rotate(np.pi)

        arcs = VGroup(top_arc, bottom_arc)
        arcs.set_width(top_line.get_width())

        # Position arcs
        top_arc.next_to(top_line, UP)
        top_arc.set_color(YELLOW)
        bottom_arc.next_to(bottom_line, DOWN)
        bottom_arc.set_color(BLUE)

        return arcs

    def get_arc_labels(self, arcs):
        top_arc, bottom_arc = arcs

        top = Text("Xác suất", font="Noto Sans")
        top.next_to(top_arc, UP)
        top.set_color(top_arc.get_color())

        bottom = Text("Thống kê", font="Noto Sans")
        bottom.next_to(bottom_arc, DOWN)
        bottom.set_color(bottom_arc.get_color())

        return VGroup(top, bottom)

class ProbabilityThumbnail(Scene):
    def construct(self):
        # Background
        bg = Rectangle(
            width=14,
            height=8,
            fill_color=BLACK,
            fill_opacity=1
        )
        self.add(bg)

        # Dice (left)
        # dice = Square(side_length=1.8, color=WHITE)
        # dots = VGroup(
        #     Dot(dice.get_center() + UP * 0.4),
        #     Dot(dice.get_center() + DOWN * 0.4),
        #     Dot(dice.get_center() + LEFT * 0.4),
        #     Dot(dice.get_center() + RIGHT * 0.4),
        #     Dot(dice.get_center())
        # )
        # dice_group = VGroup(dice, dots).shift(LEFT * 4)
        dice_group = ImageMobject("assets/dice.png").scale(0.2).shift(LEFT * 4)

        # Probability line (center)
        prob_line = NumberLine(
            x_range=[0, 1, 0.2],
            length=5,
            include_numbers=True
        )
        prob_line.shift(DOWN * 1.0)

        dot = Dot(color=YELLOW).move_to(prob_line.n2p(1/6))

        # Bell curve (right)
        axes = Axes(
            x_range=[-3, 3],
            y_range=[0, 0.5],
            x_length=4,
            y_length=2.5,
            axis_config={"include_tip": False}
        ).shift(RIGHT * 4 + DOWN * 1)

        bell = axes.plot(
            lambda x: (1 / np.sqrt(2 * np.pi)) * np.exp(-x**2 / 2),
            color=BLUE
        )

        # Main title
        title = Text(
            "XÁC SUẤT & THỐNG KÊ",
            font_size=72, font="Noto Sans",
            weight=BOLD
        ).to_edge(UP)
        title[:7].set_color(YELLOW)
        title[8:].set_color(BLUE)

        # Add all
        self.add(
            dice_group,
            prob_line,
            dot,
            axes,
            bell,
            title
        )
