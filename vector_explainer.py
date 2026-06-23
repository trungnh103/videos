from manim import *
import numpy as np

V_COLOR = YELLOW
W_COLOR = MAROON_B
SUM_COLOR = PINK

def coord_vec(point, color=BLUE, stroke_width=3):
    """Create a 2D Vector from origin to `point` (tuple)."""
    return Vector(point, color=color, stroke_width=stroke_width)

class IntroScene(Scene):
    def construct(self):
        self.add_sound("voiceovers/IntroScene.mp3")
        motion = SVGMobject("assets/car.svg").scale(0.7).shift(3*LEFT+2*UP)
        motion_text = Text("Chuyển động", font="Noto Sans").scale(0.65).next_to(motion, DOWN)
        force = SVGMobject("assets/pull.svg").shift(3*RIGHT+2*UP)
        force_text = Text("Lực", font="Noto Sans").scale(0.65).next_to(force, DOWN)
        graphics = SVGMobject("assets/graphics.svg").shift(3*LEFT+2*DOWN)
        graphics_text = Text("Đồ họa", font="Noto Sans").scale(0.65).next_to(graphics, DOWN)
        navigation = SVGMobject("assets/navigation.svg").shift(3*RIGHT+2*DOWN)
        navigation_text = Text("Điều hướng", font="Noto Sans").scale(0.65).next_to(navigation, DOWN)
        title = Text("Vectơ?", font="Noto Sans", color=YELLOW)
        subtitle = Text("Độ lớn + Hướng", font="Noto Sans").scale(0.7).next_to(title, DOWN)
        arrow = Arrow(start=LEFT, end=RIGHT, color=YELLOW).shift(UP)
        self.play(Write(title), run_time=1.5)
        self.wait(2)
        self.play(DrawBorderThenFill(motion), Write(motion_text))
        self.play(DrawBorderThenFill(force), Write(force_text))
        self.play(DrawBorderThenFill(graphics), Write(graphics_text))
        self.play(DrawBorderThenFill(navigation), Write(navigation_text))
        self.wait()
        self.play(motion.animate.shift(RIGHT), rate_func=there_and_back)
        self.wait()
        self.play(force.animate.shift(LEFT), rate_func=there_and_back)
        self.wait()
        self.play(Flash(graphics))
        self.wait()
        self.play(Transform(
            VGroup(motion, motion_text, force, force_text, graphics, graphics_text, navigation, navigation_text),
            arrow))
        self.wait(3)
        self.play(Write(subtitle))
        self.wait(21)

class ScalarsVectorsScene(Scene):
    def construct(self):
        self.add_sound("voiceovers/ScalarsVectorsScene.mp3")
        title = Text("Số vô hướng vs Vectơ", font="Noto Sans", font_size=40)
        title[:9].set_color(BLUE)
        title[-5:].set_color(YELLOW)
        title.scale(1.2)
        title.to_edge(UP)
        line = Line(LEFT * 6, RIGHT * 6, color=WHITE).set_stroke(width=3)
        line.next_to(title, DOWN, buff=0.1)
        self.play(Write(title), Create(line), run_time=2)
        self.wait()
        self.play(ApplyWave(title))

        scalar_box = Rectangle(width=4, height=3).shift(LEFT*3)
        vector_box = Rectangle(width=4, height=3).shift(RIGHT*3)
        scalar_label = Text("Số vô hướng", font="Noto Sans", color=BLUE).scale(0.65).next_to(scalar_box, UP)
        vector_label = Text("Vectơ", font="Noto Sans", color=YELLOW).scale(0.65).next_to(vector_box, UP)
        self.play(Create(scalar_box), Create(vector_box), Write(scalar_label), Write(vector_label))
        self.wait(4)

        scalar_icons = [
            ("assets/temperature.svg", "30°C", 0.4),
            ("assets/mass.svg", "2 kg", 0.2), 
            ("assets/time.svg", "5 s", 0.4),
        ]
        scalars = Mobject()
        for icon, magnitude, scale in scalar_icons:
            image = SVGMobject(icon)
            image.scale(scale)
            image.set_stroke(width=1)
            magnitude = Text(magnitude).scale(0.6).next_to(image, RIGHT)
            image.add(magnitude)
            scalars.add(image)
        scalars.arrange(DOWN, aligned_edge=LEFT).move_to(scalar_box.get_center())
        self.play(LaggedStart(*[FadeIn(scalar, shift=UP) for scalar in scalars], lag_ratio=2.5))
        self.wait(5.5)

        vectors = Mobject()
        vector_icons = [
            ("assets/velocity.svg", "5 m/s", 0.3),
            ("assets/force_box.svg", "200 newton", 0.4), 
            ("assets/acceleration.svg", "9,80665 m/s2", 0.4),
        ]
        for icon, magnitude, scale in vector_icons:
            image = SVGMobject(icon)
            image.scale(scale)
            magnitude = Text(magnitude).scale(0.6).next_to(image, RIGHT)
            image.add(magnitude)
            vectors.add(image)
        vectors.arrange(DOWN, aligned_edge=LEFT).move_to(vector_box.get_center())
        self.play(LaggedStart(*[FadeIn(vector, shift=UP) for vector in vectors], lag_ratio=3))
        self.wait(5)

        note = Text("Số vô hướng: chỉ có độ lớn. Vectơ: độ lớn và hướng.", font="Noto Sans")
        note.scale(0.7).to_edge(DOWN)
        self.play(Write(note))
        self.wait(3)

