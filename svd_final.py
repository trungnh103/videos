from manim import *
import random
from manim import *
from PIL import Image
import numpy as np
import os

def transform(v, matrix, threeD=False):
            end = v.get_end()        
            if threeD:
                res = matrix @ end
            else:
                res = matrix @ end[:2]
            v_new = np.array([res[0], res[1], 0])
            return Vector(v_new, color=v.get_color())
def get_youtube_video(color=RED_E):
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
            fill_color=color,
            color=color,
            fill_opacity=1
        )

        play_button.move_to(screen.get_center())

        return VGroup(screen, play_button)
def create_grid():
    window_height = 4
    window_width = 6
    window_rect = Rectangle(
            width=window_width,
            height=window_height,
            color=WHITE
        ).set_z_index(12)
    big_rect = Rectangle(width=20, height=20, fill_color=BLACK, fill_opacity=1, stroke_width=0)
    hole = Rectangle(
            width=window_width,
            height=window_height
        )
    wall_with_hole = Difference(big_rect, hole, fill_color=BLACK, fill_opacity=1, stroke_width=0).set_z_index(10)
    
    grid = NumberPlane(
        x_range=[-6, 6, 1],
        y_range=[-4, 4, 1],
        background_line_style={
            "stroke_color": BLUE_E,
            "stroke_width": 1,
            "stroke_opacity": 0.5,
        },
    ).set_stroke(opacity=0.3)
    points = VGroup()
    for x in np.arange(-6, 7, 1):
        for y in np.arange(-4, 5, 1):

            dot = Dot(
                point=[x, y, 0],
                radius=0.05,
                color=YELLOW
            )

            dot.original_position = np.array([x, y, 0])

            points.add(dot)    
    return window_rect, wall_with_hole, grid, points
def floatingMatrices(scene):
        matrices = VGroup(
            Matrix([[1, 2], [3, 4]]),
            Matrix([[5, 6], [7, 8]]),
            Matrix([[9, 1], [2, 3]]),
            Matrix([[4, 5], [6, 7]]),
            Matrix([[8, 9], [1, 2]])
        )

        for m in matrices:
            m.scale(0.8)
            m.move_to([
                random.uniform(-5, 5),
                random.uniform(-3, 3),
                0
            ])
        scene.add_sound("voiceovers/game-start.mp3")
        scene.play(LaggedStart(*[FadeIn(m) for m in matrices], lag_ratio=0.2))

        for _ in range(3):
            animations = []
            for m in matrices:
                new_pos = [
                    random.uniform(-5, 5),
                    random.uniform(-3, 3),
                    0
                ]
                animations.append(m.animate.move_to(new_pos))
            scene.add_sound("voiceovers/whoosh407576.mp3")
            scene.play(*animations, run_time=.5)
        scene.play(FadeOut(matrices))
def heatmapSweep(scene):
        rows, cols = 6, 6
        cell_size = 0.9

        values = np.arange(rows * cols).reshape(rows, cols)

        grid = VGroup()
        labels = VGroup()

        vmin = values.min()
        vmax = values.max()

        def heat_color(v):
            alpha = (v - vmin) / (vmax - vmin)
            return interpolate_color(BLUE, RED, alpha)

        for r in range(rows):
            row = VGroup()
            label_row = VGroup()

            for c in range(cols):
                val = values[r, c]

                square = Square(side_length=cell_size)
                square.set_fill(heat_color(val), opacity=0.8)
                square.set_stroke(WHITE, width=1)

                square.move_to([c * cell_size, -r * cell_size, 0])

                txt = Text(str(val)).scale(0.35)
                txt.move_to(square.get_center())

                row.add(square)
                label_row.add(txt)

            grid.add(row)
            labels.add(label_row)

        grid.center()
        labels.center()

        scene.play(FadeIn(grid), Write(labels))
        scene.wait(2)
        scene.play(FadeOut(grid, labels))
def get_chip_icon(label="LLM", body_color=BLUE_E):
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

        for i in range(1, num_pins_per_side + 1):
            pin = Rectangle(height=pin_length, width=pin_width)
            pin.move_to(
                chip_body.get_top()
                + UP * (pin_length / 2)
                + LEFT * (chip_body.width / 2 - i * spacing)
            )
            pins.add(pin)

        for i in range(1, num_pins_per_side + 1):
            pin = Rectangle(height=pin_length, width=pin_width)
            pin.move_to(
                chip_body.get_bottom()
                + DOWN * (pin_length / 2)
                + LEFT * (chip_body.width / 2 - i * spacing)
            )
            pins.add(pin)

        for i in range(1, num_pins_per_side + 1):
            pin = Rectangle(height=pin_width, width=pin_length)
            pin.move_to(
                chip_body.get_left()
                + LEFT * (pin_length / 2)
                + DOWN * (chip_body.height / 2 - i * spacing)
            )
            pins.add(pin)

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

        chip_label = Text(label, font_size=72, weight=BOLD)
        chip_label.move_to(chip_body.get_center())
        chip_label.set_color(WHITE)
        return VGroup(chip_body, pins, chip_label)
def create_grid_double():
    window_height = 4
    window_width = 6
    window_rect_left = Rectangle(
            width=window_width,
            height=window_height,
            color=WHITE
        ).shift(3.5*LEFT).set_z_index(12)
    window_rect_right = Rectangle(
            width=window_width,
            height=window_height,
            color=WHITE
        ).shift(3.5*RIGHT).set_z_index(12)
    big_rect = Rectangle(width=20, height=20, fill_color=BLACK, fill_opacity=1, stroke_width=0)
    hole = Union(
        Rectangle(
            width=window_width,
            height=window_height
        ).shift(3.5*LEFT),
        Rectangle(
            width=window_width,
            height=window_height
        ).shift(3.5*RIGHT))
    wall_with_hole = Difference(big_rect, hole, fill_color=BLACK, fill_opacity=1, stroke_width=0).set_z_index(10)
    
    grid_left = NumberPlane(
        x_range=[-3, 3, 1],
        y_range=[-2, 2, 1],
        background_line_style={
            "stroke_color": BLUE_E,
            "stroke_width": 1,
            "stroke_opacity": 0.5,
        },
    ).set_stroke(opacity=0.3).move_to(window_rect_left.get_center())
    grid_right = NumberPlane(
        x_range=[-3, 3, 1],
        y_range=[-2, 2, 1],
        background_line_style={
            "stroke_color": BLUE_E,
            "stroke_width": 1,
            "stroke_opacity": 0.5,
        },
    ).set_stroke(opacity=0.3).move_to(window_rect_right.get_center())
    return window_rect_left, window_rect_right, wall_with_hole, grid_left, grid_right
def animate_points_matrix(points, matrix, back_to_origin=0):
    positions = []
    for dot in points:
        positions.append(dot.get_center() + back_to_origin*LEFT)

    return [
            *[
                dot.animate.move_to(
                    np.append(matrix @ pos[:2], 0)
                ).shift(back_to_origin*RIGHT)
                for dot, pos in zip(points, positions)
            ]]
