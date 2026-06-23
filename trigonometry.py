from manim import *
import random

def get_conditional_angle(l1, l2, tol=1e-3, radius=0.6):
        v1 = l1.get_unit_vector()
        v2 = l2.get_unit_vector()

        # Use only the z-component (scalar) to check parallelism
        cross_z = np.cross(v1, v2)[-1]
        parallel = abs(cross_z) < tol

        if parallel:
            return Line(l1.get_end(), l2.get_end())
        else:
            return Angle(l1, l2, radius=radius, stroke_width=1)

class AngleOfElevation(Scene):
    def construct(self):

        # Title
        title = Text("Angle of Elevation", font_size=60).to_edge(UP)
        self.play(Write(title))

        # Ground line
        ground = Line(LEFT*4, RIGHT*4).shift(DOWN*2)
        ground_label = Text("Horizontal ground", font_size=28).next_to(ground, DOWN)
        self.play(Create(ground), FadeIn(ground_label))

        # Observer point
        observer = Dot(point=ground.get_left() + RIGHT*0.5)
        observer_label = Text("Observer", font_size=28).next_to(observer, DOWN)
        self.play(FadeIn(observer), FadeIn(observer_label))

        # Object above ground (e.g., top of a building)
        obj = Dot(point=UP*1.5)
        obj_label = Text("Object", font_size=28).next_to(obj, UP)
        self.play(FadeIn(obj), FadeIn(obj_label))

        # Line of sight
        line_of_sight = Line(observer.get_center(), obj.get_center(), color=YELLOW)
        self.play(Create(line_of_sight))

        # Vertical dashed line from object to ground
        drop_line = DashedLine(obj.get_center(), obj.get_center() + DOWN*3.5)
        self.play(Create(drop_line))

        # Angle arc for angle of elevation
        angle = Angle(
            ground,
            line_of_sight,
            radius=1,
            other_angle=False,
            color=BLUE
        )
        angle_label = MathTex(r"\theta", font_size=40).next_to(angle, RIGHT*0.7 + UP*0.2)

        self.play(Create(angle), FadeIn(angle_label))

        # Explanation text
        explanation = (
            Text("The Angle of Elevation is the angle between", font_size=32)
            .to_edge(DOWN)
        )
        explanation2 = (
            Text("the horizontal ground and the line of sight upward.", font_size=32)
            .next_to(explanation, DOWN)
        )

        self.play(FadeIn(explanation), FadeIn(explanation2))
        self.wait(2)

        # Highlight animation
        self.play(angle.animate.set_color(RED), run_time=1)
        self.wait(1)
from manim import *

class RocketLandingAngles(Scene):
    def construct(self):
        # Rocket center
        origin = ORIGIN

        # Rocket tilt angle in radians
        tilt_angle = 20 * DEGREES  # rocket rotated 20 degrees from vertical

        # Rocket axis vector
        rocket_length = 2.0
        rocket_axis_vector = rocket_length * np.array([np.sin(tilt_angle), np.cos(tilt_angle), 0])

        # Velocity vector (downwards)
        velocity_vector = np.array([0, -1.5, 0])

        # Draw rocket axis
        rocket_axis_ray = Line(origin, origin + rocket_axis_vector, color=WHITE)
        # Draw velocity vector
        velocity_ray = Line(origin, origin + velocity_vector, color=RED)

        # Draw angle of attack
        aoa_arc = Angle(
            rocket_axis_ray,
            velocity_ray,
            radius=0.5,
            color=GREEN
        )
        aoa_label = MathTex(r"\text{AoA }(\alpha)", color=GREEN).next_to(aoa_arc, LEFT)

        # Display
        self.play(Create(rocket_axis_ray), Create(velocity_ray))
        self.play(Create(aoa_arc), FadeIn(aoa_label))
        self.wait(2)

from manim import *
import math  # <-- FIXED: Added math module

class RocketLandingAngles1(Scene):
    def construct(self):

        # ----------------------------
        # Title
        # ----------------------------
        title = Text("Rocket Landing Angles", font_size=56).to_edge(UP)
        self.play(Write(title))

        # ----------------------------
        # Rocket Icon
        # ----------------------------
        body = Rectangle(width=0.4, height=2, color=WHITE, fill_opacity=1)
        nose = Triangle(color=WHITE, fill_opacity=1).scale(0.35)
        nose.next_to(body, UP, buff=-0.01)

        left_fin = Polygon(
            [-0.2, -1, 0], [-0.6, -1.4, 0], [-0.2, -1.4, 0],
            color=WHITE, fill_opacity=1
        )
        right_fin = left_fin.copy().flip().shift([0.8, 0, 0])

        rocket = VGroup(body, nose, left_fin, right_fin)
        rocket.move_to(DOWN)

        self.play(FadeIn(rocket, shift=UP))

        # ----------------------------
        # Local vertical reference
        # ----------------------------
        vertical = Line(DOWN*3, UP*3, color=BLUE)
        vertical_label = Text("Local Vertical", font_size=28, color=BLUE)
        vertical_label.next_to(vertical, RIGHT)

        self.play(Create(vertical), FadeIn(vertical_label))

        # ----------------------------
        # Tilt rocket (Landing Pitch Angle)
        # ----------------------------
        tilt_deg = 20

        tilted_rocket = rocket.copy().rotate(tilt_deg * DEGREES)

        # Create pitch angle arc
        pitch_angle_arc = Angle(
            vertical,
            Line(ORIGIN, [math.sin(tilt_deg * DEGREES), math.cos(tilt_deg * DEGREES), 0]),
            radius=1.2,
            color=YELLOW,
        )

        pitch_label = MathTex(r"\text{Pitch Angle }(\theta_p)", color=YELLOW) \
                      .next_to(pitch_angle_arc, RIGHT)

        self.play(Transform(rocket, tilted_rocket))
        self.play(Create(pitch_angle_arc), FadeIn(pitch_label))
        self.wait(1)

        # ----------------------------
        # Velocity vector (downward)
        # ----------------------------
        velocity = Arrow(
            start=rocket.get_center()+UP*1.2,
            end=rocket.get_center()+DOWN*1.2,
            color=RED,
            buff=0
        )
        velocity_label = Text("Velocity", color=RED, font_size=28)
        velocity_label.next_to(velocity, RIGHT)

        self.play(Create(velocity), FadeIn(velocity_label))
        self.wait(1)

        # ----------------------------
        # Angle of Attack (AoA)
        # ----------------------------
        # ----------------------------
# Angle of Attack (AoA)
# ----------------------------

        # -----------------------------------