class InCoordinate(Scene):
    def construct(self):
        title = Text("Vectơ trong không gian 2D", font="Noto Sans", color=YELLOW)
        title.set_z_index(3)
        title.scale(0.7).to_corner(UL)
        self.play(Write(title))
        self.add_sound("voiceovers/InCoordinate.mp3")
        axes = NumberPlane()
        v = Vector([3,2], color=YELLOW)
        
        label = v.coordinate_label(color=YELLOW)
        arrow_right = LabeledLine("3", start=ORIGIN, end=RIGHT*3, label_position=0.5, color=GREEN)
        arrow_up = LabeledLine("2", start=RIGHT*3, end=RIGHT*3 + UP*2, label_position=0.5, color=RED)
        self.play(Create(axes))
        self.wait(2)
        self.play(GrowArrow(v))
        self.wait()
        self.play(Write(label))
        self.wait(2.5)
        self.play(FocusOn(ORIGIN))
        self.play(FocusOn(v.get_end()))
        self.wait(2)
        self.add_sound("voiceovers/line.mp3")
        self.play(Create(arrow_right))
        self.add_sound("voiceovers/line.mp3")
        self.play(Create(arrow_up))
        self.play(FadeOut(arrow_right), FadeOut(arrow_up))
        self.wait(4)
        self.play(v.animate(path_arc=-3*PI/2).shift(LEFT * 4 + DOWN), run_time = 3)
        self.wait()
        self.play(v.animate.shift(-LEFT * 4 + UP))
        self.wait()

class Vector3D(ThreeDScene):
    def construct(self):
        title = Text("Vectơ trong không gian 3D", font="Noto Sans", color=YELLOW)
        self.add_fixed_in_frame_mobjects(title)
        title.scale(0.7).to_corner(UL)
        self.play(Write(title))
        self.add_sound("voiceovers/Vector3D.mp3")
        axes = ThreeDAxes()
        arrow = Arrow3D(
            start=np.array([0, 0, 0]),
            end=np.array([2, 1, 3]),
            color=YELLOW,
            resolution=8
        )
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.play(Create(axes), Create(arrow))
        
        z = Tex("z").set_color(BLUE).to_edge(UP).shift(0.2*LEFT)
        self.add_fixed_in_frame_mobjects(z)
        
        line1 = Line3D(np.array([0, 0, 0]), np.array([2, 0, 0]), color=GREEN)
        line2 = Line3D(np.array([2, 0, 0]), np.array([2, 1, 0]), color=RED)
        line3 = Line3D(np.array([2, 1, 0]), np.array([2, 1, 3]), color=BLUE)
        lines = VGroup(line1, line2, line3)

        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(6)
        self.play(Indicate(z))
        self.wait(3)
        array = Matrix([[2], [1], [3]])
        array.shift(2*RIGHT+2*UP)
        self.add_fixed_in_frame_mobjects(array)
        coordinates = array.get_entries()
        brackets = array.get_brackets()
        coordinates[0].set_color(GREEN).set_opacity(0)
        coordinates[1].set_color(RED).set_opacity(0)
        coordinates[2].set_color(BLUE).set_opacity(0)
        # self.add(brackets)
        for mob, line in zip(coordinates, lines):
            self.play(mob.animate.set_opacity(1))
            self.add_sound("voiceovers/line.mp3")
            self.play(Create(line))
        self.wait(8)
        self.stop_ambient_camera_rotation()
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES)
        self.wait()


