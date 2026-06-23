from manim import *
from pi_creature_scene import *

def get_line_chart(color=BLUE):
    axes = VGroup(
            Line(0.25 * LEFT, 4 * RIGHT),
            Line(0.25 * DOWN, 3 * UP),
        )
    axes.set_stroke(GRAY_B, 2)

    times = np.arange(0, 4.25, 0.25)
    prices = [
        0.1, 0.5, 1.75, 1.5,
        2.75, 2.2, 1.3, 0.8,
        1.1, 1.3, 1.2, 1.4,
        1.5, 1.7, 1.2, 1.3,
    ]
    graph = VMobject()
    graph.set_points_as_corners([
        time * RIGHT + price * UP
        for time, price in zip(times, prices)
    ])
    graph.set_stroke(color, width=4)

    return VGroup(axes, graph)
    
class DerivativeThumbnail(Scene):
    def construct(self):
        title = Text(
            "Đạo hàm?",
            font="Montserrat",
            weight=BOLD,
        ).scale(2.2).to_edge(UP)
        subtitle = Text(
            "Tỷ lệ thay đổi",
            font="Montserrat",
            weight=SEMIBOLD,
        ).scale(1.1).next_to(title, DOWN, buff=0.3).set_color_by_gradient(BLUE, GREEN, YELLOW, RED)
        
        line_chart = get_line_chart()
        line_chart.to_corner(UR)
        rocket = SVGMobject("assets/rocket.svg").to_corner(UL)
        small = PiCreature().scale(0.2).set_color(BLUE)
        small.change_mode("confused")
        medium = PiCreature().scale(0.4).set_color(GREEN)
        medium.change_mode("thinking")
        normal = PiCreature().scale(0.7).set_color(YELLOW)
        normal.change_mode("happy")
        large = PiCreature().scale(1.2).set_color(RED)
        large.change_mode("hooray")
        cups= VGroup(small, medium, normal, large).arrange(RIGHT).to_edge(DOWN)
        self.add(title, subtitle, line_chart, rocket, cups)

class DerivativeThumbnail1(Scene):
    def construct(self):
        # Colors optimized for thumbnails
        BG = "#0E0E0E"
        CURVE_COLOR = YELLOW
        TANGENT_COLOR = BLUE_B
        DOT_COLOR = RED
        TEXT_COLOR = WHITE

        self.camera.background_color = BG

        # Axes (thicker for visibility, no numbers for simplicity)
        ax = Axes(
            x_range=[-3, 5],
            y_range=[-1, 8],
            x_length=12,
            y_length=6,
            axis_config={"stroke_width": 4, "color": GRAY_E},
        ).move_to(DOWN * 0.5)
        self.add(ax)
        
        # Function
        curve = ax.plot(lambda x: 0.3 * (x - 1) ** 2 + 1, color=CURVE_COLOR, stroke_width=10)
        self.add(curve)

        # Focus point for derivative visualization
        focus_x = 2.0
        focus_point = ax.c2p(focus_x, 0.3 * (focus_x - 1) ** 2 + 1)

        dot = Dot(point=focus_point, radius=0.18, color=DOT_COLOR)
        self.add(dot)

        # Tangent line at focus point
        # TangentLine(
        #         graph,
        #         alpha=alpha.get_value(),
        #         color=GREEN,
        #         length=4
        #     )
        tangent = ax.get_secant_slope_group(
                x=focus_x, graph=curve, dx=0.01
                ).set_color(TANGENT_COLOR).set_stroke(width=12)
        # tangent = ax.get_tangent_line(
        #     x=focus_x,
        #     graph=curve,
        #     length=7,
        # ).set_color(TANGENT_COLOR).set_stroke(width=12)
        self.add(tangent)

        # Big thumbnail title
        title = Text(
            "Derivative?",
            font="Montserrat",
            weight=BOLD,
            color=TEXT_COLOR
        ).scale(2.2).to_edge(UP)
        self.add(title)

        # Sub-text (optional, strong callout)
        subtitle = Text(
            "Rate of Change",
            font="Montserrat",
            weight=SEMIBOLD,
            color=BLUE_B
        ).scale(1.1).next_to(title, DOWN, buff=0.3)
        self.add(subtitle)

        # Slight glow/highlight around derivative visuals
        glow = Circle(radius=1.6, color=DOT_COLOR).move_to(dot.get_center())
        glow.set_stroke(width=12, opacity=0.35)
        self.add(glow)

        # Freeze so last frame is used for thumbnail screenshot
        self.wait()