class Intro(Scene):
    def construct(self):
        self.add_sound("voiceovers/svd_intro.mp3")
        ai = get_chip_icon("AI", PURPLE).scale(0.4)
        self.add_sound("voiceovers/game-start.mp3")
        self.play(Create(ai))
        self.wait()
        self.play(FadeOut(ai))
        self.neuralNetMatrix()
        floatingMatrices(self)
        heatmapSweep(self)
        self.largeDataFrame()
        self.svdIntro()
        self.wait(3)
    def neuralNetMatrix(self):
        input_layer = VGroup(*[Circle(radius=0.3, color=BLUE) for _ in range(3)]).arrange(DOWN, buff=0.5)
        output_layer = VGroup(*[Circle(radius=0.3, color=GREEN) for _ in range(2)]).arrange(DOWN, buff=0.8)
        layers = VGroup(input_layer, output_layer).arrange(RIGHT, buff=3)

        input_labels = MathTex("x_1", "x_2", "x_3").scale(0.8)
        for i, label in enumerate(input_labels):
            label.move_to(input_layer[i])
        
        output_labels = MathTex("y_1", "y_2").scale(0.8)
        for i, label in enumerate(output_labels):
            label.move_to(output_layer[i])

        connections = VGroup()
        for i_node in input_layer:
            for o_node in output_layer:
                line = Line(i_node.get_right(), o_node.get_left(), stroke_width=2, color=GRAY)
                connections.add(line)

        self.play(Create(input_layer), Write(input_labels))
        self.play(Create(output_layer), Write(output_labels))
        self.play(Create(connections))
        self.wait()

        matrix_eq = MathTex(
            r"\begin{bmatrix} w_{11} & w_{12} & w_{13} \\ w_{21} & w_{22} & w_{23} \end{bmatrix}",
            r"\begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix}",
            r"=",
            r"\begin{bmatrix} y_1 \\ y_2 \end{bmatrix}"
        ).to_edge(DOWN)

        self.play(
            connections.animate.set_stroke(opacity=0.2),
            Write(matrix_eq)
        )
        
        rect = SurroundingRectangle(matrix_eq[0][1:10], color=YELLOW) 
        self.add_sound("voiceovers/click.wav")
        self.play(Create(rect), output_layer[0].animate.set_color(YELLOW))
        self.wait()
        self.play(*[FadeOut(mob) for mob in self.mobjects])
    def largeDataFrame(self):
        data = [
            ["Name", "Age", "Score", "City"],
            ["Alice", "24", "88", "New York"],
            ["Bob", "27", "92", "London"],
            ["Charlie", "22", "79", "Paris"],
            ["David", "29", "85", "Tokyo"],
            ["Eva", "26", "91", "Berlin"],
            ["Frank", "23", "76", "Toronto"],
            ["Grace", "28", "89", "Sydney"],
            ["Hannah", "25", "94", "Rome"],
            ["Ivan", "30", "82", "Moscow"],
            ["Julia", "21", "87", "Madrid"],
        ]
        table = Table(
            data,
            include_outer_lines=True,
            line_config={"stroke_color": WHITE, "stroke_width": 2},
        )
        table.scale(0.5)
        header_colors = [BLUE, GREEN, RED, PURPLE]
        header_bg = VGroup()
        for j in range(len(data[0])):
            cell = table.get_cell((1, j+1))
            rect = Rectangle(
                width=cell.width,
                height=cell.height,
                fill_color=header_colors[j],
                fill_opacity=1,
                stroke_color=WHITE,
                stroke_width=2,
            )
            rect.move_to(cell.get_center())
            header_bg.add(rect)
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(header_bg, table))
        for j in range(len(data[0])):
            table.get_entries((1, j+1)).set_color(WHITE)
        self.wait()
        self.play(FadeOut(header_bg, table))
    def svdIntro(self):
        letters = VGroup(*[Text(c) for c in "SVD"])
        letters.arrange(RIGHT, buff=1.5)

        boxes = VGroup(*[
            Square(side_length=1.5, color=TEAL).move_to(letter)
            for letter in letters
        ])
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(LaggedStart(*[FadeIn(box) for box in boxes], lag_ratio=0.3))
        self.wait(0.3)
        self.add_sound("voiceovers/click.wav")
        self.play(LaggedStart(*[FadeIn(letter) for letter in letters], lag_ratio=0.4))
        self.wait(0.8)

        svd_group = VGroup(*[VGroup(b, l) for b, l in zip(boxes, letters)])
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(
            svd_group.animate.scale(0.7).to_edge(UP),
        )
        full_text = Text("Singular Value Decomposition").scale(0.8).next_to(svd_group, DOWN)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(full_text))
        self.wait(4)

        explanation = VGroup(
            Text("• Cải thiện hiệu quả lưu trữ", font="Noto Sans", color=GREEN, font_size=26),
            Text("• Tăng tốc quá trình huấn luyện mô hình", font="Noto Sans", color=YELLOW, font_size=26),
            Text("• Nâng cao khả năng giải thích", font="Noto Sans", color=PURPLE, font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT)
           
        for e in explanation:
            self.add_sound("voiceovers/ding-402325.mp3")
            self.play(FadeIn(e, shift=UP))
            self.wait(.5)
        self.wait()
        self.play(LaggedStart(*[Flash(letter) for letter in letters], lag_ratio=0.4))
        self.wait(3)
def scaleArrows():
    h_arrow = DoubleArrow(
        start=LEFT*0.8,
        end=RIGHT*0.8
    ).shift(LEFT * .5)

    v_arrow = DoubleArrow(
        start=DOWN*0.8,
        end=UP*0.8
    ).shift(RIGHT * .5)
    return VGroup(h_arrow, v_arrow)
def rotateArrow():
    start = DOWN*.2
    end = RIGHT*.2
    return CurvedArrow(
        start_point=start,
        end_point=end,
        angle=-PI*1.5
    )
class MatrixTypesReview(Scene):
    def pastVideo(self):
        video_rect = Rectangle(
            width=6,
            height=3.5,
            color=WHITE
        )
        video_rect.set_fill(BLACK, opacity=0.3)
        video_rect.move_to(ORIGIN)
        thumbnail = ImageMobject("assets/thumbnail.png")
        thumbnail.scale_to_fit_width(video_rect.width)
        thumbnail.scale_to_fit_height(video_rect.height)
        thumbnail.move_to(video_rect.get_center())
        play_button = Triangle()
        play_button.set_fill(WHITE, opacity=0.9)
        play_button.set_stroke(width=0)
        play_button.scale(0.4)
        play_button.rotate(-PI / 2)
        play_button.move_to(video_rect.get_center())
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(Create(video_rect))
        self.play(FadeIn(thumbnail))
        self.play(FadeIn(play_button, scale=0.5))
        self.wait()
        self.add_sound("voiceovers/click.wav")
        self.play(FadeOut(play_button), video_rect.animate.set_fill(BLACK, opacity=0.8))
        self.wait()
        self.play(*[FadeOut(mob) for mob in self.mobjects])
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/MatrixTypesReview.mp3")
        self.pastVideo()
        title_diag = Text("1. Ma trận chéo: Co giãn thuần túy", font="Noto Sans"
                          ).add_background_rectangle().scale(0.7).to_edge(UP)
        
        grid = NumberPlane(background_line_style={"stroke_opacity": 0.3}).set_stroke(opacity=0.3)
        circle = Circle(radius=1, color=TEAL).set_fill(TEAL, opacity=0.3)
        
        i_hat = Vector([1, 0], color=YELLOW)
        j_hat = Vector([0, 1], color=PINK)
        
        group_diag = VGroup(grid, circle)
        
        matrix_diag_tex = MathTex(r"\Lambda = ")
        matrix_diag = Matrix([[3, 0], [0, 2]])
        matrix_diag_group = VGroup(matrix_diag_tex, matrix_diag).arrange(RIGHT)
        
        bg_rect_diag = BackgroundRectangle(matrix_diag_group, color=BLACK, fill_opacity=0.85, buff=0.2)
        diag_overlay = VGroup(bg_rect_diag, matrix_diag_group)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(title_diag), FadeIn(diag_overlay))
        entries = matrix_diag.get_entries()
        entries[0].set_color(YELLOW)
        entries[3].set_color(PINK)
        start = entries[0].get_center()   
        end = entries[3].get_center()     
        diag_line = Line(start, end)
        diag_line.set_stroke(color=BLUE, width=12)
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(Create(diag_line))
        self.wait(3)
        self.play(FadeOut(diag_line))
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(diag_overlay.animate.to_edge(DOWN), 
                  Create(grid), Create(circle))
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(GrowArrow(i_hat), GrowArrow(j_hat))
        self.wait()
        L_matrix = [[3, 0], 
                    [0, 2]]
        i_hat_new = transform(i_hat, L_matrix)
        j_hat_new = transform(j_hat, L_matrix)
        self.add_sound("voiceovers/shooting-star.mp3")
        self.play(
            group_diag.animate.apply_matrix(L_matrix),
            Transform(i_hat, i_hat_new),
            Transform(j_hat, j_hat_new),
            run_time=5,
            rate_func=smooth
        )
        self.wait(2)
        self.play(FadeOut(group_diag, j_hat, i_hat), FadeOut(title_diag), FadeOut(diag_overlay))

        title_ortho = Text("2. Ma trận trực giao: Phép quay cứng", font="Noto Sans"
                           ).add_background_rectangle().scale(0.7).to_edge(UP)
        grid_2 = NumberPlane(background_line_style={"stroke_opacity": 0.3}).set_stroke(opacity=0.3)
        circle_2 = Circle(radius=1, color=TEAL).set_fill(TEAL, opacity=0.3)

        i_hat_2 = Vector([1, 0], color=YELLOW)
        j_hat_2 = Vector([0, 1], color=PINK)
        
        group_ortho = VGroup(grid_2, circle_2, i_hat_2, j_hat_2)

        matrix_ortho_tex = MathTex(r"Q = ")
        matrix_ortho = Matrix([[r"\cos(45^\circ)", r"-\sin(45^\circ)"], 
                               [r"\sin(45^\circ)", r"\cos(45^\circ)"]])
        entries = matrix_ortho.get_entries()
        VGroup(entries[0], entries[2]).scale(0.7).shift(0.25*LEFT)
        VGroup(entries[1], entries[3]).scale(0.7).shift(0.25*RIGHT)
        matrix_ortho_group = VGroup(matrix_ortho_tex, matrix_ortho).arrange(RIGHT)
        
        bg_rect_ortho = BackgroundRectangle(matrix_ortho_group, color=BLACK, fill_opacity=0.85, buff=0.2)
        ortho_overlay = VGroup(bg_rect_ortho, matrix_ortho_group)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(title_ortho), FadeIn(ortho_overlay))
        self.wait(4)
        eq = MathTex(
            r"Q^T = Q^{-1}",
            font_size=72
        )
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(FadeIn(eq), ortho_overlay.animate.to_edge(DOWN))
        self.wait()
        box = SurroundingRectangle(eq, color=BLUE)
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(Create(box))
        self.wait()
        self.play(FadeOut(eq, box))
        self.add_sound("voiceovers/click.wav")
        self.play(Create(grid_2), Create(circle_2))
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(GrowArrow(i_hat_2), GrowArrow(j_hat_2))
        self.wait()
        angle = 45 * DEGREES
        Q_matrix = [[np.cos(angle), -np.sin(angle)], 
                    [np.sin(angle),  np.cos(angle)]]
        self.add_sound("voiceovers/shooting-star.mp3")
        self.play(
            group_ortho.animate.apply_matrix(Q_matrix),
            run_time=5,
            rate_func=smooth
        )
        self.wait(2)
class SVDFormulaBreakdown(Scene):
    def transformMachine(self):
        matrix = [[3, 1], [1, 2]]
        matrix_tex = MathTex(
            "A = \\begin{bmatrix} 3 & 1 \\\\ 1 & 2 \\end{bmatrix}"
        ).to_edge(UP).set_z_index(12)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(matrix_tex))
        window_rect, wall_with_hole, grid, points = create_grid()
        self.play(FadeIn(wall_with_hole))
        self.add_sound("voiceovers/click.wav")
        self.play(Create(window_rect))
        self.play(Create(grid), FadeIn(points))
        
        anims = animate_points_matrix(points, matrix) 
        self.add_sound("voiceovers/shooting-star.mp3")
        self.play(
            grid.animate.apply_matrix(matrix),
            *anims,
            run_time=2,
            rate_func=linear
        )
        self.wait()
        self.play(FadeOut(points, grid))
        self.play(FadeOut(matrix_tex, window_rect, wall_with_hole))
    
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/SVDFormulaBreakdown.mp3")
        self.transformMachine()
        matrix = MathTex("A", font_size=80)
        equation = MathTex("A", "=", "U", r"\Sigma", "V^T", font_size=80)
        
        equation.set_color_by_tex("U", BLUE)
        equation.set_color_by_tex(r"\Sigma", YELLOW)
        equation.set_color_by_tex("V^T", GREEN)

        mat_A = Matrix(
            [
                ["a_{11}", "a_{12}", r"\dots", "a_{1n}"],
                ["a_{21}", "a_{22}", r"\dots", "a_{2n}"],
                [r"\vdots", r"\vdots", r"\ddots", r"\vdots"],
                ["a_{m1}", "a_{m2}", r"\dots", "a_{mn}"]
            ],
            h_buff=1.3,
            v_buff=0.8
        )
        for element in mat_A.get_entries():
            element.set_font_size(32)
        eq = MathTex("=", font_size=60)
        mat_U = MathTex(
            r"\begin{bmatrix} "
            r"| & & | \\ "
            r"\mathbf{u}_1 & \dots & \mathbf{u}_m \\ "
            r"| & & | "
            r"\end{bmatrix}", 
            font_size=42, color=BLUE
        )

        mat_Sigma = MathTex(
            r"\begin{bmatrix} "
            r"\sigma_1 & & \\ "
            r"& \ddots & \\ "
            r"& & \sigma_n "
            r"\end{bmatrix}", 
            font_size=42, color=YELLOW
        )

        mat_VT = MathTex(
            r"\begin{bmatrix} "
            r"\text{---} & \mathbf{v}_1^T & \text{---} \\ "
            r" & \vdots & \\ "
            r"\text{---} & \mathbf{v}_n^T & \text{---} "
            r"\end{bmatrix}", 
            font_size=42, color=GREEN
        )

        full_equation = VGroup(mat_A, eq, mat_U, mat_Sigma, mat_VT).arrange(RIGHT, buff=0.4)
        full_equation.scale(0.75).center()
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(mat_A))
        self.wait()
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(matrix))
        self.wait(4)
        self.add_sound("voiceovers/correct_answer_toy.mp3")
        self.play(FadeOut(mat_A), ReplacementTransform(matrix, equation), run_time=2)
        self.wait(2)
        self.play(LaggedStart(*[Indicate(equation[i], color=equation[i].get_color()) for i in (2,3,4)], lag_ratio=0.5))
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(equation.animate.to_edge(UP))
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(ReplacementTransform(equation[4].copy(), mat_VT), run_time=1.5)
        self.wait(4)
        vt_explain = Text("Vectơ kỳ dị phải", font="Noto Sans",
                          color=mat_VT.get_color()).scale(0.45).next_to(mat_VT, DOWN)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(vt_explain))
        self.wait(3)
        rotateArrow_vt = rotateArrow().next_to(mat_VT, DOWN)
        self.add_sound("voiceovers/click.wav")
        self.play(ReplacementTransform(vt_explain, rotateArrow_vt))
        self.wait(4)
        self.play(
            Rotate(rotateArrow_vt, angle=2*PI, rate_func=linear),
            run_time=3
            )
        self.wait()
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(ReplacementTransform(equation[3].copy(), mat_Sigma), run_time=1.5)
        self.wait(4)
        sigma_explain = Text("Giá trị kỳ dị", font="Noto Sans",
                          color=mat_Sigma.get_color()).scale(0.45).next_to(mat_Sigma, DOWN)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(sigma_explain))
        self.wait(4)
        descending = Tex(
            r"$\sigma_1 \geq \sigma_2 \geq \sigma_3 \geq \dots \geq 0$"
        ).next_to(sigma_explain, DOWN, buff=1)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(descending))
        self.wait(3)
        scaleArrows_sigma = scaleArrows().next_to(mat_Sigma, DOWN)
        self.add_sound("voiceovers/click.wav")
        self.play(ReplacementTransform(VGroup(sigma_explain, descending), scaleArrows_sigma))
        self.wait(2)
        self.play(LaggedStart(*[Indicate(arrow, color=mat_Sigma.get_color()) for arrow in scaleArrows_sigma], lag_ratio=1))
        self.wait(4)
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(ReplacementTransform(equation[2].copy(), mat_U), run_time=1.5)
        self.wait(4)
        u_explain = Text("Vectơ kỳ dị trái", font="Noto Sans",
                          color=mat_U.get_color()).scale(0.45).next_to(mat_U, DOWN)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(u_explain))
        self.wait()
        rotateArrow_u = rotateArrow().next_to(mat_U, DOWN)
        self.add_sound("voiceovers/click.wav")
        self.play(ReplacementTransform(u_explain, rotateArrow_u))
        self.wait()
        self.play(
            Rotate(rotateArrow_u, angle=-2*PI, rate_func=linear),
            run_time=3
            )
        self.wait(2)
        self.add_sound("voiceovers/correct_answer_toy.mp3")
        self.play(
            ReplacementTransform(equation[0].copy(), mat_A),
            Write(eq)
        )

        self.wait(3)