class VectorAddition(Scene):
    def construct(self):  
        title = Text("Phép cộng vectơ", font="Noto Sans", color=YELLOW).scale(0.7)
        title.set_z_index(3)
        self.play(Write(title))
        self.add_sound("voiceovers/VectorAddition.mp3")
        self.play(title.animate.to_corner(UL))
        
        plane = NumberPlane()
        A = Vector([1, 2], color=YELLOW)
        B = Vector([3,-1], color=MAROON_B)
        B_moving = Vector([3,-1], color=MAROON_B)
        sum_vec = Vector([4,1], color=PINK)
        A_text = MathTex(r"\vec{a}").move_to(A.get_center()).shift(0.4*LEFT)
        B_text = MathTex(r"\vec{b}").move_to(B.get_center()).shift(0.4*DOWN)
        sum_label = MathTex(r"\vec{a}+\vec{b}").move_to(sum_vec.get_center()).shift(0.4*RIGHT+0.4*DOWN)
        label_A = A.coordinate_label()
        label_B = B_moving.coordinate_label()
        self.play(Create(plane))
        self.play(GrowArrow(A), FadeIn(A_text))
        self.play(GrowArrow(B_moving), FadeIn(B_text))
        B_tail_to_A = B_moving.copy()
        B_tail_to_A.shift(A.get_end())
        self.wait(3)
        self.play(Transform(B_moving, B_tail_to_A),
                  B_text.animate.move_to(B_tail_to_A.get_center()).shift(0.4*UP))
        self.wait(1.5)
        self.play(GrowArrow(sum_vec))
        self.wait(3)
        self.play(Write(sum_label))

        self.wait()
        self.play(FadeOut(B_moving), FadeOut(B_text), FadeOut(sum_vec), FadeOut(sum_label), FadeOut(A_text))
        B_copy = B.copy()
        self.play(GrowArrow(B_copy))
        self.play(FadeIn(label_A),
                  label_A.animate.next_to(A.get_end(), UP))
        self.play(FadeIn(label_B))
        plus = MathTex("+").next_to(label_A, RIGHT)
        self.play(Transform(B_copy, B_tail_to_A),
                  FadeIn(plus),
                  label_B.animate.next_to(plus, RIGHT))
        equal = MathTex("=").next_to(label_B, RIGHT)
        label_sum = sum_vec.coordinate_label()
        label_sum.next_to(equal, RIGHT)
        entries_A = label_A.get_entries()
        entries_B = label_B.get_entries()
        entries_sum = label_sum.get_entries()
        brackets = label_sum.get_brackets()

        self.play(GrowArrow(sum_vec),
                  FadeIn(equal),
                  FadeIn(brackets),
                  TransformFromCopy(VGroup(entries_A[0], plus, entries_B[0]), entries_sum[0]),
                  TransformFromCopy(VGroup(entries_A[1], plus, entries_B[1]), entries_sum[1]))
        self.wait(6)
        self.play(FadeOut(label_A), FadeOut(label_B), FadeOut(label_sum), FadeOut(plus), FadeOut(equal), FadeOut(sum_vec), FadeOut(B_copy))
        self.play(GrowArrow(B))
        A.set_z_index(3)
        B.set_z_index(3)
        parallelogram = Polygon(ORIGIN, A.get_end(), A.get_end()+B.get_end(), B.get_end())
        self.wait(3)
        self.play(Create(parallelogram))
        self.play(GrowArrow(sum_vec))
        self.wait(11)

