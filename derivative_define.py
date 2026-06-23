from manim import *
from pi_creature_scene import *

class FathersOfCalculus(PiCreatureScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.names = [
            ("assets/Newton.png", "Newton"),
            ("assets/Bolt.png", "Bolt"), 
            ("assets/Leibniz.png", "Leibniz"),
        ]
        self.picture_height = 2.5
    def construct(self):
        self.add_sound("voiceovers/bolt.mp3")
        men = Mobject()
        for name, title in self.names:
            image = ImageMobject(name)
            image.set_height(self.picture_height)
            title = Text(title).scale(0.6).next_to(image, DOWN)
            image.add(title)
            men.add(image)
        row_1 = Group(men[0], men[2]).arrange(RIGHT, aligned_edge = UP)
        Group(row_1, men[1]).arrange(DOWN).shift(0.7*DOWN)
        instant_rate_of_change = Text("Tốc độ thay đổi tức thời", font="Noto Sans").scale(0.65)
        instant_rate_of_change.to_edge(UP)
        instant_rate_of_change[5:12].set_color_by_gradient(BLUE, RED_D)
        cup =  self.pi_creatures[0]
        common = MathTex("???")
        common.next_to(cup, UP)
        newton = men[0]
        bolt = men[1]
        leibniz = men[2]
        self.play(FadeIn(newton))
        self.play(cup.animate.look_at(newton))
        self.wait(2.5)
        self.play(FadeIn(leibniz))
        self.wait(9.5)
        self.play(FadeIn(bolt))
        self.play(cup.animate.look_at(bolt))
        self.play(cup.animate.change_mode("thinking"))
        self.wait(10)
        self.play(cup.animate.change_mode("confused"))
        self.play(
            Write(common, run_time = 1)
        )
        self.wait(4)
        self.play(FadeOut(common), Write(instant_rate_of_change, run_time = 1))
        self.play(cup.animate.look_at(instant_rate_of_change))
        self.play(cup.animate.change_mode("surprised"))
        self.wait(1)
        self.play(FocusOn(bolt))
        self.wait(5)
        self.play(Indicate(instant_rate_of_change))
        self.play(cup.animate.change_mode("hooray"))
        self.wait()
  
class IntroduceGraph(PiCreatureScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_time = 6.5
        self.end_time = 3
        self.dt = 1.0
    def construct(self):
        super().construct()
        cup =  self.pi_creatures[0]
        cup.to_corner(DR)
        cup.look(DL)
        self.add_sound("voiceovers/define_dev.mp3")
        axes = Axes(
            x_range=(0, 10), y_range=(0, 100, 10), x_length=6, y_length=6, tips=False
        ).to_edge(LEFT, buff=1)
        graph = self.graph_sigmoid_trajectory_function(axes)
        origin = axes.coords_to_point(0, 0)        
        y_label = axes.get_y_axis_label(
            Text("Quãng đường (mét)", font="Noto Sans").scale(0.65),buff=0.3,
        )
        x_label = axes.get_x_axis_label(Text("Thời gian (giây)", font="Noto Sans").scale(0.65), edge=DOWN, direction=DOWN, buff=0.3)
        
        self.play(Create(axes, run_time=2))
        self.play(Write(y_label, run_time=1))
        self.play(Write(x_label, run_time=1))
        self.wait(5)
        
        self.calculate_velocity(axes, graph, origin)
        self.wait()

    def calculate_velocity(self, axes, graph, origin, **kwargs):
        d_label = Tex("100").next_to(axes.c2p(0, 100), LEFT, buff=0.2).set_color(BLUE)
        t_label = Tex("9.58").next_to(axes.c2p(10, 0), DOWN, buff=0.2).set_color(YELLOW)
        origin_dot = Dot(axes.get_origin(), color=RED_D)
        end = Dot(graph.point_from_proportion(1), color=RED_D)
        d_line = axes.get_horizontal_line(graph.point_from_proportion(1))
        s_line = axes.get_vertical_line(graph.point_from_proportion(1))
        dashed_line = DashedLine(origin_dot, end, stroke_width = 2, color=RED_D)
        
        self.play(Create(origin_dot))
        self.add_sound("voiceovers/click.wav")
        self.wait(1)
        self.play(FocusOn(origin_dot))
        self.wait(2)
        self.play(Write(d_label, run_time=1), Write(t_label, run_time=1))
        self.wait(2)
        self.play(Create(end), Create(d_line), Create(s_line))
        self.add_sound("voiceovers/click.wav")
        self.wait(2)
        self.play(FocusOn(end))
        self.play(Wiggle(d_label))
        self.wait(3)
        velocity = MathTex(r"\text{v} \raisebox{-0.6em}{\text{tb}}")
        change_over_change = MathTex(r" &= \frac{\text{s}}{\text{t}}")
        formula = MathTex(r" &= \frac{\text{100}\text{ m}}{\text{9.58}\text{ s}}")
        
        approximate = MathTex(r"\approx 10.4 \frac{\text{m}}{\text{s}}")
        group = VGroup(velocity, change_over_change, formula, approximate)
        group.arrange(RIGHT)
        group.to_corner(UP + RIGHT)
        first_group = VGroup(velocity, change_over_change)
        self.play(FadeIn(first_group, lag_ratio=0.5, run_time=3))
        self.wait(3)
        
        self.play(Create(dashed_line))  
        self.add_sound("voiceovers/line.mp3")   
        
        self.wait(4)
        s = formula[0][1:4]
        t = formula[0][6:10]
        s.set_color(BLUE)
        t.set_color(YELLOW)
        s.target, t.target = d_label, t_label
        for mob in s, t:
            mob.save_state()
            mob.move_to(mob.target)
        self.play(FadeIn(formula),
            *[mob.animate.restore() for mob in (s, t)]
        )
        
        self.wait(7)
        
        self.play(Write(approximate))  
        self.wait(13)
        s_of_t = Tex("s(t)")
        s_of_t.next_to(
            graph.point_from_proportion(0.9), 
            UP,
            buff = SMALL_BUFF
        )
        
        self.play(Create(graph, run_time=3), Write(s_of_t))
        self.wait()
        self.play(FadeOut(dashed_line))

        self.wait(4)
        self.comment_on_slope(axes, origin)
        self.play(Circumscribe(group, fade_out=True))
        self.wait(3)
        self.play(group.animate.set_opacity(0.6))
        
        self.wait(7)
        self.show_two_times_on_distance(axes, graph)

    def graph_sigmoid_trajectory_function(self, axes, **kwargs):
        func = lambda x: 100*smooth(x/10)
        graph = axes.plot(func, color=BLUE)
        self.s_graph = graph
        return graph
        
    def comment_on_slope(self, axes, origin):
        delta_t = 1
        curr_time = 0
        ghost_line = Line(
            origin, 
            axes.coords_to_point(delta_t, 100)
        )
        rect = Rectangle().replace(ghost_line, stretch = True)
        rect.set_stroke(width = 0)
        rect.set_fill(YELLOW, opacity = 0.3)

        change_lines = self.get_change_lines(axes, curr_time, delta_t)
        self.play(FadeIn(rect))
        self.wait()
        self.play(Write(change_lines))
        self.wait()
        for x in range(1, 10):
            self.add_sound("voiceovers/slidecard03.wav")
            curr_time = x
            new_change_lines = self.get_change_lines(axes, curr_time, delta_t)
            self.play(
                rect.animate.move_to(axes.coords_to_point(curr_time, 0), DOWN+LEFT),
                Transform(change_lines, new_change_lines)
            )
            self.wait()
        self.play(*list(map(FadeOut, [rect, change_lines])))
        self.rect = rect

    def get_change_lines(self, axes, curr_time, delta_t = 1):
        p1 = axes.input_to_graph_point(
            curr_time, self.s_graph
        )
        p2 = axes.input_to_graph_point(
            curr_time+delta_t, self.s_graph
        )
        interim_point = p2[0]*RIGHT + p1[1]*UP
        delta_t_line = Line(p1, interim_point, color = YELLOW)
        delta_s_line = Line(interim_point, p2, color = BLUE)
        brace = Brace(delta_s_line, RIGHT, buff = SMALL_BUFF)
        return VGroup(delta_t_line, delta_s_line, brace)

    def show_two_times_on_distance(self, axes, graph, **kwargs):
        point = Dot(graph.point_from_proportion(0.5), color=RED_D)
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(point))
        self.wait()
        
        dtTracker = ValueTracker(1.0)
        p1 = always_redraw(lambda: Dot().move_to(axes.input_to_graph_point(5, graph)).set_opacity(0))
        p2 = always_redraw(lambda: Dot().move_to(axes.input_to_graph_point(5+dtTracker.get_value(), graph))
                           .set_opacity(0))
        interim_point = always_redraw(
            lambda: Dot().move_to(axes.input_to_graph_point(5+dtTracker.get_value(), graph)[0] * RIGHT + axes.input_to_graph_point(5, graph)[1] * UP)
            .set_opacity(0)
        )
        self.add(p1, p2, interim_point)
        dt_line = always_redraw(lambda: Line(p1.get_center(), interim_point.get_center(), color = YELLOW))
        ds_line = always_redraw(lambda: Line(interim_point.get_center(), p2.get_center(), color = BLUE))
        dt_brace = always_redraw(lambda: Brace(dt_line, DOWN, buff = SMALL_BUFF))
        ds_brace = always_redraw(lambda: Brace(ds_line, RIGHT, buff = SMALL_BUFF))
        dt_text = always_redraw(lambda: Tex(r"dt").next_to(dt_brace, DOWN, buff = SMALL_BUFF))
        ds_text = always_redraw(lambda: Tex(r"ds").next_to(ds_brace, RIGHT, buff = SMALL_BUFF))
        def get_secant_line(p1, p2):
            secant_line = Line(p1.get_center(), p2.get_center())
            secant_line.set_color(RED_D)
            secant_line.scale(
                4/secant_line.get_length()
            )
            return secant_line
        secant_line = always_redraw(lambda: get_secant_line(p1, p2))

        for line, brace, derivative in (dt_line, dt_brace, dt_text), (ds_line, ds_brace, ds_text):
            brace.set_color(line.get_color())
            derivative.set_color(line.get_color())
            derivative.add_background_rectangle()
            self.play(
                Create(line),
                GrowFromCenter(brace),
                Write(derivative)
            )
            self.wait()
        self.play(
                Create(secant_line)
            )
        
        change_over_time = MathTex(r"\frac{ds}{dt}(t)=")
        
        ds_over_dt = MathTex(r"\frac{s(t+dt)-s(t)}{dt}")
        ds_over_dt[0][4:6].set_color(YELLOW)
        ds_over_dt[0][-2:].set_color(YELLOW)

        define_derivative = VGroup(change_over_time, ds_over_dt).arrange(RIGHT)
        define_derivative.shift(UP+ 3*RIGHT)
        ds = change_over_time[0][0:2]
        ds.set_color(BLUE)
        dt = change_over_time[0][3:5]
        dt.set_color(YELLOW)
        ds.target, dt.target = ds_text, dt_text
        for mob in ds, dt:
            mob.save_state()
            mob.move_to(mob.target)
        self.play(
            FadeIn(define_derivative),
            *[mob.animate.restore() for mob in (ds, dt)]
        )

        self.wait(4)
        self.play(Indicate(graph))
        self.wait()
        self.play(Wiggle(dt_text))
        
        self.wait(2)
        self.play(Circumscribe(define_derivative, fade_out=True))
        self.play(
            dtTracker.animate.set_value(0.01), run_time=5, rate_func=linear
        )
        self.play(FocusOn(point))
        self.wait(2)
        self.play(Indicate(secant_line))
        self.wait(6)
        angle = secant_line.get_angle()
        derivative = Text("Đạo hàm", font="Noto Sans").scale(0.7)
        derivative.set_color_by_gradient(BLUE, RED_D).rotate(angle)
        derivative.next_to(point, LEFT+UP, buff=1) 
        arrow = CurvedArrow(
            start_point=derivative.get_right(),   
            end_point=point.get_center(),
            radius= 8                 
        )
        self.add_sound("voiceovers/bubble-button.wav")
        self.play(Write(derivative), Create(arrow))
        self.wait(2)
        self.play(Indicate(derivative))
        self.wait(2)
        self.add_sound("voiceovers/error.wav")
        self.play(Circumscribe(ds_over_dt[0][-2:], fade_out=True))
        self.wait(4)
        brace = Brace(ds_over_dt, DOWN, buff = SMALL_BUFF)
        dt_to_zero = brace.get_text("$dt \\to 0$")
        VGroup(*dt_to_zero[0][:2]).set_color(YELLOW)
        self.play(Create(brace), Write(dt_to_zero))
        self.wait()
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob is not derivative]
        )
        self.wait()
        definition_title = Text("Định nghĩa đạo hàm", font="Noto Sans").scale(0.7)
        definition_text = definition_title[0:9]
        definition_title.to_edge(UP)
        deri_text = definition_title[9:]
        self.play(Write(definition_text), derivative.animate.rotate(-angle).move_to(deri_text))
        self.add_sound("voiceovers/dev_define.mp3")
        self.wait()
        definition = MathTex(
            r"f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}"
        ).scale(1.4)

        self.play(Write(definition))
        self.wait()
        self.add_sound("voiceovers/dev_formula.mp3")
        self.play(Indicate(definition[0][:5]))
        self.wait()
        self.play(Indicate(definition[0][6:12]))
        self.wait()
        self.play(Indicate(definition[0][12:18]))
        self.wait()
        self.play(Indicate(definition[0][19:23]))
        self.play(Indicate(definition[0][24:]))
        self.wait()

