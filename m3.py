from manim import *
import numpy as np
from scipy.stats import norm

class MeanMedianMode(Scene):
    def construct(self):
        # Sample data
        data = [2, 3, 3, 5, 7, 8, 8, 8, 10]
        sorted_data = sorted(data)

        # Title
        title = Text("Mean, Median, Mode", font_size=48)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # Number line
        number_line = NumberLine(
            x_range=[0, 11, 1],
            length=10,
            include_numbers=True
        ).shift(DOWN)

        self.play(Create(number_line))

        # Dots for data
        dots = VGroup()
        for x in data:
            dot = Dot(number_line.n2p(x), color=BLUE)
            dots.add(dot)

        self.play(FadeIn(dots))
        self.wait(1)

        # ---------------- MEAN ----------------
        mean_value = np.mean(data)
        mean_dot = Dot(number_line.n2p(mean_value), color=YELLOW)

        mean_label = Text(f"Mean = {mean_value:.2f}", font_size=32)\
            .next_to(mean_dot, UP)

        self.play(
            Create(mean_dot),
            Write(mean_label)
        )
        self.wait(2)

        self.play(FadeOut(mean_dot), FadeOut(mean_label))

        # ---------------- MEDIAN ----------------
        median_value = np.median(sorted_data)
        median_dot = Dot(number_line.n2p(median_value), color=GREEN)

        median_label = Text(f"Median = {median_value}", font_size=32)\
            .next_to(median_dot, UP)

        self.play(
            Create(median_dot),
            Write(median_label)
        )
        self.wait(2)

        self.play(FadeOut(median_dot), FadeOut(median_label))

        # ---------------- MODE ----------------
        mode_value = max(set(data), key=data.count)

        mode_dots = VGroup(
            *[dot for dot, x in zip(dots, data) if x == mode_value]
        ).set_color(RED)

        mode_label = Text(f"Mode = {mode_value}", font_size=32)\
            .next_to(number_line, DOWN)

        self.play(
            mode_dots.animate.scale(1.5),
            Write(mode_label)
        )

        self.wait(3)
from manim import *
import numpy as np
from scipy.integrate import quad

# 📈 PDF curve
# 🔴 Mode → highest point of the curve
# 🟡 Mean → balance point (expected value)
# 🟢 Median → splits area under curve into 50% / 50%
class MeanMedianModePDF(Scene):
    def construct(self):
        # -----------------------------
        # Define an arbitrary PDF
        # -----------------------------
        def pdf(x):
            # Skewed distribution example
            return np.exp(-(x - 1)**2 / 2) + 0.4 * np.exp(-(x - 4)**2 / 0.5)
            # return 1.0 * (1/((x-1)*0.8*np.sqrt(2*np.pi))) * np.exp(-(np.log(x-1)**2)/(2*0.5**2))

        x_min, x_max = -2, 7

        # -----------------------------
        # Axes
        # -----------------------------
        axes = Axes(
            x_range=[x_min, x_max, 1],
            y_range=[0, 1.5, 0.5],
            x_length=10,
            y_length=4,
            axis_config={"include_numbers": True}
        ).shift(DOWN)

        labels = axes.get_axis_labels(x_label="x", y_label="p(x)")
        self.play(Create(axes), Write(labels))

        # -----------------------------
        # Plot PDF
        # -----------------------------
        pdf_graph = axes.plot(pdf, color=BLUE)
        self.play(Create(pdf_graph))
        self.wait(1)

        # -----------------------------
        # MODE (maximum of PDF)
        # -----------------------------
        xs = np.linspace(x_min, x_max, 2000)
        ys = pdf(xs)
        mode_x = xs[np.argmax(ys)]

        mode_line = axes.get_vertical_line(
            axes.c2p(mode_x, pdf(mode_x)),
            color=RED
        )

        mode_label = Text("Mode", font_size=30, color=RED)\
            .next_to(mode_line, UP)

        self.play(Create(mode_line), Write(mode_label))
        self.wait(1)

        # -----------------------------
        # MEAN (expected value)
        # -----------------------------
        normalization, _ = quad(pdf, x_min, x_max)

        mean_x, _ = quad(lambda x: x * pdf(x), x_min, x_max)
        mean_x /= normalization

        mean_line = axes.get_vertical_line(
            axes.c2p(mean_x, pdf(mean_x)),
            color=YELLOW
        )

        mean_label = Text("Mean", font_size=30, color=YELLOW)\
            .next_to(mean_line, UP)

        self.play(Create(mean_line), Write(mean_label))
        self.wait(1)

        # -----------------------------
        # MEDIAN (50% probability mass)
        # -----------------------------
        cumulative = np.array([
            quad(pdf, x_min, x)[0] / normalization for x in xs
        ])

        median_x = xs[np.argmin(np.abs(cumulative - 0.5))]

        median_line = axes.get_vertical_line(
            axes.c2p(median_x, pdf(median_x)),
            color=GREEN
        )

        median_label = Text("Median", font_size=30, color=GREEN)\
            .next_to(median_line, UP)

        self.play(Create(median_line), Write(median_label))
        self.wait(3)