class GeometricIntuition(ZoomedScene):
    def glow_circle(self, radius, color):
        glow = Circle(radius=radius*1.6)
        glow.set_fill(color, opacity=0.15)
        glow.set_stroke(color, width=8, opacity=0.4)

        core = Circle(radius=radius)
        core.set_fill(color, 1)
        core.set_stroke(WHITE, 1)

        return VGroup(glow, core)
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/apply_A.mp3")
        A = np.array([[3, 1], 
                      [0, 2]])

        U, S, VT = np.linalg.svd(A)
        Sigma = np.array([
            [S[0], 0],
            [0, S[1]]
        ])
        window_rect_left, window_rect_right, wall_with_hole, grid_left, grid_right = create_grid_double()
        self.add_sound("voiceovers/click.wav")
        self.play(self.camera.frame.animate.move_to(window_rect_left.get_center()),
                  FadeIn(wall_with_hole, window_rect_left, grid_left))
        self.wait(3)
        unit_circle_left = Circle(radius=.5, color=WHITE, stroke_width=2)
        V = VT.T 
        v1_vec = V[:, 0]
        v2_vec = V[:, 1]
        points_left = VGroup()

        singular_positions = [
            np.array([v1_vec[0]/2, v1_vec[1]/2, 0]),
            np.array([v2_vec[0]/2, v2_vec[1]/2, 0]),
            np.array([-v1_vec[0]/2, -v1_vec[1]/2, 0]),
            np.array([-v2_vec[0]/2, -v2_vec[1]/2, 0])
        ]

        colors = [BLUE, GREEN, ORANGE, PURPLE]

        for c, col in zip(singular_positions, colors):
            point = self.glow_circle(radius=0.08, color=col).move_to(c)
            points_left.add(point)
        VGroup(unit_circle_left, points_left).move_to(window_rect_left.get_center())
        unit_circle_right = unit_circle_left.copy().move_to(window_rect_right.get_center())
        points_right = points_left.copy().move_to(window_rect_right.get_center())
        self.add_sound("voiceovers/zipper-zip.mp3")
        self.play(Create(unit_circle_left))
        self.add_sound("voiceovers/nomagician-successfinish.mp3")
        self.play(LaggedStart(*[FadeIn(p) for p in points_left], lag_ratio=0.5))
        self.wait(.5)
        self.add_sound("voiceovers/pop-268648.mp3")
        label_A = Text("Áp dụng A", font="Noto Sans").set_z_index(12).next_to(window_rect_left, UP)
        self.play(FadeIn(label_A))
        self.wait(3)
        anims = animate_points_matrix(points_left, A, back_to_origin=-3.5)
        self.add_sound("voiceovers/shooting-star.mp3")
        self.play(*anims,
                  unit_circle_left.animate.center().apply_matrix(A).move_to(window_rect_left.get_center()),
                  run_time=3)
        self.add_sound("voiceovers/3_steps.mp3")
        self.wait(.5)
        self.add_sound("voiceovers/click.wav")
        self.play(Create(window_rect_right), FadeIn(grid_right),
                  self.camera.frame.animate.move_to(ORIGIN).set(width=14))
        self.wait()
        self.add_sound("voiceovers/zipper-zip.mp3")
        self.play(Create(unit_circle_right))
        self.add_sound("voiceovers/nomagician-successfinish.mp3")
        self.play(LaggedStart(*[FadeIn(p) for p in points_right], lag_ratio=0.5))
        self.wait()
        label1 = Text("Áp dụng Vᵀ (xoay)", font="Noto Sans").set_z_index(12).next_to(window_rect_right, UP)
        self.add_sound("voiceovers/apply_vt.mp3")
        anims = animate_points_matrix(points_right, VT, back_to_origin=3.5)
        self.add_sound("voiceovers/shooting-star.mp3")
        self.play(
            *anims, FadeIn(label1),
            unit_circle_right.animate.center().apply_matrix(VT).move_to(window_rect_right.get_center()),
            run_time=3)
        self.wait()
        label2 = Text("Áp dụng Σ (kéo giãn)", font="Noto Sans").set_z_index(12).next_to(window_rect_right, UP)
        self.add_sound("voiceovers/apply_sigma.mp3")
        anims = animate_points_matrix(points_right, Sigma, back_to_origin=3.5)
        self.add_sound("voiceovers/shooting-star.mp3")
        self.play(
            *anims, Transform(label1, label2),
            unit_circle_right.animate.center().apply_matrix(Sigma).move_to(window_rect_right.get_center()),
            run_time=3)
        self.wait(4)
        label3 = Text("Áp dụng U (xoay)", font="Noto Sans").set_z_index(12).next_to(window_rect_right, UP)
        self.add_sound("voiceovers/apply_u.mp3")
        anims = animate_points_matrix(points_right, U, back_to_origin=3.5)
        self.add_sound("voiceovers/shooting-star.mp3")
        self.play(
            *anims, Transform(label1, label3),
            unit_circle_right.animate.center().apply_matrix(U).move_to(window_rect_right.get_center()),
            run_time=3)
        self.wait(.5)
        final_text = Text("A = U Σ Vᵀ", font="Noto Sans").set_z_index(12).next_to(window_rect_right, UP)
        self.add_sound("voiceovers/correct_answer_toy.mp3")
        self.play(Transform(label1, final_text))
        self.wait(.5)
        self.add_sound("voiceovers/rotate_stretch_rotate.mp3")
        self.play(Indicate(label1))
        self.wait(.5)
        
        final_text = Text("Quay → Kéo giãn → Quay", font="Noto Sans",
                          ).scale(0.6).set_z_index(12).to_edge(DOWN)
        arrows = VGroup(rotateArrow(), scaleArrows(), rotateArrow()
                        ).scale(0.6).set_z_index(12).arrange(RIGHT, buff=1).next_to(final_text, UP)
        self.add_sound("voiceovers/bright-notification.mp3")
        self.play(Write(final_text), FadeIn(arrows), run_time=3)
        self.wait(3)
    
