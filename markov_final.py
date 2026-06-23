from manim import *
import numpy as np
import random

def get_youtube_video():
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

        play_button.move_to(screen.get_center())

        return VGroup(screen, play_button)
def get_nn():
        matrix_tex = MathTex(
            r"W^{[l]} =",
            r"\begin{bmatrix}"
            r"w^{[l]}_{11} & w^{[l]}_{12} & \cdots & w^{[l]}_{1n^{[l-1]}} \\"
            r"w^{[l]}_{21} & w^{[l]}_{22} & \cdots & w^{[l]}_{2n^{[l-1]}} \\"
            r"\vdots & \vdots & \ddots & \vdots \\"
            r"w^{[l]}_{n^{[l]}1} & w^{[l]}_{n^{[l]}2} & \cdots & w^{[l]}_{n^{[l]}n^{[l-1]}}"
            r"\end{bmatrix}",
            font_size=36
        )

        matrix_tex.to_edge(LEFT, buff=1)
        matrix_tex.shift(DOWN * 0.5)

        def layer(n, x_pos):
            return VGroup(*[
                Circle(radius=0.25, color=BLUE_D, fill_opacity=1)
                for _ in range(n)
            ]).arrange(DOWN, buff=0.35).move_to([x_pos, 0, 0])

        input_layer = layer(5, 2)
        hidden_layer = layer(6, 3.8)
        output_layer = layer(3, 5.6)

        for neuron in hidden_layer:
            neuron.set_color(BLUE_C)
        for neuron in output_layer:
            neuron.set_color(BLUE_B)

        def connect_layers(layer1, layer2):
            return VGroup(*[
                Line(
                    n1.get_center(),
                    n2.get_center(),
                    stroke_color=BLUE_C,
                    stroke_width=2
                )
                for n1 in layer1
                for n2 in layer2
            ])

        connections_1 = connect_layers(input_layer, hidden_layer)
        connections_2 = connect_layers(hidden_layer, output_layer)
        return VGroup(matrix_tex, connections_1, connections_2, input_layer, hidden_layer, output_layer)
def get_chip_icon(label="LLM", body_color=BLUE_E):
    # Chip body
        chip_body = RoundedRectangle(
            corner_radius=0.2,
            width=4,
            height=4,
            stroke_width=4
        )
        chip_body.set_fill(body_color, opacity=0.85)

        pin_length = 0.5
        pin_width = 0.15
        num_pins_per_side = 6
        spacing = chip_body.width / (num_pins_per_side + 1)

        pins = VGroup()

        # Top pins (extend upward)
        for i in range(1, num_pins_per_side + 1):
            pin = Rectangle(height=pin_length, width=pin_width)
            pin.move_to(
                chip_body.get_top()
                + UP * (pin_length / 2)
                + LEFT * (chip_body.width / 2 - i * spacing)
            )
            pins.add(pin)

        # Bottom pins (extend downward)
        for i in range(1, num_pins_per_side + 1):
            pin = Rectangle(height=pin_length, width=pin_width)
            pin.move_to(
                chip_body.get_bottom()
                + DOWN * (pin_length / 2)
                + LEFT * (chip_body.width / 2 - i * spacing)
            )
            pins.add(pin)

        # Left pins (extend left)
        for i in range(1, num_pins_per_side + 1):
            pin = Rectangle(height=pin_width, width=pin_length)
            pin.move_to(
                chip_body.get_left()
                + LEFT * (pin_length / 2)
                + DOWN * (chip_body.height / 2 - i * spacing)
            )
            pins.add(pin)

        # Right pins (extend right)
        for i in range(1, num_pins_per_side + 1):
            pin = Rectangle(height=pin_width, width=pin_length)
            pin.move_to(
                chip_body.get_right()
                + RIGHT * (pin_length / 2)
                + DOWN * (chip_body.height / 2 - i * spacing)
            )
            pins.add(pin)

        pins.set_fill(GREY_C, opacity=1)
        pins.set_stroke(width=2)

        # Label
        chip_label = Text(label, font_size=72, weight=BOLD)
        chip_label.move_to(chip_body.get_center())
        chip_label.set_color(WHITE)
        return VGroup(chip_body, pins, chip_label)

def get_page(frame_color=GREY_E):
        # --- Browser Window Frame ---
        frame = RoundedRectangle(
            width=10,
            height=6,
            corner_radius=0.2,
            stroke_width=2
        )
        frame.set_fill(frame_color, opacity=0.5)
        frame.to_edge(DOWN, buff=0.5)

        # --- Top Bar ---
        top_bar = Rectangle(
            width=9.8,
            height=0.8,
            stroke_width=0
        )
        top_bar.set_fill(GREY_D, opacity=1)
        top_bar.align_to(frame, UP)

        # --- Browser Buttons ---
        red = Circle(radius=0.12, color=RED, fill_opacity=1)
        yellow = Circle(radius=0.12, color=YELLOW, fill_opacity=1)
        green = Circle(radius=0.12, color=GREEN, fill_opacity=1)

        buttons = VGroup(red, yellow, green).arrange(RIGHT, buff=0.2)
        buttons.move_to(top_bar.get_left() + RIGHT*0.8)

        # --- Address Bar ---
        address_bar = RoundedRectangle(
            width=5,
            height=0.4,
            corner_radius=0.1,
            stroke_width=1
        )
        address_bar.set_fill(WHITE, opacity=1)
        address_bar.move_to(top_bar.get_center())

        return VGroup(frame, top_bar, buttons, address_bar)
def glow_pulse(edge):
            glow = edge.copy()
            glow.set_color(YELLOW)
            glow.set_stroke(width=edge.get_stroke_width() * 2)
            glow.set_z_index(10)
            return glow
class Memoryless(Scene):
    def construct(self):
        self.add_sound("voiceovers/Memoryless.mp3")
        cafe = SVGMobject("assets/cafe.svg").scale(0.8).move_to(LEFT*3.5 + UP)
        home = SVGMobject("assets/home.svg").move_to(RIGHT*3 + UP)
        office = SVGMobject("assets/office.svg").move_to(2*DOWN)
        user = SVGMobject("assets/user.svg").set_color(GOLD_E).scale(0.6).move_to(LEFT*2 + 0.5*UP)
        self.play(FadeIn(cafe))
        self.add_sound("voiceovers/ui_pop_up.mp3")
        self.play(FadeIn(user))
        self.wait()
        self.play(FadeIn(home))
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(user.animate.shift(RIGHT*3.5), FadeOut(cafe))
        self.wait()
        self.play(FadeIn(office))
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(user.animate.next_to(office, RIGHT), FadeOut(home))
        self.wait(2)
        
        title = Text("Markov Chains", font="Noto Sans", font_size=64)
        subtitle = Text("Tương lai chỉ phụ thuộc vào hiện tại", font="Noto Sans", font_size=36).next_to(title, DOWN)
        self.add_sound("voiceovers/shine2.mp3")
        self.play(Transform(VGroup(cafe, home, office), title), FadeOut(user))
        self.play(FadeIn(subtitle))
        self.wait()
        search = SVGMobject("assets/search_engine.svg").shift(3*LEFT+2*UP)
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(DrawBorderThenFill(search))
        nn = get_nn().scale(0.4).shift(3*RIGHT+2*UP)
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(Create(nn))
        finance = SVGMobject("assets/finance.svg").shift(3*LEFT+2*DOWN)
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(DrawBorderThenFill(finance))
        weather = SVGMobject("assets/weather.svg").shift(3*RIGHT+2*DOWN)
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(DrawBorderThenFill(weather))
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