from manim import *
import numpy as np
from collections import Counter

class MeanMedianModeBar(Scene):
    def construct(self):
        # -----------------------------
        # Data
        # -----------------------------
        data = [2, 3, 3, 5, 7, 8, 8, 8, 10]
        counts = Counter(data)

        values = sorted(counts.keys())
        frequencies = [counts[v] for v in values]

        # -----------------------------
        # Bar chart
        # -----------------------------
        chart = BarChart(
            frequencies,
            bar_names=[str(v) for v in values],
            y_range=[0, max(frequencies) + 1, 1],
            y_length=4,
            x_length=8,
            bar_colors=[BLUE] * len(frequencies)
        )

        chart.to_edge(DOWN)

        title = Text("Mean, Median, Mode", font_size=44).to_edge(UP)

        self.play(Write(title))
        self.play(Create(chart))
        self.wait(1)

        # -----------------------------
        # MODE (highest frequency)
        # -----------------------------
        mode_value = counts.most_common(1)[0][0]
        mode_index = values.index(mode_value)
        mode_bar = chart.bars[mode_index]

        mode_label = Text(f"Mode = {mode_value}", font_size=30, color=RED)\
            .next_to(chart, RIGHT)

        self.play(
            mode_bar.animate.set_color(RED).scale(1.1),
            Write(mode_label)
        )
        self.wait(1)

        # -----------------------------
        # MEDIAN (middle value)
        # -----------------------------
        sorted_data = sorted(data)
        median_value = np.median(sorted_data)
        median_index = values.index(int(median_value))
        median_bar = chart.bars[median_index]

        median_label = Text(f"Median = {median_value}", font_size=30, color=GREEN)\
            .next_to(mode_label, DOWN)

        self.play(
            median_bar.animate.set_color(GREEN),
            Write(median_label)
        )
        self.wait(1)

        # -----------------------------
        # MEAN (average)
        # -----------------------------
        mean_value = np.mean(data)

        mean_arrow = Arrow(
            start=chart.get_bottom() + DOWN * 0.5,
            end=chart.get_bottom() + UP * 0.5,
            color=YELLOW
        ).move_to(chart.x_axis.n2p(mean_value))

        mean_label = Text(f"Mean ≈ {mean_value:.2f}", font_size=30, color=YELLOW)\
            .next_to(median_label, DOWN)

        self.play(
            GrowArrow(mean_arrow),
            Write(mean_label)
        )

        self.wait(3)

class MedianSorting(Scene):
    def construct(self):
        # --------------------------------
        # Raw (unsorted) data
        # --------------------------------
        data = [2, 8, 3, 10, 3, 8, 5, 8, 7]

        title = Text("Finding the Median", font_size=44)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # --------------------------------
        # Display data as boxes (unsorted)
        # --------------------------------
        boxes = VGroup()
        labels = VGroup()

        for val in data:
            box = Square(0.8)
            label = Text(str(val), font_size=32)
            label.move_to(box)
            group = VGroup(box, label)
            boxes.add(group)

        boxes.arrange(RIGHT, buff=0.3).shift(UP * 1)
        self.play(FadeIn(boxes))
        self.wait(1)

        # --------------------------------
        # Sort step-by-step (bubble-sort style)
        # --------------------------------
        sorted_data = sorted(data)
        index_map = {val: [] for val in data}
        for i, val in enumerate(sorted_data):
            index_map[val].append(i)

        target_positions = boxes.copy()
        target_positions.arrange(RIGHT, buff=0.3).shift(DOWN * 1)

        # Create a sorted reference row
        sorted_boxes = VGroup()
        for val in sorted_data:
            box = Square(0.8)
            label = Text(str(val), font_size=32)
            label.move_to(box)
            sorted_boxes.add(VGroup(box, label))

        sorted_boxes.arrange(RIGHT, buff=0.3).shift(DOWN * 1)

        self.play(FadeIn(sorted_boxes))
        self.wait(1)

        # --------------------------------
        # Highlight median
        # --------------------------------
        median_index = len(sorted_data) // 2
        median_value = sorted_data[median_index]

        median_box = sorted_boxes[median_index]
        median_box.set_color(GREEN)

        median_label = Text(
            f"Median = {median_value}",
            font_size=36,
            color=GREEN
        ).next_to(sorted_boxes, DOWN)

        self.play(
            median_box.animate.scale(1.2),
            Write(median_label)
        )

        self.wait(3)

