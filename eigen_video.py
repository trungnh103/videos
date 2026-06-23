from manim import *
import numpy as np

class EigenHook(LinearTransformationScene):
    def __init__(self, **kwargs):
        LinearTransformationScene.__init__(
            self,
            show_basis_vectors=False,
            show_coordinates=False,
            leave_ghost_vectors=False,
            **kwargs
        )

    def construct(self):
        self.plane.fade(0.3)
        self.wait()
        self.add_sound("voiceovers/EigenHook.mp3")
        title = Text("Áp dụng ma trận", font="Noto Sans")
        title.scale(0.7).to_corner(UL).add_background_rectangle()
        
        matrix_values = [[2, 1], [1, 2]]
        matrix_display = Matrix(matrix_values).next_to(title, DOWN)
        matrix_display.set_color(YELLOW).add_background_rectangle()
        
        vectors = VGroup(
            *[Vector([np.cos(a), np.sin(a)])
              for a in np.linspace(0, TAU, 8, endpoint=False)]
        )
        vectors.set_color_by_gradient(GREEN, YELLOW)
        for vector in vectors:
            self.add_vector(vector)
            self.wait(0.5)
        eigen_vec1_original = Vector([np.cos(TAU*3/8), np.sin(TAU*3/8)]).set_z_index(3)
        eigen_vec2_original = Vector([np.cos(TAU*7/8), np.sin(TAU*7/8)]).set_z_index(3)
        eigen_vec3_original = Vector([np.cos(TAU*1/8), np.sin(TAU*3/8)]).set_z_index(3)
        eigen_vec4_original = Vector([np.cos(TAU*5/8), np.sin(TAU*7/8)]).set_z_index(3)
        eigen_vec1 = vectors[3]
        eigen_vec2 = vectors[7]
        eigen_vec3 = vectors[1]
        eigen_vec4 = vectors[5]
        self.play(Write(title))
        self.play(FadeIn(matrix_display))
        self.wait()
        
        matrix = np.array(matrix_values)
        self.apply_matrix(matrix, run_time=5)
        self.wait(2)
        self.play(Indicate(VGroup(eigen_vec1, eigen_vec2, eigen_vec3, eigen_vec4)), run_time=4)
        v2_end = eigen_vec2.get_end()
        v3_end = eigen_vec3.get_end()
        line_12 = Line(
            -config.frame_height/2 * v2_end,
            config.frame_height/2 * v2_end,
            color=RED
        )
        line_34 = Line(
            -config.frame_height/2 * v3_end,
            config.frame_height/2 * v3_end,
            color=RED
        )
        text = Text("Vectơ riêng (eigenvectors)", font="Noto Sans", color=YELLOW).add_background_rectangle()
        text.scale(0.65).next_to(ORIGIN, DOWN).to_edge(RIGHT)
        self.play(Write(text))
        self.wait()

        self.add_sound("voiceovers/EigenHook2.mp3")      
        fadeout_group = VGroup()
        for i in range(8):
            if i not in [1, 5]:
            # if i is not 1 and i is not 5:
                fadeout_group.add(vectors[i])
        self.play(FadeOut(fadeout_group))
        self.play(Circumscribe(matrix_display, color=GREEN))
        self.play(Indicate(eigen_vec3))
        line_v = Line(LEFT, RIGHT)
        angle = Angle(line_v, line_34, radius=0.4)
        theta = MathTex("45^\\circ").move_to(
                    Angle(line_v, line_34, radius=0.4 + 3 * SMALL_BUFF).point_from_proportion(0.5)
                    )
        theta.scale(0.7).set_color(RED).add_background_rectangle()
        self.play(Create(angle), FadeIn(theta))
        self.play(Circumscribe(theta))
        self.wait()
        self.play(Create(line_34))  
        self.play(FadeOut(theta), FadeOut(angle))  
        x_eq_y = MathTex("x=y").shift(3*UP+4*RIGHT).add_background_rectangle()   
        self.play(Write(x_eq_y))   
        self.play(FadeOut(x_eq_y))    
        self.play(FadeOut(eigen_vec3), FadeOut(eigen_vec4))
        eigen_vec3.set_color(eigen_vec3.get_color())
        self.play(Transform(eigen_vec3_original, eigen_vec3),
                  Transform(eigen_vec4_original, eigen_vec4))
        brace_x3 = Brace(eigen_vec3_original, direction=eigen_vec3_original.copy().rotate(PI / 2).get_unit_vector())
        x3text = brace_x3.get_tex("x3")
        self.play(GrowFromCenter(brace_x3), FadeIn(x3text))
        lambda_x3 = MathTex(r"\lambda = 3").set_color(eigen_vec3.get_color()).add_background_rectangle()
        lamda_symbol = lambda_x3[0][:1]
        brace_x3.put_at_tip(lambda_x3)
        self.play(Transform(x3text, lambda_x3))
        
        arrow = Arrow(0.5*UP, 0.5*DOWN, color=YELLOW).next_to(lamda_symbol, UP)
        eigenvalue_text = Text("Giá trị riêng", font="Noto Sans", color=YELLOW).add_background_rectangle()
        eigenvalue_text.scale(0.65).next_to(arrow, UP).to_edge(UP)
        self.wait()
        self.play(GrowArrow(arrow), Write(eigenvalue_text))
        self.wait(3)
        self.play(Circumscribe(lambda_x3, color=GREEN))

        
        self.play(Create(line_12))
        x_eq_negative_y = MathTex("x=-y").shift(2*DOWN+3*RIGHT).add_background_rectangle()   
        self.play(Write(x_eq_negative_y))   
        self.wait()
        self.play(FadeOut(x_eq_negative_y)) 
        self.wait()
        self.play(FadeIn(eigen_vec1), FadeIn(eigen_vec2))
        brace_x1 = Brace(eigen_vec1, direction=eigen_vec1.copy().rotate(PI / 2).get_unit_vector())
        x1text = brace_x1.get_tex("x1")    
        self.play(GrowFromCenter(brace_x1), FadeIn(x1text))
        self.wait()
        lambda_x1 = MathTex(r"\lambda = 1").set_color(eigen_vec1.get_color()).add_background_rectangle()
        brace_x1.put_at_tip(lambda_x1)
        self.play(Transform(x1text, lambda_x1))
        self.play(Circumscribe(x1text, color=GREEN))
        self.wait(5)

class EigenScaling_x2(LinearTransformationScene):
    def __init__(self, **kwargs):
        self.t_matrix = np.array([[3, 0], [1, 2]])
        super().__init__(
            show_basis_vectors=False,
            leave_ghost_vectors=False,
            include_background_plane=False,
            **kwargs
        )
    def construct(self):
        self.wait()
        self.plane.fade(0.3)
        lambda_x2 = MathTex(r"\lambda = 2")
        lambda_x2[0][:1].set_color(GREEN)
        lambda_x2.to_corner(UL).add_background_rectangle()
        self.play(Write(lambda_x2))
        vectors = VGroup(*[
            self.add_vector(
                u * x * (LEFT + UP),
                animate=False
            )
            for x in reversed(np.arange(0.5, 5, 0.5))
            for u in (-1, 1)
        ])

        vectors.set_color_by_gradient(GREEN, YELLOW)

        # Text
        words = Text("Dài gấp đôi", font="Noto Sans").scale(0.65)
        words.add_background_rectangle()
        words.next_to(
            ORIGIN,
            DOWN + LEFT,
            buff=MED_SMALL_BUFF
        )
        words.shift(MED_SMALL_BUFF * LEFT)
        words.rotate(vectors[0].get_angle())

        words.start = words.copy()
        words.start.scale(0.5)
        words.start.set_fill(opacity=0)

        self.play(Create(vectors))
        self.add_sound("voiceovers/EigenScaling_x2.mp3")
        self.play(Circumscribe(lambda_x2))
        self.wait(0.5)

        self.apply_transposed_matrix(
            self.t_matrix,
            added_anims=[Transform(words.start, words)],
            path_arc=0, run_time=2
        )

        self.wait(2)
class EigenScaling_half(LinearTransformationScene):
    def __init__(self, **kwargs):
        self.t_matrix = np.array([[3, 0], [1, 2]])
        super().__init__(
            show_basis_vectors=False,
            leave_ghost_vectors=False,
            **kwargs
        )
    def construct(self):
        self.plane.fade(0.3)
        self.wait()
        
        lambda_half = MathTex(r"\lambda = 0.5")
        lambda_half[0][:1].set_color(GREEN)
        lambda_half.to_corner(UL).add_background_rectangle()
        self.play(Write(lambda_half))
        vectors = VGroup(*[
            self.add_vector(
                u * x * (LEFT + UP),
                animate=False
            )
            for x in reversed(np.arange(0.5, 5, 1))
            for u in (-1, 1)
        ])

        vectors.set_color_by_gradient(GREEN, YELLOW)

        # Text
        words = Text("Vector bị nén lại", font="Noto Sans").scale(0.65)
        words.add_background_rectangle()
        words.next_to(
            ORIGIN,
            DOWN + LEFT,
            buff=MED_SMALL_BUFF
        )
        words.shift(MED_SMALL_BUFF * LEFT)
        words.rotate(vectors[0].get_angle())

        words.start = words.copy()
        words.start.scale(0.5)
        words.start.set_fill(opacity=0)

        self.play(Create(vectors))
        self.add_sound("voiceovers/EigenScaling_half.mp3")
        self.play(Circumscribe(lambda_half))
        self.wait(0.5)

        self.apply_inverse_transpose(
            self.t_matrix,
            added_anims=[Transform(words.start, words)],
            path_arc=0, run_time=2
        )
        self.wait(2)