class IdeaOfChange(PiCreatureScene):
    def construct(self):
        self.add_sound("voiceovers/IdeaOfChange.mp3")
        cup =  self.pi_creatures[0]
        self.play(cup.animate.change_mode("thinking"))
        line_chart = get_line_chart()
        line_chart.to_corner(DR)
        car = SVGMobject("assets/car.svg").scale(0.5).shift(LEFT*3)
        balloon = SVGMobject("assets/balloon.svg", fill_color=PURPLE_D, fill_opacity=0.5)
        car.scale(1.5).to_edge(LEFT).shift(2*UP)
        balloon.shift(2*UP+4*RIGHT)
        self.play(FadeIn(car), DrawBorderThenFill(balloon), run_time=0.5) 
        self.play(car.animate.shift(RIGHT*3), FadeToColor(cup, color=RED_D), balloon.animate.scale(1.6), Create(line_chart), run_time=5)       
        self.play(cup.animate.change_mode("conniving"))
        title = Text("Tốc độ thay đổi", font="Noto Sans")
        title[4:].set_color_by_gradient(BLUE, PURPLE_D)
        self.play(Write(title))
        self.wait()
        self.play(FadeOut(VGroup(car, line_chart, balloon, cup)))

class SlopeOfCurve(Scene):
    def construct(self):
        alpha = ValueTracker(0)
        ax = Axes(x_range=[-1, 5], y_range=[-1, 4], tips=False)
        func = lambda x: 0.35 * ((x - 2)**3 - 2 * (x - 2) + 6)
        graph = ax.plot(func, color=BLUE)
        dot = always_redraw(lambda: Dot(graph.point_from_proportion(alpha.get_value())))
        tangent = always_redraw(
            lambda: TangentLine(
                graph,
                alpha=alpha.get_value(),
                color=GREEN,
                length=4
            )
        )

        self.play(Create(ax), Create(graph))
        self.add(dot, tangent)
        slope_label = Text("Tốc độ thay đổi = Độ dốc", font="Noto Sans", color=YELLOW).scale(0.7).to_edge(UP)
        self.add_sound("voiceovers/SlopeOfCurve.mp3")
        self.play(Write(slope_label))
        self.play(alpha.animate.set_value(1), rate_func=linear, run_time=5)        
        self.wait()
class SecantToTangent(Scene):
    def construct(self):
        self.add_sound("voiceovers/SecantToTangent.mp3")
        ax = Axes(x_range=[-1, 5], y_range=[-1, 4], tips=False)
        func = lambda x: 0.35 * ((x - 2)**3 - 2 * (x - 2) + 6)
        # ax = Axes(x_range=[-2,3], y_range=[-1,5], tips=False)
        graph = ax.plot(func, color=BLUE)
        self.add(ax, graph)

        x_val = ValueTracker(2)
        def get_secant():
            secant = ax.get_secant_slope_group(
                x=2, graph=graph, dx=x_val.get_value()-1,
                dx_line_color=YELLOW, dy_line_color=BLUE,
                dx_label=MathTex(r"\Delta x"), dy_label=MathTex(r"\Delta y")
                )
            dx_label = secant[2]
            dx_label.next_to(secant[0], UP)
            return secant
        
        secant = always_redraw(lambda: get_secant())

        self.play(Create(secant))
        slope_text = Text("Độ dốc", font="Noto Sans").scale(0.7).to_edge(UP)
        arrow = MathTex(r"=").next_to(slope_text, RIGHT)
        formula = MathTex(r"\frac{\Delta y}{\Delta x}").next_to(arrow, RIGHT)
        delta_y = formula[0][:2]
        delta_x = formula[0][3:]
        delta_y.set_color(BLUE)
        delta_x.set_color(YELLOW)
        dy_label = secant[1]
        dx_label = secant[2]
        delta_y.target, delta_x.target = dy_label, dx_label
        for mob in delta_y, delta_x:
            mob.save_state()
            mob.move_to(mob.target)
        self.play(Write(VGroup(slope_text, arrow, formula)),
            *[mob.animate.restore() for mob in (delta_y, delta_x)]
        )

        self.play(x_val.animate.set_value(1.05), run_time=4)
        self.wait()        
        limit_text = Text("Khi Δx → 0, đường thẳng trở thành tiếp tuyến", font="Noto Sans").scale(0.65).next_to(formula, DOWN)
        limit_text[3:5].set_color(YELLOW)
        self.play(Write(limit_text))
        self.wait()
        self.add_sound("voiceovers/DerivativeSymbol.mp3")
        d_form = MathTex(r"\frac{dy}{dx}").next_to(arrow, RIGHT)
        d_form[0][:2].set_color(BLUE)
        d_form[0][3:].set_color(YELLOW)
        self.wait()
        self.play(TransformMatchingTex(formula, d_form))
        self.wait()
        glow = SurroundingRectangle(d_form, color=YELLOW, buff=0.2)
        self.play(Create(glow), d_form.animate.scale(1.1))
        self.wait(4)
        
