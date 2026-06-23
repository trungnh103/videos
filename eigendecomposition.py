from manim import *
import numpy as np
import random

class IntroScene(Scene):
    def construct(self):    
        self.matrixOperations()
        self.blockMatrixDecomposition()
        self.factorization()
        self.add_sound("voiceovers/engineer.mp3")
        engineer = SVGMobject("assets/working-on-a-laptop.svg")
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(engineer))
        self.wait(2)
        self.play(FadeOut(engineer))
        self.magicCircle()
        self.wait()
    def floatingMatrices(self):
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
        self.add_sound("voiceovers/game-start.mp3")
        self.play(LaggedStart(*[FadeIn(m) for m in matrices], lag_ratio=0.2))

        for _ in range(3):
            animations = []
            for m in matrices:
                new_pos = [
                    random.uniform(-5, 5),
                    random.uniform(-3, 3),
                    0
                ]
                animations.append(m.animate.move_to(new_pos))
            self.add_sound("voiceovers/whoosh407576.mp3")
            self.play(*animations, run_time=.5)
        self.play(FadeOut(matrices))
    def bitGrid(self):
        rows = 10
        cols = 16
        spacing = 0.6
        grid = VGroup()
        for r in range(rows):
            row = VGroup()
            for c in range(cols):
                bit = Text(str(random.randint(0, 1)), font_size=36)
                bit.move_to([c * spacing, -r * spacing, 0])
                row.add(bit)
            grid.add(row)

        grid.move_to(ORIGIN)
        self.add(grid)

        def update_bits(mob, dt):
            for row in mob:
                for bit in row:
                    if random.random() < 0.08:  
                        new_val = str(random.randint(0, 1))
                        bit.become(Text(new_val, font_size=36).move_to(bit.get_center()))

        grid.add_updater(update_bits)
        self.wait(5)
        grid.remove_updater(update_bits)
        self.remove(grid)
    def matrixOperations(self):
        self.add_sound("voiceovers/matrixOperations.mp3")
        # self.floatingMatrices()
        self.bitGrid()
        # Step 1: Large matrix brackets
        brackets = MathTex(r"\begin{bmatrix} \quad \end{bmatrix}")
        brackets.scale(3)  # Make it bigger
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(brackets))
        self.wait(1.5)

        # Step 2: Inverse (-1) at upper-right corner
        inverse = MathTex(r"^{-1}")
        inverse.scale(1.5)
        inverse.move_to(brackets.get_corner(UR) + 0.5 * RIGHT + 0.3 * UP)
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(FadeIn(inverse))

        # Step 3: Diagonal line across matrix
        diag_line = Line(
            brackets.get_corner(UL),
            brackets.get_corner(DR),
            stroke_width=6,
            color=YELLOW
        ).scale(0.7)
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(Create(diag_line), FadeOut(inverse), run_time=.5)

        # Step 4: Transform inverse into exponent (e.g. ^2)
        exponent = MathTex(r"^{100}")
        exponent.scale(1.5)
        exponent.move_to(brackets.get_corner(UR) + 0.5 * RIGHT + 0.3 * UP)
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(FadeIn(exponent), FadeOut(diag_line))
        self.wait(.5)
        self.play(brackets.animate.set_color(RED), FadeOut(exponent))
        small_matrices = VGroup(
            MathTex(r"\begin{bmatrix} \quad \end{bmatrix}"),
            MathTex(r"\begin{bmatrix} \quad \end{bmatrix}"),
            MathTex(r"\begin{bmatrix} \quad \end{bmatrix}")
        ).set_color(RED)

        small_matrices.scale(3)

        for m in small_matrices:
            m.move_to(brackets.get_center())

        self.add_sound("voiceovers/click.wav")
        self.play(ReplacementTransform(brackets, small_matrices))

        self.play(
            small_matrices.animate.scale(0.5).set_color(BLUE).arrange(RIGHT, buff=1.5).move_to(ORIGIN),
            run_time=3
        )
        self.wait(3)
        self.play(FadeOut(small_matrices))
        matrix_factorization_text = Text("Phân tích nhân tử ma trận", font="Noto Sans")
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(matrix_factorization_text))
        self.wait(4)
        self.play(FadeOut(matrix_factorization_text))
    def magicCircle(self):
        circle = Circle(radius=2, color=PURPLE)
        circle.set_stroke(width=6)
        symbols = VGroup(*[
            Star(n=5, color=BLUE).scale(0.3).move_to(
                circle.point_at_angle(i * TAU / 6)
            )
            for i in range(6)
        ])
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(Create(circle))
        self.add_sound("voiceovers/game-start.mp3")
        self.play(LaggedStart(*[FadeIn(s) for s in symbols]), lag_ratio=0.2)
        self.add_sound("voiceovers/twinklesparkle.mp3")
        self.play(
            Rotate(symbols, angle=TAU, run_time=2),
            circle.animate.set_color(GOLD),
            rate_func=linear
        )
        self.wait()
    def blockMatrixDecomposition(self):
        self.add_sound("voiceovers/blockMatrixDecomposition.mp3")
        title = Text("Phân tích giá trị riêng", color=YELLOW, font="Noto Sans")
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(title))
        self.wait(3)
        matrix = Matrix([
            ["a", "b", "c"],
            ["d", "e", "f"],
            ["g", "h", "i"]
        ])
        # matrix.scale(1.2)
        matrix.shift(UP)
        self.add_sound("voiceovers/click.wav")
        self.play(title.animate.to_edge(UP), Create(matrix))
        self.wait(0.5)

        colors = [RED, GREEN, BLUE]

        blocks = VGroup()
        for i, color in enumerate(colors):
            rect = Rectangle(width=2, height=1)
            rect.set_stroke(color, width=3)
            rect.set_fill(color, opacity=0.2)
            blocks.add(rect)

        blocks.arrange(RIGHT, buff=1)
        blocks.next_to(matrix, DOWN, buff=2)

        lines = VGroup()
        for i, block in enumerate(blocks):
            start = matrix.get_bottom() + (i - 1) * RIGHT * 1.2
            end = block.get_top()

            line = Line(start, end, buff=0.1)
            lines.add(line)
        self.add_sound("voiceovers/click.wav")
        self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.2),
                  LaggedStart(*[Create(b) for b in blocks], lag_ratio=0.3))
        self.wait()
        self.play(FadeOut(matrix, lines, blocks))
    def factorization(self):
        self.add_sound("voiceovers/factorization.mp3")
        number = MathTex("30")
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(number))
        self.wait(1)

        equation = MathTex("30", "=", "2", r"\times", "3", r"\times", "5")
        equation.move_to(number)
        self.add_sound("voiceovers/click.wav")
        self.play(TransformMatchingTex(number, equation))
        self.wait(2)

        factors = [equation[2], equation[4], equation[6]]
        for factor in factors:
            self.play(Indicate(factor, scale_factor=1.5, color=YELLOW))
            self.wait(0.5)
        self.wait()
        self.play(FadeOut(equation))
        eigenvalues = Text("Giá trị riêng", font="Noto Sans", color=PINK).scale(0.8).shift(LEFT * 2)
        eigenvectors = Text("Vectơ riêng", font="Noto Sans", color=YELLOW).scale(0.8).shift(RIGHT * 2)
        eigen_group = VGroup(eigenvectors, eigenvalues).arrange(RIGHT, LARGE_BUFF)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(eigenvectors))
        self.wait()
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(eigenvalues))
        self.wait(.5)
        self.play(FadeOut(eigen_group))
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
        title_diag = Text("1. Ma trận chéo: Co giãn thuần túy", font="Noto Sans").scale(0.7).to_edge(UP)
        
        grid = NumberPlane(background_line_style={"stroke_opacity": 0.3})
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
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(
            group_diag.animate.apply_matrix(L_matrix),
            Transform(i_hat, i_hat_new),
            Transform(j_hat, j_hat_new),
            run_time=5,
            rate_func=smooth
        )
        self.wait(2)
        self.play(FadeOut(group_diag, j_hat, i_hat), FadeOut(title_diag), FadeOut(diag_overlay))

        title_ortho = Text("2. Ma trận trực giao: Phép quay cứng", font="Noto Sans").scale(0.7).to_edge(UP)
        grid_2 = NumberPlane(background_line_style={"stroke_opacity": 0.3})
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
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(
            group_ortho.animate.apply_matrix(Q_matrix),
            run_time=5,
            rate_func=smooth
        )
        self.wait(2)
