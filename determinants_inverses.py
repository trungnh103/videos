from manim import *
import numpy as np
import itertools as it
import numpy as np
import copy

from pi_creature_scene import *
class IntroCollapse(Scene):
    def construct(self):    
        look_closely = SVGMobject("assets/look_closely.svg").to_edge(UP)
        self.add(look_closely)     
        matrix = Matrix([[1, 0], [0, 0]])
        matrix.set_color(YELLOW)                   
                     
        square = Square(color=BLUE)
        arrow = Arrow(LEFT, RIGHT, color=YELLOW)
        VGroup(matrix, arrow, square).arrange(RIGHT)
        self.play(Create(matrix))
        self.add_sound("voiceovers/IntroCollapse.mp3")
        self.play(Circumscribe(matrix, fade_out=True, color=GREEN)) 
        self.play(GrowArrow(arrow), FadeIn(square))
        self.play(ApplyMatrix([[1, 0], [0, 0]], square))
        self.wait(2)
        fix = SVGMobject("assets/4.svg").to_edge(UP) 
        self.remove(look_closely) 
        self.add(fix)
        self.wait(2)
        negative_one = MathTex("-1").next_to(matrix, UR, buff=SMALL_BUFF)
        negative_one.target = fix
        negative_one.save_state()
        negative_one.move_to(negative_one.target)
        self.play(Restore(negative_one))
        self.wait(2)
        cry = SVGMobject("assets/10.svg").to_edge(UP)
        self.remove(fix)
        self.add(cry)
        self.wait()
        self.play(FadeOut(cry))
        self.remove(negative_one)
        title = Text("Định thức của ma trận", font="Noto Sans", color=YELLOW)
        title.scale(0.7).to_edge(UP)
        self.play(Write(title))  
        self.wait(4)


# ---------------------------------------------------------
class DeterminantAsArea(LinearTransformationScene):
    def construct(self):
        self.add_sound("voiceovers/DeterminantAsArea.mp3")
        
        label = Text("Diện tích = 1", font="Noto Sans", color=YELLOW)
        label.scale(0.7).to_edge(UP).add_background_rectangle()
        self.wait(6)
        self.add_unit_square()
        self.play(Flash(self.square))
        self.play(FadeIn(label))
        matrix = [[2, 1], [1, 1]]
        self.wait(2)
        self.apply_matrix(matrix)
        self.wait()

        new_label = Text("Diện tích = |det(A)|", font="Noto Sans", color=YELLOW)
        new_label.scale(0.7).to_edge(UP).add_background_rectangle()
        self.play(Transform(label, new_label))
        self.wait(2)

class ThisSquareTellsEverything(LinearTransformationScene):
    def __init__(self, **kwargs):
        super().__init__(
            show_basis_vectors=False,
            leave_ghost_vectors=False,
            include_background_plane=False,
            **kwargs
        )
    def construct(self):
        self.add_sound("voiceovers/DeterminantAsArea_part1.mp3")
        self.add_unit_square()
        area = MathTex("1")
        area.move_to(self.square)
        question = MathTex("?")
        question.move_to(self.square)
        
        # Text
        words = Text("Diện tích = 1", font="Noto Sans", color=YELLOW)
        words.scale(0.65).to_corner(UP + RIGHT)
        words.add_background_rectangle()

        # Arrow pointing to the square
        arrow = Arrow(
            words.get_bottom(),
            self.square.get_right()
        )

        self.play(Flash(self.square), FadeIn(VGroup(words, arrow)))
        self.wait(3)
        self.play(FadeOut(VGroup(words, arrow)))
        self.wait()      
        self.add_moving_mobject(area, target_mobject=question)
        self.apply_transposed_matrix([[1.5, -0.5], [1, 1.5]])
        self.wait()
        self.play(Indicate(question))
        
        self.wait(2)

class NameDeterminant(LinearTransformationScene):
    def __init__(self, **kwargs):
        self.t_matrix = [[3, 0], [2, 2]]
        self.voiceover = "voiceovers/DeterminantAsArea_part2.mp3"
        super().__init__(**kwargs)

    def construct(self):
        self.add_sound(self.voiceover)
        self.plane.fade(0.3)

        # Unit square
        self.add_unit_square(color=YELLOW_E, opacity=0.5)

        # Title
        title = Text("Định thức đo lường sự thay đổi diện tích", font="Noto Sans")
        title.to_edge(UP).scale(0.7)
        title[:8].set_color(YELLOW) 
        self.add(title)
        self.title = title
        matrix_background, matrix, det_text = self.get_matrix()
        
        # self.add(matrix_background, matrix)

        A = Tex("A")
        area_label = VGroup(A.copy(), A.copy(), A)
        area_label.move_to(self.square)

        # Determinant value
        det = np.linalg.det(self.t_matrix)
        # if np.round(det) == det:
        if det < 0 or det > 1:
            det = int(det)
        area_label_target = VGroup(
            Tex(str(det)),
            MathTex(r"\cdot"),
            A.copy()
        )

        if 0 < det < 1:
            area_label_target.scale(det)

        area_label_target.arrange(RIGHT, buff=0.1)
        self.add_moving_mobject(area_label, target_mobject=area_label_target)
        self.apply_transposed_matrix(self.t_matrix)
        self.add_foreground_mobject(matrix_background, matrix)
        self.wait()
        
        det_mob_copy = area_label[0].copy()
        new_det_mob = det_mob_copy.copy().set_height(
            det_text[0].get_height()
        )
        new_det_mob.next_to(det_text, RIGHT, buff=0.2)
        new_det_mob.add_background_rectangle()

        det_mob_copy.add_background_rectangle(opacity=0)

        self.play(Write(det_text))
        self.play(Transform(det_mob_copy, new_det_mob))
        self.wait()
    def get_matrix(self):
        matrix = Matrix(np.array(self.t_matrix).transpose())
        matrix.set_column_colors(GREEN, RED)
        matrix.next_to(self.title, DOWN, buff = 0.5)
        matrix.shift(2*LEFT)
        matrix_background = BackgroundRectangle(matrix)
        det_text = get_det_text(matrix, 0, initial_scale_factor=1)
        det_text.remove(det_text.split()[-1])
        return matrix_background, matrix, det_text