# Angle of Attack (AoA) -- FIXED
# -----------------------------------

        origin = rocket.get_center()

        # Compute REAL rocket axis after tilt
        top = rocket.get_top()
        bottom = rocket.get_bottom()

        rocket_axis_dir = top - bottom
        rocket_axis_dir = rocket_axis_dir / np.linalg.norm(rocket_axis_dir)

        # Velocity direction (straight down)
        velocity_dir = DOWN

        # Create two rays from same point
        rocket_axis_ray = Line(origin, origin + rocket_axis_dir, color=WHITE)
        velocity_ray = Line(origin, origin + velocity_dir, color=RED)

        # The rays now are NOT parallel → angle works
        aoa_arc = Angle(
            rocket_axis_ray,
            velocity_ray,
            radius=0.8,
            color=GREEN
        )

        aoa_label = MathTex(r"\text{AoA }(\alpha)", color=GREEN) \
            .next_to(aoa_arc, LEFT)

        self.play(Create(aoa_arc), FadeIn(aoa_label))



        # ----------------------------
        # Flight Path Angle
        # ----------------------------
        ground = Line(LEFT*6, RIGHT*6, color=GRAY)
        ground_label = Text("Ground", font_size=28)
        ground_label.next_to(ground, DOWN)

        self.play(FadeIn(ground), FadeIn(ground_label))

        fpa_arc = Angle(
            ground,
            velocity,
            radius=1.2,
            color=ORANGE,
            other_angle=True
        )
        fpa_label = MathTex(r"\text{Flight Path Angle }(\gamma)", color=ORANGE) \
                   .next_to(fpa_arc, DOWN+RIGHT)

        self.play(Create(fpa_arc), FadeIn(fpa_label))
        self.wait(2)

        # End
        self.play(*[FadeOut(mob) for mob in self.mobjects])

class AngleOfElevationEye(Scene):
    def construct(self):

        # Title
        title = Text("Angle of Elevation", font_size=60).to_edge(UP)
        self.play(Write(title))

        # Ground line
        ground = Line(LEFT*4, RIGHT*4).shift(DOWN*2)
        ground_label = Text("Horizontal ground", font_size=28).next_to(ground, DOWN)
        self.play(Create(ground), FadeIn(ground_label))

        # ----------------------
        # EYE ICON
        # ----------------------
        eye_outer = Ellipse(width=1.2, height=0.7, color=BLACK, stroke_width=4)
        eye_inner = Circle(radius=0.18, color=BLACK, fill_opacity=1)
        eye_inner.move_to(eye_outer.get_center())
        eye_icon = VGroup(eye_outer, eye_inner)
        eye_icon.move_to(ground.get_left() + RIGHT*0.8)

        observer_label = Text("Observer", font_size=28).next_to(eye_icon, DOWN)
        self.play(FadeIn(eye_icon), FadeIn(observer_label))

        # ----------------------
        # TREE ICON
        # ----------------------
        trunk = Rectangle(width=0.35, height=1, color="#5B3A29", fill_opacity=1)
        leaves = Circle(radius=0.9, color=GREEN, fill_opacity=1, stroke_color=BLACK)
        leaves.next_to(trunk, UP, buff=-0.2)

        tree_icon = VGroup(leaves, trunk)
        tree_icon.move_to(UP*1.5)
        tree_label = Text("Tree", font_size=28).next_to(tree_icon, UP)

        self.play(FadeIn(tree_icon), FadeIn(tree_label))

        # Line of sight
        line_of_sight = Line(
            eye_icon.get_center(),
            leaves.get_center(),
            color=YELLOW
        )
        self.play(Create(line_of_sight))

        # ----------------------
        # LABEL ALIGNED TO LINE OF SIGHT
        # ----------------------
        los_label = Text("Line of Sight", font_size=26, color=YELLOW)

        # Position at midpoint
        los_label.move_to(line_of_sight.get_midpoint())

        # Rotate label to match line angle
        los_label.rotate(line_of_sight.get_angle())

        self.play(FadeIn(los_label))

        # Vertical dashed line
        drop_line = DashedLine(
            leaves.get_center(),
            leaves.get_center() + DOWN*3,
            dash_length=0.15
        )
        self.play(Create(drop_line))

        # Angle of elevation
        angle = Angle(
            ground,
            line_of_sight,
            radius=1.1,
            color=BLUE
        )
        angle_label = MathTex(r"\theta", font_size=40).next_to(angle, RIGHT*0.7 + UP*0.2)

        self.play(Create(angle), FadeIn(angle_label))

        # Explanation text
        explanation = Text("The Angle of Elevation is the angle between", font_size=32).to_edge(DOWN)
        explanation2 = Text("the horizontal ground and the line of sight upward.", font_size=32).next_to(explanation, DOWN)

        self.play(FadeIn(explanation), FadeIn(explanation2))
        self.wait(2)

        # Highlight angle
        self.play(angle.animate.set_color(RED))
        self.wait(1)

class AngleOfElevationTree(Scene):
    def construct(self):

        # Title
        title = Text("Angle of Elevation", font_size=60).to_edge(UP)
        self.play(Write(title))

        # Ground line
        ground = Line(LEFT*4, RIGHT*4).shift(DOWN*2)
        ground_label = Text("Horizontal ground", font_size=28).next_to(ground, DOWN)
        self.play(Create(ground), FadeIn(ground_label))

        # ----------------------
        # Eye Icon (Observer)
        # ----------------------
        eye_outer = Ellipse(width=1.2, height=0.6, color=WHITE, fill_opacity=1)
        eye_inner = Circle(radius=0.15, color=BLACK, fill_opacity=1)
        eye_icon = VGroup(eye_outer, eye_inner)

        observer = eye_icon.move_to(ground.get_left() + RIGHT*0.7)
        observer_label = Text("Observer", font_size=28).next_to(observer, DOWN)

        self.play(FadeIn(observer), FadeIn(observer_label))

        # ----------------------
        # Tree Icon (Object)
        # ----------------------
        trunk = Rectangle(width=0.3, height=0.8, color=MAROON, fill_opacity=1)
        leaves = Circle(radius=0.7, color=GREEN, fill_opacity=1)
        leaves.next_to(trunk, UP, buff=-0.3)
        
        tree_icon = VGroup(leaves, trunk).move_to(UP*1.5)
        tree_label = Text("Tree", font_size=28).next_to(tree_icon, UP)

        self.play(FadeIn(tree_icon), FadeIn(tree_label))

        # Line of sight
        line_of_sight = Line(observer.get_center(), tree_icon.get_top(), color=YELLOW)
        self.play(Create(line_of_sight))

        # Vertical dashed line from tree to ground
        drop_line = DashedLine(tree_icon.get_top(), tree_icon.get_top() + DOWN*3)
        self.play(Create(drop_line))

        # Angle arc for angle of elevation
        angle = Angle(
            ground,
            line_of_sight,
            radius=1,
            other_angle=False,
            color=BLUE
        )
        angle_label = MathTex(r"\theta", font_size=40).next_to(angle, RIGHT*0.7 + UP*0.2)

        self.play(Create(angle), FadeIn(angle_label))

        # Explanation text
        explanation = (
            Text("The Angle of Elevation is the angle between", font_size=32)
            .to_edge(DOWN)
        )
        explanation2 = (
            Text("the horizontal ground and the line of sight upward.", font_size=32)
            .next_to(explanation, DOWN)
        )

        self.play(FadeIn(explanation), FadeIn(explanation2))
        self.wait(2)

        # Highlight the angle
        self.play(angle.animate.set_color(RED), run_time=1)
        self.wait(1)