from manim import *
import numpy as np
from collections import Counter

class MeanMedianModeBarChart(Scene):
    def construct(self):
        # -----------------------------
        # Raw data
        # -----------------------------
        data = [2, 8, 3, 10, 3, 8, 5, 8, 7]

        title = Text("Mean, Median, Mode", font_size=44)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # -----------------------------
        # Show unsorted data
        # -----------------------------
        boxes = VGroup()
        for val in data:
            box = Square(0.8)
            label = Text(str(val), font_size=32)
            label.move_to(box)
            boxes.add(VGroup(box, label))

        boxes.arrange(RIGHT, buff=0.3).shift(UP * 1.2)
        self.play(FadeIn(boxes))
        self.wait(1)

        # -----------------------------
        # Sort animation (conceptual)
        # -----------------------------
        sorted_data = sorted(data)
        sorted_boxes = VGroup()

        for val in sorted_data:
            box = Square(0.8)
            label = Text(str(val), font_size=32)
            label.move_to(box)
            sorted_boxes.add(VGroup(box, label))

        sorted_boxes.arrange(RIGHT, buff=0.3).shift(UP * 0.1)

        self.play(Transform(boxes, sorted_boxes))
        self.wait(1)

        # -----------------------------
        # Highlight median
        # -----------------------------
        n = len(sorted_data)
        median_index = n // 2
        median_value = sorted_data[median_index]

        median_box = boxes[median_index]
        median_box.set_color(GREEN)

        median_label = Text(
            f"Median = {median_value}",
            font_size=32,
            color=GREEN
        ).next_to(boxes, DOWN)

        self.play(
            median_box.animate.scale(1.2),
            Write(median_label)
        )
        self.wait(2)

        self.play(FadeOut(boxes), FadeOut(median_label))

        # -----------------------------
        # BarChart construction
        # -----------------------------
        counts = Counter(data)
        values = sorted(counts.keys())
        frequencies = [counts[v] for v in values]

        chart = BarChart(
            frequencies,
            bar_names=[str(v) for v in values],
            y_range=[0, max(frequencies) + 1, 1],
            y_length=4,
            x_length=8,
            bar_colors=[BLUE] * len(values),
        ).to_edge(DOWN)

        self.play(Create(chart))
        self.wait(1)

        # -----------------------------
        # MODE
        # -----------------------------
        mode_value = counts.most_common(1)[0][0]
        mode_index = values.index(mode_value)

        mode_label = Text(
            f"Mode = {mode_value}",
            font_size=30,
            color=RED
        ).next_to(chart, RIGHT)

        self.play(
            chart.bars[mode_index].animate.set_color(RED).scale(1.1),
            Write(mode_label)
        )
        self.wait(1)

        # -----------------------------
        # MEDIAN (BarChart)
        # -----------------------------
        median_bar_index = values.index(median_value)

        median_label_chart = Text(
            f"Median = {median_value}",
            font_size=30,
            color=GREEN
        ).next_to(mode_label, DOWN)

        self.play(
            chart.bars[median_bar_index].animate.set_color(GREEN),
            Write(median_label_chart)
        )
        self.wait(1)

        # -----------------------------
        # MEAN
        # -----------------------------
        mean_value = np.mean(data)

        mean_arrow = Arrow(
            start=chart.get_bottom() + DOWN * 0.5,
            end=chart.get_bottom() + UP * 0.5,
            color=YELLOW
        ).move_to(chart.x_axis.n2p(mean_value))

        mean_label = Text(
            f"Mean ≈ {mean_value:.2f}",
            font_size=30,
            color=YELLOW
        ).next_to(median_label_chart, DOWN)

        self.play(
            GrowArrow(mean_arrow),
            Write(mean_label)
        )

        self.wait(3)
from manim import *
import numpy as np
from collections import Counter