class AreaExample(LinearTransformationScene):
    def __init__(self, **kwargs):
        super().__init__(
            show_basis_vectors=False, 
            include_background_plane=False,
            **kwargs)
        self.voiceover = "voiceovers/NegativeExample.mp3"
        self.t_matrix = [[2, -1], [1, -3]]
        self.explainer = "Định thức dương giữ nguyên hướng.\nĐịnh thức âm đảo ngược hướng."
        self.explainer_early = None
        self.edge = LEFT
        self.run_time = 2
        self.move_det_to_square = True
        self.invertibleVsSingular = False
        self.inverse = False
        self.inverse_matrix = None
        self.voiceover2 = None
    def construct(self):
        self.plane.fade()
        self.add_sound(self.voiceover)
        self.add_unit_square()
        
        matrix = Matrix(np.array(self.t_matrix).T)
        matrix.to_edge(UP)
        matrix.shift(LEFT * 2)
        matrix.add_background_rectangle()
        matrix.get_entries().set_color(BLUE)
        det = np.linalg.det(self.t_matrix)
        # if np.round(det) == det:
        if det <= 0 or det > 1:
            det = int(np.round(det))
        
        det_text = get_det_text(
            matrix, determinant = det, initial_scale_factor=1
        )
        for mob in det_text.split():
            if isinstance(mob, Tex):
                mob.add_background_rectangle()
        det_text_display = Mobject()
        if self.invertibleVsSingular:         
            if det == 0:
                det_text_display = MathTex(r"det(A) = 0").move_to(matrix)
            else:
                det_text_display = MathTex(r"det(A) \neq 0").move_to(matrix)
            self.play(Write(det_text_display))
        else:
            self.play(Write(matrix), Write(det_text))   
        if self.explainer_early:
            text = Text(self.explainer_early, font="Noto Sans", color=YELLOW)
            text.scale(0.65).to_edge(LEFT).shift(UP)
            self.play(Write(text), run_time=self.run_time)
        self.wait()
        self.apply_transposed_matrix(self.t_matrix)
        
        if self.move_det_to_square:
            det_number = det_text.split()[-1].copy()       
            if 0 < det < 1:
                det_number.scale(det)   
            self.play(det_number.animate.move_to(self.square))
        if self.voiceover2:
            self.add_sound(self.voiceover2)
            self.play(Circumscribe(det_text_display, color=GREEN))
        if self.explainer:
            text = Text(self.explainer, font="Noto Sans", color=YELLOW)
            text.scale(0.65).to_edge(self.edge).shift(DOWN)
            self.play(Write(text), run_time=self.run_time)
        if self.inverse:
            self.wait()           
            self.apply_transposed_matrix(self.inverse_matrix)                
        self.wait(2)
class ExpansionExample(AreaExample):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.voiceover = "voiceovers/ExpansionExample.mp3"
        self.t_matrix = [[0, -1.5], [2, 1]]
        self.explainer = None
        self.move_det_to_square = True
        self.invertibleVsSingular = False
class ContractionExample(AreaExample):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.voiceover = "voiceovers/ContractionExample.mp3"
        self.t_matrix = [[0.5, -0.5], [0.5, 0.5]]
        self.explainer = None
        self.move_det_to_square = True
        self.invertibleVsSingular = False
class ZeroExample(AreaExample):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.voiceover = "voiceovers/ZeroExample_part1.mp3"
        self.t_matrix = [[4, 2], [2, 1]]
        self.explainer = "Sự biến đổi này phá hủy chiều không gian.\n Một vật thể hai chiều trở thành một chiều."
        self.run_time = 4
        self.edge = RIGHT
        self.move_det_to_square = True
        self.invertibleVsSingular = False
class SecondZeroExample(AreaExample):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.voiceover = "voiceovers/ZeroExample_part2.mp3"
        self.t_matrix = [[0, 0], [0, 0]]
        self.explainer = None
        self.move_det_to_square = True
        self.invertibleVsSingular = False

class SecondDeterminantExample(NameDeterminant):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.voiceover = "voiceovers/DeterminantAsArea_part2.mp3"
        self.t_matrix = [[-1, -1], [1, -1]]
        
class DeterminantIsOneHalf(NameDeterminant):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.voiceover = "voiceovers/DeterminantAsArea_part3.mp3"
        self.t_matrix = [[0.5, -0.5], [0.5, 0.5]]
    CONFIG = {
        "t_matrix" : [[0.5, -0.5], [0.5, 0.5]],
        "foreground_plane_kwargs" : {
            "x_radius" : config.frame_width,
            "y_radius" : config.frame_width,
            "secondary_line_ratio" : 0
        },
    }