class ImageToMatrix(MovingCameraScene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/image_compression.mp3")
        title = Text("Nén ảnh", font="Noto Sans", color=YELLOW, weight=BOLD)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(title))
        self.wait()
        self.play(Unwrite(title))
        self.add_sound("voiceovers/ImageToMatrix.mp3")
        self.digitalImage()
        self.imageCompression()
    def digitalImage(self):
        matrix_size = 12 
        image_path = "assets/lenna_color.png"  
        
        if os.path.exists(image_path):
            original_img = ImageMobject(image_path)
            img_pil = Image.open(image_path).convert("L")
            img_resizing = img_pil.resize((matrix_size, matrix_size))
            data = np.array(img_resizing)
        else:
            print(f"⚠️ Image '{image_path}' not found. Using fallback data.")
            original_img = ImageMobject(np.uint8(np.random.rand(100, 100, 3) * 255))
            data = np.zeros((matrix_size, matrix_size))
            center = matrix_size / 2 - 0.5
            for i in range(matrix_size):
                for j in range(matrix_size):
                    dist = np.sqrt((i - center)**2 + (j - center)**2)
                    val = 255 * np.exp(-dist**2 / 12)
                    data[i, j] = min(max(int(val), 0), 255)

        original_img.height = 3.0 # Set a reasonable starting size
        original_img.move_to(ORIGIN)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(original_img))
        self.wait()

        squares_2d = []
        all_squares = VGroup()
        
        for i in range(matrix_size):
            row_list = []
            for j in range(matrix_size):
                val = data[i, j]
                color = rgb_to_color((val/255, val/255, val/255))
                
                sq = Square(
                    side_length=0.2, 
                    stroke_width=0, 
                    fill_opacity=1, 
                    fill_color=color
                )
                row_list.append(sq)
                all_squares.add(sq)
            squares_2d.append(row_list)
        
        all_squares.arrange_in_grid(rows=matrix_size, cols=matrix_size, buff=0)
        all_squares.replace(original_img)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(
            FadeOut(original_img),
            FadeIn(all_squares),
            run_time=1.5
        )
        self.wait()
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(
            all_squares.animate.scale(2.0),
            run_time=2
        )
        self.wait()
        
        self.play(
            all_squares.animate.set_stroke(color=GRAY, width=1),
            run_time=1.5
        )
        self.wait()
        
        all_numbers = VGroup()
        for i in range(matrix_size):
            for j in range(matrix_size):
                val = int(data[i, j])
                text_color = BLACK if val > 128 else WHITE
                
                num = Text(str(val), font_size=24, color=text_color)
                num.scale_to_fit_height(all_squares[0].height * 0.4) # Dynamic scaling
                num.move_to(squares_2d[i][j].get_center())
                
                all_numbers.add(num)
        self.add_sound("voiceovers/game-start.mp3")
        self.play(FadeIn(all_numbers, lag_ratio=0.01), run_time=2.5)
        self.wait(1.5)

        def create_brackets(mobject):
            ul, dl, ur, dr = mobject.get_corner(UL), mobject.get_corner(DL), mobject.get_corner(UR), mobject.get_corner(DR)
            buff, width = 0.2, 0.3
            
            left_bracket = VGroup(
                Line(ul + LEFT * buff, ul + LEFT * buff + RIGHT * width),
                Line(ul + LEFT * buff, dl + LEFT * buff),
                Line(dl + LEFT * buff, dl + LEFT * buff + RIGHT * width)
            ).set_color(WHITE).set_stroke(width=4)
            
            right_bracket = VGroup(
                Line(ur + RIGHT * buff, ur + RIGHT * buff + LEFT * width),
                Line(ur + RIGHT * buff, dr + RIGHT * buff),
                Line(dr + RIGHT * buff, dr + RIGHT * buff + LEFT * width)
            ).set_color(WHITE).set_stroke(width=4)
            
            return left_bracket, right_bracket

        left_bracket, right_bracket = create_brackets(all_squares)
        self.add_sound("voiceovers/correct_answer_toy.mp3")
        self.play(
            all_squares.animate.set_fill(opacity=0).set_stroke(opacity=0),
            all_numbers.animate.set_color(WHITE),
            Create(left_bracket),
            Create(right_bracket),
            run_time=2
        )
        self.wait()
        self.play(FadeOut(left_bracket, right_bracket, all_numbers))
    def imageCompression(self):
        img = Image.open("assets/lenna_color.png").convert("RGB")
        img_np = np.array(img) / 255.0  # normalize

        R = img_np[:, :, 0]
        G = img_np[:, :, 1]
        B = img_np[:, :, 2]

        def compute_svd(channel):
            U, S, Vt = np.linalg.svd(channel, full_matrices=False)
            return U, S, Vt

        R_svd = compute_svd(R)
        G_svd = compute_svd(G)
        B_svd = compute_svd(B)

        def reconstruct(rank):
            def rebuild(U, S, Vt):
                return (U[:, :rank] @ np.diag(S[:rank]) @ Vt[:rank, :])

            R_rec = rebuild(*R_svd)
            G_rec = rebuild(*G_svd)
            B_rec = rebuild(*B_svd)

            img_rec = np.stack([R_rec, G_rec, B_rec], axis=2)
            img_rec = np.clip(img_rec, 0, 1)
            return (img_rec * 255).astype(np.uint8)

        ranks = [1, 10, 100]
        recon_images = [reconstruct(r) for r in ranks]

        def to_manim_image(np_img):
            pil_img = Image.fromarray(np_img)
            return ImageMobject(pil_img)

        original_mob = to_manim_image((img_np * 255).astype(np.uint8))
        recon_mobs = [to_manim_image(im) for im in recon_images]

        all_images = [original_mob] + recon_mobs
        for im in all_images:
            im.scale(0.6)

        labels = [
            Text("Original", font="Noto Sans").scale(0.6),
            Text("Rank 1", font="Noto Sans").scale(0.6),
            Text("Rank 10", font="Noto Sans").scale(0.6),
            Text("Rank 100", font="Noto Sans").scale(0.6),
        ]

        grid = Group()
        for i, (img_mob, label) in enumerate(zip(all_images, labels)):
            group = Group(img_mob, label).arrange(DOWN)
            label.next_to(img_mob, DOWN)
            grid.add(group)

        grid.arrange_in_grid(rows=2, cols=2, buff=0.5)
        self.add_sound("voiceovers/nomagician-successfinish.mp3")
        self.play(LaggedStart(*[FadeIn(im) for im in grid], lag_ratio=1))
        self.wait(3)

class MatrixRepresentation(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/MatrixRepresentation.mp3")
        title = Text("Biểu diễn ma trận", font="Noto Sans", font_size=36).to_edge(UP)
        matrix = MathTex("A").scale(1.5)
        eq_compact = MathTex(
            "A", "=", "U", r"\Sigma", "V^T"
        ).scale(1.5)
        
        eq_compact[2].set_color(BLUE)   # U
        eq_compact[3].set_color(YELLOW)  # Sigma
        eq_compact[4].set_color(GREEN) # V^T
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(title))
        self.wait()
        self.add_sound("voiceovers/image_matrix.mp3")
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(matrix))
        self.wait(2)
        self.add_sound("voiceovers/correct_answer_toy.mp3")
        self.play(ReplacementTransform(matrix, eq_compact))
        self.wait(2)
        self.play(LaggedStart(*[Indicate(eq_compact[i], color=eq_compact[i].get_color()) for i in (2,3,4)], lag_ratio=1))
        self.wait()
        eq_expanded = MathTex(
            "A", "=", 
            r"\sigma_1", "u_1", "v_1^T", "+",
            r"\sigma_2", "u_2", "v_2^T", "+",
            r"\dots", "+",
            r"\sigma_n", "u_n", "v_n^T"
        ).scale(0.9)
        
        for i in [2, 6, 12]: eq_expanded[i].set_color(YELLOW)  # Sigmas
        for i in [3, 7, 13]: eq_expanded[i].set_color(BLUE)   # u vectors
        for i in [4, 8, 14]: eq_expanded[i].set_color(GREEN) # v vectors
        self.add_sound("voiceovers/correct_answer_toy.mp3")
        self.play(TransformMatchingTex(eq_compact, eq_expanded), run_time=2)
        self.wait()
        self.add_sound("voiceovers/Low_rank_approximation.mp3")
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(eq_expanded.animate.shift(UP * 2))
        
        frame = SurroundingRectangle(eq_expanded[2:5], color=PINK, buff=0.1)
        layer_text = Text("Ma trận hạng 1 (Lớp thông tin)", font="Noto Sans", font_size=24, color=PINK).next_to(frame, DOWN)
        self.add_sound("voiceovers/zipper-zip.mp3")
        self.play(Create(frame), Write(layer_text))
        self.wait(.5)

        sigma_val = MathTex(r"\sigma_1").set_color(YELLOW).scale(1.2)
        u_vec = Matrix([["u_{11}"], ["u_{21}"], ["u_{31}"]]).set_color(BLUE)
        v_vec = Matrix([["v_{11}", "v_{12}", "v_{13}"]]).set_color(GREEN)
        
        rank1_group = VGroup(sigma_val, u_vec, v_vec).arrange(RIGHT, buff=0.2)
        equals = MathTex("=")
        
        layer_matrix = Matrix([
            [r"\dots", r"\dots", r"\dots"],
            [r"\dots", r"\dots", r"\dots"],
            [r"\dots", r"\dots", r"\dots"]
        ])
        VGroup(rank1_group, equals, layer_matrix).arrange(RIGHT).shift(DOWN * 1.5)
        layer1_text = Text("Lớp 1", font="Noto Sans", font_size=36
                           ).move_to(layer_matrix.get_center())
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(
            FadeOut(layer_text),
            TransformFromCopy(eq_expanded[2], rank1_group[0]), # Sigma
            TransformFromCopy(eq_expanded[3], rank1_group[1]), # u vector
            TransformFromCopy(eq_expanded[4], rank1_group[2]), # v vector
        )
        self.wait(.5)

        layer_bg = BackgroundRectangle(layer_matrix, color=WHITE, fill_opacity=0.1)
        layer_group = VGroup(layer_bg, layer_matrix, layer1_text)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(equals), Write(layer_group))
        self.wait(3)

        layer2_text = Text("Lớp 2 (Chi tiết hơn)", font="Noto Sans", font_size=20)
        layer_matrix_2 = Matrix([
            [r"\dots", r"\dots", r"\dots"],
            [r"\dots", r"\dots", r"\dots"],
            [r"\dots", r"\dots", r"\dots"]
        ])
        layer2_text.move_to(layer_matrix_2.get_center())
        layer_group_2 = VGroup(layer_matrix_2, layer2_text).move_to(layer_group)

        frame_2 = SurroundingRectangle(eq_expanded[6:9], color=PINK, buff=0.1)
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(
            Transform(frame, frame_2),
            Transform(layer_group, layer_group_2),
            rank1_group[0].animate.become(MathTex(r"\sigma_2").set_color(YELLOW).scale(1.2).move_to(rank1_group[0])),
            rank1_group[1].animate.become(Matrix([["u_{12}"], ["u_{22}"], ["u_{32}"]]).set_color(BLUE).move_to(rank1_group[1])),
            rank1_group[2].animate.become(Matrix([["v_{21}", "v_{22}", "v_{23}"]]).set_color(GREEN).move_to(rank1_group[2])),
            run_time=1.5
        )
        self.wait(4)
class SingularValueEconomy(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/SingularValueEconomy.mp3")
        sigma_matrix = MathTex(
            r"\Sigma = \begin{bmatrix} \sigma_1 & 0 & \dots & 0 \\ 0 & \sigma_2 & \dots & 0 \\ \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & \dots & \sigma_n \end{bmatrix}"
        ).shift(UP * 1)
        
        condition = MathTex(
            r"\sigma_1 \geq \sigma_2 \geq \dots \geq \sigma_n \geq 0", 
            color=YELLOW
        ).next_to(sigma_matrix, DOWN, buff=0.5)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(sigma_matrix))
        self.wait()
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(condition))
        self.wait(2)

        self.play(
            FadeOut(sigma_matrix),
            FadeOut(condition)
        )

        axes = Axes(
            x_range=[0, 100, 10],  # 100 singular values
            y_range=[0, 100, 20],  # Magnitude
            x_length=8,
            y_length=4.5,
            axis_config={"include_tip": False}
        ).shift(DOWN * 0.5)

        x_label = axes.get_x_axis_label("Index \ (i)", direction=DOWN, buff=0.3)
        y_label = axes.get_y_axis_label("\sigma_i", direction=LEFT, buff=0.3)
        self.add_sound("voiceovers/click.wav")
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label))

        decay_func = lambda x: 90 * np.exp(-0.08 * x) + 2
        curve = axes.plot(decay_func, color=BLUE)
        self.add_sound("voiceovers/zipper-zip.mp3")
        self.play(Create(curve), run_time=2)
        self.wait()

        k_value = 20
        
        divider = DashedLine(
            start=axes.c2p(k_value, 0),
            end=axes.c2p(k_value, 100),
            color=WHITE
        )
        k_label = MathTex("k=20", font_size=24).next_to(divider, DOWN, buff=0.2)
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(Create(divider), Write(k_label))

        signal_area = axes.get_area(curve, x_range=[0, k_value], color=YELLOW, opacity=0.5)
        signal_text = Text("'Tín hiệu'\n(Giữ lại)", font="Noto Sans", color=YELLOW, font_size=20, line_spacing=1).next_to(signal_area, RIGHT, buff=0.5).shift(UP*1.5)

        noise_area = axes.get_area(curve, x_range=[k_value, 100], color=GRAY, opacity=0.3)
        noise_text = Text("'Nhiễu'\n(Loại bỏ)", font="Noto Sans", color=GRAY, font_size=20, line_spacing=1).next_to(divider, RIGHT, buff=2).shift(DOWN*0.5)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(
            FadeIn(signal_area),
            Write(signal_text)
        )
        self.wait(1)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(
            FadeIn(noise_area),
            Write(noise_text)
        )
        self.wait(4)   
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.svdImageCompression() 
    def svdImageCompression(self):
        try:
            img = Image.open("assets/lenna_color.png").convert('L')
            img = img.resize((200, 200)) 
            img_array = np.array(img) / 255.0
        except FileNotFoundError:
            x = np.linspace(-5, 5, 200)
            X, Y = np.meshgrid(x, x)
            img_array = (np.sin(X**2 + Y**2) + 1) / 2.0

        m, n = img_array.shape
        U, S_vals, VT = np.linalg.svd(img_array, full_matrices=False)
        k_tracker = ValueTracker(1)
        def get_reconstructed_image(k):
            k = max(1, int(k)) 
            recon = U[:, :k] @ np.diag(S_vals[:k]) @ VT[:k, :]
            
            recon_img = np.clip(recon * 255, 0, 255).astype(np.uint8)
            recon_rgb = np.stack((recon_img,)*3, axis=-1)
            
            return ImageMobject(recon_rgb).scale(4)

        dynamic_image = get_reconstructed_image(1)
        dynamic_image.to_edge(LEFT, buff=1.5)
        title = MathTex(r"\text{SVD Image Compression } (A_k \approx A)", font_size=42).to_edge(UP)

        k_label = always_redraw(lambda: MathTex(
            rf"k = {int(k_tracker.get_value())}", font_size=36
        ).next_to(dynamic_image, DOWN, buff=0.3))

        storage_label = always_redraw(lambda: MathTex(
            rf"\text{{Storage: }}{((int(k_tracker.get_value()) * (m + n + 1)) / (m * n) * 100):.1f}\%", 
            font_size=28, 
            color=YELLOW_B
        ).next_to(k_label, DOWN, buff=0.2))

        orig_rgb = np.stack((np.clip(img_array * 255, 0, 255).astype(np.uint8),)*3, axis=-1)
        orig_image = ImageMobject(orig_rgb).scale(4).to_edge(RIGHT, buff=1.5)
        
        orig_label = MathTex(rf"\text{{Original }} (k = {min(m, n)})", font_size=36)
        orig_label.next_to(orig_image, DOWN, buff=0.3)
        orig_storage = Text("Storage: 100%", font="Noto Sans", font_size=18, color=WHITE).next_to(orig_label, DOWN, buff=0.1)

        def update_image(mob):
            new_mob = get_reconstructed_image(k_tracker.get_value())
            new_mob.move_to(mob.get_center())
            mob.become(new_mob)

        dynamic_image.add_updater(update_image)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(title))
        self.wait(2)
        self.add_sound("voiceovers/svdImageCompression.mp3")
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(
            FadeIn(dynamic_image), FadeIn(k_label), FadeIn(storage_label),
            FadeIn(orig_image), FadeIn(orig_label), FadeIn(orig_storage),
            run_time=2
        )
        self.wait(3)
        self.add_sound("voiceovers/click.wav")
        self.play(k_tracker.animate.set_value(10), run_time=3, rate_func=linear)
        self.wait()
        self.add_sound("voiceovers/click.wav")
        self.play(k_tracker.animate.set_value(50), run_time=4, rate_func=linear)
        self.wait()
        self.add_sound("voiceovers/click.wav")
        self.play(k_tracker.animate.set_value(min(m, n)), run_time=10, rate_func=smooth)
        self.wait(3)