class ShowScalarMultiplication(Scene):
    def construct(self):
        
        title = Text("Phép nhân vô hướng", font="Noto Sans", color=YELLOW)
        title.scale(0.7).set_z_index(3)
        self.play(Write(title))
        self.add_sound("voiceovers/ShowScalarMultiplication.mp3")
        self.play(title.animate.to_corner(UL))
        plane = NumberPlane()
        self.add(plane)

        v = Vector([3, 1], color=YELLOW)
        label = MathTex(r"\vec{v}").move_to(v.get_center())
        label.shift(0.4*LEFT+0.4*UP)
        self.play(GrowArrow(v), FadeIn(label))
        self.wait(8)
        self.play(Indicate(v))

        self.scale_vector(v, 2, label, shift=0.4*LEFT+0.4*UP)
        self.scale_vector(v, 0.5, label, shift=0.4*LEFT+0.4*UP)
        self.scale_vector(v, -1, label, shift=0.4*RIGHT+0.4*DOWN)
        long_v = Vector(2*v.get_end(), color=YELLOW)
        long_minus_v = Vector(-2*v.get_end(), color=YELLOW)
        self.play(
            FadeOut(label),
            Transform(v, long_v)
        )
        self.play(Transform(v, long_minus_v, run_time = 1.5))
        self.wait()

    def scale_vector(self, v, factor, v_label, v_name="v", factor_tex=None, shift=0.4*LEFT+0.4*UP):
        starting_mobjects = self.get_top_level_mobjects().copy()

        if factor_tex is None:
            factor_tex = str(factor)

        scaled_vector = Vector(factor * v.get_end(), color=YELLOW)

        label_tex = f"{factor_tex}\\vec{{\\textbf{{{v_name}}}}}"
        scaled_label = MathTex(label_tex).move_to(scaled_vector.get_center())
        scaled_label.shift(shift)

        factor_mob = MathTex(factor_tex)
        factor_mob.shift(1.5*RIGHT+2.5*UP)

        factor_parts = factor_mob.submobjects
        label_parts = scaled_label.submobjects

        factor_in_label = VGroup(*label_parts[:len(factor_parts)])
        label_remainder = VGroup(*label_parts[len(factor_parts):])

        self.play(Write(factor_mob))
        self.add_sound("voiceovers/line.mp3")
        self.play(
            v.copy().animate.set_color(GREY_D),
            v_label.copy().animate.set_color(GREY_D),

            Transform(factor_mob, factor_in_label),
            Transform(v.copy(), scaled_vector),
            Transform(v_label.copy(), label_remainder),
        )
        self.wait()
        self.clear()
        self.add(*starting_mobjects)

class MagnitudeScene(Scene):
    def construct(self):
        title = Text("Độ lớn của một vectơ", font="Noto Sans", color=YELLOW)
        title.scale(0.7).set_z_index(3)
        self.play(Write(title))
        self.add_sound("voiceovers/MagnitudeScene.mp3")
        self.play(title.animate.to_corner(UL))
        plane = NumberPlane()
        plane.set_opacity(0.3)
        self.play(Create(plane))

        v = Vector([4,3], color=YELLOW)
        label = v.coordinate_label()
        label.add_background_rectangle()
        x, y = label.get_entries()
        x.set_color(GREEN)
        y.set_color(RED)
        self.play(GrowArrow(v), FadeIn(label), run_time=1.5)
        self.wait(3)

        x_proj = Line(ORIGIN, np.array([4,0,0]), color=GREEN)
        y_proj = Line(np.array([4,0,0]), np.array([4,3,0]), color=RED)
        hyp = Line(ORIGIN, np.array([4,3,0]), color=YELLOW)
        triangle = VGroup(x_proj, y_proj, hyp)
        self.play(Create(triangle))
        
        self.play(x.copy().animate.next_to(x_proj, DOWN))
        self.play(y.copy().animate.next_to(y_proj, RIGHT))
        self.wait()
        magnitude = MathTex(r"|v|")
        magnitude[0][1:2].set_color(YELLOW)
        equal_text1 = MathTex(r"=")
        equation = MathTex(r"\sqrt{4^2+3^2}")
        equal_text2 = MathTex(r"=")
        result = MathTex(r"5").set_color(YELLOW)
        VGroup(magnitude, equal_text1, equation, equal_text2, result).arrange(RIGHT).shift(2.5*LEFT+2.5*UP)
        equation_x = equation[0][2:3]
        equation_x.set_color(GREEN)
        equation_y = equation[0][5:6]
        equation_y.set_color(RED)
        equation_x.target, equation_y.target = x, y
        for mob in equation_x, equation_y:
            mob.save_state()
            mob.move_to(mob.target)
        self.play(TransformFromCopy(hyp, magnitude), FadeIn(equal_text1),)
        self.wait()
        self.play( Write(equation),
                  *[mob.animate.restore() for mob in (equation_x, equation_y)], run_time=2)
        self.play(FadeIn(equal_text2), Write(result))
        self.wait(14)