class DeterminantIsZero(NameDeterminant):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.voiceover = "voiceovers/DeterminantAsArea_part2.mp3"
        self.t_matrix = [[4, 2], [2, 1]]
class DeterminantIsNegative(NameDeterminant):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.voiceover = "voiceovers/DeterminantAsArea_part2.mp3"
        self.t_matrix = [[2, -1], [1, -3]]

class SecondDeterminantIsZeroExamlpe(NameDeterminant):
    def __init__(self, **kwargs):
        super().__init__(show_basis_vectors=False, **kwargs)
        self.voiceover = "voiceovers/DeterminantAsArea_part2.mp3"
        self.t_matrix = [[0, 0], [0, 0]]

class DeterminantIsThree(NameDeterminant):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.t_matrix = [[0, -1.5], [2, 1]]
        self.voiceover = "voiceovers/DeterminantAsArea_part3.mp3"
        
# ---------------------------------------------------------
class DeterminantFormula2x2(Scene):
    def construct(self):
        self.add_sound("voiceovers/DeterminantFormula2x2.mp3") 
        title = Text("Cách tính định thức", font="Noto Sans", color=YELLOW)
        self.play(SpinInFromNothing(title, angle=2 * PI))
        self.play(title.animate.scale(0.7).to_edge(UP))
        line = Line(LEFT * 6, RIGHT * 6, color=YELLOW).set_stroke(width=3)
        line.next_to(title, DOWN, buff=0.1)            
        self.play(GrowFromCenter(line))
        matrix = MobjectMatrix([[MathTex("a"), MathTex("b")], [MathTex("c"), MathTex("d")]])
        formula = MathTex("ad - bc").next_to(matrix, DOWN, LARGE_BUFF)
        ad = formula[0][:2].set_color(RED)
        bc = formula[0][-2:].set_color(GREEN)
        minus =  formula[0][2:3]    
        equal = MathTex("=").next_to(formula, LEFT)
        det_text1 = MathTex("det(A)").next_to(equal, LEFT)
        det_text2 = MathTex("|A|").next_to(equal, LEFT)
        entries = matrix.get_entries().set_color(BLUE)
        a = entries[0]
        b = entries[1]
        c = entries[2]
        d = entries[3]
        formula_group = VGroup(det_text1, det_text2, equal, formula).scale(1.2)

        self.play(Create(matrix))
        self.wait()
        cramer_rule = Text("Quy tắc Cramer", font="Noto Sans").scale(0.7).next_to(line, DOWN)
        self.play(Write(cramer_rule))
        self.wait(2)
        self.play(a.animate.set_color(RED), 
                  ShowPassingFlash(Line(a, d, color=RED), time_width=1),
                  d.animate.set_color(RED))
        line_ad = Line(d, ad, path_arc=-PI/2).set_color(RED)
        self.wait(2)
        self.play(ShowPassingFlash(line_ad, time_width=1), Write(ad))
        self.wait(2)
        self.play(b.animate.set_color(GREEN), 
                  ShowPassingFlash(Line(b, c, color=GREEN), time_width=1),
                  c.animate.set_color(GREEN))
        self.wait(2)
        line_bc = Line(c, bc, path_arc=PI/2).set_color(GREEN)
        self.play(ShowPassingFlash(line_bc, time_width=1), Write(bc))
        self.wait(1.5)
        self.play(Write(minus))
        self.wait(1.5)
        self.play(Write(det_text1), Write(equal))
        self.wait()
        self.play(Circumscribe(det_text1))
        self.wait(2.5)
        self.play(Transform(det_text1, det_text2))
        self.play(Flash(det_text1))
        self.wait()
        self.play(FadeOut(matrix), FadeOut(formula_group))
        self.add_sound("voiceovers/DeterminantFormula2x2_example_part1.mp3") 
        matrix_example = Matrix([
            [1, 2],
            [3, 4]
        ])
        entries_example = matrix_example.get_entries().set_color(BLUE)
        a_example = entries_example[0]
        b_example = entries_example[1]
        c_example = entries_example[2]
        d_example = entries_example[3]
        
        equal_copy = MathTex("=").next_to(matrix_example, LEFT)
        matrix_name = MathTex("A", color=BLUE).next_to(equal_copy, LEFT)
        self.play(Write(matrix_name), Write(equal_copy), Write(matrix_example))
        result = MathTex(r"\\det(A) = 1\cdot4 - 2\cdot3=-2")
        result[0][4:5].set_color(BLUE)
        ad_example = result[0][7:10].set_color(RED)
        bc_example = result[0][11:14].set_color(GREEN)
        result.next_to(matrix_example, DOWN, LARGE_BUFF)
        self.play(Write(result[0][:7]))
        self.play(Circumscribe(matrix))
        self.wait(1.5)
        self.play(a_example.animate.set_color(RED), 
                  ShowPassingFlash(Line(a_example, d_example, color=RED), time_width=1),
                  d_example.animate.set_color(RED),
                  FadeIn(ad_example))
        self.wait()
        self.play(b_example.animate.set_color(GREEN), 
                  ShowPassingFlash(Line(b_example, c_example, color=GREEN), time_width=1),
                  c_example.animate.set_color(GREEN),
                  FadeIn(bc_example))
        self.play(FadeIn(result[0][10:11]))
        self.play(FocusOn(result[0][10:11]))
        self.wait()
        self.add_sound("voiceovers/DeterminantFormula2x2_example_part2.mp3")
        self.play(Write(result[0][14:]))
        self.play(Flash(result[0][15:]))
        self.wait(2)