class MeanMedianModeBarChart2(Scene):
    def construct(self):
        # -----------------------------
        # Raw data
        # -----------------------------
        data = [2, 8, 3, 10, 3, 8, 5, 8, 7]

        title = Text("Mean, Median, Mode", font_size=44)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        # -----------------------------
        # Sorting to find median
        # -----------------------------
        boxes = VGroup()
        for val in data:
            box = Square(0.8)
            label = Text(str(val), font_size=32)
            label.move_to(box)
            boxes.add(VGroup(box, label))

        boxes.arrange(RIGHT, buff=0.3).shift(UP * 1.2)
        self.play(FadeIn(boxes))

        sorted_data = sorted(data)
        sorted_boxes = VGroup()
        for val in sorted_data:
            box = Square(0.8)
            label = Text(str(val), font_size=32)
            label.move_to(box)
            sorted_boxes.add(VGroup(box, label))

        sorted_boxes.arrange(RIGHT, buff=0.3).shift(UP * 0.1)
        self.play(Transform(boxes, sorted_boxes))

        median_index = len(sorted_data) // 2
        median_value = sorted_data[median_index]

        boxes[median_index].set_color(GREEN)
        median_label = Text(f"Median = {median_value}", font_size=32, color=GREEN)
        median_label.next_to(boxes, DOWN)

        self.play(
            boxes[median_index].animate.scale(1.2),
            Write(median_label)
        )
        self.wait(2)

        self.play(FadeOut(boxes), FadeOut(median_label))

        # -----------------------------
        # BarChart
        # -----------------------------
        counts = Counter(data)
        values = sorted(counts.keys())
        frequencies = [counts[v] for v in values]

        chart = BarChart(
            frequencies,
            bar_names=[str(v) for v in values],
            y_range=[0, max(frequencies) + 1, 1],
            y_length=4,
            x_length=8,
            bar_colors=[BLUE] * len(values),
        ).to_edge(DOWN)

        self.play(Create(chart))
        self.wait(1)

        # -----------------------------
        # Mode
        # -----------------------------
        mode_value = counts.most_common(1)[0][0]
        mode_index = values.index(mode_value)

        mode_label = Text(f"Mode = {mode_value}", font_size=30, color=RED)
        mode_label.next_to(chart, RIGHT)

        self.play(
            chart.bars[mode_index].animate.set_color(RED).scale(1.1),
            Write(mode_label)
        )
        self.wait(1)

        # -----------------------------
        # Median (on BarChart)
        # -----------------------------
        median_bar_index = values.index(median_value)
        median_label_chart = Text(
            f"Median = {median_value}",
            font_size=30,
            color=GREEN
        ).next_to(mode_label, DOWN)

        self.play(
            chart.bars[median_bar_index].animate.set_color(GREEN),
            Write(median_label_chart)
        )
        self.wait(1)

        # -----------------------------
        # Mean with Balancing Beam
        # -----------------------------
        mean_value = np.mean(data)

        # Pivot
        pivot = Triangle(color=YELLOW, fill_opacity=1)\
            .scale(0.15)\
            .next_to(chart, DOWN, buff=0.1)

        # Beam
        beam = Line(
            LEFT * 3,
            RIGHT * 3,
            stroke_width=6,
            color=YELLOW
        )
        beam.next_to(pivot, UP, buff=0)

        # Mean position marker
        mean_x = chart.x_axis.n2p(mean_value)[0]
        pivot.move_to([mean_x, pivot.get_center()[1], 0])
        beam.move_to(pivot.get_top())

        mean_label = Text(
            f"Mean ≈ {mean_value:.2f}",
            font_size=30,
            color=YELLOW
        ).next_to(median_label_chart, DOWN)

        self.play(
            FadeIn(pivot),
            Create(beam),
            Write(mean_label)
        )

        self.wait(3)
        # -----------------------------
        # Mean with Animated Balancing Beam
        # -----------------------------
        mean_value = np.mean(data)

        # Pivot (triangle)
        pivot = Triangle(color=YELLOW, fill_opacity=1)\
            .scale(0.15)\
            .next_to(chart, DOWN, buff=0.1)

        mean_x = chart.x_axis.n2p(mean_value)[0]
        pivot.move_to([mean_x, pivot.get_center()[1], 0])

        # Beam (initially tilted)
        beam = Line(
            LEFT * 3,
            RIGHT * 3,
            stroke_width=6,
            color=YELLOW
        )

        beam.move_to(pivot.get_top())
        beam.rotate(15 * DEGREES, about_point=pivot.get_top())

        mean_label = Text(
            f"Mean ≈ {mean_value:.2f}",
            font_size=30,
            color=YELLOW
        ).next_to(median_label_chart, DOWN)

        self.play(
            FadeIn(pivot),
            Create(beam),
            Write(mean_label)
        )

        # Animate beam settling (damped oscillation)
        self.play(
            Rotate(
                beam,
                angle=-30 * DEGREES,
                about_point=pivot.get_top(),
                rate_func=rate_functions.ease_in_out_sine
            ),
            run_time=1
        )

        self.play(
            Rotate(
                beam,
                angle=20 * DEGREES,
                about_point=pivot.get_top(),
                rate_func=rate_functions.ease_in_out_sine
            ),
            run_time=0.8
        )

        self.play(
            Rotate(
                beam,
                angle=-5 * DEGREES,
                about_point=pivot.get_top(),
                rate_func=rate_functions.ease_out_sine
            ),
            run_time=0.5
        )

        self.play(
            Rotate(
                beam,
                angle=0 * DEGREES,
                about_point=pivot.get_top()
            ),
            run_time=0.3
        )
        # -----------------------------
        # Outliers can pull the mean
        # -----------------------------
        explanation = Text(
            "Outliers can pull the mean",
            font_size=36,
            color=YELLOW
        ).to_edge(UP)

        self.play(Write(explanation))
        self.wait(1)

        # Original mean
        mean_value = np.mean(data)
        mean_x = chart.x_axis.n2p(mean_value)[0]

        # Pivot & beam (balanced)
        pivot = Triangle(color=YELLOW, fill_opacity=1)\
            .scale(0.15)\
            .next_to(chart, DOWN, buff=0.1)
        pivot.move_to([mean_x, pivot.get_center()[1], 0])

        beam = Line(LEFT * 3, RIGHT * 3, stroke_width=6, color=YELLOW)
        beam.move_to(pivot.get_top())

        self.play(FadeIn(pivot), Create(beam))
        self.wait(1)

        # -----------------------------
        # Add an outlier
        # -----------------------------
        outlier_value = 20
        outlier_bar = chart.add_bar(
            value=1,
            name=str(outlier_value),
            color=ORANGE
        )

        self.play(
            outlier_bar.animate.set_color(ORANGE),
            run_time=1
        )
        self.wait(0.5)

        # New dataset with outlier
        new_data = data + [outlier_value]
        new_mean = np.mean(new_data)
        new_mean_x = chart.x_axis.n2p(new_mean)[0]

        # -----------------------------
        # Beam tilts due to outlier
        # -----------------------------
        self.play(
            Rotate(
                beam,
                angle=-20 * DEGREES,
                about_point=pivot.get_top(),
                rate_func=rate_functions.ease_in_out_sine
            ),
            run_time=1
        )

        # -----------------------------
        # Pivot slides to new mean
        # -----------------------------
        self.play(
            pivot.animate.move_to([new_mean_x, pivot.get_center()[1], 0]),
            beam.animate.rotate(
                20 * DEGREES,
                about_point=pivot.get_top()
            ),
            run_time=2,
            rate_func=rate_functions.ease_in_out_sine
        )

        # Small settling
        self.play(
            Rotate(
                beam,
                angle=-5 * DEGREES,
                about_point=pivot.get_top(),
                rate_func=rate_functions.ease_out_sine
            ),
            run_time=0.4
        )

        self.play(
            Rotate(
                beam,
                angle=0 * DEGREES,
                about_point=pivot.get_top()
            ),
            run_time=0.3
        )

        # -----------------------------
        # Median stays stable
        # -----------------------------
        median_marker = DashedLine(
            chart.x_axis.n2p(median_value) + DOWN * 0.2,
            chart.x_axis.n2p(median_value) + UP * 3,
            color=GREEN
        )

        median_text = Text(
            "Median stays stable",
            font_size=28,
            color=GREEN
        ).next_to(median_marker, UP)

        self.play(Create(median_marker), Write(median_text))
        self.wait(3)