class Eigenvectors(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/Eigenvectors.mp3")
        title = Text("Các thành phần cơ bản: \nVectơ riêng và giá trị riêng",
                     font="Noto Sans").add_background_rectangle()
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(title))
        self.wait()
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(title.animate.scale(0.8).to_edge(UP))
        self.wait(3)
        plane = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            },
        )
        self.play(Create(plane))
        self.wait()
        self.change_direction()
        self.stay_on_span()
        self.play(FadeOut(plane), run_time=.5)
        self.eigenEquation()
        self.wait(4)
    def change_direction(self):
        A = np.array([[1, 1],
                      [0.5, 1]])
        A_display = np.round(A, 2)

        matrix_tex = Matrix(A_display).shift(3.5*LEFT+1.5*UP).add_background_rectangle()
        matrix_label = MathTex("A =").next_to(matrix_tex, LEFT)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(matrix_label), Create(matrix_tex))
        self.wait(3)
        v1 = np.array([2, 1, 0])
        v2 = np.array([-1, -2, 0])

        vec1 = Vector(v1, color=BLUE)
        vec2 = Vector(v2, color=GREEN)
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(GrowArrow(vec1), GrowArrow(vec2))

        def full_span_line(direction, color):
            d = direction / np.linalg.norm(direction)
            return Line(
                start=-10 * d,
                end=10 * d,
                color=color
            ).set_opacity(0.3)

        line1 = full_span_line(v1, BLUE)
        line2 = full_span_line(v2, GREEN)
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(Create(line1), Create(line2))
        self.wait()
        
        def transform(v):
            res = A @ v[:2]
            return np.array([res[0], res[1], 0])

        v1_new = transform(v1)
        v2_new = transform(v2)

        vec1_new = Vector(v1_new, color=YELLOW)
        vec2_new = Vector(v2_new, color=RED)
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(
            Transform(vec1, vec1_new),
            Transform(vec2, vec2_new),
            run_time=3
        )
        self.wait()
        self.play(FadeOut(vec1, vec2, line1, line2, matrix_label, matrix_tex))

    def stay_on_span(self):
        P = np.array([[2, -1],
                      [1,  2]])

        D = np.array([[2, 0],
                      [0, 0.5]])
        A = P @ D @ np.linalg.inv(P)

        A_display = np.round(A, 2)

        matrix_tex = Matrix(A_display).shift(3.5*LEFT+1.5*UP).add_background_rectangle()
        matrix_label = MathTex("A =").next_to(matrix_tex, LEFT)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(matrix_label), Create(matrix_tex))

        self.wait()
        v1 = np.array([2, 1, 0])
        v2 = np.array([-1, 2, 0])

        vec1 = Vector(v1, color=BLUE)
        vec2 = Vector(v2, color=GREEN)
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(GrowArrow(vec1), GrowArrow(vec2))

        def full_span_line(direction, color):
            d = direction / np.linalg.norm(direction)
            return Line(-10 * d, 10 * d, color=color).set_opacity(0.3)

        line1 = full_span_line(v1, BLUE)
        line2 = full_span_line(v2, GREEN)
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(Create(line1), Create(line2))

        def transform(v):
            res = A @ v[:2]
            return np.array([res[0], res[1], 0])

        v1_new = transform(v1)
        v2_new = transform(v2)

        vec1_new = Vector(v1_new, color=YELLOW)
        vec2_new = Vector(v2_new, color=RED)
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(
            Transform(vec1, vec1_new),
            Transform(vec2, vec2_new),
            run_time=3
        )
        self.wait(.5)
        self.play(FadeOut(vec1, vec2, matrix_label, matrix_tex, line1, line2), run_time=.5)
    def eigenEquation(self):
        equation = MathTex(
            "A", r"\,", r"\vec{v}", r"=", r"\lambda", r"\vec{v}"
        )

        equation[2].set_color(YELLOW)       
        equation[4].set_color(PINK)    
        equation[5].set_color(YELLOW)

        v_text = Text(
            "Vectơ riêng (v) — giữ nguyên hướng ban đầu",
            color=YELLOW, font="Noto Sans",
            font_size=28
        )
        v_text.next_to(equation, DOWN, buff=0.8)
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(v_text, shift=UP))
        self.wait(3)

        lambda_text = Text(
            "Giá trị riêng (λ) — hệ số tỷ lệ",
            color=PINK, font="Noto Sans",
            font_size=28
        )
        lambda_text.next_to(v_text, DOWN, buff=0.5)
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(lambda_text, shift=UP))
        self.wait(4)
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(equation, shift=UP))
        self.wait(3)
        box = SurroundingRectangle(equation, color=BLUE)
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(Create(box))
class Eigendecomposition(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/Eigendecomposition.mp3")
        title = Text("Công thức phân tích giá trị riêng", font="Noto Sans", font_size=48, color=BLUE).to_edge(UP)
        self.title = title
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(title))
        self.wait()
        self.matrixEigenvectors()
        self.wait()
        self.define()
        self.wait()
    def matrixEigenvectors(self):
        matrix_A = Matrix([
            ["a_{11}", "a_{12}", "...", "a_{1n}"],
            ["a_{21}", "a_{22}", "...", "a_{2n}"],
            ["\\vdots", "\\vdots", "\\ddots", "\\vdots"],
            ["a_{n1}", "a_{n2}", "...", "a_{nn}"]
        ])
        matrix_A.scale(0.8)
        matrix_A.to_edge(LEFT)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(matrix_A))
        self.wait(1)

        eigen_eq = MathTex(
            "A ", 
            "v_i", 
            "=", 
            "\\lambda_i", 
            " ", 
            "v_i", 
            ", \\quad i=1,2,\\dots,n"
        )
        eigen_eq.next_to(matrix_A, RIGHT, buff=1)

        eigen_eq.set_color_by_tex("v_i", YELLOW)
        eigen_eq.set_color_by_tex("\\lambda_i", PINK)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(eigen_eq))
        self.wait(4)
        self.play(FadeOut(matrix_A, eigen_eq))
    def define(self):
        formula = MathTex("A", "=", "Q", r"\Lambda", "Q^{-1}", font_size=60)
        formula.next_to(self.title, DOWN, buff=1.0)

        # Color coding
        formula[2].set_color(BLUE)      # Q
        formula[3].set_color(YELLOW)    # Λ
        formula[4].set_color(GREEN)     # Q⁻¹
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(formula), run_time=4)
        self.wait()
        self.play(Indicate(formula[0], color=WHITE))
        self.wait()
        q_matrix = MathTex(
            r"Q = \begin{bmatrix} \mathbf{v}_1 & \mathbf{v}_2 & \cdots & \mathbf{v}_n \end{bmatrix}",
            font_size=36
        ).next_to(formula, DOWN, buff=1)
        q_matrix.set_color(BLUE)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(q_matrix))
        self.wait(3)
        lambda_matrix = MathTex(
            r"\Lambda = \begin{bmatrix}\lambda_1 & 0 & \cdots & 0 \\ 0 & \lambda_2 & \cdots & 0 \\ \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & \cdots & \lambda_n\end{bmatrix}",
            font_size=36
        ).next_to(q_matrix, DOWN, buff=.5)
        lambda_matrix.set_color(YELLOW)
        self.play(Write(lambda_matrix))
        self.wait(4)
        self.play(Indicate(formula[4], color=GREEN))
        self.wait(4)