class Scene1_Hook(Scene):
    def construct(self):
        self.add_sound("voiceovers/Scene1_Hook.mp3")
        bg = ImageMobject("assets/Scene1_Hook.png")
        bg.scale_to_fit_height(config.frame_height)  
        bg.scale_to_fit_width(config.frame_width)    
        bg.move_to(ORIGIN)
        self.add(bg) 
        self.wait(6)
        self.play(bg.animate.set_opacity(0.1))
        text = Text("Làm thế nào để đo (lượng) góc (giác)...?", gradient=(RED, BLUE, GREEN), font="Noto Sans")
        self.play(Write(text))
        self.wait(7)
class Scene2_Why(Scene):
    def construct(self):
        self.add_sound("voiceovers/Scene2_Why.mp3")
        bg = ImageMobject("assets/Scene2_Why.png")
        bg.scale_to_fit_height(config.frame_height)  
        bg.scale_to_fit_width(config.frame_width)    
        bg.move_to(ORIGIN)
        self.add(bg) 
        self.wait(10)
        self.play(bg.animate.set_opacity(0.1))
        text = Text("Lượng giác = Góc + Tỷ số", gradient=(RED, BLUE, GREEN), font="Noto Sans")
        self.play(Write(text))
        self.wait(2)

class Scene3_RightTriangle(Scene):
    def construct(self):
        self.add_sound("voiceovers/Scene5_3.mp3")
        title = Text("Tam giác vuông", gradient=(RED, BLUE, GREEN), font="Noto Sans").scale(0.8).to_corner(UL)
        self.play(Write(title))
        A = DOWN + LEFT
        B = DOWN + LEFT * 5
        C = UP * 2 + LEFT

        opp = Line(C, A, color=RED)
        hyp = Line(B, C, color=YELLOW)
        adj = Line(A, B, color=BLUE)
        triangle = VGroup(adj, hyp, opp)

        right_angle = RightAngle(Line(A, B), Line(A, C))
        angle = Angle(Line(B, A), Line(B, C), radius=0.8)
        theta = MathTex(r"\theta", color=GREEN).move_to(
            Angle(Line(B, A), Line(B, C), radius=0.8 + 3 * SMALL_BUFF).point_from_proportion(0.5)
            )

        opp_text = MathTex("a", color=RED).move_to((C + A)/2).shift(RIGHT*0.5)
        opp_text_vn = Text("(đối)", font="Noto Sans").scale(0.65).next_to(opp_text, DOWN)
        adj_text = MathTex("b", color=BLUE).move_to((A + B)/2).shift(DOWN*0.4)
        adj_text_vn = Text("(kề)", font="Noto Sans").scale(0.65).next_to(adj_text, RIGHT)
        hyp_text = MathTex("h", color=YELLOW).move_to((B + C)/2).shift(0.5*UP + 0.5*LEFT)
        hyp_text_vn = Text("(huyền)", font="Noto Sans").scale(0.65).next_to(hyp_text, DOWN).shift(LEFT)

        self.play(Create(triangle), Create(right_angle))
        self.wait()
        self.play(Create(angle), FadeIn(theta))
        self.wait()
        self.play(Write(opp_text), Write(opp_text_vn))
        self.wait(0.5)
        self.play(Write(adj_text), Write(adj_text_vn))
        self.wait(0.5)
        self.play(Write(hyp_text), Write(hyp_text_vn))
        self.wait(4.5)

        sin_ratio = MathTex(r"\sin\theta = \frac{\text{a}}{\text{h}}").next_to(C, RIGHT).shift(2*RIGHT)
        sin_theta = sin_ratio[0][3:4]
        sin_theta.set_color(GREEN)
        sin_opp = sin_ratio[0][5:6]
        sin_hyp = sin_ratio[0][-1:]
        sin_opp.set_color(RED)
        sin_hyp.set_color(YELLOW)
        sin_opp.target, sin_hyp.target = opp_text, hyp_text
        csc_arrow = MathTex(r"\rightarrow").next_to(sin_ratio, RIGHT)
        csc_ratio = MathTex(r"\csc\theta = \frac{\text{h}}{\text{a}}").next_to(csc_arrow, RIGHT)
        csc_theta = csc_ratio[0][3:4]
        csc_theta.set_color(GREEN)
        csc_opp = csc_ratio[0][-1:]
        csc_hyp = csc_ratio[0][5:6]
        csc_opp.set_color(RED)
        csc_hyp.set_color(YELLOW)
        csc_opp.target, csc_hyp.target = sin_opp, sin_hyp

        cos_ratio = MathTex(r"\cos\theta = \frac{\text{b}}{\text{h}}").next_to(sin_ratio, DOWN)
        cos_theta = cos_ratio[0][3:4]
        cos_theta.set_color(GREEN)
        cos_adj = cos_ratio[0][5:6]
        cos_hyp = cos_ratio[0][-1:]
        cos_adj.set_color(BLUE)
        cos_hyp.set_color(YELLOW)
        cos_adj.target, cos_hyp.target = adj_text, hyp_text
        sec_arrow = MathTex(r"\rightarrow").next_to(cos_ratio, RIGHT)
        sec_ratio = MathTex(r"\sec\theta = \frac{\text{h}}{\text{b}}").next_to(sec_arrow, RIGHT)
        sec_theta = sec_ratio[0][3:4]
        sec_theta.set_color(GREEN)
        sec_adj = sec_ratio[0][-1:]
        sec_hyp = sec_ratio[0][5:6]
        sec_adj.set_color(BLUE)
        sec_hyp.set_color(YELLOW)
        sec_adj.target, sec_hyp.target = cos_adj, cos_hyp

        tan_ratio = MathTex(r"\tan\theta = \frac{\text{a}}{\text{b}}").next_to(cos_ratio, DOWN)
        tan_theta = tan_ratio[0][3:4]
        tan_theta.set_color(GREEN)
        tan_opp = tan_ratio[0][5:6]
        tan_adj = tan_ratio[0][-1:]
        tan_opp.set_color(RED)
        tan_adj.set_color(BLUE)
        tan_adj.target, tan_opp.target = adj_text, opp_text
        cot_arrow = MathTex(r"\rightarrow").next_to(tan_ratio, RIGHT)
        cot_ratio = MathTex(r"\cot\theta = \frac{\text{b}}{\text{a}}").next_to(cot_arrow, RIGHT)
        cot_theta = cot_ratio[0][3:4]
        cot_theta.set_color(GREEN)
        cot_opp = cot_ratio[0][-1:]
        cot_adj = cot_ratio[0][5:6]
        cot_opp.set_color(RED)
        cot_adj.set_color(BLUE)
        cot_opp.target, cot_adj.target = tan_opp, tan_adj
        
        for mob in sin_opp, sin_hyp:
            mob.save_state()
            mob.set_opacity(0)
            mob.move_to(mob.target)
        for mob in cos_adj, cos_hyp:
            mob.save_state()
            mob.set_opacity(0)
            mob.move_to(mob.target)
        for mob in tan_adj, tan_opp:
            mob.save_state()
            mob.set_opacity(0)
            mob.move_to(mob.target)
        self.play(Write(sin_ratio))
        self.play(Write(cos_ratio))
        self.play(Write(tan_ratio))
        self.wait()

        for mob in sin_opp, sin_hyp:
            mob.set_opacity(1)
        
        
        self.play(*[mob.animate.restore() for mob in (sin_opp, sin_hyp)])
        self.wait()
        for mob in cos_adj, cos_hyp:
            mob.set_opacity(1)
        self.play(*[mob.animate.restore() for mob in (cos_adj, cos_hyp)])
        self.wait()
        for mob in tan_adj, tan_opp:
            mob.set_opacity(1)
        self.play(*[mob.animate.restore() for mob in (tan_opp, tan_adj)])
        self.wait(6)
        
        for mob in csc_opp, csc_hyp:
            mob.save_state()
            mob.move_to(mob.target)
            mob.set_opacity(0)
        self.play(Write(csc_arrow), Write(csc_ratio))

        for mob in sec_adj, sec_hyp:
            mob.save_state()
            mob.move_to(mob.target)
            mob.set_opacity(0)
        self.play(Write(sec_arrow), Write(sec_ratio))

        for mob in cot_opp, cot_adj:
            mob.save_state()
            mob.move_to(mob.target)
            mob.set_opacity(0)
        self.play(Write(cot_arrow), Write(cot_ratio))
        self.wait(2)
        
        for mob in csc_opp, csc_hyp:
            mob.set_opacity(1)
        self.play(*[mob.animate.restore() for mob in (csc_hyp, csc_opp)], run_time=1.5)
        for mob in sec_adj, sec_hyp:
            mob.set_opacity(1)
        self.play(*[mob.animate.restore() for mob in (sec_adj, sec_hyp)], run_time=1.5)
        for mob in cot_opp, cot_adj:
            mob.set_opacity(1)
        self.play(*[mob.animate.restore() for mob in (cot_opp, cot_adj)], run_time=1.5)
        self.play(FadeOut(opp_text), FadeOut(opp_text_vn), FadeOut(adj_text), FadeOut(adj_text_vn), FadeOut(hyp_text), FadeOut(hyp_text_vn))

        tri_small = VGroup(triangle, right_angle, angle, theta)
        tri_large = tri_small.copy().scale(1.8)
        self.play(Transform(tri_small, tri_large))
        self.wait(2)
        ratio_group = VGroup(sin_ratio, csc_arrow, csc_ratio, cos_ratio, sec_arrow, sec_ratio, tan_ratio, cot_arrow, cot_ratio)
        # glow = SurroundingRectangle(ratio_group, color=YELLOW, buff=0.2)
        # self.play(Create(glow))
        self.play(Circumscribe(ratio_group, fade_out=True))
        self.wait(8)
        self.play(Flash(ratio_group, line_length=1, flash_radius=ratio_group.width/2, 
                        run_time=2, num_lines=30, rate_func=rush_from))
        self.play(FadeOut(title), FadeOut(tri_small), FadeOut(ratio_group))