class MarkovChainWeather(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/MarkovChainWeather.mp3")
        sunny = Circle(radius=1, color=YELLOW, fill_opacity=0.3).shift(LEFT * 3 + UP)
        cloudy = Circle(radius=1, color=GRAY, fill_opacity=0.3).shift(RIGHT * 3 + UP)
        rainy = Circle(radius=1, color=BLUE, fill_opacity=0.3).shift(DOWN * 2)

        sunny_label = Text("Nắng", font="Noto Sans").scale(0.6).move_to(sunny)
        cloudy_label = Text("Mây", font="Noto Sans").scale(0.6).move_to(cloudy)
        rainy_label = Text("Mưa", font="Noto Sans").scale(0.6).move_to(rainy)
        self.add_sound("voiceovers/shine2.mp3")
        self.play(Create(sunny), Write(sunny_label))
        self.wait(2)

        arrow_sc = Arrow(
            sunny.get_right(),
            cloudy.get_left(),
            buff=0.0
        )

        arrow_sr = Arrow(
            sunny.point_at_angle(-PI/3),
            rainy.point_at_angle(2.5*PI/3),
            buff=0.0
        )

        loop_s = CurvedArrow(
            sunny.point_at_angle(PI/3),
            sunny.point_at_angle(2*PI/3),
            angle=PI*1.5
        )
        self.add_sound("voiceovers/click.wav")
        self.play(Create(loop_s))
        self.wait()
        self.add_sound("voiceovers/click.wav")
        self.play(Create(cloudy), Write(cloudy_label), Create(arrow_sc))
        self.add_sound("voiceovers/click.wav")
        self.add_sound("voiceovers/rain-loop.mp3")
        self.play(Create(rainy), Write(rainy_label), Create(arrow_sr))

        self.wait(4)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        music = get_youtube_video().scale(0.5).shift(LEFT * 3)
        tech = get_youtube_video().scale(0.5).shift(RIGHT * 3)
        gaming = get_youtube_video().scale(0.5).shift(DOWN * 3)
        gov = SVGMobject("assets/city-hall.svg").set_color(GRAY).shift(DOWN * 2 + RIGHT * 4)
        VGroup(music, tech, gaming).to_corner(UL).shift(DOWN)

        music_label = Text("Âm nhạc", font="Noto Sans").scale(0.6).next_to(music, DOWN)
        tech_label = Text("Công nghệ", font="Noto Sans").scale(0.6).next_to(tech, DOWN)
        gaming_label = Text("Gaming", font="Noto Sans").scale(0.6).next_to(gaming, DOWN)
        gov_label = Text("Trang chính phủ", font="Noto Sans").scale(0.45).next_to(gov, DOWN)
        self.add_sound("voiceovers/game-start.mp3")
        self.play(FadeIn(VGroup(music, tech, gaming, music_label, tech_label, gaming_label)))

        transitions = {
            "Music": [("Music", 0.6), ("Tech", 0.4)],
            "Tech": [("Tech", 0.3), ("Gaming", 0.5), ("Music", 0.2)],
            "Gaming": [("Gaming", 0.7), ("Music", 0.3)]
        }

        state_positions = {
            "Music": music,
            "Tech": tech,
            "Gaming": gaming
        }

        user = SVGMobject("assets/user.svg").set_color(GOLD_E).scale(0.6).move_to(music.get_right()).set_z_index(3)
        self.add_sound("voiceovers/ui_pop_up.mp3")
        self.play(FadeIn(user))
        
        current_state = "Music"
        for i in range(18):
            if i==2:
                self.add_sound("voiceovers/youtube.mp3")
            choices = transitions[current_state]
            r = random.random()
            cumulative = 0
            for state, prob in choices:
                cumulative += prob
                if r <= cumulative:
                    next_state = state
                    break
            self.add_sound("voiceovers/click.wav")
            self.play(
                state_positions[current_state].animate.set_stroke(width=6),
                run_time=0.2
            )
            self.play(
                user.animate.move_to(state_positions[next_state].get_right()),
                run_time=0.8
            )

            self.play(
                state_positions[current_state].animate.set_stroke(width=2),
                run_time=0.2
            )

            current_state = next_state
            if i==5:
                self.add_sound("voiceovers/gov_site.mp3")
            if i==9:
                self.play(Create(gov), Write(gov_label))
        self.wait(3)

class KnightRandomWalk(Scene):
    def construct(self):
        board_size = 8
        square_size = 0.8

        # Create chessboard squares
        board = VGroup()
        squares = {}

        for row in range(board_size):
            for col in range(board_size):
                color = WHITE if (row + col) % 2 == 0 else GREY
                square = Square(side_length=square_size)
                square.set_fill(color, opacity=1)
                square.set_stroke(BLACK, width=1)
                square.move_to(
                    np.array([
                        (col - board_size/2 + 0.5) * square_size,
                        (row - board_size/2 + 0.5) * square_size,
                        0
                    ])
                )
                board.add(square)
                squares[(row, col)] = square

        self.play(Create(board))

        # Knight starting position
        knight_pos = (0, 0)

        knight = Text("♞", color=YELLOW, weight=BOLD).scale(0.6)
        knight.move_to(squares[knight_pos].get_center())
        self.play(FadeIn(knight))

        # Possible knight moves
        knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

        steps = 25  # Number of random moves

        for _ in range(steps):
            valid_moves = []

            for move in knight_moves:
                new_row = knight_pos[0] + move[0]
                new_col = knight_pos[1] + move[1]

                if 0 <= new_row < board_size and 0 <= new_col < board_size:
                    valid_moves.append((new_row, new_col))

            if not valid_moves:
                break

            knight_pos = random.choice(valid_moves)

            self.play(
                knight.animate.move_to(
                    squares[knight_pos].get_center()
                ),
                run_time=0.5
            )

        self.wait(2)

class NeonLudo(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/NeonLudo.mp3")
        horse_race = ImageMobject("assets/horse-race.png"
                                    ).scale(0.2).to_edge(LEFT, LARGE_BUFF).to_edge(UP)
        self.play(FadeIn(horse_race))

        board, path_positions = self.create_neon_board()
        self.add_sound("voiceovers/game-start.mp3")
        self.play(FadeIn(board), run_time=2)

        horse = self.glow_circle(radius=0.18, color=PURE_RED)
        horse.move_to(path_positions[0])
        self.add_sound("voiceovers/ui_pop_up.mp3")
        self.play(FadeIn(horse))

        # Neon dice
        dice = self.create_neon_dice(1)
        dice.to_edge(RIGHT).shift(DOWN)
        self.play(FadeIn(dice))

        current_index = 0

        for _ in range(6):
            roll = random.randint(1, 6)

            # Dice flicker animation
            for _ in range(8):
                temp = random.randint(1, 6)
                new_dice = self.create_neon_dice(temp).move_to(dice)
                self.play(Transform(dice, new_dice), run_time=0.07)

            final_dice = self.create_neon_dice(roll).move_to(dice)
            self.play(Transform(dice, final_dice), run_time=0.2)

            # Move horse
            for _ in range(roll):
                current_index = (current_index + 1) % len(path_positions)
                self.add_sound("voiceovers/moving-with-table.mp3")
                self.play(
                    horse.animate.move_to(path_positions[current_index]),
                    run_time=0.2
                )

        self.wait(2)

    def create_neon_board(self):
        board = VGroup()
        tile = 0.45
        n = 15
        path_positions = []

        def pos(r, c):
            x = (c - n/2) * tile + tile/2
            y = (n/2 - r) * tile - tile/2
            return np.array([x, y, 0])

        # Dark base grid with neon lines
        for r in range(n):
            for c in range(n):
                sq = Square(tile)
                sq.move_to(pos(r, c))
                sq.set_fill("#050505", 1)
                sq.set_stroke("#111111", 1)
                board.add(sq)

        # Neon path loop
        coords = []

        for c in range(6, 9):
            coords.append((0, c))
        for r in range(1, 9):
            coords.append((r, 8))
        for c in range(9, 15):
            coords.append((8, c))
        for r in range(9, 15):
            coords.append((r, 6))
        for c in range(5, -1, -1):
            coords.append((6, c))
        for r in range(5, -1, -1):
            coords.append((r, 6))

        for (r, c) in coords:
            neon_tile = Square(tile)
            neon_tile.move_to(pos(r, c))
            neon_tile.set_fill("#0a0a0a", 1)
            neon_tile.set_stroke(PURE_GREEN, 2)
            board.add(neon_tile)
            path_positions.append(pos(r, c))

        return board, path_positions

    def glow_circle(self, radius, color):
        glow = Circle(radius=radius*1.6)
        glow.set_fill(color, opacity=0.15)
        glow.set_stroke(color, width=8, opacity=0.4)

        core = Circle(radius=radius)
        core.set_fill(color, 1)
        core.set_stroke(WHITE, 1)

        return VGroup(glow, core)
    
    def create_neon_dice(self, face):
        size = 0.8

        glow = RoundedRectangle(
            corner_radius=0.2,
            width=size,
            height=size
        )
        glow.set_stroke(PURE_BLUE, 8, opacity=0.4)
        glow.set_fill("#0a0a0a", 1)

        box = RoundedRectangle(
            corner_radius=0.2,
            width=size,
            height=size
        )
        box.set_stroke(PURE_BLUE, 2)
        box.set_fill("#111111", 1)

        dots = VGroup()
        positions = {
            1: [(0,0)],
            2: [(-0.2,0.2),(0.2,-0.2)],
            3: [(-0.25,0.25),(0,0),(0.25,-0.25)],
            4: [(-0.25,0.25),(0.25,0.25),(-0.25,-0.25),(0.25,-0.25)],
            5: [(-0.25,0.25),(0.25,0.25),(0,0),(-0.25,-0.25),(0.25,-0.25)],
            6: [(-0.25,0.3),(0.25,0.3),(-0.25,0),(0.25,0),(-0.25,-0.3),(0.25,-0.3)]
        }

        for (x,y) in positions[face]:
            dot = Dot([x,y,0], radius=0.06, color=PURE_BLUE)
            dots.add(dot)

        return VGroup(glow, box, dots)

class RandomWalkUpdater(Scene):
    def construct(self):
        num_walkers = 1
        # step_size = 0.2
        step_size = 0.5
        # step_interval = 0.1   # time between steps
        step_interval = 0.5
        run_time = 10         # total animation time

        colors = [BLUE, RED, GREEN, YELLOW, PURPLE]

        walkers = VGroup()
        paths = VGroup()

        for i in range(num_walkers):
            start = ORIGIN

            # dot = Dot(start, color=colors[i % len(colors)])
            dot = SVGMobject("assets/look_closely.svg")
            path = VMobject(color=colors[i % len(colors)])
            path.set_points_as_corners([start, start])

            # Custom attributes for timing
            dot.time_since_step = 0
            dot.path = path

            def updater(mob, dt):
                mob.time_since_step += dt

                if mob.time_since_step >= step_interval:
                    mob.time_since_step = 0

                    direction = random.choice([
                        UP, DOWN, LEFT, RIGHT
                    ])

                    new_pos = mob.get_center() + direction * step_size
                    mob.move_to(new_pos)
                    # mob.path.add_points_as_corners([new_pos])

            dot.add_updater(updater)

            walkers.add(dot)
            paths.add(path)
        grid = NumberPlane()
        self.add(grid, walkers)

        self.wait(run_time)
        self.play(FocusOn(dot))
        self.wait(3)

        # Optional: stop updating at end
        for w in walkers:
            w.clear_updaters()

        self.wait(2)
        self.play(FadeOut(grid, dot))
        title = Text("Markov chains", font="Noto Sans", weight=BOLD, font_size=40)
        self.play(Write(title))
        self.wait()
        search = SVGMobject("assets/search_engine.svg").shift(3*LEFT+2*UP)
        self.play(DrawBorderThenFill(search))
        nn = get_nn().scale(0.4).shift(3*RIGHT+2*UP)
        self.play(Create(nn))
        finance = SVGMobject("assets/finance.svg").shift(3*LEFT+2*DOWN)
        self.play(DrawBorderThenFill(finance))
        weather = SVGMobject("assets/weather.svg").shift(3*RIGHT+2*DOWN)
        self.play(DrawBorderThenFill(weather))
        self.wait(3)

class States(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/States.mp3")
        title = Text("Trạng thái", font="Noto Sans", weight=BOLD)
        self.play(SpinInFromNothing(title), run_time=1.5)
        self.wait()
        self.play(title.animate.scale(0.75).to_edge(UP))
        self.wait(2)
        a = Circle(radius=0.7, color=RED).shift(LEFT * 2.5)
        b = Circle(radius=0.7, color=BLUE).shift(RIGHT * 2.5)
        c = Circle(radius=0.7, color=GREEN).shift(DOWN * 2.5)
        nodes = VGroup(a, b, c)

        a_label = Text("A").scale(0.6).move_to(a)
        b_label = Text("B").scale(0.6).move_to(b)
        c_label = Text("C").scale(0.6).move_to(c)
        labels = VGroup(a_label, b_label, c_label)
        self.add_sound("voiceovers/game-start.mp3")
        self.play(Create(nodes))
        self.wait()
        self.play(LaggedStart(*[Write(label) for label in labels], lag_ratio=0.5))
        self.wait()
        def highlight(target_index):
            animations = []
            for i, node in enumerate(nodes):
                if i == target_index:
                    animations.append(node.animate.set_fill(opacity=1))
                    animations.append(node.animate.set_stroke(width=4))
                    animations.append(labels[i].animate.set_opacity(1))
                else:
                    animations.append(node.animate.set_fill(opacity=0.1))
                    animations.append(node.animate.set_stroke(width=1))
                    animations.append(labels[i].animate.set_opacity(0.2))
            return animations
        for _ in range(3):
            self.add_sound("voiceovers/soccer-ball-kick.mp3")
            self.play(*highlight(0))  # Highlight A
            self.wait(0.2)
            self.add_sound("voiceovers/soccer-ball-kick.mp3")
            self.play(*highlight(1))  # Highlight B
            self.wait(0.2)
            self.add_sound("voiceovers/soccer-ball-kick.mp3")
            self.play(*highlight(2))  # Highlight C
            self.wait(0.2)
        self.play(
            nodes.animate.set_fill(opacity=1),
            nodes.animate.set_stroke(width=4),
            labels.animate.set_opacity(1),
        )

        arrow_ab = CurvedArrow(
            a.get_right(),
            b.get_left(),
            angle=-PI/4
        )

        arrow_bc = CurvedArrow(
            b.get_bottom(),
            c.get_right(),
            angle=-PI/4
        )

        arrow_ca = CurvedArrow(
            c.get_left(),
            a.get_bottom(),
            angle=-PI/4
        )

        loop_a = CurvedArrow(
            a.point_at_angle(PI/3),
            a.point_at_angle(2*PI/3),
            angle=PI*1.5
        )

        loop_b = CurvedArrow(
            b.point_at_angle(PI/3),
            b.point_at_angle(2*PI/3),
            angle=PI*1.5
        )

        loop_c = CurvedArrow(
            c.point_at_angle(-PI/3),
            c.point_at_angle(-2*PI/3),
            angle=-PI*1.5
        )

        p_ab = MathTex("0.4").next_to(arrow_ab, UP)
        p_bc = MathTex("0.5").next_to(arrow_bc, RIGHT)
        p_ca = MathTex("0.3").next_to(arrow_ca, LEFT)

        p_aa = MathTex("0.6").next_to(loop_a, UP)
        p_bb = MathTex("0.5").next_to(loop_b, UP)
        p_cc = MathTex("0.7").next_to(loop_c, DOWN)
        prob_group = VGroup(arrow_ca, arrow_ab, arrow_bc, loop_c, loop_a, loop_b, p_cc, p_ca, p_ab, p_aa, p_bb, p_bc)
        self.add_sound("voiceovers/click.wav")
        self.play(
            Create(arrow_ab),
            Create(arrow_bc),
            Create(arrow_ca),
            Create(loop_a),
            Create(loop_b),
            Create(loop_c),
            run_time=2
        )
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(
            Write(p_ab), Write(p_bc), Write(p_ca),
            Write(p_aa), Write(p_bb), Write(p_cc)
        )
        self.wait()
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(loop_a.animate.set_color(YELLOW))
        self.play(Indicate(p_aa), loop_a.animate.set_color(WHITE))
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(arrow_ab.animate.set_color(YELLOW))
        self.play(Indicate(p_ab), arrow_ab.animate.set_color(WHITE))
        self.wait()
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(VGroup(nodes, labels, prob_group).animate.scale(0.65).shift(UP))
        self.wait()
        def show_sum(prob1, prob2, state):
            box1 = SurroundingRectangle(prob1, color=state.get_color())
            box2 = SurroundingRectangle(prob2, color=state.get_color())
            self.add_sound("voiceovers/click.wav")
            self.play(Create(box1), Create(box2))
            equation = MathTex(
                prob1.tex_string,
                "+",
                prob2.tex_string,
                "=",
                "1"
            ).to_edge(DOWN)
            equation.set_color(state.get_color())
            prob1_equation = equation[0]
            prob2_equation = equation[2]
            prob1_equation.target, prob2_equation.target = prob1, prob2
            for mob in (prob1_equation, prob2_equation):
                mob.save_state()
                mob.move_to(mob.target)
            self.add_sound("voiceovers/sword-swing.wav")
            self.play(Write(equation), *[mob.animate.restore() for mob in (prob1_equation, prob2_equation)])
            self.wait()
            self.play(FadeOut(equation, box1, box2))
        show_sum(p_aa, p_ab, a)
        show_sum(p_bb, p_bc, b)
        show_sum(p_cc, p_ca, c)
        self.wait(3)
class MarkovProperty_short(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/MarkovProperty1.mp3")
        title = Text("Tính chất Markov", font="Noto Sans", weight=BOLD)
        self.play(SpinInFromNothing(title), run_time=1.5)
        self.wait()
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(title.animate.scale(0.75).to_edge(UP))
        self.wait()
        weathers = VGroup(SVGMobject("assets/sunny.svg").scale(0.6),
                          MathTex(r"\rightarrow"),
                          SVGMobject(r"assets/cloudy.svg").scale(0.6),
                          MathTex(r"\rightarrow"),
                          SVGMobject("assets/rainy.svg").scale(0.6),
                          MathTex(r"\rightarrow"),
                          Text("?", font="Noto Sans", font_size=64, weight=BOLD))
        weathers.arrange(RIGHT)
        formula = MathTex(
            r"P(X_{n+1} \mid X_n, X_{n-1}, \dots) = P(X_{n+1} \mid X_n)"
        ).scale(0.8)
        formula[0][2:6].set_color(BLUE)
        formula[0][7:18].set_color(YELLOW)
        formula[0][-8:-4].set_color(BLUE)
        formula[0][-3:-1].set_color(YELLOW)
        VGroup(weathers, formula).arrange(DOWN, LARGE_BUFF)
        for mob in weathers:
            index = weathers.submobjects.index(mob)
            if index in (0, 2, 4, 6):
                self.add_sound("voiceovers/pop-402323.mp3")
            else:
                self.add_sound("voiceovers/sword-swing.wav")
            self.play(FadeIn(mob))      
            if index in (2, 4):
                self.play(*[previous.animate.set_opacity(0.2) for previous in weathers.submobjects[index-2:index]])
        self.add_sound("voiceovers/MarkovProperty2.mp3")
        self.add_sound("voiceovers/shine2.mp3")
        self.play(Write(formula))
        self.wait()
        self.add_sound("voiceovers/ding.wav")
        self.play(Circumscribe(formula[0][2:6], color=GREEN))
        self.wait(0.5)
        self.add_sound("voiceovers/ding.wav")
        self.play(Circumscribe(formula[0][7:18], color=GREEN))
        self.wait(0.5)
        self.add_sound("voiceovers/ding.wav")
        self.play(Circumscribe(formula[0][-8:-4], color=GREEN))
        self.wait(0.5)
        self.add_sound("voiceovers/ding.wav")
        self.play(Circumscribe(formula[0][-3:-1], color=GREEN))
        self.wait()
        lightbulb = SVGMobject("assets/light-bulb.svg").scale(0.5).to_corner(UR, LARGE_BUFF)
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(lightbulb, shift=DOWN))
        self.wait(4)
        self.play(FadeOut(formula, lightbulb, weathers, title))
        self.wait(2)
        
class TransitionMatrix(Scene):
    def construct(self):
        self.wait()
        title = Text("Ma trận chuyển đổi", font="Noto Sans", weight=BOLD)
        self.play(SpinInFromNothing(title), run_time=1.5)
        self.wait()
        self.play(FadeOut(title))
        self.add_sound("voiceovers/TransitionMatrix1.mp3")
        a = Circle(radius=0.6, color=RED).shift(LEFT * 2.5)
        b = Circle(radius=0.6, color=BLUE).shift(RIGHT * 2.5)
        c = Circle(radius=0.6, color=GREEN).shift(DOWN * 2.5)
        nodes = VGroup(a, b, c).shift(1.2*UP)

        a_label = Text("A").scale(0.8).move_to(a)
        b_label = Text("B").scale(0.8).move_to(b)
        c_label = Text("C").scale(0.8).move_to(c)
        labels = VGroup(a_label, b_label, c_label)
        
        arrow_ab = CurvedArrow(
            a.get_right(),
            b.get_left(),
            angle=-PI/4
        )

        arrow_bc = CurvedArrow(
            b.get_bottom(),
            c.get_right(),
            angle=-PI/4
        )

        arrow_ca = CurvedArrow(
            c.get_left(),
            a.get_bottom(),
            angle=-PI/4
        )

        loop_a = CurvedArrow(
            a.point_at_angle(PI/3),
            a.point_at_angle(2*PI/3),
            angle=PI*1.5
        )

        loop_b = CurvedArrow(
            b.point_at_angle(PI/3),
            b.point_at_angle(2*PI/3),
            angle=PI*1.5
        )

        loop_c = CurvedArrow(
            c.point_at_angle(-PI/3),
            c.point_at_angle(-2*PI/3),
            angle=-PI*1.5
        )

        p_ab = MathTex("0.4").next_to(arrow_ab, UP)
        p_bc = MathTex("0.5").next_to(arrow_bc, RIGHT)
        p_ca = MathTex("0.3").next_to(arrow_ca, LEFT)

        p_aa = MathTex("0.6").next_to(loop_a, UP)
        p_bb = MathTex("0.5").next_to(loop_b, UP)
        p_cc = MathTex("0.7").next_to(loop_c, DOWN)
        prob_group = VGroup(VGroup(loop_a, arrow_ab, p_aa, p_ab),
                            VGroup(loop_b, arrow_bc, p_bb, p_bc),
                            VGroup(loop_c, arrow_ca, p_cc, p_ca))
        
        VGroup(nodes, labels, prob_group).scale(0.6).to_edge(LEFT, LARGE_BUFF).to_edge(UP)
        self.add_sound("voiceovers/game-start.mp3")
        self.play(Create(nodes), Write(labels), FadeIn(prob_group))
        self.wait()

        transition_matrix = VGroup(
            MathTex("P ="),
            Matrix([
                ["0.6", "0.4", "0.0"],
                ["0.0", "0.5", "0.5"],
                ["0.3", "0.0", "0.7"],
            ])
        ).arrange(RIGHT)

        transition_matrix.to_edge(RIGHT, MED_LARGE_BUFF).shift(1.1*UP)

        row_labels = VGroup(VGroup(a, a_label).copy().scale(0.7), VGroup(b, b_label).copy().scale(0.7), VGroup(c, c_label).copy().scale(0.7)).arrange(DOWN, buff=0.3)
        row_labels.next_to(transition_matrix[1], LEFT)

        col_labels = VGroup(VGroup(a, a_label).copy().scale(0.7), VGroup(b, b_label).copy().scale(0.7), VGroup(c, c_label).copy().scale(0.7)).arrange(RIGHT, buff=0.8)
        col_labels.next_to(transition_matrix[1], UP)
        self.add_sound("voiceovers/shine2.mp3")
        self.play(FadeIn(transition_matrix[1].get_brackets()))
        self.wait(3)
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(row_labels))
        self.wait(2)
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(col_labels))
        self.wait()
        ent = transition_matrix[1].get_entries()
        ent[0].target, ent[1].target, ent[4].target, ent[5].target, ent[6].target, ent[8].target = p_aa, p_ab, p_bb, p_bc, p_ca, p_cc
        for mob in (ent[0], ent[1], ent[4], ent[5], ent[6], ent[8]):
            mob.save_state()
            mob.move_to(mob.target)
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(FadeIn(transition_matrix[1].get_entries()),
                  *[mob.animate.restore() for mob in (ent[0], ent[1], ent[4], ent[5], ent[6], ent[8])])
        self.wait(2)
        def highlight(target_index):
            animations = []
            for i, node in enumerate(nodes):
                if i == target_index:
                    animations.append(node.animate.set_fill(opacity=1))
                    animations.append(node.animate.set_stroke(width=4))
                    animations.append(labels[i].animate.set_opacity(1))
                    animations.append(prob_group[i][:2].animate.set_stroke(opacity=1))
                    animations.append(prob_group[i][0].tip.animate.set_fill(opacity=1))
                    animations.append(prob_group[i][1].tip.animate.set_fill(opacity=1))
                    animations.append(prob_group[i][2:].animate.set_opacity(1))
                    
                else:
                    animations.append(node.animate.set_fill(opacity=0.1))
                    animations.append(node.animate.set_stroke(width=1))
                    animations.append(labels[i].animate.set_opacity(0.2))
                    animations.append(prob_group[i][:2].animate.set_stroke(opacity=0.2))
                    animations.append(prob_group[i][0].tip.animate.set_fill(opacity=0.2))
                    animations.append(prob_group[i][1].tip.animate.set_fill(opacity=0.2))
                    animations.append(prob_group[i][2:].animate.set_opacity(0.2))
            return animations

        for i in range(3):
            box = SurroundingRectangle(transition_matrix[1].get_rows()[i], color=nodes[i].get_color())
            self.add_sound("voiceovers/click.wav")
            self.play(Create(box), *highlight(i))
            self.wait()
            self.play(FadeOut(box))
        self.add_sound("voiceovers/TransitionMatrix2.mp3")
        self.play(
            nodes.animate.set_fill(opacity=1),
            nodes.animate.set_stroke(width=4),
            labels.animate.set_opacity(1),
            *[prob_state[:2].animate.set_stroke(opacity=1) for prob_state in prob_group],
            *[prob_state[0].tip.animate.set_fill(opacity=1) for prob_state in prob_group],
            *[prob_state[1].tip.animate.set_fill(opacity=1) for prob_state in prob_group],
            *[prob_state[2:].animate.set_opacity(1) for prob_state in prob_group]
        ) 
        self.wait()
        self.add_sound("voiceovers/ui_pop_up.mp3")
        self.play(FadeOut(row_labels, col_labels), FadeIn(transition_matrix[0]))
        self.wait()    
        man = ImageMobject("assets/dreamdigitalartist-man.png").scale(0.4).shift(0.5*LEFT)
        self.add_sound("voiceovers/fragment_retrievewav.mp3")
        self.play(FadeIn(man))
        self.wait(2)
        self.play(Indicate(transition_matrix, color=BLUE))
        self.wait(3)
        
        P = np.array([
            [0.6, 0.4, 0.0],
            [0.0, 0.5, 0.5],
            [0.3, 0.0, 0.7]
        ])

        pi = np.array([1.0, 0.0, 0.0])
        vector = Matrix([[f"{x:.2f}" for x in pi]])
        pi_vector = VGroup(
            MathTex("\\pi  = "),
            vector.copy()
        ).arrange(RIGHT).to_edge(LEFT, LARGE_BUFF).shift(1.1*UP)
        col_labels_vector = col_labels.copy().next_to(pi_vector[1], UP)
        self.add_sound("voiceovers/StateVector.mp3")
        self.play(FadeOut(prob_group, man))
        self.wait(2)
        self.add_sound("voiceovers/ui_pop_up.mp3")
        self.play(FadeIn(pi_vector[0], pi_vector[1].get_brackets()), 
                  *[Transform(VGroup(node, label), label_vector) for node, label, label_vector in zip(nodes, labels, col_labels_vector)])
        self.wait(2)
        self.add_sound("voiceovers/beep.mp3")
        self.play(FocusOn(nodes[0]))
        self.play(*[nodes[i].animate.set_fill(opacity=0.1) for i in (1, 2)],
                  *[nodes[i].animate.set_stroke(width=1) for i in (1, 2)],
                  *[labels[i].animate.set_opacity(0.2) for i in (1, 2)])
        self.wait()
        pi_vector_ent = pi_vector[1].get_entries()
        for entry in pi_vector_ent:
            self.add_sound("voiceovers/happy-coin.wav")
            self.play(FadeIn(entry))
            self.wait(0.5)
        self.wait()
        matrix = Matrix([
            [f"{x:.1f}" for x in row]
            for row in P
        ])
        equals = MathTex("=")
        pi_next = pi @ P
        result = Matrix([[f"{x:.2f}" for x in pi_next]])

        VGroup(vector, matrix, equals, result).arrange(RIGHT).to_edge(DOWN, LARGE_BUFF)
        vector.target, matrix.target = pi_vector[1], transition_matrix[1]
        for mob in (vector, matrix):
            mob.save_state()
            mob.move_to(mob.target)
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(*[mob.animate.restore() for mob in (vector, matrix)])
        self.wait(2)
        self.add_sound("voiceovers/click.wav")
        self.play(Write(equals))
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(Write(result))
        self.wait(4)
        pi_next_next = pi_next @ P
        result_next = Matrix([[f"{x:.2f}" for x in pi_next_next]]).move_to(result)
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(FadeOut(vector), result.animate.move_to(vector))
        self.wait()
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(Write(result_next))
        self.wait(5)

class MarkovConvergence(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/MarkovConvergence.mp3")
        P = np.array([
            [0.6, 0.4, 0.0],
            [0.0, 0.5, 0.5],
            [0.3, 0.0, 0.7]
        ])

        eigvals, eigvecs = np.linalg.eig(P.T)
        idx = np.argmin(np.abs(eigvals - 1))
        stationary = np.real(eigvecs[:, idx])
        stationary = stationary / np.sum(stationary)

        title = Text("Stationary Distribution", font="Noto Sans").scale(0.7)
        title.to_edge(UP)
        subtitle = Text("Phân bố dừng", font="Noto Sans", color=GRAY).scale(0.6).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))

        matrix = Matrix(
            [[0.6, 0.4, 0.0],
             [0.0, 0.5, 0.5],
             [0.3, 0.0, 0.7]],
            h_buff=1.2,
            v_buff=0.8
        ).scale(0.7)

        matrix_label = MathTex("P =").next_to(matrix, LEFT)
        matrix_group = VGroup(matrix_label, matrix)
        matrix_group.set_color(BLUE).to_corner(UL)
        self.add_sound("voiceovers/game-start.mp3")
        self.play(FadeIn(matrix_group))
        self.wait()

        stationary_matrix = Matrix(
            [[f"{stationary[0]:.2f}"],
             [f"{stationary[1]:.2f}"],
             [f"{stationary[2]:.2f}"]],
        ).scale(0.8)

        pi_label = MathTex(r"\pi =").next_to(stationary_matrix, LEFT)
        pi_group = VGroup(pi_label, stationary_matrix)
        pi_group.set_color(YELLOW).to_corner(UR)
        self.add_sound("voiceovers/beep.mp3")
        self.play(FadeIn(pi_group))
        self.wait()

        dist = np.array([1.0, 0.0, 0.0])

        chart = BarChart(
            values=dist,
            bar_names=["A", "B", "C"],
            y_range=[0, 1, 0.2],
            y_length=3.5,
            x_length=5,
            bar_colors=[RED, BLUE, GREEN],
        ).shift(DOWN * 1.2)
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(Create(chart))
        self.wait(2)

        for _ in range(15):
            dist = dist @ P

            new_chart = BarChart(
                values=dist,
                bar_names=["A", "B", "C"],
                y_range=[0, 1, 0.2],
                y_length=3.5,
                x_length=5,
                bar_colors=[RED, BLUE, GREEN],
            ).shift(DOWN * 1.2)
            self.add_sound("voiceovers/click.wav")
            self.play(Transform(chart, new_chart))

        convergence_text = VGroup(Text("Hội tụ về ", font="Noto Sans").scale(0.7), 
                                  MathTex(r"\pi").set_color(YELLOW)).arrange(RIGHT).to_edge(RIGHT)
        self.add_sound("voiceovers/ding.wav")
        self.play(FadeIn(convergence_text))
        self.wait()
        self.play(FadeOut(convergence_text))
        eigen_eq = MathTex(r"\pi = \pi P").scale(0.9)
        eigen_eq[0][0].set_color(YELLOW)
        eigen_eq[0][-1].set_color(BLUE)
        eigen_eq[0][-2].set_color(YELLOW)
        self.add_sound("voiceovers/shine2.mp3")
        self.play(Write(eigen_eq))
        self.play(Flash(eigen_eq))
        self.wait(2)
        self.add_sound("voiceovers/wiggle.mp3")
        self.play(Wiggle(eigen_eq))
        self.wait(3)