class DerivativeSymbol(Scene):
    def construct(self):
        delta = MathTex(r"\frac{\Delta y}{\Delta x}", color=YELLOW).scale(1.5)
        self.play(Write(delta))
        self.wait(0.5)

        d_form = MathTex(r"\frac{dy}{dx}", color=BLUE).scale(1.5)
        self.play(TransformMatchingTex(delta, d_form))
        self.wait(1)

        glow = SurroundingRectangle(d_form, color=BLUE, buff=0.2)
        self.play(Create(glow), d_form.animate.scale(1.1))
        self.wait(1)
class DerivativeOfX2(Scene):
    def construct(self):
        self.add_sound("voiceovers/DerivativeOfX2.mp3")
        ax = Axes(x_range=[-3,3], y_range=[-1,5], tips=False)
        ax.add_coordinates().shift(0.5*DOWN)
        graph = ax.plot(lambda x: x**2, color=BLUE)
        label = ax.get_graph_label(
            graph=graph,
            label= MathTex(r"y=x^2"),
            x_val=-2,
            direction=UR,
        )
        self.add(ax, graph, label)
        x = ValueTracker(1)
        dot = always_redraw(lambda: Dot(ax.c2p(x.get_value(), x.get_value()**2), color=RED))
        line = always_redraw(lambda: ax.get_vertical_line(ax.c2p(x.get_value(), x.get_value()**2), line_config={"dashed_ratio": 0.85}))
        tangent = always_redraw(lambda: ax.get_secant_slope_group(x=x.get_value(), dx=0.001, graph=graph))
        slope_text = Text("Độ dốc", font="Noto Sans").scale(0.7).to_edge(UP)
        arrow = MathTex(r"=").next_to(slope_text, RIGHT)
        slope = always_redraw(lambda: MathTex(f"{2*x.get_value():.1f}").next_to(arrow, RIGHT))
        self.add(dot, tangent, slope_text, arrow, slope)
        self.wait(2)
        self.play(Indicate(label))
        self.wait(2)
        self.add(line)
        self.play(Circumscribe(slope, fade_out=True))
        self.play(x.animate.set_value(2), run_time=2)
        self.play(Circumscribe(slope, fade_out=True))
        self.wait()
class SpeedMeaning(Scene):
    def construct(self):
        ax = Axes(x_range=[0,5], y_range=[0,6], tips=False)
        graph = ax.plot(lambda t: 0.3*(t**3) - t**2 + 2, color=BLUE)
        self.add(ax, graph)

        car = SVGMobject("assets/car.svg").scale(0.5)
        t = ValueTracker(0.1)
        car.add_updater(lambda m: m.move_to(ax.c2p(t.get_value(), graph.underlying_function(t.get_value()))))

        speed_gauge = DecimalNumber(0, num_decimal_places=1, include_sign=False).to_corner(UR)
        speed_gauge.add_updater(lambda d: d.set_value(0.9*(3*t.get_value()**2 - 2*t.get_value())))

        self.add(car, speed_gauge)
        self.play(t.animate.set_value(4.5), run_time=5)
        self.wait(1)
class DerivativeEverywhere1(Scene):
    def construct(self):
        third_width = config.frame_width / 3
        graphs = VGroup(
            FunctionGraph(lambda x: 2*np.sin(x), x_range=[PI / 2, 3 * PI / 2], color=YELLOW),
            FunctionGraph(lambda x: np.exp(-0.1*x)*np.sin(3*x), x_range=[-3, 3], color=BLUE),
            FunctionGraph(lambda x: 0.3*x, x_range=[-3, 3], color=GREEN),
        ).arrange_in_grid(rows=1, cols=3, buff=1)
        for g in graphs:
            g.stretch_to_fit_width(third_width)

        labels = VGroup(
            Text("Temperature", font_size=28),
            Text("Sound", font_size=28),
            Text("Population", font_size=28)
        ).arrange_in_grid(rows=1, cols=3, buff=1).next_to(graphs, DOWN)

        self.play(LaggedStartMap(Create, graphs))
        self.play(FadeIn(labels))
        self.wait(1)