class Scene4_SOHCAHTOA(Scene):
    def construct(self):
        sin_ratio = MathTex(r"\sin\theta = \frac{\text{a}}{\text{h}}").to_edge(UP)
        cos_ratio = MathTex(r"\cos\theta = \frac{\text{b}}{\text{h}}")
        tan_ratio = MathTex(r"\tan\theta = \frac{\text{a}}{\text{b}}").to_edge(DOWN)

        self.play(Write(sin_ratio))
        self.wait(0.5)
        self.play(Write(cos_ratio))
        self.wait(0.5)
        self.play(Write(tan_ratio))
        self.wait(1)
class Scene5_RatiosConstant(Scene):
    def construct(self):
        A = ORIGIN
        B = RIGHT * 2
        C = UP * 1.5
        tri_small = Polygon(A, B, C)

        tri_large = tri_small.copy().scale(1.8, about_point=A)

        label_small = Text("Small Triangle", font_size=28).next_to(tri_small, DOWN)
        label_large = Text("Large Triangle", font_size=28).next_to(tri_large, UP)

        ratios = MathTex(r"\frac{\text{a}}{\text{h}} = \text{constant}").to_edge(DOWN)

        self.play(Create(tri_small), FadeIn(label_small))
        self.wait(0.5)
        self.play(Transform(tri_small, tri_large), FadeIn(label_large))
        self.wait(0.5)
        self.play(Write(ratios))
        self.wait(1)