class ShowQualitativeDotProductValues(Scene):
    def construct(self):
        self.add_sound("voiceovers/ShowQualitativeDotProductValues.mp3")
        title = Text("Tích vô hướng", font="Noto Sans")
        title.set_color_by_gradient(V_COLOR, W_COLOR)
        self.play(Write(title), run_time=1.5)
        self.wait(1.5)
        self.play(ApplyWave(title))
        self.play(FadeOut(title))
        geometric_definition = Text("Định nghĩa hình học", font="Noto Sans")
        geometric_definition.scale(0.7).to_corner(UL)
        grid = NumberPlane()
        grid.set_opacity(0.3)
        self.add(grid)
        
        v_sym, dot, w_sym, algebraic_formula, comp, zero = ineq = MathTex(
            r"\vec{\mathbf{a}}",
            r"\cdot",
            r"\vec{\mathbf{b}}",
            r" = |a||b|\cos\theta",
            ">",
            "0"
        )
        ineq.to_edge(UP)
        ineq.add_background_rectangle()

        v_sym.set_color(V_COLOR)
        w_sym.set_color(W_COLOR)
        comp.set_color(GREEN)
        
        algebraic_formula[2:3].set_color(V_COLOR)
        a_value = algebraic_formula[1:4]
        
        algebraic_formula[5:6].set_color(W_COLOR)
        b_value = algebraic_formula[4:7]
        cos = algebraic_formula[7:]

        equals = MathTex("=").set_color(PINK).move_to(comp)
        less_than = MathTex("<").set_color(RED).move_to(comp)

        words = [
            Text("Cùng hướng", font="Noto Sans").scale(0.7),
            Text("Vuông góc", font="Noto Sans").scale(0.7),
            Text("Ngược chiều", font="Noto Sans").scale(0.7)
        ]
        for word, sym in zip(words, [comp, equals, less_than]):
            
            word.next_to(sym, DOWN, aligned_edge=LEFT, buff=MED_SMALL_BUFF)
            word.set_color(sym.get_color())
            word.add_background_rectangle()

        v = Vector([1.5, 1.5], color=V_COLOR).set_z_index(1)
        w = Vector([2, 2], color=W_COLOR).rotate(-np.pi / 6, about_point=ORIGIN)
        self.add(v_sym, dot, w_sym)
        starting_mobjects = self.get_top_level_mobjects().copy()
        w_copy = w.copy()

        line_v = Line(LEFT, RIGHT, color=GREY).scale(8)
        line_v.rotate(v.get_angle(), about_point=ORIGIN)
        word = words[0]
        def get_angle():
            line_w = Line(LEFT, RIGHT)
            line_w.rotate(w_copy.get_angle(), about_point=ORIGIN)
            return Angle(line_w, line_v, radius=0.8)
        def get_theta():
            line_w = Line(LEFT, RIGHT)
            line_w.rotate(w_copy.get_angle(), about_point=ORIGIN)
            return MathTex(r"\theta").move_to(
                    Angle(line_w, line_v, radius=0.8 + 3 * SMALL_BUFF).point_from_proportion(0.5)
                    )
        angle = get_angle()
        theta = get_theta()
        for mob in (v, w_copy):
            self.play(
                Create(mob)
            )
        self.play(Write(geometric_definition))
        line_a = Line(ORIGIN, v.get_end())
        brace_a = Brace(line_a, direction=line_a.copy().rotate(PI / 2).get_unit_vector())
        a_text = brace_a.get_tex("|a|")
        line_b = Line(w_copy.get_end(), ORIGIN)
        brace_b = Brace(line_b, direction=line_b.copy().rotate(PI / 2).get_unit_vector())
        b_text = brace_b.get_tex("|b|")
        self.play(FadeIn(brace_a), FadeIn(a_text), FadeIn(brace_b), FadeIn(b_text), run_time=0.5)
        
        a_value.target, b_value.target, cos.target = a_text, b_text, theta
        for mob in a_value, b_value, cos:
            mob.save_state()
            mob.move_to(mob.target)
            mob.set_opacity(0)
        self.add(algebraic_formula)
        for mob in a_value, b_value:
            mob.set_opacity(1)
        self.play(*[mob.animate.restore() for mob in (a_value, b_value)])
        self.play(Create(angle), FadeIn(theta))
        cos.set_opacity(1)
        self.play(cos.animate.restore())
        self.play(FadeOut(brace_a), FadeOut(a_text), FadeOut(brace_b), FadeOut(b_text))
        self.play(Indicate(VGroup(v_sym, dot, w_sym)))
        self.play(Indicate(a_value))
        self.play(Indicate(b_value))
        self.play(Indicate(cos))
        self.play(Write(word, run_time=1))
        self.wait()
        self.add(comp, zero)
        self.wait()   
        self.play(FadeOut(angle), FadeOut(theta))
        self.play(Rotate(w_copy, -np.pi / 3, about_point=ORIGIN))
        def get_right_angle():
            line_w = Line(LEFT, RIGHT)
            line_w.rotate(w_copy.get_angle(), about_point=ORIGIN)
            return RightAngle(line_v, line_w)
        right_angle = get_right_angle()  
        self.play(Transform(word, words[1]), FadeIn(right_angle))
        self.play(Transform(comp, equals), FadeOut(right_angle))
        self.remove(right_angle)
        self.play(Rotate(w_copy, -np.pi / 3, about_point=ORIGIN))
        angle = get_angle()
        theta = get_theta()
        self.play(Transform(word, words[2]), FadeIn(angle), FadeIn(theta))
        self.play(Transform(comp, less_than))
        self.wait()
        self.clear()

        # algebraic_definition
        self.add(*starting_mobjects)
        algebraic_definition = Text("Định nghĩa đại số", font="Noto Sans")
        algebraic_definition.scale(0.7).to_corner(UL)
        self.play(Write(algebraic_definition))
        self.play(FadeIn(v), FadeIn(w))
        equals = MathTex("=")
        algebraic_formula = MathTex(r" = a_x b_x + a_y b_y")
        a_x = algebraic_formula[0][1:3].set_color(V_COLOR)
        b_x = algebraic_formula[0][3:5].set_color(W_COLOR)
        a_y = algebraic_formula[0][6:8].set_color(V_COLOR)
        b_y = algebraic_formula[0][-2:].set_color(W_COLOR)
        a_coordinates = MobjectMatrix([[MathTex(r"a_x")], [MathTex(r"a_y")]]).set_color(V_COLOR)
        b_coordinates = MobjectMatrix([[MathTex(r"b_x")], [MathTex(r"b_y")]]).set_color(W_COLOR)
        a_coordinates.add_background_rectangle()
        b_coordinates.add_background_rectangle()
        dot = MathTex("\\cdot")
        VGroup(equals, a_coordinates, dot, b_coordinates, algebraic_formula).arrange(RIGHT).next_to(w_sym, RIGHT)
        label_a = v.coordinate_label()
        label_b = w.coordinate_label()
        a_coordinates.target, b_coordinates.target = label_a, label_b
        for mob in a_coordinates, b_coordinates:
            mob.save_state()
            mob.move_to(mob.target)
        self.add(equals, a_coordinates, dot, b_coordinates)
        self.play(*[mob.animate.restore() for mob in (a_coordinates, b_coordinates)], run_time=1.5)
        self.play(Indicate(VGroup(v_sym, dot, w_sym)))
        a_entries = a_coordinates.get_entries()
        b_entries = b_coordinates.get_entries()
        a_x.target, b_x.target, a_y.target, b_y.target = a_entries[0], b_entries[0], a_entries[1], b_entries[1]
        for mob in a_x, b_x, a_y, b_y:
            mob.save_state()
            mob.move_to(mob.target)
        self.add(algebraic_formula)
        self.play(*[mob.animate.restore() for mob in (a_x, b_x)])
        self.play(*[mob.animate.restore() for mob in (a_y, b_y)])
        self.wait(25)