class DerivativeEverywhere(Scene):
    def construct(self):
        self.temperature_change()
        self.light_change()
        self.population_grow()
        self.sound_wave()
        rect = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color=BLACK,
            fill_opacity=0.8,
            stroke_width=0
        )
        self.play(FadeIn(rect))
        tit = Text("Đạo hàm = tốc độ thay đổi ở mọi nơi.", font="Noto Sans", color=YELLOW)
        self.play(Write(tit))
        self.wait()
        
    def temperature_change(self):
        self.add_sound("voiceovers/temperature.mp3")
        line_chart = get_line_chart(color=ORANGE)
        line_chart.to_corner(UL)
        axes = line_chart[0]
        graph = line_chart[1]
        self.play(Create(axes))
        self.wait()
        self.play(Create(graph), run_time=2)

    def light_change(self):
        buildings = VGroup(
            Rectangle(height=2, width=0.8),
            Rectangle(height=3, width=1),
            Rectangle(height=1.5, width=0.6),
            Rectangle(height=2.5, width=0.9),
            Rectangle(height=1.8, width=0.7)
        )

        buildings.arrange(RIGHT, buff=0.2)
        buildings.set_fill(BLACK, opacity=1)
        buildings.set_stroke(GRAY)

        buildings.to_corner(UR)
        lights = VGroup()
        for b in buildings:
            for r in range(3, int(b.height * 3) + 1):
                for c in range(1, int(b.width * 4) + 1):
                    light = Square(0.1)
                    light.move_to(b.get_corner(UL) + RIGHT * (0.2 * c) + DOWN * (0.2 * r))
                    light.set_fill(YELLOW, opacity=0)
                    light.set_stroke(width=0)
                    lights.add(light)

        self.play(FadeIn(buildings))
        self.wait()
        self.add_sound("voiceovers/light.mp3")
        self.play(
            *[light.animate.set_fill(YELLOW, opacity=1) for light in lights],
            run_time=3,
            rate_func=smooth
        )
    
    def population_grow(self):
        def population(t):
            K = 30
            r = 1.0
            return K / (1 + np.exp(-r * (t - 3)))
        def gradient_color(d):
            colors = [BLUE, YELLOW, RED]
            n = len(colors) - 1
            pos = d * n
            i = int(np.floor(pos))
            i = np.clip(i, 0, n - 1)
            t = pos - i
            return interpolate_color(colors[i], colors[i+1], t)

        base_icon = PiCreature().scale(0.2)
        people = VGroup()
        self.add(people)
        
        num_created = 0
        total_time = 3
        row_num = 4
        col_num = 6

        def add_new_icons(mobj, dt):
            nonlocal num_created
            current_time = self.time - 8
            t_model = min(current_time / total_time * row_num, row_num)
            target_count = int(population(t_model))

            while num_created < target_count:
                age_fraction = num_created / 50 
                icon = base_icon.copy()
                c = gradient_color(age_fraction)
                icon.set_color(c).set_stroke(c)
                mobj.add(icon)
                num_created += 1

            mobj.arrange_in_grid(rows=row_num, cols=col_num, buff=0.25)
            mobj.to_corner(DL)

        people.add_updater(add_new_icons)
        self.add_sound("voiceovers/population.mp3")
        self.wait(total_time)
        people.remove_updater(add_new_icons)
    def sound_wave(self):
        graph = FunctionGraph(lambda x: np.exp(-0.1*x)*np.sin(3*x), x_range=[-3, 3], color=BLUE)
        third_width = config.frame_width / 3
        graph.stretch_to_fit_width(third_width)
        graph.to_corner(DR).shift(UP)
        self.add_sound("voiceovers/sound waves.mp3")
        self.play(Create(graph))

class DerivativeWrapUp(Scene):
    def construct(self):
        arrows = VGroup(*[
            Arrow(ORIGIN, RIGHT*1.5).rotate(i*PI/6).set_color(random_bright_color())
            for i in range(12)
        ])
        self.play(LaggedStartMap(GrowArrow, arrows))
        title = Text("Đạo hàm = Bản chất của sự thay đổi", font="Noto Sans", color=YELLOW).next_to(arrows, DOWN)
        self.add_sound("voiceovers/DerivativeWrapUp.mp3")
        self.play(Write(title), run_time=3)
        self.wait(4)
        self.play(FadeOut(arrows), FadeOut(title))