from manim import *
import numpy as np

class MeanAndOutliers(Scene):
    def construct(self):
        # Title
        title = Text("Outliers Can Pull the Mean", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))

        # Number line
        number_line = NumberLine(
            x_range=[-6, 10, 1],
            length=12,
            include_numbers=True
        )
        number_line.shift(DOWN)
        self.play(Create(number_line))

        # Initial data (roughly symmetric distribution)
        data = np.array([-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2])

        dots = VGroup(*[
            Dot(number_line.n2p(x), radius=0.07, color=BLUE)
            for x in data
        ])
        self.play(*[LaggedStart(FadeIn(dot, shift=UP, lag_ratio=0.1) for dot in dots)])
        # self.play(LaggedStartMap(FadeIn, dots, shift=UP, lag_ratio=0.1))

        # Mean calculation
        mean_value = np.mean(data)
        mean_line = always_redraw(
            lambda: DashedLine(
                number_line.n2p(mean_value),
                number_line.n2p(mean_value) + UP * 1.5,
                color=YELLOW
            )
        )

        mean_label = always_redraw(
            lambda: MathTex(r"\text{Mean}").scale(0.7).next_to(mean_line, UP)
        )

        self.play(Create(mean_line), FadeIn(mean_label))
        self.wait(1)

        # Add outliers
        outliers = np.array([7, 8, 9])
        outlier_dots = VGroup(*[
            Dot(number_line.n2p(x), radius=0.07, color=RED)
            for x in outliers
        ])

        outlier_text = Text("Add outliers", font_size=28, color=RED)
        outlier_text.next_to(number_line, DOWN)

        self.play(Write(outlier_text))
        self.play(*[LaggedStart(FadeIn(dot, shift=UP, lag_ratio=0.2) for dot in outlier_dots)])

        # Update data and animate mean shift
        new_data = np.concatenate([data, outliers])
        new_mean = np.mean(new_data)

        self.play(
            mean_line.animate.put_start_and_end_on(
                number_line.n2p(new_mean),
                number_line.n2p(new_mean) + UP * 1.5
            ),
            run_time=2
        )

        # Final emphasis text
        conclusion = Text(
            "Outliers can pull the mean",
            font_size=36,
            color=YELLOW
        )
        conclusion.to_edge(DOWN)

        self.play(Write(conclusion))
        self.wait(2)
