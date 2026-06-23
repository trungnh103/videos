from manim import *
from pi_creature_scene import *

# --- CONFIG / COLORS ---
# config.background_color = "#0f1724"  # dark navy
FUNC_COLOR = "#f9e26b"  # yellow-ish
TANGENT_COLOR = "#4cc9f0"  # cyan
ACCENT = "#ff6b6b"  # accent red
INTEGRAL_COLOR = "#9b5de5"  # purple

# --- HELPERS ---

def numeric_derivative(f, x, h=1e-4):
    """Central difference derivative approximation."""
    return (f(x + h) - f(x - h)) / (2 * h)

def tangent_line_as_plot(f, x0, ax: Axes, half_length=1.5, color=TANGENT_COLOR):
    """
    Return a Parametric mobject representing the tangent line to y=f(x) at x0.
    We compute slope numerically and plot linear function over [x0-half_length, x0+half_length].
    """
    slope = numeric_derivative(f, x0)
    y0 = f(x0)
    x_min = x0 - half_length
    x_max = x0 + half_length
    # linear function for plot
    linear = lambda x: slope * (x - x0) + y0
    line = ax.plot(linear, x_range=[x_min, x_max], color=color)
    return line

def make_riemann_rects(ax: Axes, f, a, b, n, sample="left", color=INTEGRAL_COLOR, fill_opacity=0.8):
    """
    Build a VGroup of rectangle polygons approximating area under f from a to b using n rectangles.
    sample: "left", "right", or "mid"
    """
    rects = VGroup()
    xs = np.linspace(a, b, n + 1)
    for i in range(n):
        x_left = xs[i]
        x_right = xs[i + 1]
        if sample == "left":
            x_s = x_left
        elif sample == "right":
            x_s = x_right
        else:
            x_s = 0.5 * (x_left + x_right)
        height = f(x_s)
        # ensure we handle negative heights cleanly (rects go downwards)
        top_y = max(height, 0)
        bottom_y = min(height, 0)
        p1 = ax.c2p(x_left, 0)
        p2 = ax.c2p(x_left, top_y)
        p3 = ax.c2p(x_right, top_y)
        p4 = ax.c2p(x_right, 0)
        poly = Polygon(p1, p2, p3, p4, fill_color=color, fill_opacity=fill_opacity, stroke_width=0)
        rects.add(poly)
    return rects

class Thumbnail(PiCreatureScene):
    def construct(self):
        cup =  self.pi_creatures[0]
        cup.change_mode("pondering")
        edges = []
        partitions = []
        c = 0
        layers = [2, 3, 3, 2]

        for i in layers:
            partitions.append(list(range(c + 1, c + i + 1)))
            c += i
        for i, v in enumerate(layers[1:]):
                last = sum(layers[:i+1])
                for j in range(v):
                    for k in range(last - layers[i], last):
                        edges.append((k + 1, j + last + 1))

        vertices = np.arange(1, sum(layers) + 1)

        nn = Graph(
            vertices,
            edges,
            layout='partite',
            partitions=partitions,
            layout_scale=1.5,
            vertex_config={
                           1: {"fill_color": BLUE, 'radius': 0.20},
                           2: {"fill_color": BLUE, 'radius': 0.20},
                           3: {"fill_color": ORANGE, 'radius': 0.20},
                           4: {"fill_color": ORANGE, 'radius': 0.20},
                           5: {"fill_color": ORANGE, 'radius': 0.20},
                           6: {"fill_color": ORANGE, 'radius': 0.20},
                           7: {"fill_color": ORANGE, 'radius': 0.20},
                           8: {"fill_color": ORANGE, 'radius': 0.20},
                           9: {"fill_color": BLUE, 'radius': 0.20},
                           10: {"fill_color": BLUE, 'radius': 0.20}},
        )
        
        arrow = DoubleArrow(color=YELLOW).next_to(nn, RIGHT)
        ax = Axes(
            x_range=[0, 4],
            y_range=[0, 4],
            x_length=4,
            axis_config={"color": WHITE},
        )
        ax.match_height(nn)
        func = lambda x: 0.35 * ((x - 2)**3 - 2 * (x - 2) + 6)
        graph = ax.plot(func, color=BLUE)
        slopes = ax.get_secant_slope_group(
            x=2.0,
            graph=graph,
            dx=0.01,
            secant_line_length=4,
            secant_line_color=RED_D,
        )
        graph_group = VGroup(ax, graph, slopes)
        
        VGroup(nn, arrow, graph_group).arrange(RIGHT).shift(UP+1.5*RIGHT)
        nn_text = Text("Neural network", font="Noto Sans").scale(0.65).next_to(nn, UP)
        deri_text = Text("Đạo hàm", font="Noto Sans").scale(0.65).next_to(graph_group, UP)
        question = MathTex("???")
        question.next_to(cup, UP)
        self.add(nn, nn_text, arrow, ax, graph, slopes, deri_text, question)