class GraphCarTrajectory(Scene):
    def __init__(self,
                x_min=0,
                x_max=10,
                x_labeled_nums=None,
                x_axis_label=Text("x = thời gian", font="Noto Sans").scale(0.65),
                y_min=0,
                y_max=100,
                y_tick_frequency=10,
                y_labeled_nums=None,
                y_axis_label=Text("y = vị trí", font="Noto Sans").scale(0.65),
                graph_origin=2.5*DOWN + 5*LEFT,
                default_graph_colors=None,
                default_derivative_color=None,
                time_of_journey=5,
                care_movement_rate_func=smooth,
                point_A=DOWN + 4*LEFT,
                point_B=DOWN + 5*RIGHT,
                num_ticks=8,
                tick_length=0.2,
                needle_width=0.1,
                needle_height=0.8,
                speedometer_title_text="Đồng hồ tốc độ",
                 **kwargs):
        super().__init__(**kwargs)

        self.x_min = x_min
        self.x_max = x_max
        self.x_labeled_nums = x_labeled_nums or list(range(1, 11))
        self.x_axis_label = x_axis_label

        self.y_min = y_min
        self.y_max = y_max
        self.y_tick_frequency = y_tick_frequency
        self.y_labeled_nums = y_labeled_nums or list(range(10, 110, 10))
        self.y_axis_label = y_axis_label

        self.graph_origin = graph_origin
        self.default_graph_colors = default_graph_colors or [BLUE, YELLOW]
        self.default_derivative_color = default_derivative_color or YELLOW

        self.time_of_journey = time_of_journey
        self.care_movement_rate_func = care_movement_rate_func
        self.point_A = point_A
        self.point_B = point_B
        self.num_ticks = num_ticks
        self.tick_length = tick_length
        self.needle_width = needle_width
        self.needle_height = needle_height
        self.speedometer_title_text = speedometer_title_text

    def construct(self):
        self.add_sound("voiceovers/Speed.mp3")
        title = Text("Ý nghĩa vật lý: Vận tốc", font="Noto Sans", color=YELLOW).scale(0.8).to_edge(UP)
        self.play(Write(title))
        axes = Axes(
            x_range=[self.x_min, self.x_max, 1],
            y_range=[self.y_min, self.y_max, self.y_tick_frequency],
            x_length=8,
            y_length=5,
            axis_config={"color": WHITE},
            tips=False
        )
        axes.add_coordinates().shift(self.graph_origin - axes.coords_to_point(0, 0))

        x_label = axes.get_x_axis_label(self.x_axis_label)
        y_label = axes.get_y_axis_label(self.y_axis_label)
        
        self.axes = axes

        # --- Graph ---
        graph = axes.plot(
            lambda t: 100 * smooth(t / 10),
            x_range=[0, 10],
            color=BLUE
        )

        origin = axes.coords_to_point(0, 0)
        point_A, point_B = self.point_A, self.point_B
        A = Dot(point_A)
        B = Dot(point_B)
        line = Line(point_A, point_B)
        VGroup(A, B, line).set_color(WHITE)

        for dot, tex in [(A, "A"), (B, "B")]:
            label = MathTex(tex).next_to(dot, DOWN)
            dot.add(label)

        car = SVGMobject("assets/car.svg").scale(0.5)
        self.car = car
        car.move_to(point_A).shift((car.height/2)*UP + (car.width/2)*LEFT)
        self.add(A, B, line, car)
        self.introduce_added_mobjects()
        self.play(
            car.animate.move_to(point_B).shift((car.height/2)*UP + (car.width/2)*LEFT), run_time = 2,
            *self.get_added_movement_anims())
        self.play(FadeOut(self.speedometer), FadeOut(self.speedometer_title))
        self.play(car.animate.move_to(point_A).shift((car.height/2)*UP + (car.width/2)*LEFT))
        top = axes.coords_to_point(0, 100)

        new_length = np.linalg.norm(top - origin)
        new_point_B = point_A + new_length * RIGHT

        car_line_group = VGroup(car, A, B, line)
        car_line_group.generate_target()
        for mob in car_line_group:
            mob.generate_target()

        B.target.shift(new_point_B - point_B)
        line.target.put_start_and_end_on(point_A, new_point_B)

        car_line_group.target.rotate(np.pi/2, about_point=point_A)
        car_line_group.target.shift(origin - point_A)

        self.play(
            MoveToTarget(car_line_group, path_arc=np.pi/2)
        )
        self.add(axes, x_label, y_label)
        self.add_sound("voiceovers/GraphCarTrajectory.mp3")
        self.play(Indicate(self.x_axis_label))
        self.play(Indicate(self.y_axis_label))
        self.play(
            *[FadeOut(mob) for mob in car_line_group if mob is not car]
        )
        
        self.introduce_graph(graph, origin)

    def introduce_graph(self, graph, origin):
        axes = self.axes
        velocity_graph = axes.plot_derivative_graph(
                graph = graph,
            )
        # self.t_tracker = ValueTracker(0)
        speed_gauge = DecimalNumber(0, num_decimal_places=1, include_sign=False)
        speed_gauge.add_updater(lambda d: d.set_value(axes.p2c(velocity_graph.point_from_proportion(1))[1]))
        speed_gauge.add_updater(lambda d: d.next_to(velocity_graph.point_from_proportion(1), UP+LEFT))
        h_line = always_redraw(
            lambda: Line(
                graph.point_from_proportion(1)[0]*RIGHT + origin[1]*UP,
                graph.point_from_proportion(1),
                color=YELLOW,
                stroke_width=2
            )
        )

        v_line = always_redraw(
            lambda: Line(
                origin[0]*RIGHT + graph.point_from_proportion(1)[1]*UP,
                graph.point_from_proportion(1),
                color=BLUE,
                stroke_width=2
            )
        )

        self.add(h_line, v_line)
        car = self.car
        car_target = origin*RIGHT + graph.point_from_proportion(1)*UP

        self.add(car, speed_gauge)
        
        self.play(
            Create(graph, rate_func=linear),
            Create(velocity_graph, rate_func=linear),
            car.animate.move_to(car_target).shift((car.height/2)*DOWN + (car.width/2)*LEFT), 
            run_time=self.time_of_journey
        )
        self.wait()
        self.play(FadeOut(h_line), FadeOut(v_line), FadeOut(car))
    def introduce_added_mobjects(self):
        start_angle = -np.pi / 6
        end_angle = 7 * np.pi / 6

        speedometer = Arc(start_angle=start_angle, angle=end_angle - start_angle)

        tick_angles = np.linspace(end_angle, start_angle, self.num_ticks)

        for index, angle in enumerate(tick_angles):
            vect = rotate_vector(RIGHT, angle)

            tick = Line(
                (1 - self.tick_length) * vect,
                vect
            )

            label = MathTex(str(10 * index))
            label.set_height(self.tick_length)
            label.shift((1 + self.tick_length) * vect)

            speedometer.add(tick, label)

        needle = Polygon(
            LEFT, UP, RIGHT,
            stroke_width=0,
            fill_color=YELLOW,
            fill_opacity=1
        )
        needle.stretch_to_fit_width(self.needle_width)
        needle.stretch_to_fit_height(self.needle_height)
        needle.rotate(end_angle - np.pi / 2)
        needle.move_to(speedometer.get_arc_center()).shift((needle.get_width()/2)*LEFT+(needle.get_height()/2)*DOWN)

        speedometer.add(needle)
        speedometer.needle = needle

        title = Text(self.speedometer_title_text, font="Noto Sans").scale(0.65)
        title.to_corner(UP + LEFT)
        speedometer.next_to(title, DOWN)

        self.speedometer = speedometer
        self.speedometer_title = title

        speedometer.save_state()
        speedometer.rotate(-np.pi/2, UP)
        speedometer.set_height(self.car.get_height()/4)
        speedometer.move_to(self.car)
        speedometer.shift((self.car.get_width()/8)*RIGHT+(self.car.get_height()/4)*UP)

        self.play(speedometer.animate.restore(), run_time = 2)
        self.play(Write(self.speedometer_title, run_time = 1))

    def get_added_movement_anims(self, **kwargs):
        needle = self.speedometer.needle
        center = self.speedometer.get_arc_center()

        default = dict(
            about_point=center,
            radians=-np.pi / 2,
            run_time=10,
            rate_func=there_and_back
        )
        default.update(kwargs)

        return [Rotating(needle, **default)]