class SignalVsNoise(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/SignalVsNoise.mp3")
        full_svd = MathTex("A", "=", "U", "\\Sigma", "V^T")
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(full_svd))
        self.wait()

        sum_form_full = MathTex(
            "A", "=", "\\sum_{i=1}^{r}", "\\sigma_i", "u_i", "v_i^T"
        )
        self.add_sound("voiceovers/correct_answer_toy.mp3")
        self.play(ReplacementTransform(full_svd, sum_form_full))
        self.wait()
        expanded_sum = MathTex(
            "A", "=", 
            "\\sigma_1 u_1 v_1^T", "+", "\\dots", "+", "\\sigma_k u_k v_k^T", 
            "+", "\\dots", "+", "\\sigma_r u_r v_r^T"                         
        )
        
        expanded_sum.scale(0.85)
        self.add_sound("voiceovers/correct_answer_toy.mp3")
        self.play(ReplacementTransform(sum_form_full, expanded_sum))
        self.wait()

        keep_group = VGroup(expanded_sum[2], expanded_sum[3], expanded_sum[4], expanded_sum[5], expanded_sum[6])
        drop_group = VGroup(expanded_sum[7], expanded_sum[8], expanded_sum[9], expanded_sum[10])

        brace = Brace(keep_group, DOWN, color=BLUE)
        brace_text = brace.get_text("Rank-$k$ Approximation").set_color(BLUE)
        self.add_sound("voiceovers/writin.mp3")
        self.play(GrowFromCenter(brace), Write(brace_text))
        self.wait(.5)

        self.play(drop_group.animate.set_opacity(0.3), run_time=.5)
        cross = Cross(drop_group, stroke_color=RED, stroke_width=6)
        self.add_sound("voiceovers/error.wav")
        self.play(Create(cross))
        self.wait()
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.transition()
    def transition(self):
        self.add_sound("voiceovers/recommendation_transition.mp3")
        eq = MathTex("A", "=", "U", r"\Sigma", "V^T", font_size=60)
        eq[2].set_color(BLUE)
        eq[3].set_color(YELLOW)
        eq[4].set_color(GREEN)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(eq))
        self.wait()
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(eq.animate.shift(UP * 1.5))
        rec_title_new = Text("Hệ thống đề xuất", font="Noto Sans", font_size=40, color=TEAL).to_edge(UP)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(rec_title_new))

        eq_rec = MathTex("R", "=", "U", r"\Sigma", "V^T", font_size=60).move_to(eq.get_center())
        eq_rec[2].set_color(BLUE)
        eq_rec[3].set_color(YELLOW)
        eq_rec[4].set_color(GREEN)

        self.play(TransformMatchingTex(eq, eq_rec), run_time=1.5)
        self.wait()

        label_R = Text("Đánh giá của người dùng\n(Dữ liệu thô)", font="Noto Sans", font_size=18, line_spacing=1.2).next_to(eq_rec[0], DOWN, buff=1)
        label_U = Text("Hồ sơ người dùng\n(Ai thích cái gì?)", font="Noto Sans", font_size=18, color=BLUE, line_spacing=1.2).next_to(eq_rec[2], DOWN, buff=1)
        label_S = Text("Khái niệm tiềm ẩn\n(Hành động, Hài kịch, v.v.)", font="Noto Sans", font_size=18, color=YELLOW, line_spacing=1.2).next_to(eq_rec[3], DOWN, buff=1)
        label_V = Text("Đặc điểm phim\n(Nội dung phim là gì)", font="Noto Sans", font_size=18, color=GREEN, line_spacing=1.2).next_to(eq_rec[4], DOWN, buff=1)
        VGroup(label_R, label_U, label_S, label_V).arrange(RIGHT)
        VGroup(label_U, label_V).shift(DOWN)

        arrows = VGroup(
            Line(label_R.get_top(), eq_rec[0].get_bottom(), buff=0.1, color=WHITE),
            Line(label_U.get_top(), eq_rec[2].get_bottom(), buff=0.1, color=BLUE),
            Line(label_S.get_top(), eq_rec[3].get_bottom(), buff=0.1, color=YELLOW),
            Line(label_V.get_top(), eq_rec[4].get_bottom(), buff=0.1, color=GREEN),
        )
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(
            AnimationGroup(
                FadeIn(label_R, shift=UP * 0.2), Create(arrows[0]),
                FadeIn(label_U, shift=UP * 0.2), Create(arrows[1]),
                FadeIn(label_S, shift=UP * 0.2), Create(arrows[2]),
                FadeIn(label_V, shift=UP * 0.2), Create(arrows[3]),
                lag_ratio=0.2
            )
        )
        self.wait(3)