# Scene 1 — Title & Hook
class TitleHook(PiCreatureScene):
    def construct(self):
        cup =  self.pi_creatures[0]
        self.add_sound("voiceovers/Scene 1 — Title & Hook.mp3")
        edges = []
        partitions = []
        c = 0
        layers = [2, 3, 3, 2]  # the number of neurons in each layer

        for i in layers:
            partitions.append(list(range(c + 1, c + i + 1)))
            c += i
        for i, v in enumerate(layers[1:]):
                last = sum(layers[:i+1])
                for j in range(v):
                    for k in range(last - layers[i], last):
                        edges.append((k + 1, j + last + 1))

        vertices = np.arange(1, sum(layers) + 1)

        nn = Graph(
            vertices,
            edges,
            layout='partite',
            partitions=partitions,
            layout_scale=1.5,
            vertex_config={
                           1: {"fill_color": BLUE, 'radius': 0.20},
                           2: {"fill_color": BLUE, 'radius': 0.20},
                           3: {"fill_color": ORANGE, 'radius': 0.20},
                           4: {"fill_color": ORANGE, 'radius': 0.20},
                           5: {"fill_color": ORANGE, 'radius': 0.20},
                           6: {"fill_color": ORANGE, 'radius': 0.20},
                           7: {"fill_color": ORANGE, 'radius': 0.20},
                           8: {"fill_color": ORANGE, 'radius': 0.20},
                           9: {"fill_color": BLUE, 'radius': 0.20},
                           10: {"fill_color": BLUE, 'radius': 0.20}},
        )
        
        arrow = DoubleArrow(color=YELLOW).next_to(nn, RIGHT)
        ax = Axes(
            x_range=[0, 4],
            y_range=[0, 4],
            x_length=4,
            axis_config={"color": WHITE},
        )
        ax.match_height(nn)
        func = lambda x: 0.35 * ((x - 2)**3 - 2 * (x - 2) + 6)
        graph = ax.plot(func, color=BLUE)
        slopes = ax.get_secant_slope_group(
            x=2.0,
            graph=graph,
            dx=0.01,
            secant_line_length=4,
            secant_line_color=RED_D,
        )
        graph_group = VGroup(ax, graph, slopes)
        
        VGroup(nn, arrow, graph_group).arrange(RIGHT).shift(UP+1.5*RIGHT)
        nn_text = Text("Neural network", font="Noto Sans").scale(0.65).next_to(nn, UP)
        deri_text = Text("Đạo hàm", font="Noto Sans").scale(0.65).next_to(graph_group, UP)
        self.play(Create(nn), Write(nn_text))
        self.play(Create(arrow))
        self.play(Create(ax), Create(graph), Create(slopes), Write(deri_text))
        self.wait()
        self.play(cup.animate.change_mode("confused"))
        self.play(Indicate(slopes))
        self.wait()
        question = MathTex("???")
        self.play(cup.animate.change_mode("pondering"))
        question.next_to(arrow, UP)
        self.play(Write(question))
        self.wait()

class TitleScene(Scene):
    def construct(self):
        title = Text("Derivatives for Machine Learning", font_size=60, weight=BOLD)
        subtitle = Text("The Easiest Explanation", font_size=36, color=YELLOW)
        sub2 = Text("Why do neural networks need derivatives?", font_size=30, color=BLUE)

        subtitle.next_to(title, DOWN)
        sub2.next_to(subtitle, DOWN)

        self.play(FadeIn(title, shift=UP), run_time=1.2)
        self.play(Write(subtitle))
        self.wait(0.2)
        self.play(FadeIn(sub2))
        self.wait(1)

class Scene1ZoomNeuron(Scene):
    def construct(self):
        # ----------------------------
        # Step 0: simple neural network
        # ----------------------------
        neuron = Circle(0.3, color=BLUE).set_fill(BLUE, 0.6).to_edge(LEFT)
        self.add(neuron)

        # other neurons (just for context)
        hidden = VGroup(*[Circle(0.25, color=BLUE).set_fill(BLUE,0.3).next_to(neuron, RIGHT, buff=1.5*i) for i in range(3)])
        self.add(hidden)

        self.wait(0.5)

        # ----------------------------
        # Step 1: Zoom into single neuron
        # ----------------------------
        self.play(
            neuron.animate.scale(6).move_to(ORIGIN),
            run_time=1.5,
            rate_func=smooth
        )
        self.wait(0.5)

        # ----------------------------
        # Step 2: Morph into a function graph
        # ----------------------------
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 4, 1],
            x_length=6,
            y_length=3
        ).to_edge(DOWN)

        # simple function (parabola)
        func = lambda x: 0.5 * x**2
        graph = axes.plot(func, color=YELLOW, stroke_width=4)

        # optional label
        label = MathTex("y = 0.5 x^2", font_size=36).next_to(axes, UP)

        # Transform neuron circle into graph (rough morph effect)
        self.play(
            Transform(neuron, graph),
            FadeIn(axes, shift=UP*1.5),
            FadeIn(label, shift=UP*1.5),
            run_time=2
        )

        self.wait(1)