class DeterminantFormula3x3(Scene):
    def construct(self):
        self.add_sound("voiceovers/DeterminantFormula3x3_rule.mp3")
        title = Text("Cách tính định thức", font="Noto Sans", color=YELLOW)
        title.scale(0.7).to_edge(UP)
        line = Line(LEFT * 6, RIGHT * 6, color=YELLOW).set_stroke(width=3)
        line.next_to(title, DOWN, buff=0.1)
        self.add(title, line)
        self.wait()
        
               
        
        matrix = MobjectMatrix([[MathTex("a"), MathTex("b"), MathTex("c")], 
                                [MathTex("d"), MathTex("e"), MathTex("f")],
                                [MathTex("g"), MathTex("h"), MathTex("i")]])
        matrix.get_entries().set_color(BLUE)
        a = matrix.get_entries()[0]
        b = matrix.get_entries()[1]
        c = matrix.get_entries()[2]
        d = matrix.get_entries()[3]
        e = matrix.get_entries()[4]
        f = matrix.get_entries()[5]
        g = matrix.get_entries()[6]
        h = matrix.get_entries()[7]
        i = matrix.get_entries()[8]
        right_side = VGroup(a, b, d, e, g, h).copy()
        a_right_side = right_side[0]
        b_right_side = right_side[1]
        d_right_side = right_side[2]
        e_right_side = right_side[3]
        g_right_side = right_side[4]
        h_right_side = right_side[5]
        self.play(Write(matrix))
        self.wait(3)
        self.play(Circumscribe(matrix))
        self.wait(2)
        cramer_rule = Text("Quy tắc Sarrus", font="Noto Sans").scale(0.7).next_to(line, DOWN)
        self.play(Write(cramer_rule))
        self.wait(2)
        matrix_group = VGroup(matrix, right_side).arrange(RIGHT, LARGE_BUFF)
        self.play(FadeIn(right_side, shift=RIGHT))
        self.wait(2)
        self.play(Circumscribe(matrix_group))
        self.wait()
        result = MathTex(r"\\det(A) = aei+bfg+cdh-gec-hfa-idb")
        result.next_to(matrix, DOWN, LARGE_BUFF)
        result[0][4:5].set_color(BLUE)
        aei = result[0][7:10].set_color(RED)
        bfg = result[0][11:14].set_color(RED)
        cdh = result[0][15:18].set_color(RED)
        gec = result[0][19:22].set_color(GREEN)
        hfa = result[0][23:26].set_color(GREEN)
        idb = result[0][-3:].set_color(GREEN)
        self.play(Write(result[0][:7]))
        self.play(a.animate.set_color(RED), 
                  ShowPassingFlash(Line(a, i, color=RED), time_width=1),
                  e.animate.set_color(RED),
                  i.animate.set_color(RED),
                  FadeIn(aei), run_time=1.5)
        self.wait()
        self.play(b.animate.set_color(RED), 
                  ShowPassingFlash(Line(b, g_right_side, color=RED), time_width=1),
                  f.animate.set_color(RED),
                  g_right_side.animate.set_color(RED),
                  FadeIn(result[0][10:14]), run_time=1.5)
        self.wait()
        self.play(c.animate.set_color(RED), 
                  ShowPassingFlash(Line(c, h_right_side, color=RED), time_width=1),
                  d_right_side.animate.set_color(RED),
                  h_right_side.animate.set_color(RED),
                  FadeIn(result[0][14:18]), run_time=1.5)
        self.wait()
        matrix.get_entries().set_color(BLUE)
        right_side.set_color(BLUE)
        self.play(c.animate.set_color(GREEN), 
                  ShowPassingFlash(Line(c, g, color=GREEN), time_width=1),
                  e.animate.set_color(GREEN),
                  g.animate.set_color(GREEN),
                  FadeIn(result[0][18:22]), run_time=1.5)
        self.wait()
        self.play(a_right_side.animate.set_color(GREEN), 
                  ShowPassingFlash(Line(a_right_side, h, color=GREEN), time_width=1),
                  f.animate.set_color(GREEN),
                  h.animate.set_color(GREEN),
                  FadeIn(result[0][22:26]), run_time=1.5)
        self.wait()
        self.play(b_right_side.animate.set_color(GREEN), 
                  ShowPassingFlash(Line(b_right_side, i, color=GREEN), time_width=1),
                  d_right_side.animate.set_color(GREEN),
                  i.animate.set_color(GREEN),
                  FadeIn(result[0][-4:]), run_time=1.5)
        self.wait()
        matrix.get_entries().set_color(BLUE)
        right_side.set_color(BLUE)
        self.wait()
        self.play(Circumscribe(result))
        self.play(Create(Line(a.get_center(), i.get_center(), color=RED, stroke_width=12).set_opacity(0.5)))
        self.play(Create(Line(b.get_center(), g_right_side.get_center(), color=RED, stroke_width=12).set_opacity(0.5)))
        self.play(Create(Line(c.get_center(), h_right_side.get_center(), color=RED, stroke_width=12).set_opacity(0.5)))
        self.play(Create(Line(c.get_center(), g.get_center(), color=GREEN, stroke_width=12).set_opacity(0.5)))
        self.play(Create(Line(a_right_side.get_center(), h.get_center(), color=GREEN, stroke_width=12).set_opacity(0.5)))
        self.play(Create(Line(b_right_side.get_center(), i.get_center(), color=GREEN, stroke_width=12).set_opacity(0.5)))
        self.wait(3)