class LatentFactorDiscovery(Scene):
    def netflixCinematic(self):
        logo = Text("NETFLIX", color=RED, weight=BOLD)
        logo.to_corner(UL)
        self.add_sound("voiceovers/intro_cinematic.mp3")
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(logo, shift=DOWN))
        trending = Text("Đang thịnh hành", font="Noto Sans", font_size=24)
        trending.next_to(logo, DOWN).align_to(logo, LEFT).shift(DOWN*0.5)
        self.add_sound("voiceovers/LatentFactorDiscovery.mp3")
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(trending))
        posters = Group(*[
            ImageMobject(f"posters/poster{i}.jpg").stretch_to_fit_width(1).stretch_to_fit_height(1.5)
            for i in range(1,9)
        ])
        posters.arrange(RIGHT, buff=0.3)
        posters.next_to(trending, DOWN, aligned_edge=LEFT)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(posters, shift=UP*0.3))
        self.add_sound("voiceovers/spin.mp3")
        self.play(
            posters.animate.shift(LEFT*4),
            rate_func=smooth
        )
        focus_movie = posters[5]
        highlight = SurroundingRectangle(
            focus_movie,
            color=YELLOW,
            buff=0.1
        )
        self.add_sound("voiceovers/ding-402325.mp3")
        watched_text = Text("Đã xem", font="Noto Sans", font_size=18, color=YELLOW)
        watched_text.next_to(highlight, UP)
        self.play(
            focus_movie.animate.scale(1.2),
            Create(highlight),
            FadeIn(watched_text)
        )
        
        rec_title = Text("Đề xuất dành cho bạn", font="Noto Sans", font_size=24)
        rec_title.next_to(posters, DOWN, buff=1).shift(RIGHT*4)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(rec_title, shift=DOWN))
        rec_posters = Group(*[
            ImageMobject(f"posters/poster{i}.jpg").stretch_to_fit_width(1).stretch_to_fit_height(1.5)
            for i in range(4,10)
        ])

        rec_posters.arrange(RIGHT, buff=0.3)
        rec_posters.next_to(rec_title, DOWN)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(rec_posters, shift=UP*0.3))
        glow = SurroundingRectangle(
            Group(rec_posters[0], rec_posters[1]),
            color=GREEN,
            buff=0.15
        )
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(Create(glow))
        self.wait()
        self.play(*[FadeOut(mob) for mob in self.mobjects])
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/RecommendationSystems.mp3")
        title = Text("Hệ thống đề xuất", font="Noto Sans", weight=BOLD)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(title))
        self.wait()
        self.play(Unwrite(title))
        self.netflixCinematic()
        R = np.array([
            [5, 5, 0, 0], # User 1: Loves Action, hates Romance
            [5, 0, 1, 0], # User 2: Loves Action, dislikes Romance
            [0, 1, 5, 4], # User 3: Hates Action, loves Romance
            [1, 1, 0, 5], # User 4: Dislikes Action, loves Romance
        ])

        R_mean = np.mean(R[R > 0])
        R_norm = np.where(R == 0, 0, R - R_mean)

        U, S, Vh = np.linalg.svd(R_norm, full_matrices=False)

        U_2D = U[:, :2] 
        S_2D = np.diag(S[:2])
        V_2D = Vh[:2, :] 

        user_names = ["U1", "U2", "U3", "U4"]
        movie_names = ["Matrix", "Die Hard", "Titanic", "Notebook"]

        COL_USER = BLUE
        COL_ITEM = GREEN
        COL_FACTOR = YELLOW

        title = Text("Khám phá các yếu tố tiềm ẩn bằng SVD", font="Noto Sans", font_size=36).to_edge(UP)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(title))
        matrix_label = Text("Ma trận xếp hạng phim của người dùng (R)", font="Noto Sans", font_size=24, color=GRAY).next_to(title, DOWN)
        m_entries = VGroup()
        for i, row in enumerate(R):
            row_grp = VGroup()
            for j, val in enumerate(row):
                entry = Integer(val, font_size=20, color=GRAY if val == 0 else WHITE)
                entry.move_to(np.array([j * 1.5 - 2.25, -i * 0.8 + 1.0, 0]))
                row_grp.add(entry)
            m_entries.add(row_grp)
        m_entries.shift(DOWN)
        
        u_labels = VGroup(*[Text(name, font_size=18, weight=BOLD, color=COL_USER).next_to(m_entries[i][0], LEFT, buff=0.5) for i, name in enumerate(user_names)])
        i_labels = VGroup(*[Text(name, font_size=18, weight=BOLD, color=COL_ITEM).rotate(-PI/4, about_edge=LEFT).next_to(m_entries[0][j], UP, buff=0.5) for j, name in enumerate(movie_names)])
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(matrix_label), Write(m_entries), FadeIn(u_labels), FadeIn(i_labels))
        self.wait()
        self.play(Indicate(u_labels, color=COL_USER))
        self.wait(.5)
        self.play(Indicate(i_labels, color=COL_ITEM))
        self.wait(4)

        svd_formula = MathTex(r"R \approx", "U", r"\Sigma", "V^T", font_size=48).move_to(m_entries.get_center())
        svd_formula[1].set_color(COL_USER)
        svd_formula[2].set_color(COL_FACTOR)
        svd_formula[3].set_color(COL_ITEM)
        self.add_sound("voiceovers/correct_answer_toy.mp3")
        self.play(
            FadeOut(m_entries), FadeOut(u_labels), FadeOut(i_labels),
            ReplacementTransform(matrix_label, svd_formula),
            run_time=1.5
        )
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(svd_formula.animate.to_edge(UP).shift(DOWN*0.5))
        self.wait(3)

        def create_matrix_mobject(mat, color):
            rounded = np.round(mat, 1)
            str_mat = [[str(val) for val in row] for row in rounded]
            return Matrix(str_mat).set_color(color).scale(0.6)

        u_mob = create_matrix_mobject(U_2D, COL_USER)
        s_mob = create_matrix_mobject(S_2D, COL_FACTOR)
        v_mob = create_matrix_mobject(V_2D, COL_ITEM)
        VGroup(u_mob, s_mob, v_mob).arrange(RIGHT, buff=2)
        u_desc = Text(
            "U: Ma trận người dùng\n(Hàng = Người dùng,\nCột = Thể loại)", font="Noto Sans", 
            font_size=18, 
            color=COL_USER,
            line_spacing=1.2 
        ).next_to(u_mob, DOWN)

        s_desc = Text(
            "Σ: Sức mạnh của Thể loại\n(Lớn hơn = Quan trọng hơn)", font="Noto Sans", 
            font_size=18, 
            color=COL_FACTOR,
            line_spacing=1.2
        ).next_to(s_mob, DOWN)

        v_desc = Text(
            "Vᵀ: Đặc điểm phim\n(Hàng = Thể loại,\nCột = Phim)", font="Noto Sans", 
            font_size=18, 
            color=COL_ITEM,
            line_spacing=1.2
        ).next_to(v_mob, DOWN)
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(
            FadeOut(title),
            ReplacementTransform(svd_formula[1].copy(), u_mob),    
        )
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(u_desc))
        self.wait(4)
        bond = ImageMobject("posters/bond.jpg"
                            ).stretch_to_fit_width(1.6).stretch_to_fit_height(2.4)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(bond))
        self.wait()
        bean = ImageMobject("posters/bean.jpg"
                            ).stretch_to_fit_width(1.6).stretch_to_fit_height(2.4)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeOut(bond), FadeIn(bean))
        self.wait()
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(FadeOut(bean), ReplacementTransform(svd_formula[3].copy(), v_mob), Write(v_desc))
        self.wait(4)
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(ReplacementTransform(svd_formula[2].copy(), s_mob), Write(s_desc))
        self.wait(4)

        u_highlight = SurroundingRectangle(u_mob.get_rows()[0], color=YELLOW, buff=0.1)
        v_highlight = SurroundingRectangle(v_mob.get_columns()[0], color=YELLOW, buff=0.1)
        
        highlight_text = Text(
            "Hồ sơ của Người dùng 1 phù hợp với các đặc điểm của Phim 1.", font="Noto Sans", 
            font_size=20, color=WHITE
        ).to_edge(DOWN, buff=1)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Create(u_highlight), Create(v_highlight), Write(highlight_text))
        self.wait(2)

        self.play(
            FadeOut(u_mob), FadeOut(u_desc), FadeOut(s_mob), FadeOut(s_desc), 
            FadeOut(v_mob), FadeOut(v_desc), FadeOut(u_highlight), FadeOut(v_highlight),
            FadeOut(highlight_text), FadeOut(svd_formula)
        )

        latent_axes = Axes(
            x_range=[-1.1, 1.1, 0.5], y_range=[-1.1, 1.1, 0.5],
            x_length=6, y_length=6,
            axis_config={"include_tip": True, "tip_shape": StealthTip}
        ).shift(DOWN*0.2)
        
        factor1_label = Text("Thể loại 1 (ví dụ: Hành động)", font="Noto Sans", font_size=18, color=COL_FACTOR).next_to(latent_axes.x_axis, UR, buff=0.1)
        factor2_label = Text("Thể loại 2 (ví dụ: Lãng mạn)", font="Noto Sans", font_size=18, color=COL_FACTOR).next_to(latent_axes.y_axis, UL, buff=0.1)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Create(latent_axes), Write(factor1_label), Write(factor2_label))
        
        user_dots = VGroup()
        for i, coord in enumerate(U_2D):
            pos = latent_axes.c2p(coord[0], coord[1])
            dot = Dot(pos, color=COL_USER, radius=0.1)
            label = Text(user_names[i], font_size=16).next_to(dot, UR, buff=0.05)
            user_dots.add(VGroup(dot, label))
        self.add_sound("voiceovers/nomagician-successfinish.mp3")
        self.play(AnimationGroup(*[FadeIn(grp, shift=UP*0.2) for grp in user_dots], lag_ratio=0.2))
        
        item_icons = VGroup()
        for j, coord in enumerate(V_2D.T): 
            pos = latent_axes.c2p(coord[0], coord[1])
            icon = get_youtube_video(color=COL_ITEM).set_opacity(0.5).scale(0.1).move_to(pos)
            label = Text(movie_names[j], font_size=16, color=COL_ITEM).next_to(icon, DR, buff=0.05)
            item_icons.add(VGroup(icon, label))
        self.add_sound("voiceovers/nomagician-successfinish.mp3")    
        self.play(AnimationGroup(*[FadeIn(grp, scale=0.5) for grp in item_icons], lag_ratio=0.3))
        
        connect_U1_M1 = DashedLine(start=user_dots[0][0].get_center(), end=item_icons[0][0].get_center(), color=YELLOW)
        connect_U3_M3 = DashedLine(start=user_dots[2][0].get_center(), end=item_icons[2][0].get_center(), color=YELLOW)
        
        explainer_final = Text(
            "Người dùng và phim hiện được liên kết với nhau dựa trên các yếu tố tiềm ẩn.",
            font_size=24, color=WHITE, font="Noto Sans"
        ).to_edge(DOWN)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(explainer_final))
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(Create(connect_U1_M1), Create(connect_U3_M3))
        self.wait(5)