A_COLOR = "#2828ff"
B_COLOR = "#e12828"
CP_COLOR = "#963c96"
class CrossProductScene(ThreeDScene, LinearTransformationScene):
    def __init__(self, **kwargs):
        super().__init__(
            show_basis_vectors=False,
            leave_ghost_vectors=False,
            include_background_plane=False,
            **kwargs
        )
        self.v_coords = np.array([2,0.5,0.2])
        self.w_coords = np.array([0.5,2,0.6])
        
    def construct(self):
        self.remove(self.plane)
        a_np = np.array([2,0.5,0.2])
        b_np = np.array([0.5,2,0.6])
        cross = np.cross(a_np, b_np)
        title = Text("Tích có hướng", font="Noto Sans", color=CP_COLOR).scale(0.7)   
        self.add_fixed_in_frame_mobjects(title)   
        self.play(Write(title))
        self.play(title.animate.to_corner(UL))
        self.add_sound("voiceovers/CrossProductScene.mp3")
        label = MathTex(r"\vec{a} \times \vec{b}").to_edge(UP)
        label[0][:2].set_color(A_COLOR)
        label[0][-2:].set_color(B_COLOR)
        self.add_fixed_in_frame_mobjects(label)
        self.play(FadeIn(label))
        
        starting_mobjects = self.get_top_level_mobjects().copy()
        self.wait()
        self.add_vectors_ce()
        self.wait(3)
        self.add_vector(cross/1.5, color=CP_COLOR)
        self.wait(3)
        self.show_area_ce()
        self.clear()
        self.add(*starting_mobjects)
        
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)
        a = Arrow3D(start=ORIGIN, end=np.array([2,0.5,0.2]), color=A_COLOR, resolution=8)
        b = Arrow3D(start=ORIGIN, end=np.array([0.5,2,0.6]), color=B_COLOR, resolution=8)
        try:
            self.play(Create(a), Create(b))
        except Exception:
            # fallback to Vector if Arrow3D missing
            a2 = Vector([2,0.5,0.2])
            b2 = Vector([0.5,2,0.6])
            self.play(Create(axes), GrowArrow(a2), GrowArrow(b2))
        
        perp = Arrow3D(start=ORIGIN, end=cross/1.5, color=CP_COLOR, resolution=8)
        try:
            self.play(Create(perp))
        except Exception:
            perp2 = Vector(cross/1.5)
            self.play(GrowArrow(perp2))
        
        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(8)
        self.stop_ambient_camera_rotation()
        righthand = SVGMobject("assets/Right_hand_rule_cross_product.svg").to_corner(UL)
        righthand.shift(DOWN)
        self.add_fixed_in_frame_mobjects(righthand)
        self.wait(17)
    def add_vectors_ce(self):
        v = self.add_vector(self.v_coords, color=A_COLOR)
        w = self.add_vector(self.w_coords, color=B_COLOR)

        for vect, name, direction in [(v, "a", "right"), (w, "b", "left")]:
            color = vect.get_color()
            vect.label = self.label_vector(vect, label=name, color=color, direction=direction)

        self.v, self.w = v, w

    def show_area_ce(self):
        # Add unit square
        self.add_unit_square()

        # Create matrix from vectors
        mat = np.column_stack([self.v_coords, self.w_coords])

        # Apply linear transformation
        self.square.apply_matrix(mat)

        # Animate transformed square and original vectors
        self.play(
            Create(self.square),
            Animation(self.v),
            Animation(self.w)
        )
        self.wait()

        # self.play(FadeOut(self.square))