class LinearAlgebra(Scene):
    def construct(self):
        self.wait()
        P = np.array([
            [0.7, 0.2, 0.1],
            [0.2, 0.6, 0.2],
            [0.1, 0.2, 0.7]
        ])

        state = np.array([[1.0],
                          [0.0],
                          [0.0]])

        iterations = 3

        eq1 = MathTex(r"\pi_{n+1} = \pi_n P").scale(1.2).to_edge(UP)
        eq1[0][:4].set_color(YELLOW)
        eq1[0][5:-1].set_color(YELLOW)
        eq1[0][-1].set_color(BLUE)
        eq2 = MathTex(r"\pi_n = \pi_0 P^n").scale(1.2).next_to(eq1, DOWN)
        eq2[0][:2].set_color(YELLOW)
        eq2[0][3:5].set_color(YELLOW)
        eq2[0][-2:].set_color(BLUE)
        self.add_sound("voiceovers/pop-402323.mp3")
        self.play(FadeIn(eq1, eq2))

        matrix = Matrix(
            [[f"{P[i,j]:.1f}" for j in range(3)] for i in range(3)],
            left_bracket="[",
            right_bracket="]"
        ).shift(LEFT * 3)

        matrix_label = MathTex("P =").next_to(matrix, LEFT)
        matrix_label[0][0].set_color(BLUE)
        self.add_sound("voiceovers/game-start.mp3")
        self.play(FadeIn(matrix, matrix_label))

        vector = Matrix(
            [[f"{state[i,0]:.2f}"] for i in range(3)],
            left_bracket="[",
            right_bracket="]"
        ).shift(RIGHT * 3)

        vector_label = MathTex(r"\pi_0 =").next_to(vector, LEFT)
        vector_label[0][:2].set_color(YELLOW)
        self.add_sound("voiceovers/beep.mp3")
        self.play(FadeIn(vector, vector_label))
        self.wait()

        self.add_sound("voiceovers/LinearAlgebra.mp3")
        for k in range(iterations):
            calc_group = VGroup()
            column = vector.get_columns()[0]
            new_state = []
            for i in range(3):
                row = matrix.get_rows()[i]
                self.play(
                    row.animate.set_color(BLUE),
                    column.animate.set_color(YELLOW),
                    run_time=0.5
                )
                value = sum(P[i,j] * state[j,0] for j in range(3))
                new_state.append(value)

                calc = MathTex(
                    rf"{P[i,0]:.1f}({state[0,0]:.2f}) + "
                    rf"{P[i,1]:.1f}({state[1,0]:.2f}) + "
                    rf"{P[i,2]:.1f}({state[2,0]:.2f})"
                    rf" = {value:.3f}"
                ).scale(0.6)
                calc[0][:3].set_color(BLUE)
                calc[0][4:8].set_color(YELLOW)
                calc[0][10:13].set_color(BLUE)
                calc[0][14:18].set_color(YELLOW)
                calc[0][20:23].set_color(BLUE)
                calc[0][24:28].set_color(YELLOW)

                calc.next_to(matrix, DOWN * (i + 1))
                calc_group.add(calc)
                self.add_sound("voiceovers/writin.mp3")
                self.play(Write(calc), run_time=0.4)
                
                self.play(
                    row.animate.set_color(WHITE),
                    column.animate.set_color(WHITE),
                    run_time=0.4
                )

            state = np.array(new_state).reshape((3,1))

            new_vector = Matrix(
                [[f"{state[i,0]:.3f}"] for i in range(3)],
                left_bracket="[",
                right_bracket="]"
            ).move_to(vector)

            new_label = MathTex(rf"\pi_{k+1} =").next_to(new_vector, LEFT)
            self.add_sound("voiceovers/happy-coin.wav")
            self.play(
                Transform(vector, new_vector),
                Transform(vector_label, new_label)
            )
            self.play(FadeOut(calc_group))
        self.play(FadeOut(vector, vector_label, eq1, eq2, matrix, matrix_label))
        title = Text("Phân phối dừng là một vectơ riêng", font="Noto Sans").to_edge(UP)
        eigen_def = MathTex("vP = \\lambda v").scale(1.2)
        eigen_def[0][0].set_color(YELLOW)
        eigen_def[0][1].set_color(BLUE)
        eigen_def[0][-2].set_color(GREEN)
        eigen_def[0][-1].set_color(YELLOW)
        stationary = MathTex("\\pi P = \\pi").scale(1.2).next_to(eigen_def, DOWN)
        stationary[0][0].set_color(YELLOW)
        stationary[0][1].set_color(BLUE)
        stationary[0][-1].set_color(YELLOW)
        highlight = MathTex("\\lambda = 1").set_color(GREEN).next_to(stationary, DOWN)

        self.add_sound("voiceovers/LinearAlgebra1.mp3")
        self.add_sound("voiceovers/shine2.mp3")
        self.play(Write(eigen_def))
        self.wait(4)
        eigen_def_copy = eigen_def.copy()
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(Transform(eigen_def_copy, stationary))
        self.wait(3)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(highlight))
        self.wait(2)
        self.add_sound("voiceovers/LinearAlgebra2.mp3")
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(title))
        self.add_sound("voiceovers/bad-to-the-bone.mp3")
        self.play(Circumscribe(VGroup(stationary, highlight), color=GREEN))
        self.wait(4)