class SVDCorrelations(Scene):
    def cleanScatter(self):
        axes = Axes(
            x_range=[0, 10],
            y_range=[0, 10],
            x_length=6,
            y_length=6,
            axis_config={
                "include_ticks": False,
                "include_numbers": False,
                "include_tip": False,   # 🔥 removes arrowheads
            },
        )

        np.random.seed(4)
        x1 = np.linspace(1, 5, 15)
        y1 = 0.7 * x1 + np.random.normal(0, 0.8, len(x1))
        x2 = np.linspace(5, 9, 15)
        y2 = 0.7 * x2 + np.random.normal(0, 0.8, len(x2))
        sizes1 = np.random.uniform(0.05, 0.12, len(x1))
        sizes2 = np.random.uniform(0.05, 0.12, len(x2))
        dots_group1 = VGroup(*[
            Dot(axes.c2p(x1[i], y1[i]), radius=sizes1[i], color=BLUE)
            for i in range(len(x1))
        ])
        dots_group2 = VGroup(*[
            Dot(axes.c2p(x2[i], y2[i]), radius=sizes2[i], color=GREEN)
            for i in range(len(x2))
        ])
        self.play(Create(axes))
        self.add_sound("voiceovers/nomagician-successfinish.mp3")
        self.play(LaggedStart(*[FadeIn(dot) for dot in dots_group1], lag_ratio=0.08))
        self.add_sound("voiceovers/nomagician-successfinish.mp3")
        self.play(LaggedStart(*[FadeIn(dot) for dot in dots_group2], lag_ratio=0.08))
        self.wait()
        self.play(*[FadeOut(mob) for mob in self.mobjects])
    def highlightRowsAndColumns(self):
        matrix = Matrix([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]).scale(1.5)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(matrix))
        self.wait()

        entries = matrix.get_entries()
        def get_entry(r, c):
            return entries[r * 3 + c]
        column_boxes = []
        for c in range(3):
            col_group = VGroup(*[get_entry(r, c) for r in range(3)])
            box = SurroundingRectangle(col_group, color=GREEN, buff=0.2)
            column_boxes.append(box)
        self.add_sound("voiceovers/click.wav")
        self.play(*[Create(box) for box in column_boxes])
        self.wait(.5)
        row_boxes = []
        for r in range(3):
            row_group = VGroup(*[get_entry(r, c) for c in range(3)])
            box = SurroundingRectangle(row_group, color=BLUE, buff=0.2)
            row_boxes.append(box)
        self.add_sound("voiceovers/click.wav")
        self.play(*[FadeOut(box) for box in column_boxes],
                  *[Create(box) for box in row_boxes])
        self.wait()
        self.play(*[FadeOut(mob) for mob in self.mobjects])
    def rowsColumnsBridge(self):
        formula = MathTex("A", "=", "U", r"\Sigma", "V^T", font_size=72).add_background_rectangle()
        formula[3].set_color(BLUE)
        formula[4].set_color(YELLOW)
        formula[5].set_color(GREEN)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(formula), run_time=2)
        self.wait()
        self.play(Unwrite(formula))
        matrix_left = Matrix([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]).scale(0.9).to_edge(3*LEFT)

        matrix_right = Matrix([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]).scale(0.9).to_edge(3*RIGHT)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(matrix_left), Write(matrix_right))
        self.wait()

        def get_entry(matrix, r, c):
            entries = matrix.get_entries()
            return entries[r * 3 + c]

        row_boxes = []
        for r in range(3):
            row_group = VGroup(*[get_entry(matrix_left, r, c) for c in range(3)])
            box = SurroundingRectangle(row_group, color=BLUE, buff=0.12)
            row_boxes.append(box)
        self.add_sound("voiceovers/click.wav")
        self.play(*[Create(box) for box in row_boxes], run_time=.5)
        self.wait(.5)

        col_boxes = []
        for c in range(3):
            col_group = VGroup(*[get_entry(matrix_right, r, c) for r in range(3)])
            box = SurroundingRectangle(col_group, color=GREEN, buff=0.12)
            col_boxes.append(box)
        self.add_sound("voiceovers/click.wav")
        self.play(*[Create(box) for box in col_boxes], run_time=.5)
        self.wait(.5)

        arrow = CurvedArrow(
            start_point=matrix_left.get_right(),
            end_point=matrix_right.get_left(),
            angle=-PI/3,
            color=YELLOW
        )

        svd_text = MathTex(r"A = U \Sigma V^T")
        # svd_text.set_color_by_tex("U", BLUE)
        # svd_text.set_color_by_tex("V", GREEN)
        svd_text[0][2].set_color(BLUE)
        svd_text[0][4:].set_color(GREEN)
        svd_text.scale(0.9)
        svd_text.next_to(arrow, UP, buff=0.2)
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(Create(arrow), FadeIn(svd_text))
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
    def AT_A(self):
        self.add_sound("voiceovers/AT_A.mp3")
        col_title = Text("Mối tương quan giữa các cột (Ma trận V)", font_size=32, color=GREEN,
                                       font="Noto Sans").next_to(self.title, DOWN, MED_LARGE_BUFF)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(col_title))
        
        a_matrix = MathTex(
            "\\mathbf{A}", "=", 
            "\\begin{bmatrix} "
            "| & | \\\\ "
            "\\mathbf{a}_1 & \\mathbf{a}_2 \\\\ "
            "| & | "
            "\\end{bmatrix}",
            font_size=42
        )

        pair1 = MathTex("\\mathbf{a}_1 \\cdot \\mathbf{a}_1", font_size=36).shift(LEFT * 3 + UP * 0.5)
        pair2 = MathTex("\\mathbf{a}_1 \\cdot \\mathbf{a}_2", font_size=36).shift(LEFT * 1 + UP * 0.5)
        pair3 = MathTex("\\mathbf{a}_2 \\cdot \\mathbf{a}_1", font_size=36).shift(RIGHT * 1 + UP * 0.5)
        pair4 = MathTex("\\mathbf{a}_2 \\cdot \\mathbf{a}_2", font_size=36).shift(RIGHT * 3 + UP * 0.5)
        pairs = VGroup(pair1, pair2, pair3, pair4)

        product_expr = MathTex(
            "\\mathbf{A}^\\text{T}", "\\mathbf{A}", "=",
            "\\begin{bmatrix} "
            "\\text{---} & \\mathbf{a}_1^\\text{T} & \\text{---} \\\\ "
            "\\text{---} & \\mathbf{a}_2^\\text{T} & \\text{---} "
            "\\end{bmatrix}",
            "\\begin{bmatrix} "
            "| & | \\\\ "
            "\\mathbf{a}_1 & \\mathbf{a}_2 \\\\ "
            "| & | "
            "\\end{bmatrix}",
            font_size=36
        )

        result_matrix = MathTex(
            "=",
            "\\begin{bmatrix} "
            "\\mathbf{a}_1^\\text{T}\\mathbf{a}_1 & \\mathbf{a}_1^\\text{T}\\mathbf{a}_2 \\\\ "
            "\\mathbf{a}_2^\\text{T}\\mathbf{a}_1 & \\mathbf{a}_2^\\text{T}\\mathbf{a}_2 "
            "\\end{bmatrix}",
            font_size=36
        )
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(a_matrix))
        self.wait(0.5)
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(a_matrix.animate.move_to(ORIGIN).shift(DOWN * 1.5))
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(pair1), run_time=.5)
        self.wait(0.2)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(pair2), run_time=.5)
        self.wait(0.2)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(pair3), Write(pair4), run_time=.5)
        self.wait()
        
        product_expr.move_to(ORIGIN).shift(UP * 0.5)
        self.play(FadeOut(pairs),
            FadeOut(a_matrix),
            FadeIn(product_expr))
        self.wait(.5)

        result_matrix.next_to(product_expr, DOWN, buff=0.5)
        
        self.play(
            product_expr[3].animate.set_color(YELLOW), 
            product_expr[4].animate.set_color(BLUE),   
        )
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(result_matrix), run_time=.5)
        self.wait(2)
        self.play(FadeOut(result_matrix, product_expr))
        self.add_sound("voiceovers/AT_A_svd1.mp3")
        col_eq1 = MathTex("A^T A", "=", "(U \\Sigma V^T)^T", "(U \\Sigma V^T)", font_size=36)
        col_eq1.next_to(col_title, DOWN, buff=0.5)
        
        col_eq2 = MathTex("A^T A", "=", "V \\Sigma^T", "U^T U", "\\Sigma V^T", font_size=36)
        col_eq2.next_to(col_eq1, DOWN, buff=0.5)
        
        col_eq3 = MathTex("A^T A", "=", "V \\Sigma^2 V^T", font_size=40)
        col_eq3.next_to(col_eq2, DOWN, buff=0.7)
        col_eq3[2].set_color(GREEN)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(col_eq1))
        self.wait()
        self.add_sound("voiceovers/correct_answer_toy.mp3")
        self.play(TransformMatchingTex(col_eq1.copy(), col_eq2))
        self.wait()
        self.add_sound("voiceovers/AT_A_svd2.mp3")
        brace_U = Brace(col_eq2[3], DOWN, color=YELLOW)
        brace_text_U = brace_U.get_text("$I$").set_color(YELLOW).scale(0.7)
        self.play(GrowFromCenter(brace_U))
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(brace_text_U))
        self.wait(3)
        self.add_sound("voiceovers/correct_answer_toy.mp3")
        self.play(
            TransformMatchingTex(col_eq2.copy(), col_eq3),
            FadeOut(brace_U), FadeOut(brace_text_U)
        )
        self.wait()
        self.add_sound("voiceovers/AT_A_explain.mp3")
        self.title.add(col_eq3)
        self.play(*[
            FadeOut(mob) for mob in self.mobjects
            if mob not in self.title
        ], col_eq3.animate.move_to(ORIGIN))
        self.wait()
        box = SurroundingRectangle(col_eq3, color=GREEN, buff=0.2)
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(Create(box))
        self.wait()
        self.play(Flash(col_eq3[2][0]))
        self.wait()
        self.play(Flash(col_eq3[0]))
        self.wait()
        self.play(Uncreate(box), col_eq3.animate.next_to(self.title[0], RIGHT, LARGE_BUFF))
        self.wait()
    def A_AT(self):
        self.add_sound("voiceovers/A_AT.mp3")
        row_title = Text("Mối tương quan giữa các hàng (Ma trận U)", font="Noto Sans", font_size=32, color=BLUE)
        row_title.next_to(self.title, DOWN, MED_LARGE_BUFF)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(row_title))
        a_matrix = MathTex(
            "\\mathbf{A}", "=", 
            "\\begin{bmatrix} "
            "\\text{---} & \\mathbf{a}_1 & \\text{---} \\\\ "
            "\\text{---} & \\mathbf{a}_2 & \\text{---} "
            "\\end{bmatrix}",
            font_size=42
        )

        pair1 = MathTex("\\mathbf{a}_1 \\cdot \\mathbf{a}_1", font_size=36).shift(LEFT * 3 + UP * 0.5)
        pair2 = MathTex("\\mathbf{a}_1 \\cdot \\mathbf{a}_2", font_size=36).shift(LEFT * 1 + UP * 0.5)
        pair3 = MathTex("\\mathbf{a}_2 \\cdot \\mathbf{a}_1", font_size=36).shift(RIGHT * 1 + UP * 0.5)
        pair4 = MathTex("\\mathbf{a}_2 \\cdot \\mathbf{a}_2", font_size=36).shift(RIGHT * 3 + UP * 0.5)
        pairs = VGroup(pair1, pair2, pair3, pair4)

        product_expr = MathTex(
            "\\mathbf{A}", "\\mathbf{A}^\\text{T}", "=",
            "\\begin{bmatrix} "
            "\\text{---} & \\mathbf{a}_1 & \\text{---} \\\\ "
            "\\text{---} & \\mathbf{a}_2 & \\text{---} "
            "\\end{bmatrix}",
            "\\begin{bmatrix} "
            "| & | \\\\ "
            "\\mathbf{a}_1^\\text{T} & \\mathbf{a}_2^\\text{T} \\\\ "
            "| & | "
            "\\end{bmatrix}",
            font_size=36
        )

        result_matrix = MathTex(
            "=",
            "\\begin{bmatrix} "
            "\\mathbf{a}_1\\mathbf{a}_1^\\text{T} & \\mathbf{a}_1\\mathbf{a}_2^\\text{T} \\\\ "
            "\\mathbf{a}_2\\mathbf{a}_1^\\text{T} & \\mathbf{a}_2\\mathbf{a}_2^\\text{T} "
            "\\end{bmatrix}",
            font_size=36
        )
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(a_matrix), run_time=.5)
        self.wait(0.5)
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(a_matrix.animate.move_to(ORIGIN).shift(DOWN * 1.5), run_time=.5)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(pair1), run_time=.5)
        self.wait(0.2)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(pair2), run_time=.5)
        self.wait(0.2)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(pair3), Write(pair4), run_time=.5)
        self.wait()
        
        product_expr.move_to(ORIGIN).shift(UP * 0.5)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeOut(pairs),
                  FadeOut(a_matrix),
                  FadeIn(product_expr))
        self.wait()

        result_matrix.next_to(product_expr, DOWN, buff=0.5)
        
        self.play(
            product_expr[3].animate.set_color(ORANGE),
            product_expr[4].animate.set_color(PURPLE), 
        )
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(result_matrix))
        self.wait(3)
        self.play(FadeOut(result_matrix, product_expr))
        
        row_eq1 = MathTex("A A^T", "=", "(U \\Sigma V^T)", "(U \\Sigma V^T)^T", font_size=36)
        row_eq1.next_to(row_title, DOWN, buff=0.5)
        
        row_eq2 = MathTex("A A^T", "=", "U \\Sigma", "V^T V", "\\Sigma^T U^T", font_size=36)
        row_eq2.next_to(row_eq1, DOWN, buff=0.5)
        
        row_eq3 = MathTex("A A^T", "=", "U \\Sigma^2 U^T", font_size=40)
        row_eq3.next_to(row_eq2, DOWN, buff=0.7)
        row_eq3[2].set_color(BLUE) 
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(row_eq1))
        self.wait()
        self.add_sound("voiceovers/correct_answer_toy.mp3")
        self.play(TransformMatchingTex(row_eq1.copy(), row_eq2))
        self.wait()
        self.add_sound("voiceovers/A_AT_svd.mp3")
        
        brace_V = Brace(row_eq2[3], DOWN, color=YELLOW)
        brace_text_V = brace_V.get_text("$I$").set_color(YELLOW).scale(0.7)
        self.add_sound("voiceovers/writin.mp3")
        self.play(GrowFromCenter(brace_V), Write(brace_text_V))
        self.wait(2)
        self.add_sound("voiceovers/correct_answer_toy.mp3")
        self.play(
            TransformMatchingTex(row_eq2.copy(), row_eq3),
            FadeOut(brace_V), FadeOut(brace_text_V)
        )
        self.wait()
        self.title.add(row_eq3)
        self.play(*[
            FadeOut(mob) for mob in self.mobjects
            if mob not in self.title
        ], row_eq3.animate.move_to(ORIGIN))
        self.wait()
        self.add_sound("voiceovers/A_AT_explain.mp3")
        self.play(Flash(row_eq3[2][0]))
        self.wait()
        self.play(Flash(row_eq3[0]))
        self.wait()
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(row_eq3.animate.next_to(self.title[0], LEFT, LARGE_BUFF))
        self.wait()

    def construct(self):
        self.wait()
        self.add_sound("voiceovers/SVDCorrelations_title.mp3")
        title = Text("SVD: Mối tương quan \ngiữa các hàng và giữa các cột", font="Noto Sans")
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(title))
        self.wait()
        self.play(Unwrite(title))
        self.add_sound("voiceovers/rowsColumnsBridge.mp3")
        self.cleanScatter()
        self.highlightRowsAndColumns()
        self.rowsColumnsBridge()
        
        svd_eq = MathTex("A", "=", "U", "\\Sigma", "V^T", font_size=48).to_edge(UP)
        line = Line(LEFT * 6, RIGHT * 6, color=WHITE).set_stroke(width=3)
        line.next_to(svd_eq, DOWN, buff=0.1)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(svd_eq), Create(line))
        self.wait()
        self.title = VGroup(svd_eq, line)
        self.AT_A()
        self.A_AT()
        corn = ImageMobject("assets/corn.png").scale(0.4)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(corn))
        self.add_sound("voiceovers/sigma_explain.mp3")
        self.wait(2)
        self.play(Flash(self.title[2][-1]))
        self.wait()
        self.play(Flash(self.title[3][-1]))
        self.wait(2)
        self.play(ApplyWave(self.title[3]))
        self.play(ApplyWave(self.title[2]))
        self.wait(3)