class ApplicationsScene(Scene):
    def construct(self):
        title = Title("Applications of Vectors")
        self.play(Write(title))

        apps = VGroup(
            Tex("Physics: Forces, Velocity"),
            Tex("Graphics: Lighting, Normals"),
            Tex("Navigation: Courses, Waypoints"),
            Tex("Data: Embeddings, Directional Features")
        ).arrange(DOWN, aligned_edge=LEFT)
        apps.to_edge(LEFT)
        self.play(LaggedStartMap(Write, apps, lag_ratio=0.4))
        self.wait(1.0)

        outro = Tex("Vectors are a fundamental tool across science and engineering.")
        outro.to_edge(DOWN)
        self.play(Write(outro))
        self.wait(1.0)

class VectorWrapUp(Scene):
    def construct(self):
        arrows = VGroup(*[
            Arrow(ORIGIN, RIGHT*1.5).rotate(i*PI/6).set_color(random_bright_color())
            for i in range(12)
        ])
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in arrows]))
        # self.play(LaggedStartMap(GrowArrow, arrows))
        title = Text("Vectơ là một công cụ cơ bản \ntrong khoa học và kỹ thuật.", font="Noto Sans", color=YELLOW).next_to(arrows, DOWN)
        self.add_sound("voiceovers/VectorWrapUp.mp3")
        self.play(Write(title), run_time=3)
        self.wait(7.5)
        self.add_sound("voiceovers/thank.mp3")
        thank = SVGMobject("assets/thank.svg").to_corner(UL)
        self.play(DrawBorderThenFill(thank)) 
        self.play(FadeOut(arrows), FadeOut(title))