class DeterminantFormula3x3Example(Scene):
    def construct(self):
        title = Text("Cách tính định thức", font="Noto Sans", color=YELLOW)
        title.scale(0.7).to_edge(UP)
        line = Line(LEFT * 6, RIGHT * 6, color=YELLOW).set_stroke(width=3)
        line.next_to(title, DOWN, buff=0.1)
        self.add(title, line)
        self.add_sound("voiceovers/DeterminantFormula3x3Example.mp3")       
        matrix = MobjectMatrix([[MathTex("1"), MathTex("2"), MathTex("3")], 
                                [MathTex("4"), MathTex("5"), MathTex("6")],
                                [MathTex("7"), MathTex("8"), MathTex("9")]])
        matrix.get_entries().set_color(BLUE)
        a = matrix.get_entries()[0]
        b = matrix.get_entries()[1]
        c = matrix.get_entries()[2]
        d = matrix.get_entries()[3]
        e = matrix.get_entries()[4]
        f = matrix.get_entries()[5]
        g = matrix.get_entries()[6]
        h = matrix.get_entries()[7]
        i = matrix.get_entries()[8]
        right_side = VGroup(a, b, d, e, g, h).copy()
        a_right_side = right_side[0]
        b_right_side = right_side[1]
        d_right_side = right_side[2]
        e_right_side = right_side[3]
        g_right_side = right_side[4]
        h_right_side = right_side[5]
        
        VGroup(matrix, right_side).arrange(RIGHT, LARGE_BUFF).shift(UP)
        self.play(Write(matrix), run_time=1.5)
        self.wait(3)
        self.play(FadeIn(right_side, shift=RIGHT))
        self.wait(2)
        det = MathTex(r"\\det(A) = ")
        det[0][4:5].set_color(BLUE)
        det.next_to(matrix, DOWN, LARGE_BUFF)
        det.next_to(matrix, DOWN, LARGE_BUFF).to_edge(LEFT)
        result_plus = MathTex(r"(1\cdot5\cdot9)+(2\cdot6\cdot7)+(3\cdot4\cdot8)").next_to(det, RIGHT)
        result_minus = MathTex(r"- (7\cdot5\cdot3)-(8\cdot6\cdot1)-(9\cdot4\cdot2)").next_to(result_plus, DOWN)
        result = VGroup(result_plus, result_minus)
        intermediate1 = MathTex(r"(45 + 84 + 96)-(105+48+72)").next_to(det, RIGHT)
        intermediate2 = MathTex(r"225-225").next_to(det, RIGHT)
        final_result = MathTex(r"0", color=RED).scale(1.3).next_to(det, RIGHT)   
        aei = result_plus[0][:7].set_color(RED)
        bfg = result_plus[0][8:15].set_color(RED)
        cdh = result_plus[0][-7:].set_color(RED)
        gec = result_minus[0][1:8].set_color(GREEN)
        hfa = result_minus[0][9:16].set_color(GREEN)
        idb = result_minus[0][-7:].set_color(GREEN)
        intermediate1[0][1:3].set_color(RED)
        intermediate1[0][4:6].set_color(RED)
        intermediate1[0][7:9].set_color(RED)
        intermediate1[0][12:15].set_color(GREEN)
        intermediate1[0][16:18].set_color(GREEN)
        intermediate1[0][-3:-1].set_color(GREEN)
        intermediate2[0][:3].set_color(RED)
        intermediate2[0][4:].set_color(GREEN)

        self.play(Write(det))
        self.play(a.animate.set_color(RED), 
                  ShowPassingFlash(Line(a, i, color=RED), time_width=1),
                  e.animate.set_color(RED),
                  i.animate.set_color(RED),
                  FadeIn(aei))
        self.play(b.animate.set_color(RED), 
                  ShowPassingFlash(Line(b, g_right_side, color=RED), time_width=1),
                  f.animate.set_color(RED),
                  g_right_side.animate.set_color(RED),
                  FadeIn(result_plus[0][7:15]))
        self.play(c.animate.set_color(RED), 
                  ShowPassingFlash(Line(c, h_right_side, color=RED), time_width=1),
                  d_right_side.animate.set_color(RED),
                  h_right_side.animate.set_color(RED),
                  FadeIn(result_plus[0][-8:]))
        matrix.get_entries().set_color(BLUE)
        right_side.set_color(BLUE)
        self.play(c.animate.set_color(GREEN), 
                  ShowPassingFlash(Line(c, g, color=GREEN), time_width=1),
                  e.animate.set_color(GREEN),
                  g.animate.set_color(GREEN),
                  FadeIn(result_minus[0][:8]))
        self.play(a_right_side.animate.set_color(GREEN), 
                  ShowPassingFlash(Line(a_right_side, h, color=GREEN), time_width=1),
                  f.animate.set_color(GREEN),
                  h.animate.set_color(GREEN),
                  FadeIn(result_minus[0][8:16]))
        self.play(b_right_side.animate.set_color(GREEN), 
                  ShowPassingFlash(Line(b_right_side, i, color=GREEN), time_width=1),
                  d_right_side.animate.set_color(GREEN),
                  i.animate.set_color(GREEN),
                  FadeIn(result_minus[0][-8:]))
        matrix.get_entries().set_color(BLUE)
        right_side.set_color(BLUE)

        self.wait()
        self.play(Transform(result, intermediate1))
        self.wait()
        self.play(Transform(result, intermediate2))
        self.wait()
        self.play(Transform(result, final_result))
        self.wait()
        self.add_sound("voiceovers/DeterminantFormula3x3_detIsZero.mp3")  
        self.wait() 
        self.play(Circumscribe(result))
        self.wait(3.5) 
        oh_no = SVGMobject("assets/24.svg").to_edge(DOWN)
        self.play(FadeIn(oh_no))
        self.wait() 
        self.play(ApplyMatrix([[1, 0], [0, 0]], oh_no))
        self.wait(6)