class DerivativeSlope(Scene):
    """Scene 2 — Derivatives: slope intuition with moving point & dynamic tangent"""
    def construct(self):
        self.add_sound("voiceovers/Scene 2 — Intuition First.mp3")
        ax = Axes(x_range=[-2, 3.5], y_range=[-1, 6], axis_config={"color": GREY})
        ax.add_coordinates(font_size=18)
        f = lambda x: 0.6 * (x ** 2) 
        curve = ax.plot(f, color=FUNC_COLOR, stroke_width=3)
        tracker = ValueTracker(-1.2)

        dot = always_redraw(lambda: Dot(ax.c2p(tracker.get_value(), f(tracker.get_value())), color=ACCENT))
        tangent = always_redraw(lambda: tangent_line_as_plot(f, tracker.get_value(), ax, half_length=1.5))
        slope_val = always_redraw(lambda: DecimalNumber(
            numeric_derivative(f, tracker.get_value()), num_decimal_places=2
        ).next_to(ax, UP).set_color(TANGENT_COLOR))

        slope_label = Text("Độ dốc:", font="Noto Sans").scale(0.7).next_to(slope_val, LEFT, buff=0.3)

        self.add(ax, curve, dot, tangent, slope_val, slope_label)
        self.play(tracker.animate.set_value(1.8), run_time=19, rate_func=there_and_back)
        self.wait()

class IntuitionScene(Scene):
    def construct(self):
        axes = Axes(x_range=[-2, 4], y_range=[-2, 8], tips=False)
        graph = axes.plot(lambda x: 0.5 * (x - 1)**2 + 1, color=BLUE)
        dot = Dot(axes.c2p(-1, graph.underlying_function(-1)), color=YELLOW)

        label = Text("Slope = rate of change", color=YELLOW).to_edge(UP)

        self.play(Create(axes), Create(graph))
        self.play(FadeIn(label))
        self.play(FadeIn(dot))

        def update_tangent(mob):
            t = self.time % 3 - 1.5
            x = t
            y = graph.underlying_function(x)
            dot.move_to(axes.c2p(x, y))
            # slope = graph.get_derivative()(x)
            tangent = axes.get_secant_slope_group(x, graph, dx=0.01, secant_line_color=RED)
            mob.become(tangent)
            return mob

        tangent_group = always_redraw(lambda: update_tangent(VGroup()))
        self.add(tangent_group)

        self.wait(6)

class SlopeExamplesScene(Scene):
    def construct(self):
        examples = VGroup(
            Text("Flat road → slope = 0"),
            Text("Gentle hill → small slope"),
            Text("Steep hill → large slope"),
            Text("Downhill → negative slope"),
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.8)

        self.play(FadeIn(examples, lag_ratio=0.4, run_time=2))
        self.wait(3)

class LimitFormulaScene(PiCreatureScene):
    def construct(self):
        self.add_sound("voiceovers/dinh nghia dao ham.mp3")
        cup =  self.pi_creatures[0]
        title = Text("Định nghĩa đạo hàm", color=YELLOW, font="Noto Sans").scale(0.7).to_edge(UP)
        self.play(Write(title))
        formula = MathTex(
            r"f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}"
        )
        formula.next_to(title, DOWN).shift(DOWN)
        self.play(Write(formula))
        self.play(cup.animate.change_mode("erm"))
        self.add_sound("voiceovers/dev_formula.mp3")
        self.play(Indicate(formula[0][:5]))
        self.wait()
        self.play(Indicate(formula[0][6:12]))
        self.wait()
        self.play(Indicate(formula[0][12:18]))
        self.play(Indicate(formula[0][19:23]))
        self.play(Indicate(formula[0][24:]))
        self.play(formula.animate.to_edge(LEFT))
        func = lambda x: 0.35 * ((x - 2)**3 - 2 * (x - 2) + 6)
        axes = Axes(
            x_range=[0, 4],
            y_range=[0, 4],
            x_length=6,
            y_length=5,
            tips=False
        ).to_edge(RIGHT, buff=1)

        y_label = axes.get_y_axis_label("y=f(x)")
        self.add_sound("voiceovers/Scene 4 — The Formula, Gently.mp3")
        self.play(cup.animate.change_mode("conniving"))
        self.play(Create(axes), Write(y_label))
        graph = axes.plot(func, color=BLUE)
        self.play(Create(graph))
        h = ValueTracker(1.0)
        x0 = 2.0
        dot_x0 = always_redraw(lambda: Dot(axes.c2p(x0, func(x0))))
        label_x0 = always_redraw(lambda: axes.get_T_label(x_val=x0, graph=graph, 
                                                          line_color=WHITE, triangle_size =0.0, label=Tex("x")))
        self.play(FadeIn(dot_x0), Write(label_x0))

        dot_x1 = always_redraw(lambda: Dot(axes.c2p(x0 + h.get_value(), func(x0 + h.get_value()))))
        label_x1 = always_redraw(lambda: axes.get_T_label(x_val=x0 + h.get_value(), graph=graph, 
                                                          line_color=WHITE, triangle_size =0.0, label=Tex("x + h")))
        self.play(FadeIn(dot_x1), Write(label_x1))
        
        def get_secant():
            secant = axes.get_secant_slope_group(
                x=x0, graph=graph, dx=h.get_value(), secant_line_length=4, 
                dx_label=Tex("h"), secant_line_color=RED_D
            )
            dx_label = secant[2]
            dx_label.next_to(secant[0], UP)
            return secant
        secant = always_redraw(lambda: get_secant())

        self.add(secant)
        self.play(
            h.animate.set_value(0.01), run_time=2, rate_func=linear
        )
        self.play(cup.animate.change_mode("happy"))
        self.wait()