from manim import *
import numpy as np

class HistogramMeanOutliers(Scene):
    def construct(self):
        # Title
        title = Text("Outliers Can Pull the Mean", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))

        # Generate initial data
        np.random.seed(1)
        data = np.random.normal(loc=0, scale=1, size=500)

        # Axes
        axes = Axes(
            x_range=[-5, 10, 1],
            y_range=[0, 120, 20],
            x_length=10,
            y_length=4,
            tips=False
        )
        axes.to_edge(DOWN)

        x_label = axes.get_x_axis_label("Value")
        y_label = axes.get_y_axis_label("Frequency")

        self.play(Create(axes), Write(x_label), Write(y_label))

        # Histogram parameters
        bins = np.linspace(-5, 10, 20)
        hist, bin_edges = np.histogram(data, bins=bins)

        bars = VGroup()
        for i, count in enumerate(hist):
            bar = Rectangle(
                width=axes.x_axis.unit_size * (bin_edges[i+1] - bin_edges[i]),
                height=axes.y_axis.unit_size * count,
                fill_color=BLUE,
                fill_opacity=0.7,
                stroke_width=0
            )
            bar.move_to(
                axes.c2p(
                    (bin_edges[i] + bin_edges[i+1]) / 2,
                    count / 2
                )
            )
            bars.add(bar)

        self.play(LaggedStartMap(FadeIn, bars, lag_ratio=0.05))

        # Mean line
        mean = np.mean(data)

        mean_line = DashedLine(
            axes.c2p(mean, 0),
            axes.c2p(mean, axes.y_range[1]),
            color=YELLOW
        )

        mean_label = MathTex(r"\text{Mean}", color=YELLOW).scale(0.7)
        mean_label.next_to(mean_line, UP)

        self.play(Create(mean_line), FadeIn(mean_label))
        self.wait(1)

        # Add outliers
        outliers = np.random.normal(loc=7, scale=0.4, size=50)
        new_data = np.concatenate([data, outliers])

        outlier_text = Text("Add outliers", font_size=28, color=RED)
        outlier_text.next_to(axes, UP)

        self.play(Write(outlier_text))

        # New histogram
        new_hist, _ = np.histogram(new_data, bins=bins)

        new_bars = VGroup()
        for i, count in enumerate(new_hist):
            bar = Rectangle(
                width=axes.x_axis.unit_size * (bin_edges[i+1] - bin_edges[i]),
                height=axes.y_axis.unit_size * count,
                fill_color=BLUE,
                fill_opacity=0.7,
                stroke_width=0
            )
            bar.move_to(
                axes.c2p(
                    (bin_edges[i] + bin_edges[i+1]) / 2,
                    count / 2
                )
            )
            new_bars.add(bar)

        # Animate histogram morph
        self.play(
            Transform(bars, new_bars),
            run_time=2
        )

        # Animate mean shift
        new_mean = np.mean(new_data)
        new_mean_line = DashedLine(
            axes.c2p(new_mean, 0),
            axes.c2p(new_mean, axes.y_range[1]),
            color=YELLOW
        )

        self.play(
            Transform(mean_line, new_mean_line),
            run_time=2
        )

        # Conclusion
        conclusion = Text(
            "Outliers can pull the mean",
            font_size=36,
            color=YELLOW
        )
        conclusion.to_edge(DOWN)

        self.play(Write(conclusion))
        self.wait(2)