# ---------------------------------------------------------
class DeterminantProperties(Scene):
    def construct(self):
        props = VGroup(
            Text("• Swap rows → sign flips"),
            Text("• Scale row → determinant scales"),
            Text("• Duplicate row → det = 0")
        ).arrange(DOWN, aligned_edge=LEFT)
        self.play(LaggedStartMap(Write, props, lag_ratio=0.6))
        self.wait(4)


# ---------------------------------------------------------
class InverseScene(LinearTransformationScene):
    def __init__(self, **kwargs):
        super().__init__(
            show_basis_vectors=False,
            leave_ghost_vectors=False,
            include_background_plane=False,
            **kwargs
        )

    def construct(self):
        self.add_sound("voiceovers/InverseScene.mp3")
        title = Text("Liệu ta có thể đảo ngược một phép biến đổi?", font="Noto Sans")
        title.scale(0.7).to_corner(UL).add_background_rectangle()
        self.play(Write(title))
        self.play(ApplyWave(title))
        self.add_unit_square(MAROON)
        matrix_values = [[2, 1], [1, 1]]
        matrix = Matrix(matrix_values).next_to(title, DOWN)
        matrix.set_color(PINK).add_background_rectangle()
        inverse_matrix_values = [[1, -1], [-1, 2]]
        inverse_matrix = Matrix(inverse_matrix_values).next_to(title, DOWN)
        inverse_matrix.set_color(YELLOW).add_background_rectangle()
        self.play(Create(matrix))
        self.wait()
        applying = VGroup(self.plane, self.square)
        self.play(ApplyMatrix(matrix_values, applying))
        self.wait()
        self.play(Transform(matrix, inverse_matrix))
        self.play(ApplyMatrix(inverse_matrix_values, applying))
        inverse_text = Text("Ma trận nghịch đảo", font="Noto Sans", color=YELLOW)
        inverse_text.scale(0.65).next_to(matrix, 5*RIGHT)
        inverse_text.add_background_rectangle()

        arrow = Arrow(
            inverse_text.get_left(),
            matrix.get_right()
        )
        self.play(GrowArrow(arrow), FadeIn(inverse_text))
        self.wait(2)
# ---------------------------------------------------------
class Invertible(AreaExample):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.voiceover = "voiceovers/Invertible.mp3"
        self.explainer = "Ma trận khả nghịch."
        self.t_matrix = [[1, 1], [0, 1]]
        self.move_det_to_square = False
        self.invertibleVsSingular = True
        self.edge = LEFT
        self.inverse = True
        self.inverse_matrix = [[1, -1], [0, 1]]
        self.run_time = 1
        self.voiceover2 = "voiceovers/Invertible2.mp3"

class Singular(AreaExample):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.voiceover = "voiceovers/Singular.mp3"
        self.t_matrix = [[4, 2], [2, 1]]
        self.explainer = None
        self.run_time = 1
        self.edge = RIGHT
        self.move_det_to_square = False
        self.invertibleVsSingular = True
        self.explainer_early = "Ma trận suy biến."
class InvertibleVsSingular(Scene):
    def construct(self):
        left = Text("det ≠ 0 → invertible", color=GREEN)
        right = Text("det = 0 → not invertible", color=RED)
        VGroup(left, right).arrange(DOWN, buff=1)
        self.play(FadeIn(left), FadeIn(right))
        self.wait(3)


# ---------------------------------------------------------
class BasisVectorView(Scene):
    def construct(self):
        plane = NumberPlane()
        e1 = Vector([1, 0], color=BLUE)
        e2 = Vector([0, 1], color=GREEN)
        self.play(Create(plane), GrowArrow(e1), GrowArrow(e2))
        self.wait(1)
        self.play(
            ApplyMatrix([[2, 1], [1, 1]], e1),
            ApplyMatrix([[2, 1], [1, 1]], e2)
        )
        self.wait(2)