class Scene6_UnitCircle(Scene):
    def construct(self):
        self.add_sound("voiceovers/Scene6_UnitCircle1.mp3")
        title = Text("Đường tròn đơn vị", gradient=(RED, BLUE, GREEN), font="Noto Sans").scale(0.8).to_edge(UP)
        self.play(Write(title))
        A = RIGHT * 4
        B = ORIGIN
        C = UP * 3 + RIGHT * 4

        opp = Line(C, A, color=RED)
        hyp = Line(B, C, color=YELLOW)
        adj = Line(A, B, color=BLUE)
        triangle = VGroup(adj, hyp, opp)

        angle = Angle(Line(B, A), Line(B, C), radius=0.6)
        theta = MathTex(r"\theta", color=GREEN).move_to(
            Angle(Line(B, A), Line(B, C), radius=0.6 + 3 * SMALL_BUFF).point_from_proportion(0.5))
        self.play(Create(triangle), Create(angle), FadeIn(theta), run_time=3)
        
        x_axis = Line(2.25 * LEFT, 2.25 * RIGHT)
        y_axis = Line(2.25 * DOWN, 2.25 * UP)
        point_up = MathTex("(0,1)").scale(0.65).next_to(y_axis, LEFT).shift(2.25 * UP)
        point_down = MathTex("(0,-1)").scale(0.65).next_to(y_axis, LEFT).shift(2.25 * DOWN)
        point_left = MathTex("(-1,0)").scale(0.65).next_to(x_axis, DOWN).shift(2.45 * LEFT)
        point_right = MathTex("(1,0)").scale(0.65).next_to(x_axis, DOWN).shift(2.35 * RIGHT)
        points = VGroup(point_up, point_down, point_left, point_right)
        axes = VGroup(
            x_axis,
            y_axis,
        )
        axes.set_stroke(GRAY_B, 1)
        circle = Circle(radius=2).set_stroke(WHITE, 2)
        dot = Dot(point=1.6*RIGHT + 1.2*UP, radius=0.08, color=YELLOW)

        x_line = always_redraw(lambda: Line(ORIGIN, dot.get_center(), color=YELLOW))
        proj_x = always_redraw(lambda: Line(dot.get_center(), [dot.get_x(), 0, 0], color=RED))
        proj_y = always_redraw(lambda: Line(ORIGIN, [dot.get_x(), 0, 0], color=BLUE))

        angle_rotate = always_redraw(
            lambda: get_conditional_angle(Line(ORIGIN, RIGHT), Line(ORIGIN, dot.get_center()), radius=0.6)
        )
        theta_rotate = always_redraw(
            lambda: MathTex(r"\theta", color=GREEN).move_to(
                get_conditional_angle(Line(ORIGIN, RIGHT), Line(ORIGIN, dot.get_center()), 
                                           radius=0.6 + 3 * SMALL_BUFF
                ).point_from_proportion(0.5))
            )

        self.play(Create(axes), Create(circle), FadeIn(points))
        self.play(triangle.animate.scale(0.4, about_point=B))
        opp_text = MathTex("a", color=RED).next_to(opp, RIGHT)
        adj_text = MathTex("b", color=BLUE).next_to(adj, DOWN)
        hyp_brace = Brace(hyp, direction=hyp.copy().rotate(PI / 2).get_unit_vector())
        hyp_text = hyp_brace.get_tex("h=1").set_color(YELLOW)
        
        sin_ratio = MathTex(r"\sin\theta = \frac{\text{a}}{\text{h}}").next_to(circle, RIGHT).shift(1.5*UP + RIGHT)
        sin_theta = sin_ratio[0][3:4]
        sin_theta.set_color(GREEN)
        sin_opp = sin_ratio[0][5:6]
        sin_hyp = sin_ratio[0][-1:]
        sin_opp.set_color(RED)
        sin_hyp.set_color(YELLOW)

        cos_ratio = MathTex(r"\cos\theta = \frac{\text{b}}{\text{h}}").next_to(sin_ratio, DOWN)
        cos_theta = cos_ratio[0][3:4]
        cos_theta.set_color(GREEN)
        cos_adj = cos_ratio[0][5:6]
        cos_hyp = cos_ratio[0][-1:]
        cos_adj.set_color(BLUE)
        cos_hyp.set_color(YELLOW)

        self.play(FadeIn(adj_text), FadeIn(opp_text))
        self.play(Create(hyp_brace), Create(hyp_text))
        self.wait()
        self.play(Indicate(title))
        self.play(FadeIn(sin_ratio), FadeIn(cos_ratio))
        sin_unit = MathTex("1", color=YELLOW).move_to(sin_hyp)
        cos_unit = MathTex("1", color=YELLOW).move_to(cos_hyp)
        
        sin_fac = sin_ratio[0][5:]
        new_sin = Tex("a", color=RED).move_to(sin_fac)
        self.play(Transform(sin_hyp, sin_unit))
        self.play(Transform(sin_fac, new_sin))
        cos_fac = cos_ratio[0][5:]
        new_cos = Tex("b", color=BLUE).move_to(cos_fac)
        self.play(Transform(cos_hyp, cos_unit))
        self.play(Transform(cos_fac, new_cos))
        sin_text = MathTex(r"\sin\theta").next_to(opp, RIGHT)
        sin_text[0][3:4].set_color(GREEN)
        cos_text = MathTex(r"\cos\theta").next_to(adj, DOWN)
        cos_text[0][3:4].set_color(GREEN)
        self.play(FadeOut(opp_text), FadeOut(adj_text))
        sin_text.target, cos_text.target = sin_ratio[0][:4], cos_ratio[0][:4]
        for mob in sin_text, cos_text:
            mob.save_state()
            mob.move_to(mob.target)
        self.play(*[mob.animate.restore() for mob in (sin_text, cos_text)])
        self.play(FadeOut(sin_ratio), FadeOut(cos_ratio))
                
        self.add(x_line, proj_x, proj_y, angle_rotate, theta_rotate, dot)
        self.play(FadeOut(triangle), FadeOut(angle), FadeOut(theta))
        
        def get_sin_text():
            sin_text = MathTex(r"\sin\theta").next_to(proj_x, RIGHT)
            sin_text[0][3:4].set_color(GREEN)
            return sin_text
        def get_cos_text():
            cos_text = MathTex(r"\cos\theta").next_to(proj_y, DOWN)
            cos_text[0][3:4].set_color(GREEN)
            return cos_text
        sin_text_rotate = always_redraw(get_sin_text)
        cos_text_rotate = always_redraw(get_cos_text)
        self.add(sin_text_rotate, cos_text_rotate)
        self.play(FadeOut(sin_text), FadeOut(cos_text))
        self.play(FadeOut(hyp_text), FadeOut(hyp_brace))
        self.add_sound("voiceovers/Scene6_UnitCircle2.mp3")
        self.play(Rotate(dot, angle=2*PI, about_point=ORIGIN), run_time=6)
        self.wait(6)  