class DerivativeRulesScene(Scene):
    def construct(self):
        self.add_sound("voiceovers/Scene 5 — Quick Examples.mp3")
        title = Text("Ví dụ", color=YELLOW, font="Noto Sans").to_corner(UL)
        
        ax = NumberPlane(y_range=[-1, 7], background_line_style={"stroke_opacity": 0.4})
        self.wait()
        self.add(ax)
        self.wait(3)
        self.play(Write(title))
        def square(x):
            return x ** 2
        def threeX(x):
            return 3 * x
        def sin(x):
            return np.sin(x)
        square_graph = ax.plot(
                square,
                color = PURPLE_B,
            )
        square_velocity_graph = ax.plot_derivative_graph(
                graph = square_graph,
            )
        square_rule = MathTex(r"(x^2)' = 2x")
        square_rule[0][1:3].set_color(PURPLE_B)
        square_rule[0][-2:].set_color(GREEN)
        square_rule.next_to(title, DOWN).shift(RIGHT)
        label_square = ax.get_graph_label(square_graph, "x^2", x_val=-2, direction=DL)
        label_square_velocity = ax.get_graph_label(square_velocity_graph, "2x", x_val=3, direction=RIGHT)
        labels_square = VGroup(label_square, label_square_velocity)
        self.play(Write(square_rule))
        self.wait()
        self.play(Create(square_graph), Create(square_velocity_graph), Write(labels_square))
        self.wait(2)

        threeX_graph = ax.plot(
                threeX,
                color = PURPLE_B,
            )
        threeX_velocity_graph = ax.plot_derivative_graph(
                graph = threeX_graph,
            )
        threeX_rule = MathTex(r"(3x)' = 3")
        threeX_rule[0][1:3].set_color(PURPLE_B)
        threeX_rule[0][-1:].set_color(GREEN)
        threeX_rule.next_to(title, DOWN).shift(RIGHT)
        label_threeX = ax.get_graph_label(threeX_graph, "3x", x_val=1, direction=UR)
        label_threeX_velocity = ax.get_graph_label(threeX_velocity_graph, "3", x_val=3, direction=UP)
        labels_threeX = VGroup(label_threeX, label_threeX_velocity)
        self.play(Transform(square_rule, threeX_rule))
        self.play(Transform(square_graph, threeX_graph))
        self.play(Transform(square_velocity_graph, threeX_velocity_graph))
        self.play(Transform(labels_square, labels_threeX))
        self.wait(2)

        sin_graph = ax.plot(
                sin,
                color = PURPLE_B,
            )
        sin_velocity_graph = ax.plot_derivative_graph(
                graph = sin_graph,
            )
        sin_rule = MathTex(r"(\sin x)' = \cos x")
        sin_rule[0][1:5].set_color(PURPLE_B)
        sin_rule[0][-4:].set_color(GREEN)
        sin_rule.next_to(title, DOWN).shift(RIGHT)
        label_sin = ax.get_graph_label(sin_graph, "sin x", x_val=PI / 2, direction=UP)
        label_sin_velocity = ax.get_graph_label(sin_velocity_graph, "cos x", x_val=PI, direction=DOWN)
        labels_sin = VGroup(label_sin, label_sin_velocity)
        self.play(Transform(square_rule, sin_rule))
        self.play(Transform(square_graph, sin_graph))
        self.play(Transform(square_velocity_graph, sin_velocity_graph))
        self.play(Transform(labels_square, labels_sin))
        self.wait()