class ThePhilosophyOfSVD(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/ThePhilosophyOfSVD.mp3")
        title = Text("Triết lý của SVD", font="Noto Sans", font_size=36, color=LIGHT_GREY).to_edge(UP).add_background_rectangle()
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(title, shift=DOWN*0.3))

        formula = MathTex("A", "=", "U", r"\Sigma", "V^T", font_size=72).add_background_rectangle()
        formula[3].set_color(BLUE)
        formula[4].set_color(YELLOW)
        formula[5].set_color(GREEN)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(formula), run_time=2)
        self.wait()
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(formula.animate.scale(0.7).next_to(title, DOWN, buff=0.5))

        plane = NumberPlane(
            x_range=[-5, 5], y_range=[-4, 4], 
            background_line_style={"stroke_opacity": 0.2, "stroke_color": DARK_GREY}
        ).set_stroke(opacity=0.3)
        
        circle = Circle(radius=1.5, color=WHITE, stroke_width=2)

        angle = 30 * DEGREES
        v1 = Vector([1.5 * np.cos(angle), 1.5 * np.sin(angle)], color=GREEN)
        v2 = Vector([-1.5 * np.sin(angle), 1.5 * np.cos(angle)], color=GREEN)
        
        v_label = Text("V: Góc nhìn tự nhiên", font="Noto Sans", font_size=20, color=GREEN).to_corner(DL)

        self.play(FadeIn(plane))
        self.add_sound("voiceovers/zipper-zip.mp3")
        self.play(Create(circle))
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(GrowArrow(v1), GrowArrow(v2), FadeIn(v_label))
        self.wait(2)

        matrix_A = [[1.5, 0.5], [0.5, 1.2]]
        
        ellipse = circle.copy().apply_matrix(matrix_A).set_color(BLUE)
        u1 = transform(v1, matrix_A).set_color(BLUE)
        u2 = transform(v2, matrix_A).set_color(BLUE)
        
        transform_text = Text("Mọi sự biến đổi lộn xộn...", font="Noto Sans", font_size=24).to_edge(DOWN)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(transform_text))
        self.add_sound("voiceovers/shooting-star.mp3")
        self.play(
            Transform(circle, ellipse),
            Transform(v1, u1),
            Transform(v2, u2),
            FadeOut(v_label),
            run_time=3,
            path_arc=0.2 
        )
        self.wait(1)

        right_angle = RightAngle(u1, u2, length=0.3, color=BLUE)
        
        sigma_text = Text("...có tính đối xứng hoàn hảo, tiềm ẩn.", font="Noto Sans", font_size=24, color=YELLOW).next_to(transform_text, UP, buff=0.5)
        self.add_sound("voiceovers/click.wav")
        self.play(
            u1.animate.set_color(BLUE),
            u2.animate.set_color(BLUE),
            Create(right_angle),
            Write(sigma_text)
        )
        self.wait(3)

        self.play(
            *[FadeOut(m) for m in self.mobjects if m != formula]
        )
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(formula.animate.move_to(ORIGIN).scale(1.5), run_time=2)
        
        final_quote = Text(
            "\"Dữ liệu có hình dạng.\nSVD tìm ra góc nhìn của nó.\"", font="Noto Sans", 
            font_size=36, slant=ITALIC, line_spacing=1.2, 
        ).next_to(formula, DOWN, buff=1.5)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(final_quote, shift=UP*0.2), run_time=2)
        self.wait(4)
        orbit_center = RIGHT * 7 + DOWN * 4

        symbols_tex = [
            r"\alpha", r"\beta", r"\gamma", r"\delta", r"\epsilon", r"\zeta", r"\eta",
            r"\theta", r"\iota", r"\kappa", r"\lambda", r"\mu", r"\nu", r"\xi",
            r"+", r"-", r"\times", r"\div", r"=", r"\neq", r"<", r">",
            r"\sqrt{2}", r"\int", r"\sum", r"\lim", r"\infty", r"\partial",
            r"\mathbb{N}", r"\mathbb{Z}", r"\mathbb{Q}", r"\mathbb{R}", r"\mathbb{C}",
            r"\forall", r"\exists", r"\in", r"\notin", r"\subset", r"\supset",
            r"\wedge", r"\vee", r"\neg", r"\implies", r"\iff", r"\bot", r"\top"
        ]

        num_orbits = 8
        radii = [2 + i * 0.8 for i in range(num_orbits)]
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK]
        speeds = [0.1 + i * 0.05 for i in range(num_orbits)] # Different rotation speeds
        spin_speeds = [0.5 + i * 0.2 for i in range(num_orbits)] # Different self-spin speeds
        num_symbols_per_orbit = [3, 4, 5, 8, 11, 14, 17, 23] # Total must match len(symbols_tex)
        speeds = [0.2 - i * 0.02 for i in range(num_orbits)] # Slower for outer orbits
        spin_speeds = [1.0 - i * 0.1 for i in range(num_orbits)] # Slower spin for outer orbits

        random.shuffle(symbols_tex)

        symbols_by_orbit = []
        start_index = 0
        for num in num_symbols_per_orbit:
            end_index = start_index + num
            symbols_by_orbit.append(symbols_tex[start_index:end_index])
            start_index = end_index
        all_symbols = VGroup()
        for i in range(num_orbits):
            orbit_symbols = VGroup()
            symbols_on_this_orbit = symbols_tex[i::num_orbits]
            num_symbols_on_orbit = len(symbols_on_this_orbit)
            
            for j, tex in enumerate(symbols_on_this_orbit):
                symbol = MathTex(tex, color=colors[i % len(colors)]).scale(0.8)
                angle = 2 * PI * j / num_symbols_on_orbit
                symbol.move_to(orbit_center + radii[i] * (np.cos(angle) * RIGHT + np.sin(angle) * UP))
                symbol.rotate(angle)
                orbit_symbols.add(symbol)

            def create_updater(orbit_group, radius, speed, spin_speed):
                def updater(mob, dt):
                    mob.rotate(speed * dt, about_point=orbit_center)
                    for submob in mob:
                        submob.rotate(-speed * dt)
                        submob.rotate(spin_speed * dt)
                return updater

            orbit_symbols.add_updater(create_updater(orbit_symbols, radii[i], speeds[i], spin_speeds[i]))
            all_symbols.add(orbit_symbols)        
        self.add(all_symbols)
        self.wait(10)
class SVDThumbnail(Scene):
    def construct(self):
        # Configuration: Adjusted n slightly to fit 3 squares comfortably
        m = 4.5
        n = 2.4 
        stroke_thickness = 6
        
        # --- Matrices ---
        matrix_a = Rectangle(width=n, height=m, color=GRAY_D, stroke_width=stroke_thickness, fill_opacity=0.5)
        eq_sign = MathTex("=", color=WHITE).scale(2.5)

        # U Matrix (m x m) - 4 columns
        u_cols = VGroup(*[
            Rectangle(width=m/4, height=m, color=BLUE_D, stroke_width=stroke_thickness, fill_opacity=0.5) 
            for _ in range(4)
        ]).arrange(RIGHT, buff=0.05)
        
        dot1 = MathTex(r"\cdot", color=WHITE).scale(2.5)

        # Sigma Matrix (m x n) - Now with 3 singular values
        sigma_outline = Rectangle(width=n, height=m, color=GRAY_A, stroke_width=stroke_thickness)
        
        # Calculate square size to fit 3 perfectly across the width n
        sq_size = n / 3
        sigma_diags = VGroup(*[
            Square(side_length=sq_size, color=YELLOW, stroke_width=stroke_thickness, fill_opacity=0.8).move_to(
                sigma_outline.get_corner(UL) 
                + RIGHT * (i * sq_size + sq_size/2) 
                + DOWN * (i * sq_size + sq_size/2)
            ) for i in range(3) # Changed to 3
        ])
        matrix_sigma = VGroup(sigma_outline, sigma_diags)

        dot2 = MathTex(r"\cdot", color=WHITE).scale(2.5)

        # V^T Matrix (n x n) - 3 horizontal rows
        vt_rows = VGroup(*[
            Rectangle(width=n, height=n/3, color=GREEN_D, stroke_width=stroke_thickness, fill_opacity=0.5) 
            for _ in range(3)
        ]).arrange(DOWN, buff=0.05)

        # --- Layout ---
        equation_elements = [matrix_a, eq_sign, u_cols, dot1, matrix_sigma, dot2, vt_rows]
        equation_core = VGroup(*equation_elements).arrange(RIGHT, buff=0.35, aligned_edge=DOWN)

        # Center math symbols vertically relative to the height of A/U
        for symbol in [eq_sign, dot1, dot2]:
            symbol.shift(UP * (m/2))

        # --- Labels ---
        def get_thumbnail_label(obj, name, size):
            label = VGroup(
                MathTex(name, color=WHITE).scale(1.8),
                # MathTex(size, color=GRAY_A).scale(1.0)
            ).arrange(DOWN, buff=0.2)
            label.next_to(obj, DOWN, buff=0.4)
            return label

        label_a = get_thumbnail_label(matrix_a, "A", "m \\times n")
        label_u = get_thumbnail_label(u_cols, "U", "m \\times m")
        label_sigma = get_thumbnail_label(matrix_sigma, r"\Sigma", "m \\times n")
        label_vt = get_thumbnail_label(vt_rows, "V^T", "n \\times n")

        # --- Final assembly ---
        full_vis = VGroup(equation_core, label_a, label_u, label_sigma, label_vt)
        full_vis.center().scale(0.9) # Slightly smaller scale to ensure labels aren't too close to edge

        self.add(full_vis)