def transform(v, matrix, threeD=False):
            end = v.get_end()        
            if threeD:
                res = matrix @ end
            else:
                res = matrix @ end[:2]
            v_new = np.array([res[0], res[1], 0])
            return Vector(v_new, color=v.get_color())
class EigendecompositionVisual(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/EigendecompositionVisual.mp3")
        title = Text("Trực giác hình học (Quy trình \"ba bước\")", 
                     font="Noto Sans", gradient=[BLUE, YELLOW, GREEN])
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(title))
        self.wait()
        self.play(FadeOut(title))
        Q_matrix = np.array([[1., 1., 0.], 
                             [0., 1., 0.],
                             [0., 0., 1.]])
        
        Lambda_matrix = np.array([[2., 0., 0.], 
                             [0., 3., 0.],
                             [0., 0., 1.]])
        
        Q_inv_matrix = np.linalg.inv(Q_matrix)
        A_matrix = Q_matrix @ Lambda_matrix @ Q_inv_matrix

        bg_plane = NumberPlane(
            background_line_style={"stroke_opacity": 0.2}
        ).add_coordinates()
        
        moving_plane = NumberPlane(
            faded_line_ratio=0,
            background_line_style={"stroke_opacity": 0.6, "stroke_color": BLUE}
        )

        v1 = Vector([1, 0], color=YELLOW)
        v2 = Vector([1, 1], color=PINK)
        
        v1_label = MathTex("\\vec{v}_1").next_to(v1.get_end(), DOWN)
        v2_label = MathTex("\\vec{v}_2").next_to(v2.get_end(), UP)
        
        equation = MathTex(
            "A", "=", "Q", r"\Lambda", "Q^{-1}"
        ).to_corner(UL).add_background_rectangle()
        equation[1].set_color(WHITE) 
        equation[3].set_color(BLUE)  
        equation[4].set_color(YELLOW) 
        equation[5].set_color(GREEN)   
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(equation))
        self.wait()
        self.play(FadeIn(bg_plane), Create(moving_plane))
        self.wait(4)
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(GrowArrow(v1), FadeIn(v1_label))
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(GrowArrow(v2), FadeIn(v2_label))
        self.wait()

        step1_label = Text("1. Áp dụng Q⁻¹ (Thay đổi góc nhìn)", font_size=24, color=GREEN,
                           font="Noto Sans").add_background_rectangle().shift(2*UP+3*LEFT)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(step1_label))

        vec1_new = transform(v1, Q_inv_matrix, threeD=True)
        vec2_new = transform(v2, Q_inv_matrix, threeD=True)
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(
            moving_plane.animate.apply_matrix(Q_inv_matrix),
            Transform(v1, vec1_new),
            Transform(v2, vec2_new),
            v1_label.animate.next_to(Q_inv_matrix @ v1.get_end(), DOWN),
            v2_label.animate.next_to(Q_inv_matrix @ v2.get_end(), RIGHT),
            run_time=7
        )
        self.wait(4)

        step2_label = Text("2. Áp dụng Λ (Tác động cốt lõi)", font_size=24, color=YELLOW,
                           font="Noto Sans").add_background_rectangle().next_to(step1_label, DOWN, aligned_edge=LEFT)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(step2_label))
        self.wait(2)

        vec1_new = transform(v1, Lambda_matrix, threeD=True)
        vec2_new = transform(v2, Lambda_matrix, threeD=True)
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(
            moving_plane.animate.apply_matrix(Lambda_matrix),
            Transform(v1, vec1_new),
            Transform(v2, vec2_new),
            v1_label.animate.next_to((Lambda_matrix @ Q_inv_matrix) @ np.array([1, 0, 0]), DOWN),
            v2_label.animate.next_to((Lambda_matrix @ Q_inv_matrix) @ np.array([1, 1, 0]), RIGHT),
            run_time=7
        )
        self.wait(4)

        step3_label = Text("3. Áp dụng Q (Trở về trạng thái \nbình thường)", font_size=24, color=BLUE,
                           font="Noto Sans").add_background_rectangle().next_to(step2_label, DOWN, aligned_edge=LEFT)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(step3_label))

        vec1_new = transform(v1, Q_matrix, threeD=True)
        vec2_new = transform(v2, Q_matrix, threeD=True)
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(
            moving_plane.animate.apply_matrix(Q_matrix),
            Transform(v1, vec1_new),
            Transform(v2, vec2_new),
            v1_label.animate.next_to(A_matrix @ np.array([1, 0, 0]), DOWN),
            v2_label.animate.next_to(A_matrix @ np.array([1, 1, 0]), UP),
            run_time=5
        )
        
        final_label = Text("Tương đương với việc áp dụng trực tiếp A", font_size=24, color=YELLOW,
                           font="Noto Sans").add_background_rectangle().next_to(step3_label, DOWN, buff=1, aligned_edge=LEFT)
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(FadeIn(final_label), Indicate(equation[1]))
        self.wait(2)