class RandomWalker_short(Scene):
    def construct(self):
        self.add_sound("voiceovers/RandomWalker.mp3")
        vertices = ["A", "B", "C", "D"]

        P = {
            "A": {"A": 0.0, "B": 0.5, "C": 0.3, "D": 0.2},
            "B": {"A": 0.3, "B": 0.0, "C": 0.5, "D": 0.2},
            "C": {"A": 0.25, "B": 0.25, "C": 0.00, "D": 0.5},
            "D": {"A": 0.4, "B": 0.3, "C": 0.3, "D": 0.0},
        }

        edges = [(u, v) for u in vertices for v in vertices if P[u][v] > 0]

        graph = DiGraph(
            vertices,
            edges,
            layout="circular",
            layout_scale=2,
            labels=True,
            vertex_config={
                "radius": 0.4,
                "A": {"fill_color": BLUE},
                "B": {"fill_color": MAROON},
                "C": {"fill_color": GRAY},
                "D": {"fill_color": GREEN}
            },
            edge_config={
                "stroke_width": 2,
                "tip_config": {"tip_length": 0, "tip_width": 0},
            },
        )
        self.add_sound("voiceovers/game-start.mp3")
        self.play(Create(graph))

        edge_labels = VGroup()

        for (u, v) in edges:
            prob = P[u][v]
            label = MathTex(f"{prob:.2f}").scale(0.5)

            edge = graph.edges[(u, v)]
            midpoint = edge.get_center()

            direction = edge.get_unit_vector()
            normal = np.array([-direction[1], direction[0], 0])
            label.move_to(midpoint + 0.3 * normal)

            edge_labels.add(label)

        self.wait()

        title = Text("Người đi bộ ngẫu nhiên", font="Noto Sans", font_size=32)
        title.to_edge(UP)
        self.add_sound("voiceovers/pop-402323.mp3")
        self.play(FadeIn(title))

        counts = {v: 0 for v in vertices}
        total_steps = ValueTracker(0)

        def get_distribution():
            total = max(total_steps.get_value(), 1)
            lines = []
            for v in vertices:
                prob = counts[v] / total
                lines.append(f"{v}: {prob:.2f}")
            return VGroup(
                *[Text(line, font_size=28) for line in lines]
            ).arrange(DOWN, aligned_edge=LEFT).to_corner(UR).shift(LEFT)

        distribution_display = always_redraw(get_distribution)
        
        walker = Dot(color=YELLOW)
        walker.move_to(graph.vertices["A"].get_center())
        self.add_sound("voiceovers/pop-402323.mp3")
        self.play(FadeIn(walker), FadeIn(distribution_display))

        bar_width = 0.4
        max_bar_height = 3
        bar_spacing = 0.8

        bars = VGroup()
        labels = VGroup()

        for i, v in enumerate(vertices):
            bar = Rectangle(width=bar_width, height=0.01,
                            fill_color=graph.vertices[v].get_color(), fill_opacity=0.8)
            bar.move_to(RIGHT*3 + DOWN*1.5 + RIGHT*i*bar_spacing)
            bars.add(bar)

            label = Text(v).scale(0.5)
            label.next_to(bar, DOWN, buff=0.2)
            labels.add(label)

        def update_bars(mob):
            total = max(sum(counts.values()), 1)
            for i, v in enumerate(vertices):
                prob = counts[v] / total
                height = prob * max_bar_height
                bars[i].stretch_to_fit_height(max(height, 0.01))
                bars[i].move_to(
                    RIGHT*3 + DOWN*1.5 + RIGHT*i*bar_spacing
                    + UP*height/2
                )

        bars.add_updater(update_bars)
        self.add_sound("voiceovers/pop-402323.mp3")
        self.play(FadeIn(bars), FadeIn(labels))

        current_state = "A"
        # steps = 200
        steps = 15

        for _ in range(steps):
            counts[current_state] += 1
            total_steps.increment_value(1)

            probs = list(P[current_state].values())
            next_state = np.random.choice(
                list(P[current_state].keys()),
                p=probs
            )
            active_edge = graph.edges[(current_state, next_state)]
            glow = glow_pulse(active_edge)
            self.add(glow)
            self.add_sound("voiceovers/soccer-ball-kick.mp3")
            self.play(
                walker.animate.move_to(
                    graph.vertices[next_state].get_center()
                ),
                FadeOut(glow)
            )

            current_state = next_state

        self.wait()