class LossSlopeScene_LuxuryEdition(PiCreatureScene):
    def construct(self):
        arrow_feedback = Arrow(start=RIGHT+UP, end=LEFT+UP, color=PURPLE)
        feedback = Tex("Feedback").scale(0.65).next_to(arrow_feedback, UP)
        edges = []
        partitions = []
        c = 0
        layers = [2, 3, 3, 2]

        for i in layers:
            partitions.append(list(range(c + 1, c + i + 1)))
            c += i
        for i, v in enumerate(layers[1:]):
                last = sum(layers[:i+1])
                for j in range(v):
                    for k in range(last - layers[i], last):
                        edges.append((k + 1, j + last + 1))

        vertices = np.arange(1, sum(layers) + 1)

        nn = Graph(
            vertices,
            edges,
            layout='partite',
            partitions=partitions,
            layout_scale=1.5,
            vertex_config={
                           1: {"fill_color": BLUE, 'radius': 0.20},
                           2: {"fill_color": BLUE, 'radius': 0.20},
                           3: {"fill_color": ORANGE, 'radius': 0.20},
                           4: {"fill_color": ORANGE, 'radius': 0.20},
                           5: {"fill_color": ORANGE, 'radius': 0.20},
                           6: {"fill_color": ORANGE, 'radius': 0.20},
                           7: {"fill_color": ORANGE, 'radius': 0.20},
                           8: {"fill_color": ORANGE, 'radius': 0.20},
                           9: {"fill_color": BLUE, 'radius': 0.20},
                           10: {"fill_color": BLUE, 'radius': 0.20}},
        )
        nn.next_to(arrow_feedback, LEFT)
        nn_text = Text("Neural network", font="Noto Sans").scale(0.65).next_to(nn, UP)
        self.add_sound("voiceovers/Scene 6 — Why Machine Learning Cares.mp3")
        self.play(Create(nn), Write(nn_text), run_time=0.5)
        loss_fn = lambda w: (w - 1)**2 + 1
        dloss_fn = lambda w: 2 * (w - 1)

        axes = Axes(x_range=[-3, 3], y_range=[0, 8], tips=False)
        axes.match_height(nn)
        
        axes.next_to(arrow_feedback, RIGHT)
        loss_func_label = Text("Hàm mất mát (loss)", font="Noto Sans").scale(0.65)
        loss_func_label.next_to(axes, UP).shift(RIGHT)
        self.play(Create(axes), Write(loss_func_label), run_time=0.5)
        
        # heatmap-style curve (slope magnitude → color)
        def color_map(w):
            m = abs(dloss_fn(w))
            return color_gradient([BLUE, YELLOW, RED], [0, 2, 6], m)

        samples = np.linspace(-3, 3, 200)
        curve = VMobject()
        curve.set_points_smoothly(
            [axes.c2p(w, loss_fn(w)) for w in samples]
        )
        curve.set_color_by_gradient(BLUE, YELLOW, RED)
        self.play(Create(curve), run_time=0.5)
        self.play(Create(arrow_feedback), Write(feedback), run_time=0.5)

        # starting
        w = -2
        dot = Dot(axes.c2p(w, loss_fn(w)), color=YELLOW)
        trail = TracedPath(dot.get_center, stroke_color=WHITE, stroke_width=2)
        self.add(dot, trail)

        cup =  self.pi_creatures[0]

        # labels
        w_label = always_redraw(
            lambda: MathTex(f"w = {w:.2f}", font_size=36)
                .next_to(dot, UP)
        )
        slope_label = always_redraw(
            lambda: MathTex(f"slope = {dloss_fn(w):+.2f}", font_size=32)
                .next_to(dot, RIGHT).shift(0.5*RIGHT)
        )
        loss_label = always_redraw(
            lambda: MathTex(f"loss = {loss_fn(w):.2f}", font_size=32)
                .next_to(dot, DOWN)
        )
        self.add(w_label, slope_label, loss_label)

        # gradient descent updater
        learning_rate = 0.3
        sound_played = False

        def update_dot(mob, dt):
            nonlocal w, sound_played
            slope = dloss_fn(w)
            w -= learning_rate * slope * dt
            mob.move_to(axes.c2p(w, loss_fn(w)))

            if abs(slope) < 0.03:
                if not sound_played:
                    sound_played = True
                    self.add_sound("voiceovers/ding.wav")
                cup.change_mode("hooray")
            elif abs(slope) < 0.3:
                cup.change_mode("happy")
            else:
                cup.change_mode("thinking")

        dot.add_updater(update_dot)

        # direction arrow
        arrow = always_redraw(
            lambda: Arrow(
                dot.get_center(),
                dot.get_center() +
                LEFT * np.sign(dloss_fn(w)) * 0.8,
                buff=0.1,
                color=RED
            )
        )
        self.add(arrow)
        self.wait()
        self.play(Indicate(slope_label))
        self.wait()
        self.play(Indicate(w_label))
        self.wait(0.5)
        self.play(Indicate(loss_label))
        self.wait(7)
        dot.remove_updater(update_dot)