class DeriveEigendecomposition(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/DeriveEigendecomposition.mp3")
        title = Text("Suy ra phép phân tích giá trị riêng", font="Noto Sans", font_size=40).to_edge(UP)
        fundamental = MathTex("A", "\\vec{v}", "=", "\\lambda", "\\vec{v}")
        fundamental.set_color_by_tex("\\vec{v}", YELLOW)
        fundamental.set_color_by_tex("\\lambda", PINK)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(title))
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(fundamental))
        self.wait()
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(fundamental.animate.shift(UP * 1.5))

        eq1 = MathTex("A", "\\vec{v}_{1}", "=", "\\lambda_{1}", "\\vec{v}_{1}")
        eq2 = MathTex("A", "\\vec{v}_{2}", "=", "\\lambda_{2}", "\\vec{v}_{2}")
        
        eq1.set_color_by_tex_to_color_map({"v_{1}": YELLOW, "lambda_{1}": PINK})
        eq2.set_color_by_tex_to_color_map({"v_{2}": YELLOW, "lambda_{2}": PINK})

        eqs = VGroup(eq1, eq2).arrange(DOWN)
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(TransformMatchingShapes(fundamental.copy(), eq1))
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(TransformMatchingShapes(fundamental.copy(), eq2))
        self.wait()

        ap_side = MathTex("A", "\\underbrace{[\\vec{v}_1 \\quad \\vec{v}_2]}_{Q}", "=")
        ap_side.set_color_by_tex("v", YELLOW)
        
        pd_side = MathTex("\\underbrace{[\\vec{v}_1 \\quad \\vec{v}_2]}_{Q}", 
                          "\\underbrace{\\begin{bmatrix} \\lambda_1 & 0 \\\\ 0 & \\lambda_2 \\end{bmatrix}}_{\Lambda}")
        pd_side.set_color_by_tex("v", YELLOW)
        pd_side.set_color_by_tex("\\lambda", PINK)
        
        full_eq = VGroup(ap_side, pd_side).arrange(RIGHT).shift(DOWN * 1.5)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(ap_side))
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(pd_side))
        self.wait(2)

        final_ap_pd = MathTex("A", "Q", "=", "Q", r"\Lambda").scale(1.5).shift(DOWN * 1.5)
        final_ap_pd.set_color_by_tex("Q", YELLOW)
        final_ap_pd.set_color_by_tex(r"\Lambda", PINK)
        self.add_sound("voiceovers/click.wav")
        self.play(
            FadeOut(ap_side), FadeOut(pd_side),
            FadeIn(final_ap_pd)
        )
        self.play(Indicate(final_ap_pd))
        self.wait(1)

        result = MathTex("A", "=", "Q", r"\Lambda", "Q^{-1}").scale(1.5).shift(DOWN * 1.5)
        result.set_color_by_tex("Q", YELLOW)
        result.set_color_by_tex(r"\Lambda", PINK)

        box = SurroundingRectangle(result, color=BLUE, buff=MED_SMALL_BUFF)
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(TransformMatchingTex(final_ap_pd, result))
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(Create(box)) 
        self.wait(2)