colors = {
            "A": BLUE_C,
            "B": MAROON_D,
            "C": GREY_BROWN,
            "D": GREEN_E,
        }
class PageRankFlow(Scene):
    def construct(self):
        # self.wait()
        # self.add_sound("voiceovers/PageRankFlow_part1.mp3")
        google = SVGMobject("assets/google.svg").scale(0.45).to_corner(UL)
        subtitle = Tex("PageRank").next_to(google, RIGHT)
        self.add(google, subtitle)
        self.wait()
        # -----------------------------
        # 1. GRAPH STRUCTURE
        # -----------------------------
        positions = {
            "A": LEFT * 4.5,
            "B": UP * 2 + LEFT*1.5,
            "C": RIGHT,
            "D": DOWN * 2 + LEFT*1.5,
        }
        

        nodes = {
            k: get_page(frame_color=colors[k]).scale(0.15).move_to(pos)
            for k, pos in positions.items()
        }

        labels = {
            k: Text(k, font_size=28, weight=BOLD).move_to(v.get_center())
            for k, v in nodes.items()
        }

        edges = [
            ("A", "B"),
            ("B", "C"),
            ("C", "A"),
            ("C", "D"),
            ("D", "C"),
        ]

        arrows = VGroup(*[
            Arrow(
                nodes[a],
                nodes[b],
                buff=0.2,
                stroke_width=2
            )
            for a, b in edges
        ])
        arrows[2].shift(0.3*DOWN)
        arrows[3].shift(0.1*LEFT+0.1*UP)
        arrows[4].shift(0.1*RIGHT+0.1*DOWN)
        for k in nodes:
            # self.add_sound("voiceovers/ui_pop_up.mp3")
            self.play(FadeIn(nodes[k]), FadeIn(labels[k]))

        self.play(Create(arrows))

        # -----------------------------
        # 2. INITIAL PAGERANK VALUES
        # -----------------------------
        ranks = {
            "A": ValueTracker(0.25),
            "B": ValueTracker(0.25),
            "C": ValueTracker(0.25),
            "D": ValueTracker(0.25),
        }

        rank_labels = {
            k: always_redraw(
                lambda k=k: DecimalNumber(
                    ranks[k].get_value(),
                    num_decimal_places=3,
                    font_size=24
                ).next_to(nodes[k], DOWN)
            )
            for k in nodes
        }
        shares = {
            "A": ValueTracker(0),
            "B": ValueTracker(0),
            "C": ValueTracker(0),
            "D": ValueTracker(0),
        }

        self.play(*[FadeIn(v, target_position=google) for v in rank_labels.values()], run_time=2)
        self.wait()
        vertices = positions.keys()
        visit_counts = {v: 0 for v in vertices}
        total_steps = ValueTracker(1)

        bar_width = 0.4
        max_bar_height = 3
        bar_spacing = 0.8

        bars = VGroup()
        labels = VGroup()

        for i, v in enumerate(vertices):
            bar = Rectangle(width=bar_width, height=0.01,
                            fill_color=colors[v], fill_opacity=0.8)
            bar.move_to(RIGHT*4 + RIGHT*i*bar_spacing)
            bars.add(bar)

            label = Text(v).scale(0.5)
            label.next_to(bar, DOWN, buff=0.2)
            labels.add(label)

        def update_bars(mob):
            total = max(sum(visit_counts.values()), 1)
            for i, v in enumerate(vertices):
                prob = visit_counts[v] / total
                height = prob * max_bar_height
                bars[i].stretch_to_fit_height(max(height, 0.01))
                bars[i].move_to(
                    RIGHT*4 + RIGHT*i*bar_spacing
                    + UP*height/2
                )

        bars.add_updater(update_bars)

        self.play(FadeIn(bars), FadeIn(labels))
        share_texts = VGroup()

        # -----------------------------
        # 3. FLOW ANIMATION FUNCTION
        # -----------------------------
        def flow(source, targets):
            value = ranks[source].get_value()
            share = value / len(targets)

            dots = VGroup(*[
                Dot(
                    nodes[source].get_center(),
                    radius=0.07,
                    color=YELLOW
                )
                for _ in targets
            ])

            self.add(dots)
            glows = VGroup()
            for target in targets:
                index = edges.index((source, target))
                active_edge = arrows[index]
                glow = glow_pulse(active_edge)
                glows.add(glow)
            self.play(
                *[
                    dot.animate.move_to(nodes[t].get_center())
                    for dot, t in zip(dots, targets)
                ],
                FadeOut(glows),
                run_time=0.5
            )

            self.remove(dots)

            for t in targets:
                must_shift = shares[t].get_value() > 0
                shares[t].set_value(
                    shares[t].get_value() + share
                )
                share_label = MathTex("+", shares[t].get_value())
                share_label.scale(0.4).next_to(rank_labels[t], DOWN)
                if must_shift:
                    share_label.shift(0.65*RIGHT)
                self.play(FadeIn(share_label), run_time=0.2)
                share_texts.add(share_label)
            for target in targets:
                visit_counts[target] += 1
            total_steps.increment_value(1)

        # -----------------------------
        # 4. ONE ITERATION
        # -----------------------------
        self.wait(0.5)
        flow("A", ["B"])
        self.wait(0.3)
        flow("B", ["C"])
        self.wait(0.3)
        # flow("C", ["A", "D"])
        from_C = "A"
        flow("C", [from_C])
        self.wait(0.3)
        flow("D", ["C"])
        for k in ranks:
            ranks[k].set_value(shares[k].get_value())
            shares[k].set_value(0)
            for mob in share_texts.submobjects:
                self.remove(mob)
        # self.add_sound("voiceovers/win.wav")
        self.play(*[Flash(v) for v in rank_labels.values()])
        self.wait()
        for _ in range(5):
            flow("A", ["B"])
            flow("B", ["C"])
            # flow("C", ["A", "D"])
            if from_C=="A":
                from_C = "D"
            else:
                from_C = "A"
            flow("C", [from_C])
            flow("D", ["C"])
            for k in ranks:
                ranks[k].set_value(shares[k].get_value())
                shares[k].set_value(0)
            for mob in share_texts.submobjects:
                self.remove(mob)
        self.wait(3)