class LossWithNNScene(Scene):
    """
    Left: loss curve and a dot that moves by gradient descent on w.
    Right: small neural network diagram with a highlighted weight 'w' that updates live.
    An arrow visually connects the weight label to the dot on the loss curve.
    """

    def construct(self):
        # ---------- Loss function ----------
        loss_fn = lambda w: (w - 1)**2 + 1
        dloss_fn = lambda w: 2 * (w - 1)

        # Axes + loss plot (left side)
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 8, 2],
            x_length=6,
            y_length=4.5,
            tips=False
        ).to_edge(LEFT, buff=0.8)
        axes.add_coordinates(font_size=24, num_decimal_places=0)

        samples = np.linspace(-3, 3, 300)
        loss_points = [axes.c2p(x, loss_fn(x)) for x in samples]
        loss_curve = VMobject()
        loss_curve.set_points_smoothly(loss_points)
        loss_curve.set_stroke(width=3)

        # a dot representing current w on the curve
        w = -2.0  # starting weight
        dot = Dot(point=axes.c2p(w, loss_fn(w)), radius=0.08, color=YELLOW)

        # labels for axes/loss
        loss_title = MathTex(r"\text{Loss } J(w)", font_size=36).next_to(axes, UP)
        self.play(Create(axes), Write(loss_title))
        self.play(Create(loss_curve), run_time=1.2)
        self.play(FadeIn(dot))

        # ---------- Neural network diagram (right side) ----------
        # positions
        nn_center = RIGHT * 3.5  # move network to the right side
        layer_gap = 1.6
        neuron_radius = 0.22

        # input neuron
        inp_pos = np.array(nn_center) + LEFT * 1.2 + UP * 0.6
        hidden_pos = np.array(nn_center) + RIGHT * 0.0 + UP * 0.6
        out_pos = np.array(nn_center) + RIGHT * 1.2 + UP * 0.6

        input_neuron = Circle(radius=neuron_radius).move_to(inp_pos)
        hidden_neuron = Circle(radius=neuron_radius).move_to(hidden_pos)
        output_neuron = Circle(radius=neuron_radius).move_to(out_pos)

        input_label = MathTex("x", font_size=28).move_to(inp_pos)
        hidden_label = MathTex("h", font_size=28).move_to(hidden_pos)
        output_label = MathTex("y", font_size=28).move_to(out_pos)

        # connections
        conn_in_hidden = Line(input_neuron.get_right(), hidden_neuron.get_left(), stroke_width=2)
        conn_hidden_out = Line(hidden_neuron.get_right(), output_neuron.get_left(), stroke_width=2)

        # weight label on the hidden->output connection (this is the parameter w)
        weight_dot_pos = (hidden_neuron.get_right() + output_neuron.get_left()) / 2
        weight_marker = Dot(weight_dot_pos, radius=0.06, color=RED)
        weight_label = MathTex(r"w", font_size=32).next_to(weight_marker, UP)

        # group neural network items
        nn_group = VGroup(
            input_neuron, hidden_neuron, output_neuron,
            input_label, hidden_label, output_label,
            conn_in_hidden, conn_hidden_out,
            weight_marker, weight_label
        )
        nn_group.shift(RIGHT * 1.5)  # small adjustment
        self.play(FadeIn(nn_group))

        # ---------- Live weight value label and connection arrow ----------
        # numeric weight label (updates as w changes)
        numeric_weight_label = always_redraw(lambda: MathTex(f"w = {w:.2f}", font_size=32).next_to(weight_label, RIGHT))
        # arrow from numeric_weight_label to dot to show mapping w -> loss(w)
        mapping_arrow = always_redraw(lambda: Arrow(
            numeric_weight_label.get_left(),
            dot.get_center(),
            buff=0.1,
            stroke_width=2,
            max_stroke_width_to_length_ratio=6
        ))

        self.add(numeric_weight_label, mapping_arrow)

        # ---------- dynamic visuals: change weight color intensity based on magnitude of gradient ----------
        def update_weight_marker(mob):
            mag = abs(dloss_fn(w))
            # interpolate color from GREEN (small) to RED (large)
            mob.set_fill(color=interpolate_color(GREEN, RED, min(mag/4, 1.0)), opacity=1.0)
        weight_marker.add_updater(lambda m, dt: update_weight_marker(m))

        # ---------- gradient descent updater (updates w, dot, and numeric label changes automatically) ----------
        lr = 0.6
        def dot_updater(mob, dt):
            nonlocal w
            slope = dloss_fn(w)
            # gradient descent step
            w -= lr * slope * dt
            # move dot to new (w, loss)
            mob.move_to(axes.c2p(w, loss_fn(w)))
            # also update weight_label's text to pulse when changing
            # (we do the numeric label via always_redraw)
        dot.add_updater(dot_updater)

        # ---------- visual arrow on the NN connection showing magnitude and direction of update ----------
        # small arrow along the hidden->output connection that scales with step size
        conn_arrow = always_redraw(lambda: Arrow(
            start=hidden_neuron.get_right(),
            end=output_neuron.get_left(),
            buff=neuron_radius*0.4,
            stroke_width=max(1, min(abs(dloss_fn(w))*2, 6)),
            max_stroke_width_to_length_ratio=6,
        ).set_color(interpolate_color(BLUE, RED, min(abs(dloss_fn(w))/4, 1.0))))
        self.add(conn_arrow)

        # highlight output neuron color changing with loss value (visual cue)
        def update_output_neuron(mob):
            yval = loss_fn(w)
            # map yval in [1, 8] to opacity/color shift; clamp
            t = (yval - 1) / (8 - 1)
            mob.set_fill(interpolate_color(BLUE, YELLOW, min(max(t, 0), 1)), opacity=0.5)
        output_neuron.add_updater(lambda m, dt: update_output_neuron(m))

        # ---------- small explanatory label on the network ----------
        nn_text = Text("Simple network\n(Input → Hidden → Output)", font_size=24).next_to(nn_group, UP)
        self.play(FadeIn(nn_text))

        # ---------- run the animation ----------
        # briefly pause to show initial state
        self.wait(1.0)
        # let gradient descent run for a while (dot updater moves w and the network visuals respond)
        self.wait(6.0)

        # clean up updaters
        dot.remove_updater(dot_updater)
        weight_marker.clear_updaters()
        output_neuron.clear_updaters()

        # final highlight: emphasize reaching minimum
        final_box = SurroundingRectangle(VGroup(dot, numeric_weight_label, weight_marker), buff=0.25, color=YELLOW)
        self.play(Create(final_box), run_time=0.6)
        self.wait(1.5)


class GradientDescentScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=-30 * DEGREES)
        surface = Surface(
            lambda u, v: np.array([u, v, (u - 1)**2 + (v + 1)**2]),
            u_range=[-3, 3], v_range=[-3, 3],
            resolution=20
        ).set_style(fill_opacity=0.6, stroke_width=0.5)

        point = Sphere(radius=0.1, color=YELLOW).move_to([2, 2, (2 - 1)**2 + (2 + 1)**2])
        steps = [
            [1.5, 1.2], [1.1, 0.4], [0.8, -0.2], [0.6, -0.6], [0.5, -0.8]
        ]
        axes = ThreeDAxes()
        self.add(axes)
        self.play(FadeIn(surface))
        self.play(FadeIn(point))

        for x, y in steps:
            target = np.array([x, y, (x - 1)**2 + (y + 1)**2])
            self.play(point.animate.move_to(target), run_time=0.7)

        self.wait(1)