class FullEigendecompositionPower(Scene):
    def questionAnswer(self):
        question = Text("Tại sao lại phải mất công phân tích ma trận? ", font="Noto Sans", font_size=36)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(question))
        self.wait(.5)
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(question.animate.to_edge(UP))
        answer = Text("Bởi vì nó giúp cho những phép toán cực kỳ khó \ntrở nên rất dễ.", font="Noto Sans", font_size=36, color=GREEN)
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(FadeIn(answer, shift=DOWN))
        self.wait()
        self.play(FadeOut(question, answer))
    def markov(self):
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
        
        markov_group = VGroup(nodes, labels, prob_group).scale(0.6).to_edge(LEFT, LARGE_BUFF).to_edge(UP)
        self.add_sound("voiceovers/game-start.mp3")
        self.play(Create(nodes), Write(labels), FadeIn(prob_group))
        self.wait()
        eq1 = MathTex(r"\pi_{n+1} = \pi_n P").scale(1.2).to_edge(UP)
        eq1[0][:4].set_color(YELLOW)
        eq1[0][5:-1].set_color(YELLOW)
        eq1[0][-1].set_color(BLUE)
        eq2 = MathTex(r"\pi_n = \pi_0 P^n").scale(1.2).next_to(eq1, DOWN)
        eq2[0][:2].set_color(YELLOW)
        eq2[0][3:5].set_color(YELLOW)
        eq2[0][-2:].set_color(BLUE)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(eq1, eq2))
        self.wait(4)
        self.play(FadeOut(markov_group, eq1, eq2))
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/a_power.mp3")
        self.questionAnswer()
        c_map = {"A": WHITE, "Q": BLUE, "L": YELLOW, "Qi": GREEN, "I": WHITE}
        
        # 2. Part 1: The Algebraic Chain (A^n -> Q L^n Q-1)
        step1 = MathTex("A", "^n").set_color_by_tex("A", c_map["A"])
        
        step2 = MathTex("(", "Q", "\\Lambda", "Q^{-1}", ")", "^n")
        step2.set_color_by_tex("Q", c_map["Q"]).set_color_by_tex("\\Lambda", c_map["L"]).set_color_by_tex("Q^{-1}", c_map["Qi"])

        step3 = MathTex(
            "Q", "\\Lambda", "Q^{-1}", "Q", "\\Lambda", "Q^{-1}", "\\dots", "Q", "\\Lambda", "Q^{-1}"
        )
        for i in [0, 3, 7]: step3[i].set_color(c_map["Q"])
        for i in [1, 4, 8]: step3[i].set_color(c_map["L"])
        for i in [2, 5, 9]: step3[i].set_color(c_map["Qi"])

        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(step1))
        self.wait(3)
        self.markov()
        
        self.wait(0.5)
        self.add_sound("voiceovers/click.wav")
        self.play(ReplacementTransform(step1, step2))
        self.wait(0.5)
        self.add_sound("voiceovers/click.wav")
        self.play(ReplacementTransform(step2, step3))
        
        brace = Brace(step3[2:4], DOWN, buff=0.1)
        i_label = brace.get_text("$I$").set_color(WHITE)
        self.add_sound("voiceovers/click.wav")
        self.play(Create(brace), Write(i_label))
        self.play(step3[2:4].animate.set_opacity(0.3))
        self.wait()

        step4 = MathTex("Q", "\\Lambda^n", "Q^{-1}").scale(1.2)
        step4[0].set_color(c_map["Q"])
        step4[1].set_color(c_map["L"])
        step4[2].set_color(c_map["Qi"])
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(
            FadeOut(brace, i_label),
            ReplacementTransform(step3, step4)
        )
        self.wait(2)
        self.add_sound("voiceovers/lambda_diagonal.mp3")
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(step4.animate.to_edge(UP, buff=1))
        
        l_start = Matrix([["\\lambda_1", "0"], ["0", "\\lambda_2"]]).scale(0.8)
        l_start.get_brackets().set_color(YELLOW)
        
        l_expr_start = VGroup(l_start, MathTex("^n")).arrange(RIGHT, buff=0.1)
        l_expr_start[1].shift(0.8*UP)
        l_expr_start.next_to(step4, DOWN, buff=1.5)

        l_end = Matrix([["\\lambda_1^n", "0"], ["0", "\\lambda_2^n"]]).scale(0.8)
        l_end.get_brackets().set_color(YELLOW)
        l_end.move_to(l_expr_start)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(l_expr_start))
        self.play(Indicate(step4[1])) 
        self.wait(1)
        self.add_sound("voiceovers/click.wav")
        self.play(ReplacementTransform(l_expr_start, l_end))
        
        hundred_label = Text("Ngay cả khi n = 100", font="Noto Sans", font_size=24, color=GRAY).next_to(l_end, DOWN, buff=0.5)
        l_100 = Matrix([["\\lambda_1^{100}", "0"], ["0", "\\lambda_2^{100}"]]).scale(0.8).move_to(l_end)
        l_100.get_brackets().set_color(YELLOW)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(hundred_label))
        self.add_sound("voiceovers/click.wav")
        self.play(ReplacementTransform(l_end, l_100))
        
        final_rect = SurroundingRectangle(VGroup(step4, l_100), color=BLUE, buff=0.4)
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(Create(final_rect))
        self.wait(4)
class Rect(RoundedRectangle):
    def __init__(self, **kwargs):
        super().__init__(corner_radius=0.1, **kwargs)
class SymmetricMatrixExplanation(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/SymmetricMatrixExplanation.mp3")
        title = Text("Ma trận đối xứng", gradient=[BLUE, YELLOW, BLUE], font="Noto Sans").scale(0.8).to_edge(UP)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(title))
        self.wait(3)
        subtitle = MathTex("A", "=", "A^T")
        subtitle.next_to(title, DOWN)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(subtitle))
        self.wait()

        matrix_data = [
            [1, -2, 4],
            [-2, 0, 7],
            [4, 7, 9]
        ]
        matrix_a = Matrix(matrix_data)

        label_a = MathTex("A = ")
        group_a = VGroup(label_a, matrix_a).arrange(RIGHT)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(group_a))
        self.wait()
        entries = matrix_a.get_entries()
        diag_entries = VGroup(entries[0], entries[4], entries[8])
        self.add_sound("voiceovers/click.wav")
        self.play(diag_entries.animate.set_color(YELLOW))
        
        diag_line = DashedLine(
            entries[0].get_corner(UL) + UP*0.2 + LEFT*0.2,
            entries[8].get_corner(DR) + DOWN*0.2 + RIGHT*0.2,
            color=YELLOW
        )
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(Create(diag_line))
        self.wait(.5)

        pair_1 = VGroup(entries[1], entries[3])
        pair_2 = VGroup(entries[2], entries[6])
        pair_3 = VGroup(entries[5], entries[7])
        self.add_sound("voiceovers/click.wav")
        self.play(pair_1.animate.set_color(TEAL),
                  pair_2.animate.set_color(ORANGE),
                  pair_3.animate.set_color(MAROON))
        self.wait(.5)
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(
            Swap(entries[1], entries[3]),
            path_arc=PI/2,
            run_time=.5
        )
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(
            Swap(entries[2], entries[6]),
            path_arc=PI/2,
            run_time=.5
        )
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(
            Swap(entries[5], entries[7]),
            path_arc=PI/2,
            run_time=.5
        )
        self.wait()

        label_at = MathTex("A^T = ").move_to(label_a, aligned_edge=RIGHT)
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(Transform(label_a, label_at))
        self.wait(2)