class EigenScaling_negative(LinearTransformationScene):
    def __init__(self, **kwargs):
        self.t_matrix = np.array([[0.5, -1], [-1, 0.5]])
        super().__init__(
            show_basis_vectors=False,
            include_background_plane=False,
            leave_ghost_vectors=False,
            **kwargs
        )
    def construct(self):
        self.plane.fade(0.3)
        self.wait()
        
        lambda_half = MathTex(r"\lambda = -0.5")
        lambda_half[0][:1].set_color(GREEN)
        lambda_half.to_corner(UL).add_background_rectangle()
        self.play(Write(lambda_half))
        vector = self.add_vector([1, 1]).set_z_index(3)
        # span = Line(
        #     -config.frame_height/2 * vector.get_end(),
        #     config.frame_height/2 * vector.get_end(),
        #     color=MAROON_B
        # )

        # Text
        words = Text("Vector lật ngược hướng", font="Noto Sans").scale(0.65)
        words.add_background_rectangle()
        words.next_to(
            ORIGIN,
            DOWN + LEFT,
            buff=MED_SMALL_BUFF
        )
        words.shift(MED_SMALL_BUFF * LEFT)
        words.rotate(vector.get_angle())

        words.start = words.copy()
        words.start.scale(0.5)
        words.start.set_fill(opacity=0)
        # self.play(Create(span))
        self.add_sound("voiceovers/EigenScaling_negative.mp3")
        self.play(Circumscribe(lambda_half))
        self.wait(0.5)

        self.apply_transposed_matrix(
            self.t_matrix,
            added_anims=[Transform(words.start, words)],
            path_arc=0, run_time=2
        )
        self.wait(2)