class PartialDerivativesScene(ThreeDScene):
    def construct(self):
        # ====== Loss surface ======
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[0, 18, 3],
        )
        self.set_camera_orientation(phi=60 * DEGREES, theta=30 * DEGREES)
        self.play(Create(axes))

        # Loss function L(w1, w2)
        loss = lambda w1, w2: (w1 - 1)**2 + (w2 + 1)**2 + 3

        surface = Surface(
            lambda u, v: axes.c2p(u, v, loss(u, v)),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(40, 40),
            fill_opacity=0.8,
            checkerboard_colors=[BLUE_E, BLUE_D],
        )
        self.play(Create(surface), run_time=2)

        # Initial point
        w1, w2 = -2.0, 2.0
        point = Sphere(radius=0.08, color=YELLOW).move_to(axes.c2p(w1, w2, loss(w1, w2)))
        self.add(point)

        # Traced path
        path = TracedPath(point.get_center, stroke_width=3, stroke_color=WHITE)
        self.add(path)

        lr = 0.35  # learning rate

        # ====== Dynamic partial derivative arrows ======
        def dL_dw1(w1, w2):
            return 2 * (w1 - 1)

        def dL_dw2(w1, w2):
            return 2 * (w2 + 1)

        arrow_dw1 = always_redraw(
            lambda: Arrow(
                start=point.get_center(),
                end=point.get_center() + axes.c2p(-np.sign(dL_dw1(w1, w2))*0.6, 0, 0) - axes.c2p(0,0,0),
                buff=0,
                color=RED
            )
        )
        arrow_dw2 = always_redraw(
            lambda: Arrow(
                start=point.get_center(),
                end=point.get_center() + axes.c2p(0, -np.sign(dL_dw2(w1, w2))*0.6, 0) - axes.c2p(0,0,0),
                buff=0,
                color=GREEN
            )
        )
        self.add(arrow_dw1, arrow_dw2)

        # Arrow labels
        label_dw1 = always_redraw(
            lambda: MathTex(r"\frac{\partial L}{\partial w_1}", font_size=36, color=RED)
            .next_to(arrow_dw1, OUT)
        )
        label_dw2 = always_redraw(
            lambda: MathTex(r"\frac{\partial L}{\partial w_2}", font_size=36, color=GREEN)
            .next_to(arrow_dw2, OUT)
        )
        self.add(label_dw1, label_dw2)

        # ====== Updater for moving point (gradient descent) ======
        def update_point(obj, dt):
            nonlocal w1, w2
            g1 = dL_dw1(w1, w2)
            g2 = dL_dw2(w1, w2)
            w1 -= lr * g1 * dt
            w2 -= lr * g2 * dt
            obj.move_to(axes.c2p(w1, w2, loss(w1, w2)))

        point.add_updater(update_point)

        self.wait(6)
        point.remove_updater(update_point)
        self.wait()


class GradientVectorScene(Scene):
    def construct(self):
        vec = MathTex(
            r"\nabla f = \left[\frac{\partial f}{\partial w_1}, \frac{\partial f}{\partial w_2}, \dots \right]",
            font_size=58
        )
        self.play(Write(vec))
        self.wait(2)

class GradientVectorScene(Scene):
    def construct(self):
        # ===== Loss function =====
        L = lambda w1, w2: (w1 - 1)**2 + (w2 + 2)**2  # bowl surface / convex loss
        dL_dw1 = lambda w1, w2: 2 * (w1 - 1)
        dL_dw2 = lambda w1, w2: 2 * (w2 + 2)

        # Contour plot background
        ax = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=7,
            y_length=7
        )
        self.play(Create(ax))

        # Draw level sets of loss
        contours = VGroup()
        for r in np.linspace(1, 12, 8):
            circle = Circle(radius=np.sqrt(r), color=BLUE_D, stroke_opacity=0.4)
            circle.move_to(ax.c2p(1, -2))  # center at minimum
            contours.add(circle)
        self.play(FadeIn(contours, lag_ratio=0.1, run_time=1.2))

        # Starting point
        w1, w2 = -2.5, 2.0
        point = Dot(ax.c2p(w1, w2), radius=0.12, color=YELLOW)
        path = TracedPath(point.get_center, stroke_color=WHITE, stroke_width=2)
        self.add(point, path)

        # Gradient and -gradient vectors
        grad_vec = always_redraw(
            lambda: Arrow(
                point.get_center(),
                point.get_center() + 0.8 * np.array([
                    dL_dw1(w1, w2),
                    dL_dw2(w1, w2),
                    0
                ]) / 3,  # scaled for visibility
                color=RED
            )
        )
        neg_grad_vec = always_redraw(
            lambda: Arrow(
                point.get_center(),
                point.get_center() - 0.8 * np.array([
                    dL_dw1(w1, w2),
                    dL_dw2(w1, w2),
                    0
                ]) / 3,
                color=GREEN
            )
        )
        self.add(grad_vec, neg_grad_vec)

        # Labels
        grad_label = always_redraw(
            lambda: MathTex(r"\nabla L", color=RED)
                .next_to(grad_vec, UP, buff=0.15)
        )
        neg_grad_label = always_redraw(
            lambda: MathTex(r"-\nabla L", color=GREEN)
                .next_to(neg_grad_vec, DOWN, buff=0.15)
        )
        self.add(grad_label, neg_grad_label)

        # Live coordinate label
        coord_label = always_redraw(
            lambda: MathTex(
                f"(w_1={w1:.2f}, w_2={w2:.2f})",
                font_size=34
            ).next_to(point, UR)
        )
        self.add(coord_label)

        # Gradient descent motion ------------------------------------------------
        lr = 0.4

        def update_point(p, dt):
            nonlocal w1, w2
            g1 = dL_dw1(w1, w2)
            g2 = dL_dw2(w1, w2)
            w1 -= lr * g1 * dt
            w2 -= lr * g2 * dt
            p.move_to(ax.c2p(w1, w2))

        point.add_updater(update_point)
        self.wait(6)
        point.remove_updater(update_point)
        self.wait()