class DefineInverse(LinearTransformationScene):
    def __init__(self, **kwargs):
        super().__init__(
            show_basis_vectors=False, 
            include_background_plane=False,
            **kwargs)
        self.t_matrix = [[2, 1], [1, 1]]
        self.inverse_matrix = [[1, -1], [-1, 2]]
    def construct(self):
        self.add_sound("voiceovers/DefineInverse_Transform.mp3")
        self.plane.fade()
        self.add_unit_square()
        lhs = MathTex("A^{-1}", "A")
        lhs.scale(1.5).to_edge(UP).shift(3*LEFT)
        A_inv, A = lhs
        A_inv.set_color(YELLOW)
        A.set_color(BLUE)

        for mob in [A, A_inv]:
            mob.add_background_rectangle()

        A.text = "Phép biến đổi"
        A_inv.text = "Phép biến đổi nghịch đảo"

        for mob in A, A_inv:
            mob.arrow = Arrow(UP, DOWN).next_to(mob, DOWN)
            mob.text = Text(mob.text, font="Noto Sans").scale(0.7).next_to(mob.arrow, DOWN)
            mob.text.add_background_rectangle()

        self.add_foreground_mobjects(A, A_inv)

        arrow, text = A.arrow, A.text
        self.wait(2)
        self.play(Circumscribe(A_inv, color=GREEN))
        self.wait(3)
        self.play(GrowArrow(arrow), Write(text), run_time=1)
        self.add_foreground_mobjects(arrow, text)
        applying = VGroup(self.plane, self.square)
        self.play(ApplyMatrix(self.t_matrix, applying))
        self.add_sound("voiceovers/DefineInverse_InverseTransform.mp3")
        self.play(
            Transform(arrow, A_inv.arrow),
            Transform(text, A_inv.text),
        )
        self.play(ApplyMatrix(self.inverse_matrix, applying))        
        self.wait()
        self.play(FadeOut(text), FadeOut(arrow), FadeOut(applying))
        eq = MathTex("=").scale(1.5)
        identity_symbol = MathTex("I", color=GREEN).scale(1.5).next_to(eq, RIGHT)
        identity = Matrix([[1, 0], [0, 1]]).next_to(eq, RIGHT)
        identity.get_entries().set_color(GREEN)
        self.play(lhs.animate.next_to(eq, LEFT))
        self.play(FadeIn(eq), FadeIn(identity))
        self.wait()
        self.play(Transform(identity, identity_symbol))
        self.wait()
class InverseFormula2x2(Scene):
    def construct(self):
        self.add_sound("voiceovers/InverseFormula2x2.mp3") 
        title = Text("Công thức tìm Ma trận nghịch đảo", font="Noto Sans", color=YELLOW)
        title.scale(0.7).to_edge(UP)
        line = Line(LEFT * 6, RIGHT * 6, color=YELLOW).set_stroke(width=3)
        line.next_to(title, DOWN, buff=0.1)            
        self.play(Write(title), GrowFromCenter(line))
        original_matrix_text = MathTex("A=")
        matrix = MobjectMatrix([[MathTex("a"), MathTex("b")], [MathTex("c"), MathTex("d")]])
        matrix.get_entries().set_color(BLUE)
        formula = MathTex("A^{-1} = \\frac{1}{\\det(A)}",
                          "\\begin{pmatrix} d & -b \\\\ -c & a \\end{pmatrix}"
                          ).arrange(RIGHT)
        det = formula[0][5:11]
        left_group = VGroup(original_matrix_text, matrix).arrange(RIGHT)
        left_group.shift(3*LEFT)
        formula.shift(3*RIGHT)
        self.play(FadeIn(left_group))
        self.wait()
        self.play(FadeIn(formula), Flash(formula))
        self.wait(2)
        self.play(Circumscribe(det, color=GREEN))
        self.wait(9)
class InverseFormula2x2eExample(Scene):
    def construct(self):
        self.add_sound("voiceovers/example.mp3") 
        title = Text("Công thức tìm Ma trận nghịch đảo", font="Noto Sans", color=YELLOW)
        title.scale(0.7).to_edge(UP)
        line = Line(LEFT * 6, RIGHT * 6, color=YELLOW).set_stroke(width=3)
        line.next_to(title, DOWN, buff=0.1)            
        self.add(title, line)
        subtitle = Text("Ví dụ:", font="Noto Sans")
        subtitle.scale(0.65).next_to(line, DOWN)
        self.play(Write(subtitle))
        original_matrix_text = MathTex("A=")
        matrix = MobjectMatrix([[MathTex("4"), MathTex("3")], [MathTex("3"), MathTex("2")]])
        matrix.get_entries().set_color(BLUE)
        formula1 = MathTex("A^{-1} = \\frac{1}{(4)(2)-(3)(3)}",
                          "\\begin{pmatrix} 2 & -3 \\\\ -3 & 4 \\end{pmatrix}"
                          ).arrange(RIGHT)
        formula2 = MathTex("A^{-1} = \\frac{1}{8-9}",
                          "\\begin{pmatrix} 2 & -3 \\\\ -3 & 4 \\end{pmatrix}"
                          ).arrange(RIGHT)
        formula3 = MathTex("A^{-1} = \\frac{1}{-1}",
                          "\\begin{pmatrix} 2 & -3 \\\\ -3 & 4 \\end{pmatrix}"
                          ).arrange(RIGHT)
        formula4 = MathTex("A^{-1} = ",
                          "\\begin{pmatrix} 2 & -3 \\\\ -3 & 4 \\end{pmatrix}"
                          ).arrange(RIGHT)
        left_group = VGroup(original_matrix_text, matrix).arrange(RIGHT)
        left_group.shift(3*LEFT)
        formula1.shift(3*RIGHT)
        formula2.shift(3*RIGHT)
        formula3.shift(3*RIGHT)
        formula4.shift(3*RIGHT)
        self.play(FadeIn(left_group))
        self.wait()
        self.add_sound("voiceovers/correct-choice.wav") 
        self.play(FadeIn(formula1))
        self.wait()
        self.add_sound("voiceovers/correct-choice.wav") 
        self.play(Transform(formula1, formula2))
        self.wait()
        self.add_sound("voiceovers/correct-choice.wav") 
        self.play(Transform(formula1, formula3))
        self.wait()
        self.add_sound("voiceovers/correct-choice.wav") 
        self.play(Transform(formula1, formula4))
        self.add_sound("voiceovers/victory.wav") 
        self.play(Flash(formula1, line_length=1, flash_radius=formula1.width/2, 
                        run_time=2, num_lines=30, rate_func=rush_from))
        self.wait()
        self.add_sound("voiceovers/InverseFormula2x2eExample_check.mp3") 
        self.play(Circumscribe(formula1, color=GREEN))
        self.wait(2)
        test_result = MathTex(r"A \cdot A^{-1}=",
                              "\\begin{pmatrix} 4 & 3 \\\\ 3 & 2 \\end{pmatrix}",
                              r"\cdot",
                              "\\begin{pmatrix} -2 & 3 \\\\ 3 & -4 \\end{pmatrix}",
                              "=",
                              "\\begin{pmatrix} 1 & 0 \\\\ 0 & 1 \\end{pmatrix}")
        test_result.to_edge(DOWN, LARGE_BUFF)
        self.play(Write(test_result), run_time=2)
        self.play(Circumscribe(VGroup(test_result.split()[1],
                                      test_result.split()[2],
                                      test_result.split()[3]), color=GREEN))
        self.wait()
        self.play(Circumscribe(test_result.split()[-1], color=GREEN))
        correct = SVGMobject("assets/44.svg")
        self.play(FadeIn(correct))
        self.wait(2)