class ConstructOrthogonalMatrix(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/ConstructOrthogonalMatrix.mp3")
        V_COLOR = YELLOW
        Q_COLOR = '#00FFFF'
        V2_COLOR = PINK
        Q2_COLOR = LIGHT_PINK
        
        bg_plane = NumberPlane(
            background_line_style={"stroke_opacity": 0.2}
        ).add_coordinates()
        
        unit_circle = Circle(radius=1.0, color=WHITE).set_style(stroke_opacity=0.6)

        v1_coords = np.array([2.0, 1.0, 0.0])
        v2_coords = np.array([-1.5, 3.0, 0.0]) 
        
        v1 = Arrow(ORIGIN, v1_coords, buff=0, color=V_COLOR)
        v2 = Arrow(ORIGIN, v2_coords, buff=0, color=V2_COLOR)
        
        v1_label = MathTex("\\vec{v}_1").next_to(v1.get_end(), DOWN)
        v2_label = MathTex("\\vec{v}_2").next_to(v2.get_end(), LEFT)
        v1_label.set_color(V_COLOR)
        v2_label.set_color(V2_COLOR)

        right_angle = RightAngle(v1, v2, length=0.3, quadrant=(1,1))
        
        eq_q1 = MathTex("\\vec{q}_1", "=", "\\frac{\\vec{v}_1}{\\|\\vec{v}_1\\|}").to_corner(UL).shift(DOWN * 0.5)
        eq_q2 = MathTex("\\vec{q}_2", "=", "\\frac{\\vec{v}_2}{\\|\\vec{v}_2\\|}").next_to(eq_q1, DOWN, aligned_edge=LEFT)

        eq_q1[0].set_color(Q_COLOR)
        eq_q1[2][:3].set_color(V_COLOR)
        eq_q1[2][4:].set_color(V_COLOR)
        eq_q2[0].set_color(Q2_COLOR)
        eq_q2[2][:3].set_color(V2_COLOR)
        eq_q2[2][4:].set_color(V2_COLOR)

        matrix_Q = MathTex(
            "Q", "=", "\\begin{bmatrix} | & | \\\\ \\vec{q}_1 & \\vec{q}_2 \\\\ | & | \\end{bmatrix}"
        ).to_corner(UR).shift(DOWN * 0.5)
        matrix_Q[2][4:7].set_color(Q_COLOR)
        matrix_Q[2][7:10].set_color(Q2_COLOR)

        property_Q = MathTex("Q^{-1} = Q^T").next_to(matrix_Q, DOWN, buff=0.5)
        property_Q.set_color(YELLOW)
        property_box = SurroundingRectangle(property_Q, color=YELLOW, buff=MED_SMALL_BUFF)
        
        self.play(FadeIn(bg_plane))
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(GrowArrow(v1), GrowArrow(v2), FadeIn(v1_label), FadeIn(v2_label))
        self.add_sound("voiceovers/click.wav")
        self.play(Create(right_angle))
        self.wait()
        self.add_sound("voiceovers/click.wav")
        self.play(Create(unit_circle))
        self.wait()
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(eq_q1))
        
        q1_coords = v1_coords / np.linalg.norm(v1_coords)
        q1_arrow = Arrow(ORIGIN, q1_coords, buff=0, color=Q_COLOR)
        q1_label = MathTex("\\vec{q}_1").next_to(q1_arrow.get_end(), DOWN).set_color(Q_COLOR)
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(
            Transform(v1, q1_arrow),
            Transform(v1_label, q1_label),
            right_angle.animate.become(RightAngle(q1_arrow, v2, length=0.3, quadrant=(1,1)))
        )
        self.wait()
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(eq_q2))
        
        q2_coords = v2_coords / np.linalg.norm(v2_coords)
        q2_arrow = Arrow(ORIGIN, q2_coords, buff=0, color=Q2_COLOR)
        q2_label = MathTex("\\vec{q}_2").next_to(q2_arrow.get_end(), LEFT).set_color(Q2_COLOR)
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(
            Transform(v2, q2_arrow),
            Transform(v2_label, q2_label),
            right_angle.animate.become(RightAngle(q1_arrow, q2_arrow, length=0.3, quadrant=(1,1)))
        )
        self.wait(2)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(matrix_Q))
        self.wait(4)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(property_Q))
        self.wait(3)
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(Create(property_box))
        self.wait(3)
class SymmetricTransition(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/SymmetricTransition1.mp3")
        color_a = WHITE
        color_q = BLUE
        color_l = YELLOW
        color_inv_trans = GREEN

        eq_standard = MathTex("A", "=", "Q", "\\Lambda", "Q^{-1}").scale(1.2)
        eq_standard[0].set_color(color_a)
        eq_standard[2].set_color(color_q)
        eq_standard[3].set_color(color_l)
        eq_standard[4].set_color(color_inv_trans)

        eq_upgraded = MathTex("A", "=", "Q", "\\Lambda", "Q^T").scale(1.2)
        eq_upgraded[0].set_color(color_a)
        eq_upgraded[2].set_color(color_q)
        eq_upgraded[3].set_color(color_l)
        eq_upgraded[4].set_color(color_inv_trans)
        
        property_math = MathTex("Q^{-1}", "=", "Q^T").scale(1.2)
        property_math[0].set_color(color_inv_trans)
        property_math[2].set_color(color_inv_trans)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(eq_standard))
        self.wait()
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(eq_standard.animate.to_edge(UP, buff=1.5))
        self.wait()
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(property_math))
        self.play(
            Indicate(property_math[0]), 
            Indicate(property_math[2])
        )
        self.wait(.5)

        eq_upgraded.move_to(eq_standard) # Ensure it aligns perfectly
        self.add_sound("voiceovers/SymmetricTransition2.mp3")
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(
            ReplacementTransform(property_math[2].copy(), eq_upgraded[4]),
            ReplacementTransform(eq_standard[0:4], eq_upgraded[0:4]),
            FadeOut(eq_standard[4]),
            FadeOut(property_math),
            run_time=2
        )
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(eq_upgraded.animate.center())
        
        box = SurroundingRectangle(eq_upgraded, color=color_inv_trans, buff=0.3)
        label = Text("Đơn giản hóa tính toán!", font="Noto Sans", color=GREEN, font_size=32).next_to(box, DOWN, buff=0.5)
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(Create(box))
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(label))
        self.wait()
        q_inverse = MathTex("Q^{-1}").scale(1.2).move_to(eq_standard[4])
        cross = Cross(q_inverse)
        self.play(FadeIn(q_inverse))
        self.play(Create(cross))
        self.wait()
        self.play(FadeOut(q_inverse, cross))
        self.wait()
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(Flash(eq_upgraded[4]))
        self.wait(3)