class PageRank(Scene):
    def construct(self):
        google = SVGMobject("assets/google.svg").scale(0.45)
        subtitle = Tex("PageRank")
        VGroup(google, subtitle).arrange(RIGHT).to_edge(UP)
        self.add_sound("voiceovers/game-start.mp3")
        self.play(FadeIn(google, subtitle))
        self.wait()
        self.add_sound("voiceovers/PageRank.mp3")

        positions = {
            "A": LEFT * 4.5 + DOWN,
            "B": UP + LEFT*1.5,
            "C": RIGHT + DOWN,
            "D": DOWN * 3 + LEFT*1.5,
        }

        nodes = {
            k: get_page(frame_color=colors[k]).scale(0.15).move_to(pos)
            for k, pos in positions.items()
        }

        labels = {
            k: Text(k, font_size=28, weight=BOLD).move_to(v.get_center())
            for k, v in nodes.items()
        }

        edges = [
            ("A", "B"),
            ("A", "C"),
            ("B", "C"),
            ("C", "A"),
            ("C", "D"),
            ("D", "C"),
        ]

        arrows = VGroup(*[
            Arrow(
                nodes[a],
                nodes[b],
                buff=0.2,
                stroke_width=2
            )
            for a, b in edges
        ])
        arrows[1].shift(0.2*DOWN)
        arrows[3].shift(0.5*DOWN)
        arrows[4].shift(0.1*LEFT+0.1*UP)
        arrows[5].shift(0.1*RIGHT+0.1*DOWN)
        for k in nodes:
            self.add_sound("voiceovers/pop-402323.mp3")
            self.play(FadeIn(nodes[k]), FadeIn(labels[k]))
        self.add_sound("voiceovers/send-message.mp3")
        self.play(Create(arrows))

        surfer = SVGMobject("assets/user.svg").set_color(GOLD_E).scale(0.35)
        surfer.move_to(nodes["A"].get_left())
        self.add_sound("voiceovers/pop-402323.mp3")
        self.play(FadeIn(surfer))

        vertices = ["A", "B", "C", "D"]
        visit_counts = {v: 0 for v in vertices}
        counter_text = {
            v: Text("0", font_size=24).next_to(nodes[v], DOWN)
            for v in vertices
        }

        for text in counter_text.values():
            self.add(text)
        
        bar_width = 0.4
        max_bar_height = 3
        bar_spacing = 0.8

        bars = VGroup()
        labels = VGroup()

        for i, v in enumerate(vertices):
            bar = Rectangle(width=bar_width, height=0.01,
                            fill_color=colors[v], fill_opacity=0.8)
            bar.move_to(RIGHT*3 + RIGHT*i*bar_spacing)
            bars.add(bar)

            label = Text(v).scale(0.5)
            label.next_to(bar, DOWN, buff=0.2)
            labels.add(label)

        def update_bars(mob):
            total = max(sum(visit_counts.values()), 1)
            for i, v in enumerate(vertices):
                prob = visit_counts[v] / total
                height = prob * max_bar_height
                bars[i].stretch_to_fit_height(max(height, 0.01))
                bars[i].move_to(
                    RIGHT*3 + RIGHT*i*bar_spacing
                    + UP*height/2
                )

        bars.add_updater(update_bars)
        self.add_sound("voiceovers/pop-402323.mp3")
        self.play(FadeIn(bars), FadeIn(labels))

        damping = 0.85 
        steps = 25
        current = "A"

        for _ in range(steps):
            visit_counts[current] += 1

            new_counter = Text(
                str(visit_counts[current]),
                font_size=24
            ).next_to(nodes[current], DOWN)
            # self.add_sound("voiceovers/send-message.mp3")
            self.play(
                Transform(counter_text[current], new_counter),
                run_time=0.2
            )

            outgoing = [e[1] for e in edges if e[0] == current]

            if outgoing and random.random() < damping:
                next_node = random.choice(outgoing)
            else:
                next_node = random.choice(vertices)
            self.add_sound("voiceovers/click.wav")
            self.play(
                surfer.animate.move_to(nodes[next_node].get_left()),
                run_time=0.5
            )
            current = next_node
        self.wait()