class VectorThumbnail(LinearTransformationScene):
    def __init__(self, **kwargs):
        super().__init__(
            show_basis_vectors=False,
            leave_ghost_vectors=False,
            include_background_plane=False,
            **kwargs
        )
        self.v_coords = np.array([3, 2])
        self.w_coords = np.array([2, -1])

    def construct(self):
        title = Text(
            "Vectơ",
            font="Montserrat",
            weight=BOLD, color=YELLOW
        ).scale(2.2).to_corner(UL, buff=0.8)
        subtitle = Text(
            "Dễ hiểu",
            font="Montserrat",
            weight=SEMIBOLD, color=BLUE
        ).scale(1.1).next_to(title, DOWN, buff=0.3)
        self.add_vectors_ce()
        self.show_area_ce()
        righthand = SVGMobject("assets/Right_hand_rule_cross_product.svg")
        righthand.scale(1.5).to_corner(DL, buff=0.8)
        self.add(title, subtitle, righthand)
        self.wait()
    def add_vectors_ce(self):
        self.plane.fade()

        v = self.add_vector(self.v_coords, color=YELLOW)
        w = self.add_vector(self.w_coords, color=BLUE)
        v.coordinate_label(color=YELLOW)
        w.coordinate_label(color=BLUE)
        line_v = Line(LEFT, RIGHT)
        line_v.rotate(v.get_angle(), about_point=ORIGIN)
        line_w = Line(LEFT, RIGHT)
        line_w.rotate(w.get_angle(), about_point=ORIGIN)
        
        angle = Angle(line_w, line_v, radius=0.8)
        theta = MathTex(r"\theta").move_to(
                    Angle(line_w, line_v, radius=0.8 + 3 * SMALL_BUFF).point_from_proportion(0.5)
                    )
        badge = Circle(color=WHITE, stroke_width=5).scale(1.1).to_corner(DR, buff=0.8)
        badge_txt = Text("5 phút\n42 giây", font_size=40, weight=BOLD).move_to(badge)
        for vect, name, direction in [(v, "a", "left"), (w, "b", "down")]:
            color = vect.get_color()
            vect.label = self.label_vector(vect, label=name, color=color, direction=direction)
        
        formula = MathTex(r"\vec{a}\cdot\vec{b} = a_x b_x + a_y b_y")
        formula[0][:2].set_color(YELLOW)
        formula[0][3:5].set_color(BLUE)
        formula[0][-9:-7].set_color(YELLOW)
        formula[0][-7:-5].set_color(BLUE)
        formula[0][-4:-2].set_color(YELLOW)
        formula[0][-2:].set_color(BLUE)
        formula.scale(1.5).to_corner(UR, buff=0.8)
        self.add(angle, theta, badge, badge_txt, formula)

    def show_area_ce(self):
        self.add_unit_square()
        mat = np.column_stack([self.v_coords, self.w_coords])
        self.square.apply_matrix(mat)