from manim import *
import numpy as np

class VisualizationSkew(Scene):
    def construct(self):
        # 1. Create Axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 0.5, 0.1],
            axis_config={"include_tip": False}
        ).scale(0.8)
        
        labels = axes.get_axis_labels(x_label="Value", y_label="Density")

        # 2. Define Distribution Functions
        # Normal (Symmetrical)
        def normal_dist(x):
            return 0.4 * np.exp(-0.5 * (x - 5)**2)

        # Right Skewed (Log-normal style)
        def skewed_dist(x):
            # Shifted and scaled to look skewed on the axes
            if x <= 1: return 0
            return 1.0 * (1/((x-1)*0.8*np.sqrt(2*np.pi))) * np.exp(-(np.log(x-1)**2)/(2*0.5**2))

        # 3. Create Graphs
        normal_graph = axes.plot(normal_dist, color=BLUE)
        skewed_graph = axes.plot(skewed_dist, x_range=[1.1, 9], color=YELLOW)

        # 4. Markers for Central Tendency (Lines and Labels)
        # Normal markers (All at x=5)
        mean_line_norm = axes.get_vertical_line(axes.c2p(5, normal_dist(5)), color=RED)
        mean_label = MathTex(r"\text{Mean}", color=RED).scale(0.6).next_to(mean_line_norm, UP)
        
        # Skewed markers (Mode < Median < Mean)
        # Approximate locations for visual clarity
        mode_x, med_x, mean_x = 2.4, 3.0, 3.8
        
        mode_line_skew = axes.get_vertical_line(axes.c2p(mode_x, skewed_dist(mode_x)), color=PURPLE)
        med_line_skew = axes.get_vertical_line(axes.c2p(med_x, skewed_dist(med_x)), color=GREEN)
        mean_line_skew = axes.get_vertical_line(axes.c2p(mean_x, skewed_dist(mean_x)), color=RED)

        mode_text = Text("Mode", color=PURPLE).scale(0.4).next_to(mode_line_skew, UP)
        med_text = Text("Median", color=GREEN).scale(0.4).next_to(med_line_skew, UP, buff=0.5)
        mean_text = Text("Mean", color=RED).scale(0.4).next_to(mean_line_skew, UP)

        # --- ANIMATION SEQUENCE ---
        self.play(Write(axes), Write(labels))
        self.play(Create(normal_graph))
        self.play(Create(mean_line_norm), Write(mean_label))
        self.wait(1)
        
        self.play(
            Transform(normal_graph, skewed_graph),
            Transform(mean_line_norm, mean_line_skew),
            mean_label.animate.become(mean_text),
            run_time=2
        )
        
        self.play(
            Create(mode_line_skew), Write(mode_text),
            Create(med_line_skew), Write(med_text)
        )
        self.wait(2)

        # Title/Note
        skew_note = Text("Right Skewed: Mode < Median < Mean", font_size=24).to_edge(UP)
        self.play(Write(skew_note))
        self.wait(3)

from manim import *
import numpy as np