class SpectralSequence(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/SpectralSequence.mp3")
        inv_sqrt2 = 1 / np.sqrt(2)
        Q = np.array([[inv_sqrt2, -inv_sqrt2], 
                      [inv_sqrt2,  inv_sqrt2]])
        Q_T = Q.T
        
        Lambda = np.array([[4, 0], 
                           [0, 2]])

        plane = NumberPlane(
            x_range=[-8, 8, 1],
            y_range=[-8, 8, 1],
            background_line_style={"stroke_opacity": 0.3}
        )
        circle = Circle(radius=1, color=TEAL).set_fill(TEAL, opacity=0.3)
        vec_1 = Vector([inv_sqrt2, inv_sqrt2], color=YELLOW)
        vec_2 = Vector([-inv_sqrt2, inv_sqrt2], color=PINK)
        transformable_group = VGroup(plane, circle, vec_1, vec_2)
        equation = MathTex("A", "=", "Q", "\\Lambda", "Q^T"
                           ).to_edge(UP).shift(3*LEFT).scale(1.5)
        
        self.play(Create(plane))
        self.add_sound("voiceovers/click.wav")
        self.play(Create(circle))
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(GrowArrow(vec_1))
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(GrowArrow(vec_2))
        self.wait()
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(equation))
        self.wait()
        self.add_sound("voiceovers/click.wav")
        self.play(equation[4].animate.set_color(GREEN)) 
        vec1_new = transform(vec_1, Q_T)
        vec2_new = transform(vec_2, Q_T)
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(
            circle.animate.apply_matrix(Q_T),
            Transform(vec_1, vec1_new),
            Transform(vec_2, vec2_new),
            run_time=2,
            rate_func=smooth
        )
        self.wait()
        self.play(equation[4].animate.set_color(WHITE))
        self.add_sound("voiceovers/click.wav")
        self.play(equation[3].animate.set_color(YELLOW)) 
        vec1_new = transform(vec_1, Lambda)
        vec2_new = transform(vec_2, Lambda)
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(
            circle.animate.apply_matrix(Lambda),
            Transform(vec_1, vec1_new),
            Transform(vec_2, vec2_new),
            run_time=2,
            rate_func=smooth
        )
        self.wait(3)
        self.play(equation[3].animate.set_color(WHITE))
        self.add_sound("voiceovers/click.wav")
        self.play(equation[2].animate.set_color(BLUE)) 
        vec1_new = transform(vec_1, Q)
        vec2_new = transform(vec_2, Q)
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(
            circle.animate.apply_matrix(Q),
            Transform(vec_1, vec1_new),
            Transform(vec_2, vec2_new),
            run_time=2,
            rate_func=smooth
        )
        self.wait()
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(
            equation[2].animate.set_color(WHITE),
            equation[0].animate.set_color(TEAL)
        )
        self.wait(2)

class SpectralAnalogy(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/SpectralAnalogy.mp3")
        self.camera.background_color = BLACK
        question = Text("Tại sao lại có tên \"phân tích phổ\"?", 
                        font="Noto Sans", font_size=36).add_background_rectangle()
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(question))
        self.wait(.5)
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(question.animate.to_edge(UP))
        self.wait(.5)
        physics_center = LEFT * 4
        p1 = physics_center + LEFT * 0.7
        p2 = physics_center + RIGHT * 0.5 + UP * 0.7
        p3 = physics_center + RIGHT * 0.5 + DOWN * 0.7
        
        prism = Polygon(p1, p2, p3, color=WHITE, stroke_width=2)
        
        white_light = Line(
            start=p1 + LEFT * 2.5, 
            end=p1, 
            color=WHITE, 
            stroke_width=4
        )
        
        right_side_midpoint = (p2 + p3) / 2
        
        colors = [RED, YELLOW, BLUE]
        outgoing_lights = VGroup()
        
        for i, color in enumerate(colors):
            start_point = right_side_midpoint + UP * (0.15 - i * 0.15)
            l = Line(
                start=start_point, 
                end=start_point + RIGHT * 2 + UP * (0.6 - i * 0.6), 
                color=color, 
                stroke_width=4
            )
            outgoing_lights.add(l)
        
        math_group = VGroup()
        matrix_A = MathTex("A").scale(1.5).shift(RIGHT * 2)
        arrow = Arrow(matrix_A.get_right(), matrix_A.get_right() + RIGHT * 1.2, buff=0.1)
        
        eigen_spectrum = VGroup(
            MathTex(r"\lambda_1 v_1", color=RED),
            MathTex(r"\lambda_2 v_2", color=YELLOW),
            MathTex(r"\lambda_n v_n", color=BLUE)
        ).arrange(DOWN, buff=0.2).next_to(arrow, RIGHT)

        self.add(prism)
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(Create(white_light))
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(Create(outgoing_lights), run_time=1.5)
        self.add_sound("voiceovers/click.wav")
        self.play(Write(matrix_A), GrowArrow(arrow), Write(eigen_spectrum))
        self.wait(3)

        self.play(FadeOut(VGroup(prism, white_light, outgoing_lights, math_group, matrix_A, arrow, eigen_spectrum)))

        grid = NumberPlane().set_opacity(0.3)
        circle = Circle(radius=1, color=WHITE)
        v1 = Vector([1, 0], color=RED)
        v2 = Vector([0, 1], color=BLUE)
        
        l1_txt = f"\\lambda_1 = 2.5"
        dominant_text = Text("(Chiếm ưu thế)", font="Noto Sans").scale(0.7)
        l2_txt = f"\\lambda_2 = 0.5"
        weak_text = Text("(Yếu)", font="Noto Sans").scale(0.7)
        l1_label = VGroup(MathTex(l1_txt), dominant_text
                          ).arrange(RIGHT).set_color(RED).to_corner(DR).add_background_rectangle()
        l2_label = VGroup(MathTex(l2_txt), weak_text
                          ).arrange(RIGHT).set_color(BLUE).next_to(l1_label, UP, aligned_edge=LEFT).add_background_rectangle()
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(Create(grid), Create(circle), GrowArrow(v1), GrowArrow(v2), Write(l1_label), Write(l2_label))
        self.wait()

        matrix = [[2.5, 0], [0, 0.5]]
        vec1_new = transform(v1, matrix)
        vec2_new = transform(v2, matrix)
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(
            grid.animate.apply_matrix(matrix),
            circle.animate.apply_matrix(matrix),
            Transform(v1, vec1_new),
            Transform(v2, vec2_new),
            run_time=5
        )
        self.wait(3)
        