class Scene7_AnglesBeyond(Scene):
    def construct(self):
        self.add_sound("voiceovers/Scene7_AnglesBeyond.mp3")
        title = Text("Góc lớn hơn 90°", gradient=(RED, BLUE, GREEN), font="Noto Sans").scale(0.8).to_corner(UL)
        self.play(Write(title))
        x_axis = Line(2.25 * LEFT, 2.25 * RIGHT)
        y_axis = Line(2.25 * DOWN, 2.25 * UP)
        point_up = MathTex("(0,1)").scale(0.65).next_to(y_axis, LEFT).shift(2.25 * UP)
        point_down = MathTex("(0,-1)").scale(0.65).next_to(y_axis, LEFT).shift(2.25 * DOWN)
        point_left = MathTex("(-1,0)").scale(0.65).next_to(x_axis, DOWN).shift(2.45 * LEFT)
        point_right = MathTex("(1,0)").scale(0.65).next_to(x_axis, DOWN).shift(2.35 * RIGHT)
        points = VGroup(point_up, point_down, point_left, point_right)
        axes = VGroup(
            x_axis,
            y_axis,
        )
        axes.set_stroke(GRAY_B, 1)
        circle = Circle(radius=2, color=BLUE)
        theta = ValueTracker(0)

        moving_dot = always_redraw(
            lambda: Dot(point=circle.point_at_angle(theta.get_value()))
        )
        x_line = always_redraw(lambda: Line(ORIGIN, moving_dot.get_center(), color=GOLD))
        def get_theta():
            theta_label = MathTex(r"\theta = " + f"{int(theta.get_value()*180/PI)}^\circ")
            theta_label[0][:1].set_color(GREEN)
            theta_label.to_edge(UP)
            return theta_label
        label = always_redraw(get_theta)
        angle_rotate = always_redraw(
            lambda: get_conditional_angle(Line(ORIGIN, RIGHT), Line(ORIGIN, moving_dot.get_center()), radius=0.6)
        )
        theta_rotate = always_redraw(
            lambda: MathTex(r"\theta", color=GREEN).move_to(
                get_conditional_angle(Line(ORIGIN, RIGHT), Line(ORIGIN, moving_dot.get_center()), 
                                           radius=0.6 + 3 * SMALL_BUFF
                ).point_from_proportion(0.5))
            )

        
        self.play(Create(axes), Create(circle), FadeIn(points))
        self.add(moving_dot, x_line, label, angle_rotate, theta_rotate)

        self.play(theta.animate.set_value(2*PI), run_time=10, rate_func=there_and_back)
        self.wait()
class Scene7_Tangent(Scene):
    def construct(self):
        self.add_sound("voiceovers/Scene7_Tangent.mp3")
        tan_ratio = MathTex(r"\tan\theta = \frac{\sin\theta}{\cos\theta}")
        tan_ratio.to_corner(UL)
        tan_ratio[0][3:4].set_color(GREEN)
        tan_ratio[0][8:9].set_color(GREEN)
        tan_ratio[0][-1:].set_color(GREEN)
        self.play(Write(tan_ratio))
        self.wait()
        x_axis = Line(2.25 * LEFT, 2.25 * RIGHT)
        y_axis = Line(2.25 * DOWN, 2.25 * UP)
        axes = VGroup(
            x_axis,
            y_axis,
        )
        axes.set_stroke(GRAY_B, 1)
        circle = Circle(radius=2, color=BLUE)
        point_up = MathTex("(0,1)").scale(0.65).next_to(y_axis, LEFT).shift(2.25 * UP)
        point_down = MathTex("(0,-1)").scale(0.65).next_to(y_axis, LEFT).shift(2.25 * DOWN)
        point_left = MathTex("(-1,0)").scale(0.65).next_to(x_axis, DOWN).shift(2.45 * LEFT)
        point_right = MathTex("(1,0)").scale(0.65).next_to(x_axis, DOWN).shift(2.35 * RIGHT)
        points = VGroup(point_up, point_down, point_left, point_right)
        theta = ValueTracker(0)

        moving_dot = always_redraw(
            lambda: Dot(point=circle.point_at_angle(theta.get_value()))
        )
        x_line = always_redraw(lambda: Line(ORIGIN, moving_dot.get_center(), color=GOLD))

        def get_theta():
            theta_label = MathTex(r"\theta = " + f"{int(theta.get_value()*180/PI)}^\circ")
            theta_label[0][:1].set_color(GREEN)
            theta_label.to_edge(UP)
            return theta_label
        label = always_redraw(get_theta)
        angle_rotate = always_redraw(
            lambda: get_conditional_angle(Line(ORIGIN, RIGHT), Line(ORIGIN, moving_dot.get_center()), radius=0.6)
        )
        theta_rotate = always_redraw(
            lambda: MathTex(r"\theta", color=GREEN).move_to(
                get_conditional_angle(Line(ORIGIN, RIGHT), Line(ORIGIN, moving_dot.get_center()), 
                                           radius=0.6 + 3 * SMALL_BUFF
                ).point_from_proportion(0.5))
            )

        def get_tan_dot():
            tan = moving_dot.get_y()/moving_dot.get_x()
            x = 2
            y = tan * 2
            return Dot(point=np.array([x,y,0]))
        tan_dot = always_redraw(get_tan_dot)

        def get_dashed_line():
            y = tan_dot.get_y()
            if y >= config.frame_height:
                return VGroup()
            else:
                return DashedLine((ORIGIN), tan_dot.get_center())
        dashed_line = always_redraw(get_dashed_line)
        
        def get_tangent():
            tan = moving_dot.get_y()/moving_dot.get_x()
            x = 2
            y = tan * 2
            return Line(np.array([x,y,0]), np.array([x,0,0]), color=GREEN, stroke_width=2 )
        tangent = always_redraw(get_tangent)
        def get_tan_text():
            tan_text = MathTex(r"\tan\theta").scale(0.65).next_to(tangent, RIGHT)
            tan_text[0][3:4].set_color(GREEN)
            return tan_text
        tan_text = always_redraw(get_tan_text)

        self.play(Create(axes), FadeIn(points), Create(circle))
        self.add(moving_dot, x_line, label, angle_rotate, theta_rotate, tangent, tan_dot, dashed_line, tan_text)

        self.play(theta.animate.set_value(3*PI/2), run_time=24, rate_func=linear)