class ProbabilitySkewness(Scene):
    def construct(self):
        # 1. Setup Axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 0.6, 0.1],
            axis_config={"include_tip": False}
        ).scale(0.8).to_edge(DOWN)
        
        # 2. Define Distribution Functions
        def normal_func(x):
            return 0.5 * np.exp(-0.5 * (x - 5)**2)

        def right_skew_func(x):
            # Log-normal approximation
            if x <= 2: return 0
            return 1.2 * (1/((x-2)*0.6*np.sqrt(2*np.pi))) * np.exp(-(np.log(x-2)**2)/(2*0.4**2))

        def left_skew_func(x):
            # Mirrored Log-normal
            if x >= 8: return 0
            return 1.2 * (1/((8-x)*0.6*np.sqrt(2*np.pi))) * np.exp(-(np.log(8-x)**2)/(2*0.4**2))

        # 3. Create Graphs
        normal_graph = axes.plot(normal_func, color=BLUE)
        right_graph = axes.plot(right_skew_func, x_range=[2.1, 9.5], color=YELLOW)
        left_graph = axes.plot(left_skew_func, x_range=[0.5, 7.9], color=GREEN)

        # 4. Markers and Labels
        title = Text("Symmetrical (Normal)", font_size=32).to_edge(UP)
        
        # We will use VGroup to manage the markers (Mean, Median, Mode)
        mean_line = Line(axes.c2p(5, 0), axes.c2p(5, 0.5), color=RED)
        mean_lbl = Text("Mean", color=RED).scale(0.4).next_to(mean_line, UP)
        
        median_line = Line(axes.c2p(5, 0), axes.c2p(5, 0.5), color=WHITE)
        median_lbl = Text("Median", color=WHITE).scale(0.4).next_to(median_line, UP, buff=0.4)
        
        mode_line = Line(axes.c2p(5, 0), axes.c2p(5, 0.5), color=PURPLE)
        mode_lbl = Text("Mode", color=PURPLE).scale(0.4).next_to(mode_line, UP, buff=0.7)

        # --- ANIMATION ---
        
        # Scene 1: Normal
        self.play(Write(axes), Create(normal_graph), Write(title))
        self.play(Create(mean_line), Write(mean_lbl))
        self.wait(1)

        # Scene 2: Transition to Right Skewed
        # Locations: Mode (peak) < Median < Mean (tail)
        new_title_right = Text("Right Skewed (Positive)", font_size=32, color=YELLOW).to_edge(UP)
        
        self.play(
            Transform(normal_graph, right_graph),
            Transform(title, new_title_right),
            mean_line.animate.move_to(axes.c2p(4.2, 0.15)), # Shift to tail
            mean_lbl.animate.next_to(axes.c2p(4.2, 0.3), UP),
            run_time=2
        )
        
        # Reveal Mode and Median for Right Skew
        mode_line_r = Line(axes.c2p(3.1, 0), axes.c2p(3.1, 0.55), color=PURPLE)
        med_line_r = Line(axes.c2p(3.5, 0), axes.c2p(3.5, 0.4), color=WHITE)
        
        self.play(Create(mode_line_r), Create(med_line_r))
        self.wait(2)

        # Scene 3: Transition to Left Skewed
        # Locations: Mean (tail) < Median < Mode (peak)
        new_title_left = Text("Left Skewed (Negative)", font_size=32, color=GREEN).to_edge(UP)
        
        self.play(
            Transform(normal_graph, left_graph),
            Transform(title, new_title_left),
            mean_line.animate.move_to(axes.c2p(5.8, 0.15)), # Shift to left tail
            mean_lbl.animate.next_to(axes.c2p(5.8, 0.3), UP),
            mode_line_r.animate.move_to(axes.c2p(6.9, 0.27)), # Shift to right peak
            med_line_r.animate.move_to(axes.c2p(6.5, 0.2)), # Middle
            run_time=2
        )
        self.wait(3)

class NormalDistributionHistogramPDF(Scene):
    def construct(self):
        # Parameters
        mu = 0
        sigma = 1
        samples = 5000
        bins = 30

        # Generate data
        data = np.random.normal(mu, sigma, samples)

        # Histogram (density normalized)
        counts, bin_edges = np.histogram(data, bins=bins, density=True)
        bin_width = bin_edges[1] - bin_edges[0]

        # Axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, max(counts) * 1.3, 0.1],
            x_length=10,
            y_length=5,
            tips=False
        )

        labels = axes.get_axis_labels(
            x_label=Tex("x"),
            y_label=Tex("f(x)")
        )

        # Histogram bars
        bars = VGroup()
        for count, left_edge in zip(counts, bin_edges[:-1]):
            bar = Rectangle(
                width=axes.x_axis.unit_size * bin_width,
                height=axes.y_axis.unit_size * count,
                fill_color=BLUE,
                fill_opacity=0.7,
                stroke_width=0
            )
            bar.move_to(
                axes.c2p(
                    left_edge + bin_width / 2,
                    count / 2
                )
            )
            bars.add(bar)

        # Normal PDF curve
        pdf_curve = axes.plot(
            lambda x: norm.pdf(x, mu, sigma),
            x_range=[-4, 4],
            color=RED,
            stroke_width=4
        )

        pdf_label = Tex(
            r"$\mathcal{N}(0,1)$ PDF",
            color=RED
        ).scale(0.8).next_to(pdf_curve, UP)

        # Title
        title = Text("Normal Distribution Histogram with PDF", font_size=36)
        title.to_edge(UP)

        # Animations
        self.play(Create(axes), Write(labels))
        self.play(Write(title))
        self.play(*[LaggedStart(GrowFromEdge(bar, edge=DOWN, lag_ratio=0.03) for bar in bars)])
        # self.play(LaggedStartMap(GrowFromEdge, bars, edge=DOWN, lag_ratio=0.03))
        self.wait(0.5)
        self.play(Create(pdf_curve), FadeIn(pdf_label))
        self.wait(2)