class BackpropScene(Scene):
    def construct(self):
        # ===========================
        #  Network architecture
        # ===========================
        layer_sizes = [3, 4, 2, 1]
        layers = VGroup()
        node_radius = 0.22

        # Positioning network layers
        for i, size in enumerate(layer_sizes):
            layer = VGroup(*[
                Circle(node_radius, color=BLUE).set_fill(BLUE, 0.15)
                for _ in range(size)
            ])
            layer.arrange(DOWN, buff=0.35)
            layer.shift(RIGHT * i * 2.5)
            layers.add(layer)

        self.play(FadeIn(layers, lag_ratio=0.1, run_time=1.3))

        # Connections
        edges = VGroup()
        for l1, l2 in zip(layers[:-1], layers[1:]):
            for a in l1:
                for b in l2:
                    line = Line(a.get_right(), b.get_left(), stroke_width=2, color=GREY)
                    edges.add(line)
        self.play(Create(edges, lag_ratio=0.002))

        # ===========================
        # Forward pass animation
        # ===========================
        def activate(node):
            return node.animate.set_fill(YELLOW, 0.9).set_color(YELLOW)

        forward_text = Text("Forward pass: compute activations", font_size=36).to_edge(UP)
        self.play(Write(forward_text))

        for layer in layers:
            for node in layer:
                self.play(activate(node), run_time=0.13)

        self.wait(0.3)

        # ===========================
        # Loss display
        # ===========================
        loss = MathTex("L = (y_{pred} - y)^2", font_size=38).next_to(layers[-1], RIGHT, buff=1)
        self.play(Write(loss))
        self.wait(0.5)

        # ===========================
        # Backpropagation
        # ===========================
        self.play(Transform(forward_text, Text("Backward pass: compute gradients", font_size=36).to_edge(UP)))

        grad_color = RED
        arrows = VGroup()

        # animated gradient arrows layer by layer
        for j in reversed(range(len(layers) - 1)):
            l1 = layers[j]
            l2 = layers[j + 1]
            for b in l2:
                for a in l1:
                    arr = Arrow(
                        b.get_left(), a.get_right(),
                        color=grad_color,
                        stroke_width=6,
                        max_tip_length_to_length_ratio=0.15
                    )
                    arrows.add(arr)

            self.play(Create(arrows), run_time=0.4)

            # pulse affected nodes
            for node in l1:
                self.play(
                    node.animate.set_fill(grad_color, 0.9).set_color(grad_color),
                    run_time=0.15
                )

        self.wait(0.4)

        # ===========================
        # Gradient label overlays per layer
        # ===========================
        grad_labels = VGroup()
        for i, layer in enumerate(layers[1:]):
            label = MathTex(f"\\frac{{\\partial L}}{{\\partial W_{{{i+1}}}}}", color=RED, font_size=32)
            label.next_to(layer, DOWN)
            grad_labels.add(label)

        self.play(FadeIn(grad_labels, lag_ratio=0.2))
        self.wait(0.6)

        # highlight conceptual summary
        summary = Text("Backprop sends gradients back through layers,\nupdating weights to reduce loss.",
                       font_size=34).to_edge(DOWN)
        self.play(Write(summary))
        self.wait(1.5)


class RecapScene(PiCreatureScene):
    def construct(self):
        self.add_sound("voiceovers/Scene 11 — Recap & Motivation.mp3")
        cup =  self.pi_creatures[0]
        self.play(cup.animate.change_mode("speaking"))
        title = Text("Tóm tắt lại", font="Noto Sans", color=YELLOW).scale(0.8)
        self.play(Write(title))
        self.play(title.animate.to_corner(UL))
        self.play(cup.animate.change_mode("conniving"))
        bullets = VGroup(
            Text("• Đạo hàm = thay đổi", font="Noto Sans"),
            Text("• Mạng nơ-ron học bằng cách giảm mất mát", font="Noto Sans"),
            Text("• Độ dốc cho biết hướng di chuyển", font="Noto Sans"),
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.8)
        bullets.shift(UP)
        self.wait()
        self.play(Write(bullets[0]))
        self.play(Write(bullets[1]))
        self.play(Write(bullets[2]))
        self.play(cup.animate.change_mode("gracious"))
        self.wait()