class SineCurveUnitCircle(Scene):
    def construct(self):
        self.add_sound("voiceovers/Scene8_SineWave.mp3")
        title = Text("Sóng hình sin", gradient=(RED, BLUE, GREEN), font="Noto Sans").scale(0.8).to_edge(UP)
        self.play(Write(title))
        self.show_axis()
        self.show_circle()
        self.move_dot_and_draw_curve()
        self.wait()

    def show_axis(self):
        x_start_circle = np.array([-5.5,0,0])
        x_end_circle = np.array([-2.5,0,0])
        x_start_curve = np.array([-2,0,0])
        x_end_curve = np.array([6,0,0])

        y_start_circle = np.array([-4,-1.5,0])
        y_end_circle = np.array([-4,1.5,0])
        y_start_curve = np.array([-2,-1.5,0])
        y_end_curve = np.array([-2,1.5,0])
        negative_one_start = np.array([-2.1,-1,0])
        negative_one_end = np.array([-1.9,-1,0])
        negative_one = Line(negative_one_start, negative_one_end).set_stroke(WHITE, 1)
        negative_one_label = MathTex("-1").next_to(negative_one, LEFT)
        positive_one_start = np.array([-2.1,1,0])
        positive_one_end = np.array([-1.9,1,0])
        positive_one = Line(positive_one_start, positive_one_end).set_stroke(WHITE, 1)
        positive_one_label = MathTex("1").next_to(positive_one, LEFT)

        x_axis_circle = Line(x_start_circle, x_end_circle).set_stroke(WHITE, 1)
        x_axis_curve = Line(x_start_curve, x_end_curve).set_stroke(WHITE, 1)
        y_axis_circle = Line(y_start_circle, y_end_circle).set_stroke(WHITE, 1)
        y_axis_curve = Line(y_start_curve, y_end_curve).set_stroke(WHITE, 1)

        self.add(x_axis_circle, y_axis_circle, y_axis_curve, x_axis_curve, negative_one, 
                 positive_one, positive_one_label, negative_one_label)
        self.add_x_labels()

        self.origin_point = np.array([-4,0,0])
        self.curve_start = np.array([-2,0,0])

    def add_x_labels(self):
        x_labels = [
            MathTex(r"\pi"), MathTex(r"2 \pi"),
            MathTex(r"3 \pi"), MathTex(r"4 \pi"),
        ]

        for i in range(len(x_labels)):
            x_labels[i].next_to(np.array([2*i, 0, 0]), DOWN)
            tip = Line(np.array([2*i, -0.1, 0]), np.array([2*i, 0.1, 0])).set_stroke(WHITE, 1)
            self.add(x_labels[i], tip)

    def show_circle(self):
        circle = Circle(radius=1).set_stroke(BLUE, 2)
        circle.move_to(self.origin_point)
        self.add(circle)
        self.circle = circle

    def move_dot_and_draw_curve(self):
        orbit = self.circle
        origin_point = self.origin_point

        dot = Dot(radius=0.08)
        dot.move_to(orbit.point_from_proportion(0))
        
        self.t_offset = 0
        rate = 0.125

        def get_theta():
            theta_label = MathTex(r"\theta = " + f"{int((self.t_offset * 2)*180)}^\circ")
            theta_label[0][:1].set_color(GREEN)
            theta_label.move_to(np.array([-4,2,0]))
            return theta_label
        label = always_redraw(get_theta)
        function_label = MathTex(r"\sin\theta")
        function_label[0][3:4].set_color(GREEN)
        function_label.move_to(np.array([1,2,0]))
        def go_around_circle(mob, dt):
            self.t_offset += (dt * rate)
            mob.move_to(orbit.point_from_proportion(self.t_offset % 1))

        def get_line_to_circle():
            return Line(origin_point, dot.get_center(), color=YELLOW)

        def get_line_to_curve():
            x = self.curve_start[0] + self.t_offset * 4
            y = dot.get_center()[1]
            return DashedLine(dot.get_center(), np.array([x,y,0]), stroke_width=2 )
        def get_vertical_line_circle():
            x = dot.get_center()[0]
            y = 0
            return Line(dot.get_center(), np.array([x,y,0]), color=RED, stroke_width=2 )
        def get_vertical_line_curve():
            x = self.curve_start[0] + self.t_offset * 4
            y = dot.get_center()[1]
            return Line(np.array([x,y,0]), np.array([x,0,0]), stroke_width=2 )

        self.curve = VGroup()
        self.curve.add(Line(self.curve_start,self.curve_start))
        def get_curve():
            last_line = self.curve[-1]
            x = self.curve_start[0] + self.t_offset * 4
            y = dot.get_center()[1]
            new_line = Line(last_line.get_end(),np.array([x,y,0]), color=RED)
            self.curve.add(new_line)

            return self.curve

        dot.add_updater(go_around_circle)

        origin_to_circle_line = always_redraw(get_line_to_circle)
        dot_to_curve_line = always_redraw(get_line_to_curve)
        sine_curve_line = always_redraw(get_curve)
        vertical_line_circle = always_redraw(get_vertical_line_circle)
        vertical_line_curve = always_redraw(get_vertical_line_curve)

        self.add(dot, label, function_label)
        self.add(orbit, origin_to_circle_line, dot_to_curve_line, sine_curve_line, vertical_line_circle, vertical_line_curve)
        self.wait(17)

        dot.remove_updater(go_around_circle)

class Scene8_SineWave(Scene):
    def construct(self):
        circle = Circle(radius=1.5).shift(LEFT*3)
        dot = Dot(circle.point_at_angle(0))

        graph_ax = Axes(
            x_range=[0, 2*PI, PI/2],
            y_range=[-1.5, 1.5, 1],
            x_length=6,
            tips=False
        ).shift(RIGHT*2)

        sine_graph = graph_ax.plot(lambda x: np.sin(x), color=YELLOW)

        self.play(Create(circle), FadeIn(dot))
        self.play(Create(graph_ax), run_time=1.2)
        self.play(Create(sine_graph), run_time=2)
        self.wait(1)
class Scene9_Tangent(Scene):
    def construct(self):
        alpha = ValueTracker(0)
        axes = VGroup(
            Line(2.25 * LEFT, 2.25 * RIGHT),
            Line(2.25 * DOWN, 2.25 * UP),
        )
        axes.set_stroke(GRAY_B, 1)
        circle = Circle(radius=2)
        tan_ratio = MathTex(r"\tan\theta = \frac{\sin\theta}{\cos\theta}").next_to(circle, RIGHT)
        tan_theta = tan_ratio[0][3:4]
        tan_theta.set_color(GREEN)
        tan_opp = tan_ratio[0][5:6]
        tan_adj = tan_ratio[0][-1:]
        tan_opp.set_color(RED)
        tan_adj.set_color(BLUE)
        self.play(Write(tan_ratio))
        tangent = always_redraw(
            lambda: TangentLine(
                circle,
                alpha=alpha.get_value(),
                color=GREEN,
                length=4
            )
        )

        self.play(Create(circle))
        self.play(Create(tangent))
        self.play(alpha.animate.set_value(1), rate_func=linear, run_time=5) 
        self.wait()
class Scene10_Inverse(Scene):
    def construct(self):
        label = MathTex(r"\arcsin(0.7) = \theta")

        self.play(Write(label))
        self.wait()