class MobileTypingPrediction(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/MobileTypingPrediction1a.mp3")
        self.camera.background_color = "#1e1e1e"

        phone = RoundedRectangle(
            width=4,
            height=8,
            corner_radius=0.5
        ).set_stroke(WHITE, width=4)
        self.add_sound("voiceovers/game-start.mp3")
        self.play(Create(phone))

        chat_bg = Rectangle(
            width=3.6,
            height=6.5
        ).set_fill("#111111", opacity=1).set_stroke(width=0)

        chat_bg.move_to(phone.get_center() + UP*0.5)
        self.play(FadeIn(chat_bg))

        input_bar = RoundedRectangle(
            width=3.6,
            height=0.8,
            corner_radius=0.3
        ).set_fill("#2c2c2c", opacity=1).set_stroke(width=0)

        input_bar.move_to(phone.get_bottom() + UP*0.8)
        self.play(FadeIn(input_bar))

        prediction_bar = Rectangle(
            width=3.6,
            height=0.6
        ).set_fill("#252525", opacity=1).set_stroke(width=0)

        prediction_bar.next_to(input_bar, UP, buff=0.05)

        pred1 = Text("pizza", font="Noto Sans", font_size=24)
        pred2 = Text("toán", font="Noto Sans", font_size=24)
        pred3 = Text("bạn", font="Noto Sans", font_size=24)

        predictions = VGroup(pred1, pred2, pred3)
        predictions.arrange(RIGHT, buff=0.6)
        predictions.move_to(prediction_bar.get_center())
        self.add_sound("voiceovers/ui_pop_up.mp3")
        self.play(FadeIn(prediction_bar))

        typed = Text("", font="Noto Sans", font_size=32)
        typed.move_to(input_bar.get_left() + RIGHT*0.3)

        cursor = Rectangle(width=0.05, height=0.5).set_fill(WHITE, opacity=1)
        cursor.next_to(typed, RIGHT, buff=0.05)

        self.add(typed, cursor)

        def blink(mob, dt):
            mob.set_opacity(0 if int(self.time*2)%2==0 else 1)

        cursor.add_updater(blink)

        text_string = "Tôi yêu "
        self.add_sound("voiceovers/keyboard-typing.mp3")
        for i in range(len(text_string)):
            new_text = Text(text_string[:i+1], font="Noto Sans", font_size=32)
            new_text.move_to(typed.get_center())
            self.play(Transform(typed, new_text), run_time=0.3)
            cursor.next_to(typed, RIGHT, buff=0.05)

        self.wait(1.5)
        self.add_sound("voiceovers/MobileTypingPrediction1a1.mp3")
        self.add_sound("voiceovers/ui_pop_up.mp3")
        self.play(FadeIn(predictions))      
        self.wait(3)
        self.add_sound("voiceovers/MobileTypingPrediction1b.mp3")
        self.add_sound("voiceovers/beep.mp3")
        self.play(Indicate(pred2))
        self.wait()

        completed = Text("Tôi yêu toán", font="Noto Sans", font_size=32)
        completed.move_to(typed.get_center())
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(Transform(typed, completed))

        cursor.next_to(typed, RIGHT, buff=0.05)
        self.wait()
        pred1_new = Text("và", font="Noto Sans", font_size=24)
        pred2_new = Text("bởi vì", font="Noto Sans", font_size=24)

        predictions_new = VGroup(pred1_new, pred2_new)
        predictions_new.arrange(RIGHT, buff=0.6)
        predictions_new.move_to(prediction_bar.get_center())
        self.play(FadeOut(predictions), FadeIn(predictions_new))
        self.wait()
        self.add_sound("voiceovers/beep.mp3")
        self.play(Indicate(pred1_new))
        self.wait(2)
        completed_new = Text("Tôi yêu toán và", font="Noto Sans", font_size=32)
        completed_new.move_to(typed.get_center())
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(Transform(typed, completed_new))
        cursor.next_to(typed, RIGHT, buff=0.05)
        pred1_next = Text("AI", font_size=24)

        predictions_next = VGroup(pred1_next)
        predictions_next.arrange(RIGHT, buff=0.6)
        predictions_next.move_to(prediction_bar.get_center())
        self.play(FadeOut(predictions_new), FadeIn(predictions_next))
        self.add_sound("voiceovers/MobileTypingPrediction2.mp3")
        self.wait(7)
class WordsAsStates(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/WordsAsStates.mp3")
        title = Text("Ngôn ngữ như là trạng thái", font="Noto Sans").to_edge(UP)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(title))
        self.wait()
        words = ["Tôi", "yêu", "toán", "pizza"]

        layout = {
            "Tôi": LEFT * 3 + UP,
            "yêu": LEFT + UP,
            "toán": RIGHT*2 + UP,
            "pizza": RIGHT*2 + DOWN
        }

        vertices = {}

        for word in words:
            text = Text(word, font="Noto Sans", font_size=32)

            box = RoundedRectangle(
                corner_radius=0.2,
                width=text.width + 0.6,
                height=text.height + 0.4,
                color=BLUE,
            )
            box.set_fill(BLUE, opacity=0.5)

            text.move_to(box.get_center())

            node = VGroup(box, text)
            node.move_to(layout[word])

            vertices[word] = node

        edges = [
            ("Tôi", "yêu"),
            ("yêu", "toán"),
            ("yêu", "pizza")
        ]

        arrows = VGroup()

        for start, end in edges:
            arrow = Arrow(
                vertices[start].get_right(),
                vertices[end].get_left(),
                buff=0.15,
                stroke_width=3,
            )
            arrows.add(arrow)

        prob_math = MathTex("0.6").next_to(arrows[1], UP)
        prob_pizza = MathTex("0.4").next_to(arrows[2], LEFT)
        for v in vertices.values():
            self.add_sound("voiceovers/pop-402323.mp3")
            self.play(FadeIn(v))
        self.wait()
        for arrow in arrows:
            self.add_sound("voiceovers/send-message.mp3")
            self.play(GrowArrow(arrow))
        self.add_sound("voiceovers/click.wav")
        self.play(Write(prob_math))
        self.wait()
        self.add_sound("voiceovers/click.wav")
        self.play(Write(prob_pizza))
        self.wait(2)   
        self.add_sound("voiceovers/WordsAsStates2.mp3")
        sunny = SVGMobject("assets/sunny.svg").scale(0.3).shift(LEFT * 1.1 + 0.6*UP)
        cloudy = SVGMobject("assets/cloudy.svg").scale(0.3).shift(RIGHT * 1.1 + 0.6*UP)
        rainy = SVGMobject("assets/rainy.svg").scale(0.3).shift(DOWN * 0.7)
        weathers = VGroup(sunny, cloudy, rainy).to_edge(LEFT, LARGE_BUFF).to_edge(DOWN)

        arrow_sc = Arrow(
            sunny,
            cloudy,
            buff=0.2
        )

        arrow_sr = Arrow(
            sunny,
            rainy,
            buff=0.2
        )

        arrow_cr = Arrow(
            cloudy,
            rainy,
            buff=0.2
        )
        self.wait(1.5)
        self.add_sound("voiceovers/ui_pop_up.mp3")
        self.play(FadeIn(weathers, arrow_sc, arrow_sr, arrow_cr))
        self.wait(.5)
        self.play(FadeOut(weathers, arrow_sc, arrow_sr, arrow_cr), run_time=.5)
        positions = {
            "A": LEFT * 4.5,
            "B": UP * 2 + LEFT*1.5,
            "C": RIGHT,
            "D": DOWN * 2 + LEFT*1.5,
        }
        

        nodes = {
            k: get_page(frame_color=colors[k]).scale(0.15).move_to(pos)
            for k, pos in positions.items()
        }

        labels = {
            k: Text(k, font_size=28, weight=BOLD).move_to(v.get_center())
            for k, v in nodes.items()
        }

        edges = [
            ("A", "B"),
            ("B", "C"),
            ("C", "A"),
            ("C", "D"),
            ("D", "C"),
        ]

        arrows_pagerank = VGroup(*[
            Arrow(
                nodes[a],
                nodes[b],
                buff=0.2,
                stroke_width=2
            )
            for a, b in edges
        ])
        arrows_pagerank[2].shift(0.3*DOWN)
        arrows_pagerank[3].shift(0.1*LEFT+0.1*UP)
        arrows_pagerank[4].shift(0.1*RIGHT+0.1*DOWN)
        pagerank_group = VGroup(arrows_pagerank)
        anims = [FadeIn(arrows_pagerank)]
        for k in nodes:
            pagerank_group.add(nodes[k])
            pagerank_group.add(labels[k])
        pagerank_group.scale(0.6).to_edge(LEFT, LARGE_BUFF).to_edge(DOWN)
        for k in nodes:
            anims.append(FadeIn(nodes[k]))
            anims.append(FadeIn(labels[k]))
        self.add_sound("voiceovers/ui_pop_up.mp3")
        self.play(*anims)
        self.wait()
        
        self.play(*[FadeOut(node) for node in nodes.values()],
                  *[FadeOut(label) for label in labels.values()],
                  *[FadeOut(arrow) for arrow in arrows_pagerank])
        self.wait()
        self.add_sound("voiceovers/wiggle.mp3")
        self.play(*[Wiggle(v) for v in vertices.values()])
        self.wait(3)
class TextGeneration(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/TextGeneration.mp3")
        transitions = {
            "toán": [("và", 0.5), ("vì", 0.5)],
            "và": [("AI", 1.0)],
            "vì": [("nó", 1.0)],
            "nó": [("là", 1.0)],
            "là": [("đẹp", 1.0)],
            "AI": [("là", 1.0)],
            "đẹp": []
        }

        current_word = "toán"
        sentence = ["Tôi", "yêu", "toán"]
        
        sentence_str = " ".join(sentence)
        display_text = Text(sentence_str, font="Noto Sans", font_size=48).to_edge(UP, buff=1)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(display_text))
        self.wait(4)
        self.add_sound("voiceovers/beep.mp3")
        self.play(Indicate(display_text[-4:]))
        self.wait()
        for i in range(4):
            lookup = current_word if i != 3 else "The_2"
            options = transitions.get(lookup, [("...", 1.0)])
            
            circles = VGroup()
            labels = VGroup()
            arrows = VGroup()
            
            for idx, (word, prob) in enumerate(options):
                x_offset = (idx - 1) * 3.5  
                c = Circle(radius=0.7, color=WHITE).shift(DOWN * 2 + RIGHT * x_offset)
                l = Text(word, font="Noto Sans", font_size=24).move_to(c)
                length = len(current_word)
                a = Arrow(display_text[-length:].get_bottom(), c.get_top(), stroke_width=prob*10)
                p = MathTex(f"{prob}").scale(0.7).next_to(a.get_center(), RIGHT, buff=0.5)
                
                circles.add(c)
                labels.add(l)
                arrows.add(VGroup(a, p))
            self.add_sound("voiceovers/click.wav")
            self.play(Create(circles), Write(labels), FadeIn(arrows))
            self.wait()
            if i==0:
                self.wait()
                self.play(LaggedStart(*[circle.animate.set_color(YELLOW) for circle in circles], lag_ratio=1.5))
                self.play(*[circle.animate.set_color(WHITE) for circle in circles])
                self.wait(2)
                self.add_sound("voiceovers/TextGeneration1.mp3")
                self.wait(1.5)

            winner_idx = 0 
            winner_word = options[winner_idx][0]
            self.add_sound("voiceovers/beep.mp3")
            self.play(
                circles[winner_idx].animate.set_color(YELLOW).set_fill(YELLOW, opacity=0.3),
                arrows[winner_idx].animate.set_color(YELLOW),
                labels[winner_idx].animate.scale(1.2).set_color(YELLOW)
            )
            
            sentence.append(winner_word)
            new_sentence_str = " ".join(sentence)
            new_display = Text(new_sentence_str, font="Noto Sans", font_size=48).to_edge(UP, buff=1)
            self.add_sound("voiceovers/happy-coin.wav")
            self.play(
                Transform(display_text, new_display),
                FadeOut(circles), FadeOut(labels), FadeOut(arrows)
            )
            
            current_word = winner_word
            self.wait()
        self.add_sound("voiceovers/TextGeneration2.mp3")
        self.wait()
        self.add_sound("voiceovers/cute-sound.mp3")
        self.play(display_text.animate.set_color(GREEN).scale(1.2))
        self.wait(4)
class SlidingWindow_short(Scene):
    def construct(self):
        self.add_sound("voiceovers/SlidingWindow1.mp3")
        sentence = ["The", "quick", "brown", "fox", "jumps"]
        words = VGroup(*[Text(w) for w in sentence]).arrange(RIGHT, buff=0.5)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(words))
        self.wait(1)

        window = SurroundingRectangle(words[0:2], color=YELLOW, buff=0.2)
        window_label = Text("Trạng thái hiện tại (n=2)", font="Noto Sans", font_size=24, color=YELLOW).next_to(window, UP)
        self.add_sound("voiceovers/click.wav")
        self.play(Create(window), Write(window_label))
        self.wait(1)

        for i in range(len(words) - 2):
            target_word = words[i+2]
            
            arrow = CurvedArrow(window.get_bottom(), target_word.get_bottom() + DOWN*0.3, color=BLUE, angle=PI/2)
            prob_label = MathTex("P(Next | Window)").scale(0.6).next_to(arrow, DOWN)
            self.add_sound("voiceovers/send-message.mp3")
            self.play(Create(arrow), FadeIn(prob_label))
            self.play(Indicate(target_word, color=BLUE))
            self.play(FadeOut(arrow), FadeOut(prob_label))

            if i < len(words) - 3:
                next_window = SurroundingRectangle(words[i+1:i+3], color=YELLOW, buff=0.2)
                self.add_sound("voiceovers/click.wav")
                self.play(Transform(window, next_window))
                self.wait(0.5)

        self.play(FadeOut(window), FadeOut(window_label, words))
        self.wait()

        sentence = ["The", "Great", "Wall", "of", "China"]
        words = VGroup(*[Text(w) for w in sentence]).arrange(RIGHT, buff=0.8).shift(UP*1)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(words))
        self.wait(2)
        window = SurroundingRectangle(words[0:2], color=YELLOW)
        self.add_sound("voiceovers/click.wav")
        self.play(Create(window))
        self.add_sound("voiceovers/SlidingWindow.mp3")

        cloud_data = [
            ["Expectations", "Dane", "Gatsby"], # After "The Great"
            ["Is", "Stretches", "Was"],        # After "Great Wall"
            ["In", "And", "Built"]             # After "Wall of"
        ]

        for i in range(len(cloud_data)):
            cloud = VGroup()
            for j, alt_word in enumerate(cloud_data[i]):
                opacity = 1.0 - (j * 0.3)
                txt = Text(alt_word, font_size=20, color=BLUE, fill_opacity=opacity)
                txt.next_to(words[i+2], DOWN, buff=0.5 + (j*0.4))
                cloud.add(txt)
            self.add_sound("voiceovers/ui_pop_up.mp3")
            self.play(FadeIn(cloud, shift=UP*0.3), run_time=0.8)
            self.play(Indicate(words[i+2], color=YELLOW))
            self.wait(0.5)
            
            if i < len(cloud_data) - 1:
                next_window = SurroundingRectangle(words[i+1:i+3], color=YELLOW)
                self.add_sound("voiceovers/click.wav")
                self.play(
                    Transform(window, next_window),
                    FadeOut(cloud, shift=UP*0.3)
                )

        self.play(FadeOut(window), words.animate.set_color(GREEN))
        self.wait(3)
        self.play(FadeOut(*self.mobjects))
        self.wait()
        
        title = Text("Mô hình ngôn ngữ lớn", font="Noto Sans", font_size=42)
        title.to_edge(UP)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(title))
        self.add_sound("voiceovers/LLMScene.mp3")

        input_text = Text('"The cat sat on the"', font_size=28)
        input_box = SurroundingRectangle(input_text, buff=0.3, color=BLUE)
        input_group = VGroup(input_box, input_text)

        words = ["The", "cat", "sat", "on", "the"]
        token_boxes = VGroup(*[
            Rectangle(width=0.9, height=0.7).set_fill(BLUE, opacity=0.5)
            for _ in words
        ]).arrange(DOWN, buff=0.15)

        token_labels = VGroup(*[
            Text(word, font_size=20).move_to(token_boxes[i])
            for i, word in enumerate(words)
        ])

        tokens = VGroup(token_boxes, token_labels)

        transformer_group = get_chip_icon("LLM", PURPLE).scale(0.4)
        transformer = transformer_group[0]
        probs = BarChart(
            values=[0.1, 0.05, 0.6, 0.15, 0.1],
            bar_names=["mat", "dog", "floor", "chair", "roof"],
            y_range=[0, 0.7, 0.1],
            y_length=2.5,
            x_length=4,
        )

        prob_title = Text("Token tiếp theo", font="Noto Sans", font_size=24)
        prob_group = VGroup(prob_title, probs).arrange(DOWN, buff=0.3)

        output_text = Text('"floor"', font_size=28, color=GREEN)
        output_box = SurroundingRectangle(output_text, buff=0.3, color=GREEN)
        output_group = VGroup(output_box, output_text)

        pipeline = VGroup(
            # input_group,
            tokens,
            transformer_group,
            prob_group,
            output_group
        ).arrange(RIGHT, buff=1)

        pipeline.scale(0.85)
        pipeline.to_edge(DOWN, LARGE_BUFF)
        input_group.next_to(title, DOWN)

        arrows = VGroup(*[
            Arrow(
                pipeline[i].get_right(),
                pipeline[i + 1].get_left(),
                buff=0.2
            )
            for i in range(len(pipeline) - 1)
        ])
        self.add_sound("voiceovers/ui_pop_up.mp3")
        self.play(FadeIn(input_group))
        for token_box, token_label in zip(token_boxes, token_labels):
            self.add_sound("voiceovers/ui_pop_up.mp3")
            self.play(FadeIn(VGroup(token_box, token_label), target_position=input_group))
        self.add_sound("voiceovers/send-message.mp3")
        self.play(GrowArrow(arrows[0]), FadeIn(transformer_group))
        self.add_sound("voiceovers/send-message.mp3")
        self.play(GrowArrow(arrows[1]), FadeIn(prob_group))
        self.add_sound("voiceovers/send-message.mp3")
        self.play(GrowArrow(arrows[2]), FadeIn(output_group))
        self.wait(1)

        moving_tokens = VGroup()

        for box, label in zip(token_boxes, token_labels):
            token_copy = VGroup(
                box.copy().set_fill(YELLOW, opacity=0.8),
                label.copy()
            )
            moving_tokens.add(token_copy)

        for token in moving_tokens:
            self.add_sound("voiceovers/sword-swing.wav")
            self.play(token.animate.move_to(transformer.get_left()), run_time=0.4)

        self.play(
            transformer.animate.set_fill(PURPLE_E, opacity=0.9),
            run_time=0.5
        )
        self.play(
            transformer.animate.set_fill(PURPLE, opacity=0.5),
            run_time=0.5
        )

        for token in moving_tokens:
            self.add_sound("voiceovers/sword-swing.wav")
            self.play(
                token.animate.move_to(prob_group.get_left()),
                run_time=0.4
            )

        self.play(FadeOut(moving_tokens))

        self.play(probs.bars[2].animate.set_color(YELLOW))
        self.wait(1)
        self.add_sound("voiceovers/cute-sound.mp3")
        self.play(Indicate(output_group, color=GREEN))
        self.wait()
        self.play(FadeOut(pipeline, title, input_group, arrows))
        self.wait()
        self.add_sound("voiceovers/MarkovVsLLM.mp3")
        markov_title = Text("Mô hình Markov (bộ nhớ 1 bước)", font="Noto Sans", color=BLUE).scale(0.6)
        markov_title.shift(UP*2)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(markov_title))

        sentence1 = Text("The cat sat on the").scale(0.6)
        sentence1.next_to(markov_title, DOWN, aligned_edge=LEFT)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(sentence1))
        self.wait()

        highlight_last = SurroundingRectangle(sentence1[-3:], color=YELLOW)
        self.play(Create(highlight_last))
        self.add_sound("voiceovers/MarkovVsLLM1.mp3")

        explanation1 = Text("Chỉ dựa trên từ hiện tại: 'the'", font="Noto Sans").scale(0.5)
        explanation1.next_to(sentence1, DOWN, aligned_edge=LEFT)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(explanation1))
        self.wait(1)

        probs_markov = VGroup(
            Text("mat (0.4)").scale(0.5),
            Text("floor (0.3)").scale(0.5),
            Text("dog (0.2)").scale(0.5),
            Text("moon (0.1)").scale(0.5),
        ).arrange(DOWN, aligned_edge=LEFT)

        probs_markov.next_to(explanation1, DOWN)
        self.play(FadeIn(probs_markov, shift=RIGHT))
        self.wait(2)

        self.play(
            FadeOut(sentence1),
            FadeOut(highlight_last),
            FadeOut(explanation1),
            FadeOut(probs_markov),
            FadeOut(markov_title),
        )
        self.add_sound("voiceovers/LLM.mp3")
        llm_title = Text("LLM (Full Context Attention)", font="Noto Sans", color=GREEN).scale(0.6)
        llm_title.shift(UP*2)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(llm_title))

        sentence2 = Text("The cat sat on the").scale(0.6)
        sentence2.next_to(llm_title, DOWN, aligned_edge=LEFT)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(sentence2))
        self.wait()
        self.add_sound("voiceovers/LLM1.mp3")

        highlight_all = SurroundingRectangle(sentence2, color=YELLOW)
        self.play(Create(highlight_all))

        explanation2 = Text("Sử dụng toàn bộ ngữ cảnh câu", font="Noto Sans").scale(0.5)
        explanation2.next_to(sentence2, DOWN, aligned_edge=LEFT)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(explanation2))
        self.wait()

        probs_llm = VGroup(
            Text("mat (0.7)").scale(0.5),
            Text("floor (0.2)").scale(0.5),
            Text("dog (0.05)").scale(0.5),
            Text("moon (0.05)").scale(0.5),
        ).arrange(DOWN, aligned_edge=LEFT)

        probs_llm.next_to(explanation2, DOWN)
        for text_prob in probs_llm:
            self.play(FadeIn(text_prob, shift=RIGHT))
        self.wait()

        self.play(FadeOut(*self.mobjects))
        self.add_sound("voiceovers/LLM_last.mp3")
        chip_body, pins, label = get_chip_icon("LLM", PURPLE)

        self.play(Create(chip_body))
        self.play(LaggedStart(*[GrowFromCenter(pin) for pin in pins], lag_ratio=0.05))
        self.play(FadeIn(label))
        self.wait(2)