class ShearScene(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/ShearScene.mp3")
        plane = NumberPlane()

        e1 = Vector(RIGHT, color=GREEN)
        e2 = Vector(UP, color=RED)
        
        
        shocked = SVGMobject("assets/22.svg").shift(2*UP+2*RIGHT)
        self.play(FadeIn(plane), FadeIn(e1), FadeIn(e2), FadeIn(shocked))
        matrix = [[1, 1], [0, 1]]
        self.play(ApplyMatrix(matrix, VGroup(shocked, plane, e1, e2)), run_time=5)
        self.play(Wiggle(e1))
        self.wait(2)
        self.play(Indicate(e1))
        self.wait()
        lambda_symbol = MathTex(r"\lambda = 1").next_to(e1, DOWN)
        lambda_symbol[0][:1].set_color(GREEN)
        self.play(Write(lambda_symbol))
        self.wait(2)
class DotsStayDots(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/DotsStayDots.mp3")
        plane = NumberPlane(background_line_style={"stroke_opacity": 0.25})
        matrix = [[2, 1], [1, 2]]
        matrix_display = Matrix(matrix).to_corner(UL, LARGE_BUFF)
        matrix_display.set_color(YELLOW).add_background_rectangle()

        dots = VGroup()
        positions = []

        for x in range(-6, 6):
            for y in range(-4, 4):
                pos = np.array([x, y, 0])
                positions.append(pos)
                dots.add(Dot(pos, radius=0.06, color=GREEN))

        line_xy = Line([-8, -8, 0], [8, 8, 0], color=RED).set_z_index(-10)
        line_x_minus_y = Line([-8, 8, 0], [8, -8, 0], color=RED).set_z_index(-10)

        self.play(FadeIn(plane), FadeIn(matrix_display))
        self.play(FadeIn(line_xy), FadeIn(line_x_minus_y))
        self.play(FadeIn(dots))
        self.wait()

        self.play(
            *[
                dot.animate.move_to(
                    np.append(matrix @ pos[:2], 0)
                )
                for dot, pos in zip(dots, positions)
            ], run_time=5
        )

        self.wait(2)

class EigenDefinition(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/EigenDefinition_title.mp3")
        title = Text("ĐỊNH NGHĨA TOÁN HỌC", font="Noto Sans")
        self.play(Write(title))
        
        self.play(title.animate.scale(0.7).to_corner(UL))
        self.add_sound("voiceovers/EigenDefinition.mp3")
        eq = MathTex(
            "A\\vec{v} = \\lambda \\vec{v}"
        ).scale(1.5)
        eq[0][0].set_color(BLUE)
        eq[0][1:3].set_color(YELLOW)
        eq[0][4:5].set_color(GREEN)
        eq[0][-2:].set_color(YELLOW)

        self.play(FadeIn(eq))

        highlights = VGroup(
            SurroundingRectangle(eq[0][0], color=RED),
            SurroundingRectangle(eq[0][1:3], color=RED),
            SurroundingRectangle(eq[0][4:5], color=RED)
        )
        texts = (
            "Phép biến đổi", "Vectơ riêng", "Giá trị riêng"
        )
        for highlight, text in zip(highlights, texts):
            arrow = Arrow(UP, DOWN).next_to(highlight, DOWN)
            definition = Text(text, font="Noto Sans", color=RED).scale(0.65).next_to(arrow, DOWN)
            self.play(FadeIn(highlight), GrowArrow(arrow), Write(definition))
            self.play(FadeOut(highlight), FadeOut(arrow), FadeOut(definition))

        self.wait(5)
class Rotate3D(ThreeDScene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/Rotate3D.mp3")
        title = Text("Trục quay 3D", font="Noto Sans", color=YELLOW)
        self.add_fixed_in_frame_mobjects(title)
        title.scale(0.7).to_corner(UL)
        self.play(Write(title))
        text = Text("Vectơ riêng", font="Noto Sans", color=YELLOW)
        self.add_fixed_in_frame_mobjects(text)
        text.scale(0.65).shift(2.5*UP+3.5*RIGHT)
        
        axes = ThreeDAxes()
        arrow = Arrow3D(
            start=np.array([0, 0, 0]),
            end=np.array([2, 1, 3]),
            color=YELLOW,
            resolution=8
        )
        axis = np.array((2, 1, 3))
        cube = Cube()
        self.set_camera_orientation(phi=75 * DEGREES, theta=305 * DEGREES)
        self.play(Create(axes))
        self.play(Create(cube))
        self.play(Create(arrow))
        play_kw = {"run_time": 5}
        self.play(Rotating(cube, 180*DEGREES, axis=axis), **play_kw)
        self.wait()
class DiagonalMatrix(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/DiagonalMatrix_title.mp3")
        
        title = Text("MA TRẬN CHÉO", font="Noto Sans", color=YELLOW)
        title.add_background_rectangle()
        self.play(SpinInFromNothing(title, angle=2 * PI))
        
        self.play(title.animate.scale(0.7).to_corner(UL))
        plane = NumberPlane(background_line_style={"stroke_opacity": 0.25})
        matrix_values = [[2, 0], [0, 1]]
        matrix = Matrix(matrix_values)
        matrix.set_column_colors(YELLOW, GREEN)
        matrix.to_corner(UR, LARGE_BUFF)
        matrix.add_background_rectangle()
        entries = matrix.get_entries()
        eigen_x = entries[0]
        eigen_y = entries[3]

        x_vec = Vector([1, 0], color=YELLOW)
        y_vec = Vector([0, 1], color=GREEN)
        self.play(FadeIn(plane), FadeIn(matrix), FadeIn(x_vec), FadeIn(y_vec))
        self.add_sound("voiceovers/DiagonalMatrix.mp3")
        self.play(
            plane.animate.apply_matrix(matrix_values),
            x_vec.animate.apply_matrix(matrix_values),
            y_vec.animate.apply_matrix(matrix_values),
            run_time=2
        )
        x_coordinate = eigen_x.copy()
        y_coordinate = eigen_y.copy()
        self.play(x_coordinate.animate.next_to(x_vec, DOWN))
        self.play(y_coordinate.animate.next_to(y_vec, LEFT))
        
        self.wait(4)
        self.play(Indicate(VGroup(entries[1], entries[2]), color=RED))
        self.wait()
        self.play(Indicate(VGroup(eigen_x, eigen_y), color=RED))
        self.wait()
        self.play(Circumscribe(matrix))
        self.wait()
        self.play(Wiggle(VGroup(x_vec, y_vec)))
        self.wait()
        self.play(Indicate(VGroup(eigen_x, eigen_y)))
        self.wait()
        circ_x = Circle(color=BLUE).surround(x_coordinate, buffer_factor=2.0)
        circ_y = Circle(color=BLUE).surround(y_coordinate, buffer_factor=2.0)
        self.play(Create(circ_x), Create(circ_y))
        self.play(FadeOut(circ_x), FadeOut(circ_y))
        
        self.wait(4)
class CircleToEllipse(Scene):
    def construct(self): 
        self.wait()  
        self.add_sound("voiceovers/CircleToEllipse_title.mp3")
        title = Text("HÌNH TRÒN → ELLIPSE", font="Noto Sans", color=YELLOW)
        title.add_background_rectangle()
        self.play(SpinInFromNothing(title, angle=2 * PI))
        self.play(title.animate.scale(0.7).to_corner(UL))
        self.add_sound("voiceovers/CircleToEllipse.mp3")
        plane = NumberPlane(background_line_style={"stroke_opacity": 0.25})
        circle = Circle(radius=1, color=GREEN)
        circle.set_fill(GREEN, opacity=0.5)


        matrix_values = [[2, 1], [0, 1]]
        matrix = Matrix(matrix_values).next_to(title, DOWN)
        matrix.set_color(BLUE).add_background_rectangle()
        det_text = get_det_text(matrix, 0, initial_scale_factor=1)
        det_text.remove(det_text.split()[-1])
        for mob in det_text.split():
            if isinstance(mob, Tex):
                mob.add_background_rectangle()
        lambda1_formula = MathTex(r"\lambda _{1}").next_to(det_text, RIGHT)
        lambda2_formula = MathTex(r"\lambda _{2}").next_to(lambda1_formula, RIGHT)

        eig1 = Vector([1, 0], color=YELLOW)
        eig2 = Vector([np.sin(PI/4), -np.cos(PI/4)], color=MAROON_B)
        line_1 = Line(
            -config.frame_height/2 * eig1.get_end(),
            config.frame_height/2 * eig1.get_end(),
            color=GREEN_E
        )
        line_2 = Line(
            -config.frame_height/2 * eig2.get_end(),
            config.frame_height/2 * eig2.get_end(),
            color=GREEN_E
        )
        self.play(FadeIn(plane), FadeIn(circle), FadeIn(matrix), 
                  FadeIn(line_1), FadeIn(line_2),
                  FadeIn(eig1), FadeIn(eig2))
        self.play(
            plane.animate.apply_matrix(matrix_values),
            circle.animate.apply_matrix(matrix_values),
            eig1.animate.apply_matrix(matrix_values),
            eig2.animate.apply_matrix(matrix_values),
            run_time=3
        )
        # self.play(Wiggle(line_1), Wiggle(line_2))
        self.wait(2)
        self.play(Indicate(eig1), Indicate(eig2))
        lambda1 = MathTex(r"\lambda _{1}").set_color(YELLOW).next_to(eig1, UP)
        
        lambda2 = MathTex(r"\lambda _{2}").set_color(MAROON_B).next_to(eig2, LEFT)
        
        self.play(FadeIn(lambda1), FadeIn(lambda2))
        self.wait(3)
        lambda1_copy = lambda1.copy()
        lambda2_copy = lambda2.copy()
        self.play(lambda1_copy.animate.move_to(lambda1_formula),
                  lambda2_copy.animate.move_to(lambda2_formula), run_time=2)
        lambda1_copy.add_background_rectangle()
        lambda2_copy.add_background_rectangle()
        
        self.play(Indicate(circle))
        self.wait()
        self.play(FadeIn(det_text))
        shocked = SVGMobject("assets/22.svg").to_edge(UP)
        self.play(FadeIn(shocked),
                  Circumscribe(VGroup(det_text, lambda1_formula, lambda2_formula)))
        self.wait(3)
class CharacteristicEquation(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/CharacteristicEquation.mp3")
        title = Text("TỪ HÌNH HỌC SANG ĐẠI SỐ", font="Noto Sans", color=YELLOW)
        self.play(SpinInFromNothing(title, angle=2 * PI))
        self.play(title.animate.scale(0.7).to_corner(UL))
        row1 = MathTex("A\\vec{v} = \\lambda \\vec{v}")
        row1[0][0].set_color(BLUE)
        row1[0][1:3].set_color(YELLOW)
        row1[0][4:5].set_color(GREEN)
        row1[0][-2:].set_color(YELLOW)
        row1_eq = row1[0][3:4]

        row2_eq = MathTex("=").next_to(row1_eq, DOWN, MED_LARGE_BUFF) 
        row2_left = MathTex("A\\vec{v} - \\lambda I \\vec{v}").next_to(row2_eq, LEFT)
        row2_left[0][0].set_color(BLUE)
        row2_left[0][1:3].set_color(YELLOW)
        row2_left[0][4:5].set_color(GREEN)
        row2_left[0][-2:].set_color(YELLOW)
        row2_right = MathTex("0").next_to(row2_eq, RIGHT)
        row2 = VGroup(row2_left, row2_eq, row2_right) 

        row3_eq = MathTex("=").next_to(row2_eq, DOWN, MED_LARGE_BUFF)  
        row3_left = MathTex("(A - \\lambda I)\\vec{v}").next_to(row3_eq, LEFT)
        row3_right = MathTex("0").next_to(row3_eq, RIGHT)
        row3_left[0][1].set_color(BLUE)
        row3_left[0][3:4].set_color(GREEN)
        row3_left[0][-2:].set_color(YELLOW)
        row3 = VGroup(row3_left, row3_eq, row3_right)  
        

        row4_eq = MathTex("=").next_to(row3_eq, DOWN, MED_LARGE_BUFF)
        row4_left = MathTex("\\det(A - \\lambda I)").next_to(row4_eq, LEFT)
        row4_right = MathTex("0").next_to(row4_eq, RIGHT)
        row4_left[0][-3:-2].set_color(GREEN)
        row4_left[0][4].set_color(BLUE)
        row4 = VGroup(row4_left, row4_eq, row4_right)

        self.play(FadeIn(row1))
        insert_I = MathTex("I").next_to(row1[0][-3:], RIGHT, buff=0.1).shift(0.35*LEFT)
        self.play(row1[0][-2:].animate.shift(0.25*RIGHT), FadeIn(insert_I, shift=0.2*UP))
        Av_row1 = row1[0][:3]
        lambdaIv_row1 = VGroup(insert_I, row1[0][-3:])
        Av_row2 = row2_left[0][:3]
        lambdaIv_row2 = row2_left[0][-4:]
        Av_row1_copy = Av_row1.copy()
        lambdaIv_row1_copy = lambdaIv_row1.copy()
        self.play(Av_row1_copy.animate.move_to(Av_row2), Write(row2_left[0][3:4]),
                  lambdaIv_row1_copy.animate.move_to(lambdaIv_row2), Write(row2_eq), Write(row2_right))
        self.play(Write(row3_left[0][0]), 
                  row2_left[0][0].animate.move_to(row3_left[0][1]),
                  Write(row3_left[0][2]), 
                  row2_left[0][4:6].animate.move_to(row3_left[0][3:5]),
                  Write(row3_left[0][-3]), 
                  Transform(VGroup(row2_left[0][1:2], row2_left[0][-2:]), row3_left[0][-2:]),
                  Write(row3_eq), Write(row3_right))
        
        self.play(Indicate(row3_left[0][-4]))
        self.play(Indicate(row3_right), run_time=2)
        self.play(Circumscribe(row3))
        self.play(Circumscribe(row3_left[0][-2:]))
        self.wait(2)
        det = row3_left[0][:6].copy()
        self.play(det.animate.move_to(row4_left[0][3:9]),
                  FadeIn(row4_left[0][:3], shift=LEFT),
                  Write(row4_eq), Write(row4_right))
        self.play(Circumscribe(row4))
        self.wait(3)
        self.play(Circumscribe(row4_left[0][-3]))
        self.wait(2)
        self.play(row4.animate.next_to(title, DOWN), FadeOut(row1, row2, row3, insert_I, Av_row1_copy, lambdaIv_row1_copy, det))
        self.wait()
        self.add_sound("voiceovers/SolveEigenExample_part1.mp3")
        self.add_sound("voiceovers/ui_pop_up.mp3")
        matrix = Matrix([[3, 1], [0, 2]])
        example = Text("Ví dụ:", font="Noto Sans", color=YELLOW).scale(0.65)
        VGroup(example, matrix).arrange(RIGHT).to_corner(UR, LARGE_BUFF)
        self.play(Write(example), Write(matrix))
        self.wait()
        self.play(Circumscribe(matrix, color=GREEN))
        matrix_subtract_lambda = MobjectMatrix([[MathTex("3- \\lambda"), MathTex("1")], [MathTex("0"), MathTex("2- \\lambda")]])
        matrix_subtract_lambda.next_to(matrix, DOWN).shift(7.5*LEFT)
        det = get_det_text(matrix_subtract_lambda, 0, initial_scale_factor=1)
        det.remove(det.split()[-2], det.split()[-1])
        entries = matrix.copy().get_entries()
        entries_subtract_lambda = matrix_subtract_lambda.get_entries()
        entries_subtract_lambda[1].shift(0.5*LEFT)
        entries_subtract_lambda[2].shift(0.5*LEFT)
        entries_subtract_lambda[0][0][-1].set_color(GREEN)
        entries_subtract_lambda[3][0][-1].set_color(GREEN)
        calculation = MathTex("=(3- \\lambda)(2- \\lambda)-(1)(0)=0").next_to(det, RIGHT)
        
        self.play(Write(det), 
                  matrix.get_brackets()[0].copy().animate.move_to(matrix_subtract_lambda.get_brackets()[0]),
                  matrix.get_brackets()[1].copy().animate.move_to(matrix_subtract_lambda.get_brackets()[1]),
                  *[entries[i].animate.move_to(entries_subtract_lambda[i]) for i in range(4)])
        self.play(Transform(entries[0], entries_subtract_lambda[0]),
                  Transform(entries[3], entries_subtract_lambda[3]))
        
        self.play(FadeIn(calculation[0][:2]),
                  entries[0].copy().animate.move_to(calculation[0][2:5]),
                  FadeIn(calculation[0][5:7]),
                  entries[3].copy().animate.move_to(calculation[0][7:10]),
                  FadeIn(calculation[0][10:11]))
        self.play(FadeIn(calculation[0][11:13]),
                  entries[1].copy().animate.move_to(calculation[0][13:14]),
                  FadeIn(calculation[0][14:16]),
                  entries[2].copy().animate.move_to(calculation[0][16:17]),
                  FadeIn(calculation[0][17:18]))
        self.play(FadeIn(calculation[0][18:]))
        roots = MathTex("\\lambda = 3,\\;2").next_to(det, DOWN)
        roots[0][0].set_color(GREEN)
        
        self.add_sound("voiceovers/SolveEigenExample_part2.mp3")
        self.play(Write(roots))
        self.add_sound("voiceovers/win.wav")
        self.play(Circumscribe(roots))
        self.wait(4)
class SolveEigenExample(Scene):
    def construct(self):
        matrix = MathTex(
            "A = \\begin{pmatrix} 3 & 1 \\\\ 0 & 2 \\end{pmatrix}"
        )
        det = MathTex(
            "\\det(A - \\lambda I) = (3-\\lambda)(2-\\lambda)"
        )
        roots = MathTex("\\lambda = 3,\\;2")

        VGroup(matrix, det, roots).arrange(DOWN)

        self.play(Write(matrix))
        self.play(Write(det))
        self.play(Write(roots))
        self.wait()
class EigenApplications(Scene):
    def construct(self):
        apps = VGroup(
            Text("PCA – Trục chính dữ liệu"),
            Text("PageRank – Vector ổn định"),
            Text("Physics – Mode dao động"),
            Text("Machine Learning")
        ).arrange(DOWN)

        self.play(LaggedStartMap(FadeIn, apps, lag_ratio=0.4))
        self.wait()
class EigenSummary(Scene):
    def construct(self):
        summary = VGroup(
            Text("Eigenvector = Hướng không đổi"),
            Text("Eigenvalue = Mức co giãn"),
            Text("Ma trận = Biến đổi không gian")
        ).arrange(DOWN)

        self.play(Write(summary))
        self.wait(2)
class PageRankNetwork(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/PageRankNetwork.mp3")
        title = Text("Thuật toán xếp hạng các trang web \n của Google (PageRank)", color=YELLOW, font="Noto Sans")
        self.play(Write(title))
        
        google = SVGMobject("assets/google.svg").scale(0.45).to_corner(UL)
        subtitle = Tex("PageRank").next_to(google, RIGHT)
        self.play(Transform(title, VGroup(google, subtitle)))
        self.wait()
        nodes = {
            "A": Dot(LEFT * 3, radius=0.4, color=BLUE_C),
            "B": Dot(UP * 1.5, radius=0.4, color=MAROON_D),
            "C": Dot(RIGHT * 3, radius=0.4, color=GREY_BROWN),
            "D": Dot(DOWN * 1.5, radius=0.4, color=GREEN_E),
        }

        labels = {
            k: Text(k).scale(0.7).move_to(v.get_center())
            for k, v in nodes.items()
        }

        edges = VGroup(
            Arrow(nodes["A"], nodes["B"], stroke_width=2),
            Arrow(nodes["B"], nodes["C"], stroke_width=2),
            Arrow(nodes["C"], nodes["A"], stroke_width=2),
            Arrow(nodes["C"], nodes["D"], stroke_width=2).shift(0.1*LEFT+0.1*UP),
            Arrow(nodes["D"], nodes["C"], stroke_width=2).shift(0.1*RIGHT+0.1*DOWN),
        )

        for k in nodes:
            self.add_sound("voiceovers/ui_pop_up.mp3")
            self.play(FadeIn(nodes[k]), FadeIn(labels[k]))
            self.wait(0.5)
        
        self.play(Create(edges), run_time=4)
        self.wait()
        surfer = SVGMobject("assets/look_closely.svg").scale(0.5).next_to(nodes["A"], LEFT)
        self.play(FadeIn(surfer))

        path = ["B", "C", "D", "C", "A", "B"]
        directions = {
            "A": LEFT,
            "B": UP,
            "C": RIGHT,
            "D": DOWN,
        }
        for i in path:
            self.add_sound("voiceovers/click.wav")
            self.play(surfer.animate.next_to(nodes[i], directions[i]))
        self.wait(3)
class PageRankRandomSurfer(Scene):
    def construct(self):
        nodes = [
            Dot(LEFT * 3),
            Dot(UP * 2),
            Dot(RIGHT * 3),
            Dot(DOWN * 2),
        ]

        surfer = Dot(color=YELLOW).move_to(nodes[0])

        self.play(*[FadeIn(n) for n in nodes])
        self.play(FadeIn(surfer))

        path = [1, 2, 3, 2, 0, 1]
        for i in path:
            self.play(surfer.animate.move_to(nodes[i]), run_time=0.6)

        self.wait()
class PageRankEigen(Scene):
    def construct(self):
        eq = MathTex("Mr = r").scale(1.5)
        eig = MathTex(
            "\\Rightarrow r \\text{ is eigenvector of } M"
        )

        VGroup(eq, eig).arrange(DOWN)

        self.play(Write(eq))
        self.wait()
        self.play(Write(eig))
        self.wait()
class PageRankIteration(Scene):
    def construct(self):
        v = MathTex(
            "r^{(k+1)} = M r^{(k)}"
        ).scale(1.4)

        self.play(Write(v))
        self.wait()

        for i in range(3):
            self.play(Indicate(v))
            self.wait(0.4)
from manim import *
import numpy as np
colors = {
            "A": BLUE_C,
            "B": MAROON_D,
            "C": GREY_BROWN,
            "D": GREEN_E,
        }
class PageRankFlow(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/PageRankFlow_part1.mp3")
        google = SVGMobject("assets/google.svg").scale(0.45).to_corner(UL)
        subtitle = Tex("PageRank").next_to(google, RIGHT)
        self.add(google, subtitle)
        self.wait()
        # -----------------------------
        # 1. GRAPH STRUCTURE
        # -----------------------------
        positions = {
            "A": LEFT * 3,
            "B": UP * 2,
            "C": RIGHT * 3,
            "D": DOWN * 2,
        }
        

        nodes = {
            k: Dot(pos, radius=0.4, color=colors[k])
            for k, pos in positions.items()
        }

        labels = {
            k: Text(k, font_size=28).move_to(v.get_center())
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
        arrows[3].shift(0.1*LEFT+0.1*UP)
        arrows[4].shift(0.1*RIGHT+0.1*DOWN)
        for k in nodes:
            self.add_sound("voiceovers/ui_pop_up.mp3")
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
            self.add_sound("voiceovers/send-message.mp3")
            self.play(
                *[
                    dot.animate.move_to(nodes[t].get_center())
                    for dot, t in zip(dots, targets)
                ],
                run_time=1
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

        # -----------------------------
        # 4. ONE ITERATION
        # -----------------------------
        self.wait(0.5)
        flow("A", ["B"])
        self.wait(0.3)
        flow("B", ["C"])
        self.wait(0.3)
        flow("C", ["A", "D"])
        self.wait(0.3)
        flow("D", ["C"])
        for k in ranks:
            ranks[k].set_value(shares[k].get_value())
            shares[k].set_value(0)
            for mob in share_texts.submobjects:
                self.remove(mob)
        self.add_sound("voiceovers/win.wav")
        self.play(*[Flash(v) for v in rank_labels.values()])
        self.wait()

        # -----------------------------
        # 5. REPEAT (CONVERGENCE FEEL)
        # -----------------------------
        iterate = Text(
            "Lặp lại → hội tụ",
            font_size=36, font="Noto Sans",
            color=YELLOW
        ).to_corner(UR)
        self.add_sound("voiceovers/PageRankFlow_part2.mp3")
        self.play(FadeIn(iterate))

        for _ in range(4):
            flow("A", ["B"])
            flow("B", ["C"])
            flow("C", ["A", "D"])
            flow("D", ["C"])
            for k in ranks:
                ranks[k].set_value(shares[k].get_value())
                shares[k].set_value(0)
            for mob in share_texts.submobjects:
                self.remove(mob)
        self.add_sound("voiceovers/PageRankFlow_part3.mp3")
        self.add_sound("voiceovers/win.wav")
        self.play(*[Flash(v) for v in rank_labels.values()])
        self.wait(3)
        self.add_sound("voiceovers/PageRankFlow_part4.mp3")
        rank_vec = MathTex(
            r"""
            \begin{pmatrix}
            0.25 \\ 0.25 \\ 0.25 \\ 0.25
            \end{pmatrix}
            """
        ).scale(0.9)
        rank_vec.to_edge(RIGHT, LARGE_BUFF)
        rank_vec_from_nodes = {
            "A": rank_vec[0][4:8],
            "B": rank_vec[0][8:12],
            "C": rank_vec[0][12:16],
            "D": rank_vec[0][16:20],
        }
        rank_labels_copy = {
            k: rank_labels[k].copy()
            for k in nodes
        }
        self.play(Write(rank_vec[0][:4]), 
                  *[rank_labels_copy[k].scale(1.6).animate.move_to(rank_vec_from_nodes[k]) 
                    for k in nodes],
                  Write(rank_vec[0][-4:]))
        self.play(Circumscribe(rank_vec))
        self.wait(7)

class PageRankMarkov(Scene):
    def construct(self):
        # -----------------------------
        # 1. GRAPH (LEFT)
        # -----------------------------
        positions = {
            "A": LEFT * 4 + UP * 1.5,
            "B": LEFT * 2 + UP * 2.5,
            "C": LEFT * 1 + DOWN * 1,
            "D": LEFT * 3 + DOWN * 2.5,
        }

        nodes = {k: Dot(v, radius=0.4, color=colors[k]) for k, v in positions.items()}
        labels = {
            k: Text(k, font_size=24).move_to(nodes[k].get_center())
            for k in nodes
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
                buff=0.15,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.1
            )
            for a, b in edges
        ])
        arrows[3].shift(0.1*LEFT+0.1*UP)
        arrows[4].shift(0.1*RIGHT+0.1*DOWN)

        self.play(
            *[FadeIn(n) for n in nodes.values()],
            *[FadeIn(l) for l in labels.values()]
        )
        self.play(Create(arrows))

        # -----------------------------
        # 2. MARKOV MATRIX (RIGHT)
        # -----------------------------
        matrix = MathTex(
            r"""
            M =
            \begin{pmatrix}
            0 & 0 & \frac12 & 0 \\
            1 & 0 & 0 & 0 \\
            0 & 1 & 0 & 1 \\
            0 & 0 & \frac12 & 0
            \end{pmatrix}
            """
        )
        matrix.scale(0.8).to_edge(RIGHT)

        self.play(Write(matrix))
        node_columns = VGroup(Text("A").scale(0.65).next_to(matrix[0][6], UP),
                      Text("B").scale(0.65).next_to(matrix[0][7], UP),
                      Text("C").scale(0.65).next_to(matrix[0][10], 1.8*UP),
                      Text("D").scale(0.65).next_to(matrix[0][11], UP))

        node_rows = VGroup(Text("A").scale(0.65).next_to(matrix[0][6], 2*LEFT),
                         Text("B").scale(0.65).next_to(matrix[0][12], 2.3*LEFT),
                         Text("C").scale(0.65).next_to(matrix[0][16], 2*LEFT),
                         Text("D").scale(0.65).next_to(matrix[0][20], 2*LEFT))
        col_box_A = SurroundingRectangle(
            VGroup(matrix[0][6],
                   matrix[0][12], 
                   matrix[0][16],
                   matrix[0][20]), 
            color=YELLOW
        ).scale(1.4)
        col_box_B = SurroundingRectangle(
            VGroup(matrix[0][7],
                   matrix[0][11], 
                   matrix[0][15],
                   matrix[0][19]), # cột C (index hơi thủ công nhưng ổn)
            color=YELLOW
        ).scale(1.4)
        col_box_C = SurroundingRectangle(
            VGroup(matrix[0][10],
                   matrix[0][14], 
                   matrix[0][18],
                   matrix[0][22]), # cột C (index hơi thủ công nhưng ổn)
            color=YELLOW
        ).scale(1.4)
        col_box_D = SurroundingRectangle(
            VGroup(matrix[0][9],
                   matrix[0][15], 
                   matrix[0][19],
                   matrix[0][23]), # cột C (index hơi thủ công nhưng ổn)
            color=YELLOW
        ).scale(1.4)
        col_line_A = Line(UP, 0.7*DOWN, color=colors["A"], stroke_width=12).set_opacity(0.5).next_to(node_columns[0], DOWN)
        col_line_B = Line(UP, 0.7*DOWN, color=colors["B"], stroke_width=12).set_opacity(0.5).next_to(node_columns[1], DOWN)
        col_line_C = Line(UP, 0.7*DOWN, color=colors["C"], stroke_width=12).set_opacity(0.5).next_to(node_columns[2], DOWN)
        col_line_D = Line(UP, 0.7*DOWN, color=colors["D"], stroke_width=12).set_opacity(0.5).next_to(node_columns[3], DOWN)
        self.play(FadeIn(node_columns), FadeIn(node_rows),
                  FadeIn(col_line_A),
                  FadeIn(col_line_B),
                  FadeIn(col_line_C),
                  FadeIn(col_line_D))


        # -----------------------------
        # 3. HIGHLIGHT COLUMN = OUTGOING LINKS
        # -----------------------------
        # col_box = SurroundingRectangle(
        #     VGroup(matrix[0][10],
        #            matrix[0][14], 
        #            matrix[0][18],
        #            matrix[0][22]), # cột C (index hơi thủ công nhưng ổn)
        #     # matrix.get_columns()[2],
        #     color=YELLOW
        # ).scale(1.4)

        # arrows.set_opacity(0.5)
        # arrows[2].set_opacity(1)
        # arrows[3].set_opacity(1)
        # self.play(Create(col_box))
        # self.wait()
        # entry_A = matrix[0][10]  # 1/2 → A
        # entry_D = matrix[0][22]  # 1/2 → D

        # glow_A = SurroundingRectangle(entry_A, color=GREEN).scale(1.35).shift(0.15*UP)
        # glow_D = SurroundingRectangle(entry_D, color=GREEN).scale(1.35).shift(0.15*DOWN)

        # line_A = Line(glow_A, nodes["A"], color=GREEN)
        # line_D = Line(glow_D, nodes["D"], color=GREEN)

        # self.play(Create(glow_A), Create(line_A))
        # self.wait(0.5)
        # self.play(Create(glow_D), Create(line_D))
        # self.wait()
        # self.play(FadeOut(glow_A), FadeOut(line_A),
        #           FadeOut(glow_D), FadeOut(line_D))
        # self.play(FadeOut(col_box))
        # arrows.set_opacity(1)

        # -----------------------------
        # 4. RANK VECTOR
        # -----------------------------
        rank_vec = MathTex(
            r"""
            r =
            \begin{pmatrix}
            0.25 \\ 0.25 \\ 0.25 \\ 0.25
            \end{pmatrix}
            """
        ).scale(0.9)

        rank_vec.next_to(matrix, LEFT, buff=1)

        self.play(Write(rank_vec[0][:6]), Write(rank_vec[0][-4:]))
        rank_vec_from_nodes = {
            "A": rank_vec[0][6:10],
            "B": rank_vec[0][10:14],
            "C": rank_vec[0][14:18],
            "D": rank_vec[0][18:22],
        }
        # for k in nodes:
        #     self.play(Write(rank_vec_from_nodes[k]))
        # self.wait()

        # -----------------------------
        # 5. MATRIX MULTIPLICATION
        # -----------------------------
        equation = MathTex(
            r"r^{(k+1)} = M r^{(k)}"
        ).to_corner(UP)

        # self.play(Write(equation))
        self.wait()

        # -----------------------------
        # 6. CONVERGENCE TO EIGENVECTOR
        # -----------------------------
        eig = MathTex(
            r"M r = r"
        ).scale(1.2)

        eig.move_to(equation)

        self.play(Transform(equation, eig))
        self.wait(2)
from manim import *

class MarkovColumnMapping(Scene):
    def construct(self):
        # -----------------------------
        # GRAPH
        # -----------------------------
        pos = {
            "A": LEFT * 4 + UP * 1.5,
            "B": LEFT * 2 + UP * 2.5,
            "C": LEFT * 1 + DOWN * 0.5,
            "D": LEFT * 3 + DOWN * 2.5,
        }

        nodes = {k: Dot(v, radius=0.12) for k, v in pos.items()}
        labels = {
            k: Text(k, font_size=24).next_to(nodes[k], UP)
            for k in nodes
        }

        # edges = [
        #     ("A", "B"),
        #     ("B", "C"),
        #     ("C", "A"),
        #     ("C", "D"),
        #     ("D", "C"),
        # ]

        # arrows = VGroup(*[
        #     Arrow(
        #         nodes[a].get_center(),
        #         nodes[b].get_center(),
        #         buff=0.15,
        #         stroke_width=2
        #     )
        #     for a, b in edges
        # ])

        edges = {
            ("C", "A"): Arrow(nodes["C"], nodes["A"], buff=0.15),
            ("C", "D"): Arrow(nodes["C"], nodes["D"], buff=0.15),
        }

        self.play(
            *[FadeIn(n) for n in nodes.values()],
            *[FadeIn(l) for l in labels.values()]
        )
        self.play(*[Create(a) for a in edges.values()])

        # -----------------------------
        # MARKOV MATRIX
        # -----------------------------
        matrix = MathTex(
            r"""
            M =
            \begin{pmatrix}
            0 & 0 & \frac12 & 0 \\
            1 & 0 & 0 & 0 \\
            0 & 1 & 0 & 1 \\
            0 & 0 & \frac12 & 0
            \end{pmatrix}
            """
        ).scale(0.8)

        matrix.to_edge(RIGHT)
        self.play(Write(matrix))

        # -----------------------------
        # HIGHLIGHT NODE C
        # -----------------------------
        node_box = SurroundingRectangle(nodes["C"], color=YELLOW)
        self.play(Create(node_box))
        self.wait(0.3)

        # -----------------------------
        # HIGHLIGHT OUTGOING EDGES
        # -----------------------------
        self.play(
            *[
                edge.animate.set_color(YELLOW)
                for edge in edges.values()
            ]
        )
        self.wait(0.3)

        # -----------------------------
        # HIGHLIGHT COLUMN C (3rd column)
        # -----------------------------
        col_indices = VGroup(matrix[0][10], matrix[0][14], 
                             matrix[0][18], matrix[0][22])  # cột C
        col_box = SurroundingRectangle(col_indices, color=YELLOW).scale(1.3)

        self.play(Create(col_box))
        self.wait()

        # -----------------------------
        # MAP MATRIX ENTRIES → NODES
        # -----------------------------
        entry_A = matrix[0][10]  # 1/2 → A
        entry_D = matrix[0][18]  # 1/2 → D

        glow_A = SurroundingRectangle(entry_A, color=GREEN)
        glow_D = SurroundingRectangle(entry_D, color=GREEN)

        line_A = Line(entry_A.get_center(), nodes["A"].get_center(), color=GREEN)
        line_D = Line(entry_D.get_center(), nodes["D"].get_center(), color=GREEN)

        self.play(Create(glow_A), Create(line_A))
        self.wait(0.5)

        self.play(Create(glow_D), Create(line_D))
        self.wait(1)

        # -----------------------------
        # CLEAN UP
        # -----------------------------
        self.play(
            FadeOut(node_box),
            FadeOut(col_box),
            FadeOut(glow_A),
            FadeOut(glow_D),
            FadeOut(line_A),
            FadeOut(line_D),
        )
        self.wait()

class PageRankPowerIteration(Scene):
    def construct(self):
        self.wait()
        google = SVGMobject("assets/google.svg").scale(0.45).to_corner(UL)
        subtitle = Tex("PageRank").next_to(google, RIGHT)
        self.add(google, subtitle)
        self.wait()
        
        # -----------------------------
        # GRAPH (LEFT)
        # -----------------------------
        pos = {
            "A": LEFT * 4 + UP * 1.5,
            "B": LEFT * 2 + UP * 2.5,
            "C": LEFT * 1 + DOWN * 0.5,
            "D": LEFT * 3 + DOWN * 2.5,
        }

        nodes = {k: Dot(v, radius=0.4, color=colors[k]) for k, v in pos.items()}
        labels = {
            k: Text(k, font_size=24).move_to(nodes[k].get_center())
            for k in nodes
        }

        edges = [
            ("A", "B"),
            ("B", "C"),
            ("C", "A"),
            ("C", "D"),
            ("D", "C"),
        ]

        arrows = VGroup(*[
            Arrow(nodes[a], nodes[b], buff=0.15, stroke_width=2, max_tip_length_to_length_ratio=0.1)
            for a, b in edges
        ])
        arrows[3].shift(0.1*LEFT+0.1*UP)
        arrows[4].shift(0.1*RIGHT+0.1*DOWN)

        for k in nodes:
            self.add_sound("voiceovers/ui_pop_up.mp3")
            self.play(FadeIn(nodes[k]), FadeIn(labels[k]))
        self.add_sound("voiceovers/Markov_part1.mp3")
        
        self.play(Create(arrows))
        self.wait()

        # -----------------------------
        # PAGE RANK VALUES
        # -----------------------------
        ranks = {
            k: ValueTracker(0.25)
            for k in nodes
        }

        rank_labels = {
            k: always_redraw(
                lambda k=k: DecimalNumber(
                    ranks[k].get_value(),
                    num_decimal_places=3,
                    font_size=22
                ).next_to(nodes[k], DOWN).add_background_rectangle()
            )
            for k in nodes
        }
        self.add_sound("voiceovers/send-message.mp3")
        self.play(*[FadeIn(v, target_position=google) for v in rank_labels.values()], run_time=2)
        self.wait()

        matrix = MathTex(
            r"""
            M =
            \begin{pmatrix}
            0 & 0 & \frac12 & 0 \\
            1 & 0 & 0 & 0 \\
            0 & 1 & 0 & 1 \\
            0 & 0 & \frac12 & 0
            \end{pmatrix}
            """
        ).scale(0.8)
        matrix.to_edge(RIGHT)
        matrix[0][0].set_color(BLUE)

        self.play(Write(matrix))
        self.wait()
        self.play(FadeOut(matrix[0][:2]))
        node_columns = VGroup(Text("A").set_color(colors["A"]).scale(0.65).next_to(matrix[0][6], UP),
                      Text("B").set_color(colors["B"]).scale(0.65).next_to(matrix[0][7], UP),
                      Text("C").set_color(colors["C"]).scale(0.65).next_to(matrix[0][10], 1.8*UP),
                      Text("D").set_color(colors["D"]).scale(0.65).next_to(matrix[0][11], UP))

        node_rows = VGroup(Text("A").set_color(colors["A"]).scale(0.65).next_to(matrix[0][6], 2*LEFT),
                         Text("B").set_color(colors["B"]).scale(0.65).next_to(matrix[0][12], 2.3*LEFT),
                         Text("C").set_color(colors["C"]).scale(0.65).next_to(matrix[0][16], 2*LEFT),
                         Text("D").set_color(colors["D"]).scale(0.65).next_to(matrix[0][20], 2*LEFT))
        

        col_box_C = SurroundingRectangle(
            VGroup(matrix[0][10],
                   matrix[0][14], 
                   matrix[0][18],
                   matrix[0][22]), # cột C (index hơi thủ công nhưng ổn)
            color=YELLOW
        ).scale(1.4)
        col_line_A = Line(UP, 0.7*DOWN, color=colors["A"], stroke_width=12).set_opacity(0.5).next_to(node_columns[0], DOWN)
        col_line_B = Line(UP, 0.7*DOWN, color=colors["B"], stroke_width=12).set_opacity(0.5).next_to(node_columns[1], DOWN)
        col_line_C = Line(UP, 0.7*DOWN, color=colors["C"], stroke_width=12).set_opacity(0.5).next_to(node_columns[2], DOWN)
        col_line_D = Line(UP, 0.7*DOWN, color=colors["D"], stroke_width=12).set_opacity(0.5).next_to(node_columns[3], DOWN)
        self.add_sound("voiceovers/Markov_part2.mp3")
        self.play(FadeIn(node_columns), FadeIn(node_rows))
        self.play(FadeIn(col_line_A))
        self.play(FadeIn(col_line_B))
        self.play(FadeIn(col_line_C))
        self.play(FadeIn(col_line_D))
        self.play(FadeOut(col_line_A), FadeOut(col_line_B), FadeOut(col_line_C), FadeOut(col_line_D))
        self.wait()
        self.add_sound("voiceovers/Markov_mapping_part1.mp3")
        
        arrows.set_opacity(0.5)
        arrows[2].set_opacity(1)
        arrows[3].set_opacity(1)
        self.play(FocusOn(nodes["C"]))
        self.play(Wiggle(arrows[2]), Wiggle(arrows[3]))
        self.play(Circumscribe(matrix))
        self.wait()
        self.play(Create(col_box_C))
        self.wait()
        entry_A = matrix[0][10]  # 1/2 → A
        entry_D = matrix[0][22]  # 1/2 → D

        glow_A = SurroundingRectangle(entry_A, color=GREEN).scale(1.4).shift(0.15*UP)
        glow_D = SurroundingRectangle(entry_D, color=GREEN).scale(1.4).shift(0.15*DOWN)

        line_A = Line(glow_A, nodes["A"], color=GREEN)
        line_D = Line(glow_D, nodes["D"], color=GREEN)
        self.add_sound("voiceovers/Markov_mapping_part2.mp3")
        self.play(Create(glow_A), Create(line_A))
        self.wait()
        self.play(Create(glow_D), Create(line_D))
        self.wait(2)
        self.play(FadeOut(glow_A), FadeOut(line_A),
                  FadeOut(glow_D), FadeOut(line_D))
        self.play(FadeOut(col_box_C), FadeOut(node_columns), FadeOut(node_rows))
        self.play(FadeIn(matrix[0][:2]))
        self.wait()
        self.add_sound("voiceovers/PageRankPowerIteration_part1.mp3")
        arrows.set_opacity(1)
        rank_vec = MathTex(
            r"""
            r =
            \begin{pmatrix}
            0.25 \\ 0.25 \\ 0.25 \\ 0.25
            \end{pmatrix}
            """
        ).scale(0.9)

        rank_vec.next_to(matrix, LEFT, buff=1)
        rank_vec[0][0].set_color(YELLOW)
        
        rank_vec_from_nodes = {
            "A": rank_vec[0][6:10],
            "B": rank_vec[0][10:14],
            "C": rank_vec[0][14:18],
            "D": rank_vec[0][18:22],
        }
        rank_labels_copy = {
            k: rank_labels[k].copy()
            for k in nodes
        }
        self.play(Write(rank_vec[0][:6]), 
                  *[rank_labels_copy[k].scale(1.6).animate.move_to(rank_vec_from_nodes[k]) 
                    for k in nodes],
                  Write(rank_vec[0][-4:]))
        
        self.wait()
        equation = MathTex(
            r"r^{(k+1)} = M r^{(k)}"
        ).to_corner(UR)
        rank_vec_left = equation[0][0].set_color(YELLOW)
        matrix_text = equation[0][-5].set_color(BLUE)
        rank_vec_right = equation[0][-4].set_color(YELLOW)
        rank_vec_left.target, matrix_text.target, rank_vec_right.target = rank_vec[0][0], matrix[0][0], rank_vec[0][0]
        for mob in (rank_vec_left, matrix_text, rank_vec_right):
            mob.save_state()
            mob.move_to(mob.target)
        self.play(Write(equation), *[mob.animate.restore() for mob in (rank_vec_left, matrix_text, rank_vec_right)])
        arrow_equation = Arrow(LEFT, RIGHT).next_to(equation, LEFT)
        matrix_multiply = Text("Nhân ma trận", font="Noto Sans", color=YELLOW)
        matrix_multiply.scale(0.7).next_to(arrow_equation, LEFT)
        glow = SurroundingRectangle(equation, color=GREEN, buff=0.2)
        self.play(Create(glow), FadeIn(matrix_multiply), FadeIn(arrow_equation))
        self.wait()
        self.play(FadeOut(glow))
        

        # -----------------------------
        # MARKOV MATRIX
        # -----------------------------
        M = np.array([
            [0,   0,   0.5, 0],
            [1,   0,   0,   0],
            [0,   1,   0,   1],
            [0,   0,   0.5, 0],
        ])

        def iterate():
            current = np.array([ranks[k].get_value() for k in ["A","B","C","D"]])
            new = M @ current
            return dict(zip(["A","B","C","D"], new))

        # -----------------------------
        # ITERATIONS
        # -----------------------------
        for step in range(5):
            new_vals = iterate()

            self.play(
                *[
                    ranks[k].animate.set_value(new_vals[k])
                    for k in ranks
                ],
                run_time=1
            )

            # glow strongest node
            max_node = max(new_vals, key=new_vals.get)
            glow = SurroundingRectangle(nodes[max_node], color=YELLOW)
            self.play(Create(glow), run_time=0.3)
            self.play(FadeOut(glow), run_time=0.3)
            rank_labels_new_copy = {
                k: rank_labels[k].copy().scale(1.6).move_to(rank_vec_from_nodes[k])
                for k in nodes
            }
            self.play(*[Transform(rank_labels_copy[k], rank_labels_new_copy[k]) for k in nodes])
        # -----------------------------
        # CONVERGENCE
        # -----------------------------
        steady = MathTex(
            r"M r = r"
        ).move_to(equation)
        steady[0][0].set_color(BLUE)
        steady[0][1].set_color(YELLOW)
        steady[0][-1].set_color(YELLOW)
        self.add_sound("voiceovers/PageRankPowerIteration_part2.mp3")
        self.play(Circumscribe(rank_vec))
        self.add_sound("voiceovers/win.wav")
        self.play(Transform(equation, steady))
        self.play(FadeOut(matrix))
        final_ranks = {
            "A": "#2",
            "B": "#3",
            "C": "#1",
            "D": "#2"
        }
        for k in rank_vec_from_nodes:
            arrow = Arrow(0.5*RIGHT, 0.5*LEFT).set_color(colors[k]).next_to(rank_vec_from_nodes[k], RIGHT, MED_LARGE_BUFF)
            label = MathTex(k).set_color(colors[k]).next_to(arrow, RIGHT)
            rank = Text(final_ranks[k]).scale(0.65).set_color(colors[k]).next_to(label, RIGHT)
            self.play(FadeIn(label), GrowArrow(arrow), FadeIn(rank))
        self.wait(5)

class PageRankDamping(Scene):
    def construct(self):
        # -----------------------------
        # GRAPH
        # -----------------------------
        pos = {
            "A": LEFT * 4 + UP * 1.5,
            "B": LEFT * 2 + UP * 2.5,
            "C": LEFT * 1 + DOWN * 0.5,
            "D": LEFT * 3 + DOWN * 2.5,
        }

        nodes = {k: Dot(v, radius=0.12) for k, v in pos.items()}
        labels = {
            k: Text(k, font_size=24).next_to(nodes[k], UP)
            for k in nodes
        }

        edges = [
            ("A", "B"),
            ("B", "C"),
            ("C", "A"),
            ("C", "D"),
            ("D", "C"),
        ]

        arrows = VGroup(*[
            Arrow(nodes[a], nodes[b], buff=0.15)
            for a, b in edges
        ])

        self.play(
            *[FadeIn(n) for n in nodes.values()],
            *[FadeIn(l) for l in labels.values()]
        )
        self.play(Create(arrows))

        # -----------------------------
        # INITIAL RANKS
        # -----------------------------
        ranks = {k: ValueTracker(0.25) for k in nodes}

        rank_labels = {
            k: always_redraw(
                lambda k=k: DecimalNumber(
                    ranks[k].get_value(),
                    num_decimal_places=3,
                    font_size=22
                ).next_to(nodes[k], DOWN)
            )
            for k in nodes
        }

        self.play(*[FadeIn(v) for v in rank_labels.values()])

        # -----------------------------
        # EQUATION WITH DAMPING
        # -----------------------------
        equation = MathTex(
            r"r^{(k+1)} = \alpha M r^{(k)} + (1-\alpha)\frac{1}{n}\mathbf{1}"
        ).to_corner(UR)

        self.play(Write(equation))
        self.wait()

        alpha_text = MathTex(r"\alpha = 0.85").next_to(equation, DOWN)
        self.play(FadeIn(alpha_text))
        self.wait()

        # -----------------------------
        # MARKOV MATRIX
        # -----------------------------
        M = np.array([
            [0,   0,   0.5, 0],
            [1,   0,   0,   0],
            [0,   1,   0,   1],
            [0,   0,   0.5, 0],
        ])

        n = 4
        teleport = np.ones(n) / n

        def iterate():
            r = np.array([ranks[k].get_value() for k in ["A","B","C","D"]])
            new = 0.85 * (M @ r) + 0.15 * teleport
            return dict(zip(["A","B","C","D"], new))

        # -----------------------------
        # TELEPORT VISUAL (GLOW ALL)
        # -----------------------------
        teleport_glow = VGroup(*[
            SurroundingRectangle(nodes[k], color=BLUE, buff=0.2)
            for k in nodes
        ])

        # -----------------------------
        # ITERATIONS
        # -----------------------------
        for step in range(5):
            # teleport pulse
            self.play(FadeIn(teleport_glow), run_time=0.3)
            self.play(FadeOut(teleport_glow), run_time=0.3)

            new_vals = iterate()

            self.play(
                *[
                    ranks[k].animate.set_value(new_vals[k])
                    for k in ranks
                ],
                run_time=1
            )

        # -----------------------------
        # CONVERGENCE
        # -----------------------------
        steady = MathTex(
            r"r = \alpha M r + (1-\alpha)\frac{1}{n}\mathbf{1}"
        ).move_to(equation)

        self.play(Transform(equation, steady))
        self.wait(2)

class PageRankToEigen(Scene):
    def construct(self):
        self.add_sound("voiceovers/PageRankToEigen_part1.mp3")
        
        # -----------------------------
        # 1. GRAPH + FINAL RANK
        # -----------------------------
        pos = {
            "A": LEFT * 3 + UP * 1,
            "B": LEFT * 1.5 + UP * 2,
            "C": LEFT * 0.5 + DOWN * 0.5,
            "D": LEFT * 2.5 + DOWN * 2,
        }
        google = SVGMobject("assets/google.svg").scale(0.4).move_to(LEFT * 2 + DOWN * 0.5)

        nodes = {k: Dot(v, radius=0.4, color=colors[k]) for k, v in pos.items()}
        labels = {
            k: Text(k, font_size=22).move_to(nodes[k].get_center())
            for k in nodes
        }

        ranks = {
            "A": 0.22,
            "B": 0.18,
            "C": 0.42,
            "D": 0.18,
        }

        rank_labels = {
            k: DecimalNumber(v, num_decimal_places=2, font_size=20)
                .next_to(nodes[k], DOWN)
            for k, v in ranks.items()
        }

        self.play(
            *[FadeIn(n) for n in nodes.values()],
            *[FadeIn(l) for l in labels.values()],
            *[FadeIn(r) for r in rank_labels.values()],
            FadeIn(google)
        )
        self.wait()

        # -----------------------------
        # 2. VECTOR PAGE RANK
        # -----------------------------
        r_vec = MathTex(
            r"r = \begin{pmatrix} 0.22 \\ 0.18 \\ 0.42 \\ 0.18 \end{pmatrix}"
        ).to_corner(RIGHT)
        r_vec[0][0].set_color(YELLOW)

        self.play(Write(r_vec))

        # -----------------------------
        # 3. FADE GRAPH → ABSTRACT SPACE
        # -----------------------------
        graph_group = VGroup(*nodes.values(), *labels.values(), *rank_labels.values(), google)

        self.play(
            graph_group.animate.set_opacity(0.25),
            r_vec.animate.move_to(ORIGIN).scale(1.2)
        )

        # -----------------------------
        # 4. EIGENVECTOR EQUATION
        # -----------------------------
        eigen_eq = MathTex(
            r"M r = r"
        ).next_to(r_vec, UP)
        eigen_eq[0][0].set_color(BLUE)
        eigen_eq[0][1].set_color(YELLOW)
        eigen_eq[0][-1].set_color(YELLOW)

        self.play(Write(eigen_eq))

        # -----------------------------
        # 5. GENERALIZATION
        # -----------------------------
        general_eq = MathTex(
            r"A\vec v = \lambda \vec v"
        ).scale(1.4)
        general_eq[0][0].set_color(BLUE)
        general_eq[0][1:3].set_color(YELLOW)
        general_eq[0][-3].set_color(GREEN)
        general_eq[0][-2:].set_color(YELLOW)
        self.add_sound("voiceovers/PageRankToEigen_part2.mp3")
        self.play(
            FadeOut(eigen_eq),
            Transform(r_vec, general_eq),
            FadeOut(graph_group),
            run_time=2
        )
        self.wait()

        # -----------------------------
        # 6. FINAL TEXT
        # -----------------------------
        final_text = Text(
            "Vectơ riêng = hướng không đổi",
            font_size=36, font="Noto Sans",
        ).next_to(general_eq, DOWN)
        final_text[:10].set_color(YELLOW)

        self.play(FadeIn(final_text))
        
        thank = SVGMobject("assets/ThankYou.svg").to_corner(UL)
        
        self.wait(2)
        self.add_sound("voiceovers/thankyou.wav")
        self.play(DrawBorderThenFill(thank))
        self.wait(2)
        self.play(FadeOut(final_text), FadeOut(thank))
        self.wait()


from manim import *
import numpy as np

class PageRankEigenThumbnail(Scene):
    def construct(self):
        self.camera.background_color = "#0e1117"

        # -----------------------------
        # LEFT: GRAPH (INTERNET)
        # -----------------------------
        positions = {
            "A": LEFT * 4 + UP * 1.2,
            "B": LEFT * 2.8 + UP * 2.2,
            "C": LEFT * 2 + DOWN * 0.2,
            "D": LEFT * 3.5 + DOWN * 2,
        }

        nodes = {
            k: Dot(v, radius=0.13, color=BLUE_B)
            for k, v in positions.items()
        }

        edges = [
            ("A", "B"), ("B", "C"), ("C", "A"),
            ("C", "D"), ("D", "C")
        ]

        arrows = VGroup(*[
            Arrow(
                nodes[a].get_center(),
                nodes[b].get_center(),
                buff=0.15,
                stroke_width=3,
                color=BLUE_A
            )
            for a, b in edges
        ])

        graph = VGroup(*nodes.values(), arrows)
        graph.set_opacity(0.8)

        # -----------------------------
        # RIGHT: EIGENVECTOR
        # -----------------------------
        vector = Arrow(
            ORIGIN,
            UP * 2.5 + RIGHT * 0.5,
            buff=0,
            stroke_width=12,
            color=YELLOW
        )

        vector.move_to(RIGHT * 3)

        glow = vector.copy().set_stroke(
            width=24,
            opacity=0.3,
            color=YELLOW
        )

        # -----------------------------
        # CENTER ARROW
        # -----------------------------
        arrow_mid = MathTex(r"\Longrightarrow").scale(2)
        arrow_mid.move_to(ORIGIN)

        # -----------------------------
        # TEXT
        # -----------------------------
        text_left = Text(
            "PageRank",
            font_size=52,
            color=BLUE_B,
            weight=BOLD
        ).next_to(graph, DOWN, buff=0.6)

        text_right = Text(
            "Eigenvector?",
            font_size=56,
            color=YELLOW,
            weight=BOLD
        ).next_to(vector, DOWN, buff=0.6)

        # -----------------------------
        # ADD ALL
        # -----------------------------
        self.add(
            graph,
            glow,
            vector,
            arrow_mid,
            text_left,
            text_right
        )
from manim import *

class PageRankLogoThumbnail(Scene):
    def construct(self):
        self.camera.background_color = "#0e1117"

        # -----------------------------
        # LOGO POSITIONS (LEFT)
        # -----------------------------
        pos = {
            "google": LEFT * 4 + UP * 1.5,
            "youtube": LEFT * 2.7 + UP * 2.7,
            "wiki": LEFT * 2 + DOWN * 0.2,
            "facebook": LEFT * 3.6 + DOWN * 2.2,
        }

        logos = {
            "google": ImageMobject("google.png").scale(0.35),
            "youtube": ImageMobject("youtube.png").scale(0.35),
            "wiki": ImageMobject("wikipedia.png").scale(0.35),
            "facebook": ImageMobject("facebook.png").scale(0.35),
        }

        for k in logos:
            logos[k].move_to(pos[k])

        # -----------------------------
        # LINKS (ARROWS)
        # -----------------------------
        edges = [
            ("google", "youtube"),
            ("youtube", "wiki"),
            ("wiki", "google"),
            ("wiki", "facebook"),
            ("facebook", "wiki"),
        ]

        arrows = VGroup(*[
            Arrow(
                logos[a].get_center(),
                logos[b].get_center(),
                buff=0.25,
                stroke_width=3,
                color=BLUE_B
            )
            for a, b in edges
        ])

        graph = VGroup(*logos.values(), arrows).set_opacity(0.9)

        # -----------------------------
        # RIGHT: EIGENVECTOR ARROW
        # -----------------------------
        vector = Arrow(
            ORIGIN,
            UP * 2.8 + RIGHT * 0.6,
            buff=0,
            stroke_width=14,
            color=YELLOW
        ).move_to(RIGHT * 3)

        glow = vector.copy().set_stroke(
            width=28,
            opacity=0.35,
            color=YELLOW
        )

        # -----------------------------
        # CENTER SYMBOL
        # -----------------------------
        mid_arrow = MathTex(r"\Longrightarrow").scale(2)
        mid_arrow.move_to(ORIGIN)

        # -----------------------------
        # TEXT
        # -----------------------------
        text_left = Text(
            "PageRank",
            font_size=50,
            color=BLUE_B,
            weight=BOLD
        ).next_to(graph, DOWN, buff=0.6)

        text_right = Text(
            "Eigenvector?",
            font_size=56,
            color=YELLOW,
            weight=BOLD
        ).next_to(vector, DOWN, buff=0.6)

        # -----------------------------
        # ADD
        # -----------------------------
        self.add(
            graph,
            glow,
            vector,
            mid_arrow,
            text_left,
            text_right
        )

class TextMoreCustomization(Scene):
    def construct(self):
        text1 = Text(
            'Google',
            t2c={'[:1]': '#3174f0', '[1:2]': '#e53125',
                 '[2:3]': '#fbb003', '[3:4]': '#3174f0',
                 '[4:5]': '#269a43', '[5:]': '#e53125'}, font_size=58).scale(3)
        lambda_text = MathTex(r"\lambda").set_color('#269a43')
        lambda_text.scale(5.5).move_to(text1[4:5])
        text1[:4].shift(0.5*LEFT)
        text1[4:].shift(0.15*RIGHT)
        self.add(text1)
        self.play(Transform(text1[4:5], lambda_text))
        self.wait()