class RefreshOnDerivativeDefinition(Scene):
    start_x = 2
    start_dx = 0.7
    df_color = YELLOW
    dx_color = GREEN
    secant_line_color = MAROON_B

    def construct(self):
        axes = Axes(
            x_range=[-1, 10, 1],
            y_range=[-1, 10, 1],
            x_length=8,
            y_length=6,
            tips=False
        ).to_edge(LEFT)
        self.add(axes)

        def func(x):
            u = 0.3 * x - 1.5
            return -(u ** 3) + 5 * u + 7

        graph = axes.plot(func, color=BLUE)
        graph_label = axes.get_graph_label(graph, label="f(x)")
        labels = axes.get_axis_labels(x_label="x", y_label="y")
        self.play(Create(graph), Write(graph_label), Write(labels))
        derivative = MathTex(
            r"\frac{df}{dx}(", str(self.start_x), ")"
        )
        derivative.set_color_by_tex("df", self.df_color)
        derivative.set_color_by_tex("dx", self.dx_color)
        derivative.set_color_by_tex(str(self.start_x), RED)
        derivative.move_to(axes.coords_to_point(7, 4))

        self.play(Write(derivative))
        self.wait()

        x0 = self.start_x
        dx0 = self.start_dx

        def vline_at(x):
            return DashedLine(
                axes.c2p(x, 0),
                axes.c2p(x, func(x)),
                color=RED
            )

        start_x_v_line = vline_at(x0)
        nudged_x_v_line = vline_at(x0 + dx0)
        self.play(Create(start_x_v_line))

        dx_tracker = ValueTracker(dx0)

        def secant_x2():
            return x0 + dx_tracker.get_value()

        def secant_y2():
            return func(secant_x2())

        dx_line = always_redraw(
            lambda: Line(
                axes.c2p(x0, func(x0)),
                axes.c2p(secant_x2(), func(x0)),
                color=self.dx_color
            )
        )
        dx_label = always_redraw(
            lambda: MathTex("dx", color=self.dx_color)
                .next_to(dx_line, DOWN, buff=0.15)
        )

        df_line = always_redraw(
            lambda: Line(
                axes.c2p(secant_x2(), func(x0)),
                axes.c2p(secant_x2(), secant_y2()),
                color=self.df_color
            )
        )
        df_label = always_redraw(
            lambda: MathTex("df", color=self.df_color)
                .next_to(df_line, RIGHT, buff=0.15)
        )

        secant_line = always_redraw(
            lambda: axes.get_secant_slope_group(
                x=x0, graph=graph, dx=dx_tracker.get_value(), secant_line_length=4, 
                secant_line_color=self.secant_line_color
            )
        )

        self.play(Create(dx_line), Write(dx_label))
        self.wait()
        self.play(Create(df_line), Write(df_label))
        self.wait()
        self.play(Create(secant_line))
        self.wait()

        brace = Brace(derivative)
        dx_to_0 = MathTex("dx", r"\to 0", color=self.dx_color)
        dx_to_0.next_to(brace, DOWN)

        self.play(GrowFromCenter(brace), Write(dx_to_0))
        self.play(dx_tracker.animate.set_value(0.01), run_time=5)
        self.wait()

        new_deriv = MathTex(
            r"{f(", str(x0), "+", "dx", ")-f(", str(x0), ")\over dx}"
        )
        new_deriv.set_color_by_tex("dx", self.dx_color)
        new_deriv.set_color_by_tex("f", self.df_color)
        new_deriv.set_color_by_tex(str(x0), RED)
        new_deriv.move_to(derivative)

        new_brace = Brace(new_deriv, DOWN)

        self.play(
            ReplacementTransform(derivative, new_deriv),
            ReplacementTransform(brace, new_brace),
            dx_to_0.animate.next_to(new_brace, DOWN)
        )
        self.wait()

        lim = MathTex(r"\lim").scale(1.3)
        dx0_target = dx_to_0.copy().scale(0.7)
        dx0_target.next_to(lim, DOWN, buff=SMALL_BUFF)
        lim_group = VGroup(lim, dx0_target).move_to(new_deriv, LEFT)

        self.play(
            ReplacementTransform(new_brace, lim),
            Transform(dx_to_0, dx0_target),
            new_deriv.animate.next_to(lim_group, RIGHT),
            run_time=2
        )

        # pulse
        self.play(lim.animate.scale(1.2).set_color(YELLOW))
        self.play(lim.animate.scale(1/1.2).set_color(WHITE))

        self.wait(2)

        self.play(
            dx_tracker.animate.set_value(dx0),
            Transform(nudged_x_v_line, start_x_v_line),
            run_time=5
        )
        self.wait()