# ---------------------------------------------------------
class LinearSystem(Scene):
    def construct(self):
        self.add_sound("voiceovers/InverseFormula2x2.mp3") 
        title = Text("Giải hệ phương trình tuyến tính", font="Noto Sans", color=YELLOW)
        title.scale(0.7).to_edge(UP)
        line = Line(LEFT * 6, RIGHT * 6, color=YELLOW).set_stroke(width=3)
        line.next_to(title, DOWN, buff=0.1)            
        self.play(Write(title), GrowFromCenter(line))
        equations = self.get_equations()
    def get_equations(self):
        matrix = Matrix([
            [2, 5, 3],
            [4, 0, 8],
            [1, 3, 0]
        ])
        entries = matrix.get_entries()
        mob_matrix = [
            entries[i*3:(i+1)*3]
            for i in range(3)
        ]

        rhs = [MathTex(str(x)) for x in (-3, 0, 2)]
        variables = [MathTex(v) for v in "xyz"]

        for v, c in zip(variables, [GREEN, RED, BLUE]):
            v.set_color(c)

        equations = VGroup()
        for row in mob_matrix:
            equation = VGroup(*it.chain(*zip(
                row,
                [v.copy() for v in variables],
                [MathTex(s) for s in ["+", "+", "="]]
            )))
            equation.arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
            equation[4].shift(0.1 * DOWN)
            equation[-1].next_to(equation[-2], RIGHT)
            equations.add(equation)

        equations.arrange(DOWN, aligned_edge=RIGHT)

        for eq, r in zip(equations, rhs):
            r.next_to(eq, RIGHT)
            eq.add(r)

        equations.center()
        self.play(Write(equations))
        return equations
class Applications(Scene):
    def construct(self):
        apps = VGroup(
            Text("• Solving linear systems"),
            Text("• Change of variables"),
            Text("• Physics & ML")
        ).arrange(DOWN, aligned_edge=LEFT)
        self.play(LaggedStartMap(FadeIn, apps, lag_ratio=0.6))
        self.wait(4)


# ---------------------------------------------------------
class FinalWrap(Scene):
    def construct(self):
        text = Text("Determinants measure loss.\nInverses undo change.", font_size=40)
        self.play(Write(text))
        self.wait(4)

class HigherDimIdea(ThreeDScene):
    def construct(self):
        self.add_sound("voiceovers/HigherDimIdea.mp3")
        matrix = Matrix([[1, 0, 0.5], [0.5, 1, 0], [1, 0, 1]])
        matrix.to_corner(UL)
        det_text = get_det_text(matrix, initial_scale_factor=1)
        eq = MathTex("=")
        eq.next_to(det_text, DOWN, aligned_edge=LEFT)
        text = Text("Thể tích \n hình hộp chữ nhật", font="Noto Sans")
        text.scale(0.6).next_to(eq, RIGHT)      
        self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)
        axes = ThreeDAxes()
        cube = Cube(side_length=3, fill_opacity=0.7, fill_color=BLUE)
        self.add(cube, axes)
        self.wait(2)    
        matrix_group = VGroup(matrix, det_text, text, eq)
        matrix_group.set_color(YELLOW).scale(0.8)
        self.add_fixed_in_frame_mobjects(matrix_group)
        self.play(ApplyMatrix([[1, 0, 0.5], [0.5, 1, 0], [1, 0, 1]], VGroup(cube)))
        self.wait()
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(7)
        self.stop_ambient_camera_rotation()
        self.wait()