class Scene11_Summary(Scene):
    def construct(self):
        title = Text("Tóm lại", gradient=(RED, BLUE, GREEN), font="Noto Sans")
        self.play(Write(title))
        self.add_sound("voiceovers/Scene11_Summary.mp3")
        self.play(FadeOut(title)) 
        txt = VGroup(
            Text("Hình tam giác", font="Noto Sans", color=YELLOW),
            Text("Vòng tròn đơn vị", font="Noto Sans", color=YELLOW),
            Text("Sóng", font="Noto Sans", color=YELLOW),
        ).arrange(DOWN, buff=0.5)

        # self.play(LaggedStart(*[FadeIn(t, shift=UP) for t in txt], lag_ratio=1.5))
        self.play(FadeIn(txt[0], shift=UP))
        self.wait()
        self.play(FadeIn(txt[1], shift=UP))
        self.wait(2)
        self.play(FadeIn(txt[2], shift=UP))
        self.wait()
        
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
        self.wait(13)
        self.add_sound("voiceovers/thank.mp3")
        self.wait(2)

class TrigThumbnail(Scene):
    def construct(self):
        title = Text(
            "Lượng giác",
            font="Montserrat",
            weight=BOLD,
        ).scale(2.2).to_corner(UL)
        subtitle = Text(
            "Trực quan",
            font="Montserrat",
            weight=SEMIBOLD,
        ).scale(1.1).next_to(title, DOWN, buff=0.3).set_color_by_gradient(BLUE, GREEN, YELLOW, RED)
        
        axes = Axes(
            x_range=[-10, 10.3, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=10,
            y_length=5,
            axis_config={"color": GREEN},
            x_axis_config={
                "numbers_to_include": np.arange(-10, 10.01, 2),
                "numbers_with_elongated_ticks": np.arange(-10, 10.01, 2),
            },
            tips=False,
        )
        axes.to_edge(DOWN)
        axes_labels = axes.get_axis_labels()
        sin_graph = axes.plot(lambda x: np.sin(x), color=BLUE)
        cos_graph = axes.plot(lambda x: np.cos(x), color=RED)

        sin_label = axes.get_graph_label(
            sin_graph, "\\sin(x)", x_val=-10, direction=UP / 2
        )
        cos_label = axes.get_graph_label(cos_graph, label="\\cos(x)")

        vert_line = axes.get_vertical_line(
            axes.i2gp(TAU, cos_graph), color=YELLOW, line_func=Line
        )
        line_label = axes.get_graph_label(
            cos_graph, r"x=2\pi", x_val=TAU, direction=UR, color=WHITE
        )

        plot = VGroup(axes, sin_graph, cos_graph, vert_line)
        labels = VGroup(axes_labels, sin_label, cos_label, line_label)
        self.add(title, subtitle, plot, labels)

class ThumbnailScene(Scene):
    def construct(self):
        # Background
        bg = Rectangle(width=config.frame_width, height=config.frame_height, fill_color=BLUE_D, fill_opacity=1, stroke_opacity=0)
        self.add(bg)

        # Left column: Unit circle with projections
        circle_radius = 1.4
        circle = Circle(radius=circle_radius).move_to(LEFT * 3)
        circle.set_stroke(WHITE, 6)

        # Moving point on circle (static for thumbnail)
        angle = 40 * DEGREES
        pt = Dot(circle.point_at_angle(angle), radius=0.11)
        pt.set_fill(YELLOW)

        # Projections
        proj_x = Line(pt.get_center(), np.array([pt.get_center()[0], 0, 0]))
        proj_y = Line(pt.get_center(), np.array([0, pt.get_center()[1], 0]))

        proj_x.set_stroke("#4EA8DE", 6)
        proj_y.set_stroke("#FF7A7A", 6)

        # Small labels for sin/cos
        cos_label = MathTex("\cos\theta").scale(0.6).next_to(proj_x, DOWN, buff=0.05)
        sin_label = MathTex("\sin\theta").scale(0.6).next_to(proj_y, LEFT, buff=0.05)

        # Right column: Sine wave strip
        axes = Axes(x_range=[0, 4 * PI, PI], y_range=[-1.5, 1.5, 1], x_length=7)
        axes.to_edge(RIGHT, buff=1.0)
        axes.shift(UP * 0.3)
        axes.set_stroke(WHITE, 1.5)

        sine = axes.plot(lambda x: np.sin(x), x_range=[0, 4 * PI])
        sine.set_stroke(YELLOW, 6)

        # Visual connector: dotted line from circle to sine
        connector = DashedLine(start=circle.get_right() + RIGHT * 0.1, end=axes.get_left() + LEFT * 0.4)
        connector.set_stroke(WHITE, 2, opacity=0.6)

        # Big text (title)
        title_main = Text("TRIG", font_size=120, weight=BOLD)
        title_sub = Text("in 10 MIN", font_size=42)
        title = VGroup(title_main, title_sub).arrange(DOWN, center=False, aligned_edge=LEFT)
        title.to_corner(UR).shift(LEFT * 0.5 + DOWN * 0.5)
        title_main.set_color(WHITE)
        title_sub.set_color(YELLOW)

        # Small triangle with labels (bottom-left)
        A = LEFT * 3 + DOWN * 2.0
        B = A + RIGHT * 1.6
        C = A + RIGHT * 0.6 + UP * 1.2
        tri = Polygon(A, B, C)
        tri.set_stroke(WHITE, 3)
        opp = MathTex("Opp").scale(0.6).move_to((A + C) / 2 + LEFT * 0.1)
        adj = MathTex("Adj").scale(0.6).move_to((A + B) / 2 + DOWN * 0.1)
        hyp = MathTex("Hyp").scale(0.6).move_to((B + C) / 2 + RIGHT * 0.1)

        # Angle marker for triangle
        ang = Angle(Line(A, B), Line(A, C), radius=0.25)
        ang.set_color(YELLOW)
        ang_label = MathTex(r"\theta").scale(0.6).next_to(ang, LEFT, buff=0.05)

        # Composition order
        self.add(circle)
        self.add(pt)
        self.add(proj_x, proj_y)
        self.add(cos_label, sin_label)
        self.add(connector)
        self.add(axes, sine)
        self.add(title)
        self.add(tri, opp, adj, hyp, ang, ang_label)

        # Optional subtle vignette (fade corners)
        vignette = self._make_vignette()
        self.add(vignette)

    def _make_vignette(self):
        # A subtle dark overlay to focus center
        vignette = VGroup()
        for corner in [UL, UR, DL, DR]:
            quad = Polygon(
                corner * np.array([config.frame_width / 2, config.frame_height / 2, 0]),
                corner * np.array([config.frame_width / 2, config.frame_height / 4, 0]),
                ORIGIN,
                corner * np.array([config.frame_width / 4, config.frame_height / 2, 0])
            )
            quad.set_fill(BLACK, opacity=0.06)
            quad.set_stroke(opacity=0)
            quad.shift(-corner * 0.0)
            vignette.add(quad)
        return vignette