class PCAIntuition(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/PCAIntuition1.mp3")
        # ---------------------------------------------------------
        # SETUP: Create the axes and the synthetic data
        # ---------------------------------------------------------
        axes = Axes(
            x_range=[-8, 8], 
            y_range=[-8, 8], 
            x_length=8, 
            y_length=8,
            axis_config={"color": DARK_GRAY}
        )
        self.play(FadeIn(axes))
        
        # Generate correlated synthetic data (off-center)
        np.random.seed(42)
        cov_matrix = [[4, 3.5], [3.5, 4]] # High variance and covariance
        raw_data = np.random.multivariate_normal([3, 3], cov_matrix, 50)

        # Plot the dots
        dots = VGroup(*[Dot(axes.c2p(x, y), color=YELLOW, radius=0.06) for x, y in raw_data])
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(dots))
        self.add_sound("voiceovers/PCAIntuition3.mp3")
        self.wait()

        # ---------------------------------------------------------
        # STEP 1: Center the Data
        # ---------------------------------------------------------
        # title = Text("Step 1: Center the Data", font_size=36).to_corner(UL)
        # self.play(Write(title))

        # Calculate mean
        mean_x, mean_y = np.mean(raw_data, axis=0)
        center_dot = Dot(axes.c2p(mean_x, mean_y), color=RED, radius=0.1)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(center_dot))
        self.wait()

        # Animate moving data to the origin
        centered_data = raw_data - [mean_x, mean_y]
        animations = []
        for i, dot in enumerate(dots):
            animations.append(
                dot.animate.move_to(axes.c2p(centered_data[i,0], centered_data[i,1]))
            )
        
        # Move dots and the red center dot simultaneously
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(*animations, center_dot.animate.move_to(axes.c2p(0,0)))
        self.play(FadeOut(center_dot))
        self.wait()

        # ---------------------------------------------------------
        # STEP 2: Calculate PCA and Show PC1
        # ---------------------------------------------------------
        # title_pc1 = Text("Step 2: Find PC1 (Max Variance)", font_size=36).to_corner(UL)
        # self.play(Transform(title, title_pc1))

        # Calculate Covariance Matrix and Eigenvectors using NumPy
        cov_centered = np.cov(centered_data.T)
        eigenvalues, eigenvectors = np.linalg.eig(cov_centered)
        
        # Sort eigenvectors by eigenvalues (descending)
        idx = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:,idx]

        pc1 = eigenvectors[:,0]
        pc2 = eigenvectors[:,1]

        # Draw PC1 Axis
        pc1_line = Line(
            axes.c2p(-pc1[0]*10, -pc1[1]*10),
            axes.c2p(pc1[0]*10, pc1[1]*10),
            color='#FF00FF',
            stroke_width=2
        )
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(Create(pc1_line))

        # Draw PC1 Vector (Arrow) scaled by its importance
        pc1_vec = Arrow(
            axes.c2p(0,0), axes.c2p(pc1[0]*4, pc1[1]*4), 
            buff=0, color='#FF00FF', max_tip_length_to_length_ratio=0.1
        )
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(GrowArrow(pc1_vec))
        self.wait()

        # Show orthogonal projections from dots to PC1
        projections = VGroup()
        for i, dot in enumerate(dots):
            p = centered_data[i]
            proj_len = np.dot(p, pc1)
            proj_point = proj_len * pc1
            proj_line = DashedLine(
                axes.c2p(p[0], p[1]),
                axes.c2p(proj_point[0], proj_point[1]),
                color=BLUE, stroke_opacity=0.6, stroke_width=2
            )
            projections.add(proj_line)
        self.add_sound("voiceovers/click.wav")
        self.play(Create(projections), run_time=2)
        self.add_sound("voiceovers/PCAIntuition2.mp3")
        self.wait()

        # ---------------------------------------------------------
        # STEP 3: Show PC2
        # ---------------------------------------------------------
        # title_pc2 = Text("Step 3: Find PC2 (Orthogonal)", font_size=36).to_corner(UL)
        # self.play(Transform(title, title_pc2))

        # Draw PC2 Axis and Vector
        pc2_line = Line(
            axes.c2p(-pc2[0]*10, -pc2[1]*10),
            axes.c2p(pc2[0]*10, pc2[1]*10),
            color=GREEN,
            stroke_width=2,
            stroke_opacity=0.5
        )
        pc2_vec = Arrow(
            axes.c2p(0,0), axes.c2p(pc2[0]*2, pc2[1]*2), 
            buff=0, color=GREEN, max_tip_length_to_length_ratio=0.15
        )
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(Create(pc2_line), GrowArrow(pc2_vec))
        self.wait(2)

        # ---------------------------------------------------------
        # STEP 4: Compress (Dimensionality Reduction)
        # ---------------------------------------------------------
        # title_comp = Text("Step 4: Compress (Drop PC2)", font_size=36).to_corner(UL)
        # self.play(Transform(title, title_comp), FadeOut(projections))

        # Animate the collapse: dots move onto the PC1 line
        collapse_anims = []
        for i, dot in enumerate(dots):
            p = centered_data[i]
            proj_len = np.dot(p, pc1)
            proj_point = proj_len * pc1 # Vector math to find coordinates on the line
            collapse_anims.append(
                dot.animate.move_to(axes.c2p(proj_point[0], proj_point[1]))
            )

        # Fade out PC2 and squash the points
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(
            *collapse_anims, 
            FadeOut(pc2_line), 
            FadeOut(pc2_vec), 
            run_time=2.5
        )
        
        # Final text
        # final_text = Text("Data is now 1D!", font_size=36, color=YELLOW).next_to(title, DOWN, aligned_edge=LEFT)
        # self.play(Write(final_text))
        self.wait(4)
class CircleEllipseThumbnail(Scene):
    def construct(self):
        # Title (slightly smaller)
        title = Text("EIGEN", font_size=72, weight=BOLD)
        title.to_edge(UP)

        # --- Eigenvectors (45°) ---
        v1 = np.array([1, 1])
        v2 = np.array([-1, 1])

        v1 = v1 / np.linalg.norm(v1)
        v2 = v2 / np.linalg.norm(v2)

        # --- Eigenvalues ---
        lambda1 = 3
        lambda2 = 1

        # Build matrix
        Q = np.column_stack((v1, v2))
        Lambda = np.diag([lambda1, lambda2])
        A = Q @ Lambda @ Q.T

        radius = 1.6

        circle = Circle(radius=radius, color=BLUE, stroke_width=4)
        # circle.set_fill(BLUE, opacity=0.15)

        ellipse = circle.copy()
        ellipse.apply_matrix(A)
        ellipse.set_color(PINK)
        # ellipse.set_stroke(width=8)
        # ellipse.set_fill(YELLOW, opacity=0.15)

        eig1 = Arrow(
            ORIGIN,
            lambda1 * radius * np.array([v1[0], v1[1], 0]),
            buff=0,
            stroke_width=8
        )

        eig2 = Arrow(
            ORIGIN,
            radius * np.array([v2[0], v2[1], 0]),
            buff=0,
            stroke_width=6
        )

        glow = ellipse.copy().set_stroke(width=20, opacity=0.1)
        visual = VGroup(circle, glow, ellipse, eig1, eig2)
        visual.move_to(ORIGIN)
        label_q1 = MathTex("q_1", font_size=48)
        label_q2 = MathTex("q_2", font_size=48)
        direction_v1 = np.array([v1[0], v1[1], 0])
        direction_v2 = np.array([v2[0], v2[1], 0])
        label_q1.next_to(eig1.get_end(), direction=direction_v1, buff=0.2)
        label_q2.next_to(eig2.get_end(), direction=direction_v2, buff=0.2)
        self.add(visual, label_q1, label_q2)