class MatChanProEndScreen(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/end-screen.mp3")
        formulas = [
            r"\int_a^b f(x)\,dx",
            r"e^{i\pi}+1=0",
            r"\frac{d}{dx}x^2=2x",
            r"\sum_{n=1}^{\infty}\frac{1}{n^2}",
            r"\lim_{x\to0}\frac{\sin x}{x}",
            r"\nabla \cdot \vec{F}"
        ]

        floating = VGroup()
        for _ in range(25):
            tex = MathTex(random.choice(formulas), font_size=30)
            tex.set_color(random.choice([BLUE, TEAL, PURPLE, GREEN]))
            tex.set_opacity(0.12)

            tex.move_to([
                random.uniform(-8, 8),
                random.uniform(-4.5, 4.5),
                0
            ])

            tex.add_updater(lambda m, dt: m.shift(UP * 0.25 * dt))
            floating.add(tex)

        self.add(floating)

        title = Text("Thanks for Watching!", font_size=64)
        title.set_color_by_gradient(TEAL, BLUE)
        title.to_edge(UP)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(title))
        self.wait(0.5)

        subscribe = RoundedRectangle(
            corner_radius=0.2,
            width=4,
            height=1.2,
            color=RED,
            fill_opacity=1
        )
        subscribe.next_to(title, DOWN, buff=1.5)

        button_text = Text("SUBSCRIBE", font_size=36, color=WHITE)
        button_group = VGroup(subscribe, button_text)

        button_text.move_to(subscribe.get_center())
        self.wait(15)

        self.play(FadeOut(VGroup(
            title,
            floating
        )), run_time=2)

        self.wait()
        
class MarkovThumbnailClean(Scene):
    def construct(self):
        robot = ImageMobject("assets/robot.png").scale(0.4).shift(3*LEFT + DOWN)
        sunny = SVGMobject("assets/sunny.svg").scale(0.6).shift(LEFT * 2 + UP)
        cloudy = SVGMobject("assets/cloudy.svg").scale(0.6).shift(RIGHT * 2 + UP)
        rainy = SVGMobject("assets/rainy.svg").scale(0.6).shift(DOWN * 1.5)
        weathers = VGroup(sunny, cloudy, rainy).to_edge(RIGHT, LARGE_BUFF)

        arrow_sc = CurvedArrow(
            sunny.get_corner(UR),
            cloudy.get_corner(UL),
            angle=-PI/4
        )
        arrow_cr = CurvedArrow(
            cloudy.get_bottom(),
            rainy.get_corner(UR),
            angle=-PI/4
        )
        arrow_rs = CurvedArrow(
            rainy.get_corner(UL),
            sunny.get_bottom(),
            angle=-PI/4
        )

        title = Text("MARKOV CHAINS", weight=BOLD)
        title.scale(1.8)
        title.set_color(YELLOW)
        title.to_edge(UP)

        self.add(weathers, arrow_sc, arrow_rs, arrow_cr, title, robot)