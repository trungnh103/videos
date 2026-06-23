from manim import *
import numpy as np
from pi_creature_scene import *

class NormalDistributionHistogram(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/std1.mp3")
        # Parameters
        mu = 0          # mean
        sigma = 1       # standard deviation
        samples = 5000
        bins = 30

        # Generate normal distribution samples
        data = np.random.normal(mu, sigma, samples)

        # Compute histogram
        counts, bin_edges = np.histogram(data, bins=bins, density=True)
        bin_width = bin_edges[1] - bin_edges[0]

        # Axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, max(counts) * 1.2, 0.1],
            x_length=10,
            y_length=5,
            y_axis_config={"stroke_opacity": 0},
            x_axis_config={"include_ticks": False, "stroke_opacity": 0},
            tips=False
        )

        bars = VGroup()
        for count, left_edge in zip(counts, bin_edges[:-1]):
            bar = Rectangle(
                width=axes.x_axis.unit_size * bin_width,
                height=axes.y_axis.unit_size * count,
                fill_color=BLUE,
                fill_opacity=0.8,
                stroke_width=0
            )
            bar.move_to(
                axes.c2p(
                    left_edge + bin_width / 2,
                    count / 2
                )
            )
            bars.add(bar)

        # Title
        title_mmm = Text("Trung bình, Trung vị và Mode", font="Noto Sans", font_size=36)
        title_mmm.to_edge(UP)
        title_st = Text("Phương sai & Độ lệch chuẩn", font="Noto Sans", font_size=36)
        title_st[:9].set_color(YELLOW)
        title_st[10:].set_color(BLUE)
        title_st.to_edge(UP)
        arrow_leftright = Arrow(LEFT, RIGHT).shift(3*LEFT)
        arrow_rightleft = Arrow(RIGHT, LEFT).shift(3*RIGHT)
        arrow_leftleft = Arrow(RIGHT, LEFT).shift(3*LEFT)
        arrow_rightright = Arrow(LEFT, RIGHT).shift(3*RIGHT)

        # Animations
        self.add(axes)
        # self.play(FadeIn(title_mmm))
        self.play(FadeIn(title_mmm), *[LaggedStart(GrowFromEdge(bar, edge=DOWN, lag_ratio=0.01) for bar in bars)])
        self.play(FadeIn(arrow_leftright, shift=RIGHT), FadeIn(arrow_rightleft, shift=LEFT))
        self.wait()
        self.play(FadeOut(arrow_leftright), FadeOut(arrow_rightleft),
                  FadeOut(title_mmm, shift=DOWN), FadeIn(title_st))
        self.play(FadeIn(arrow_leftleft, shift=LEFT), FadeIn(arrow_rightright, shift=RIGHT), run_time=2)
            
        self.wait(3)

class VisualizingDeviationComparison(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/std2.mp3")
        # --- Setup ---
        # Main Title
        main_title = Text("Cùng giá trị trung bình, độ lệch chuẩn khác nhau", font="Noto Sans", font_size=32).to_edge(UP)
        mean_value_text = Text("Trung bình = 30", font="Noto Sans", font_size=24, color=RED)
        per_day = Text("/ngày", font="Noto Sans", font_size=24, color=RED)
        coffee = PiCreature().scale(0.15).set_color(DARK_BROWN)
        mean_value_label = VGroup(mean_value_text, coffee, per_day).arrange(RIGHT, SMALL_BUFF).next_to(main_title, DOWN)
        # 1. Create Number Lines (Axes) for side-by-side comparison
        # Range from 0 to 60 to accommodate the 5 and 55 extremes
        axis_config = {"include_tip": False, "numbers_to_exclude": [30]} # Exclude 30 to mark it specially later
        
        line_a = NumberLine(x_range=[0, 60, 10], length=5, font_size=20, **axis_config).to_edge(LEFT, buff=1).shift(DOWN)
        line_b = NumberLine(x_range=[0, 60, 10], length=5, font_size=20, **axis_config).to_edge(RIGHT, buff=1).shift(DOWN)

        # Labels for the lines
        label_a_title = Text("Quán A: Độ lệch thấp", font="Noto Sans", font_size=24, color=BLUE).next_to(line_a, UP, buff=1.5)
        label_a_desc = Text("(Thường xuyên ở mức 29-31)", font="Noto Sans", font_size=18, color=GRAY).next_to(label_a_title, DOWN)
        
        label_b_title = Text("Quán B: Độ lệch cao", font="Noto Sans", font_size=24, color=ORANGE).next_to(line_b, UP, buff=1.5)
        label_b_desc = Text("(Dao động mạnh: 5 đến 55)", font="Noto Sans", font_size=18, color=GRAY).next_to(label_b_title, DOWN)

        # Mark the Shared Mean (30) on both lines
        mean_mark_a = Line(line_a.n2p(30) + UP*0.5, line_a.n2p(30) + DOWN*0.5, color=RED, stroke_width=3)
        mean_mark_b = Line(line_b.n2p(30) + UP*0.5, line_b.n2p(30) + DOWN*0.5, color=RED, stroke_width=3)
        mean_num_a = Text("30", color=RED, font_size=20).next_to(mean_mark_a, DOWN)
        mean_num_b = Text("30", color=RED, font_size=20).next_to(mean_mark_b, DOWN)

        # --- Data Points (Daily Sales) ---
        # Shop A: Tightly clustered around 30
        data_a = [29, 30, 31, 29.5, 30.5, 30, 31] 
        # Use slight y-offsets to prevent dots from overlapping perfectly
        dots_a = VGroup(*[Dot(line_a.n2p(x) + UP*np.random.uniform(-0.2, 0.2), color=BLUE, radius=0.08) for x in data_a])

        # Shop B: Spread out, including extremes 5 and 55
        data_b = [5, 55, 30, 20, 40, 15, 45]
        dots_b = VGroup(*[Dot(line_b.n2p(x) + UP*np.random.uniform(-0.2, 0.2), color=ORANGE, radius=0.08) for x in data_b])


        # --- Animation Sequence ---
        
        # 1. Setup the stage
        self.play(Write(main_title), Write(mean_value_label))
        self.play(
            Create(line_a), Create(line_b),
            Write(label_a_title), Write(label_a_desc),
            Write(label_b_title), Write(label_b_desc)
        )
        
        # 2. Show the shared Mean
        self.play(
            Create(mean_mark_a), Write(mean_num_a),
            Create(mean_mark_b), Write(mean_num_b)
        )
        self.wait(0.5)

        # 3. Plot Shop A (Low Deviation)
        self.play(LaggedStartMap(GrowFromCenter, dots_a, lag_ratio=0.1), run_time=1.5)
        
        # Highlight tightness with a bracket or box
        tight_box = SurroundingRectangle(dots_a, color=BLUE, buff=0.2, fill_color=BLUE, fill_opacity=0.1)
        self.play(Create(tight_box))
        self.wait(1)

        # 4. Plot Shop B (High Deviation)
        # Show extremes first for emphasis
        dot_5 = dots_b[0]
        dot_55 = dots_b[1]
        label_5 = Text("5!", font_size=16).next_to(dot_5, DOWN)
        label_55 = Text("55!", font_size=16).next_to(dot_55, DOWN)

        self.play(GrowFromCenter(dot_5), Write(label_5))
        self.play(GrowFromCenter(dot_55), Write(label_55))
        
        # Fill in the rest
        remaining_dots_b = VGroup(*dots_b[2:])
        self.play(LaggedStartMap(GrowFromCenter, remaining_dots_b, lag_ratio=0.1))

        # Highlight spread with a wider box
        wide_box = SurroundingRectangle(dots_b, color=ORANGE, buff=0.2, fill_color=ORANGE, fill_opacity=0.1)
        self.play(Create(wide_box))

        self.wait(4)

class VarianceSDFormulas(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/std3.mp3")
        # 1. Title
        title = Text("Định nghĩa Phương sai và Độ lệch chuẩn", font="Noto Sans", font_size=36).to_edge(UP)
        title[9:18].set_color(YELLOW)
        title[20:].set_color(BLUE)
        self.play(Write(title))
        self.wait(0.5)

        # 2. Variance Section
        var_title = Text("Phương sai (\u03c3\u00b2)", font="Noto Sans", color=YELLOW, font_size=32).shift(UP * 2)
        var_formula = MathTex(
            r"\sigma^2 = \frac{\sum_{i=1}^{N} (x_i - \mu)^2}{N}",
            color=YELLOW
        ).scale(1.2)

        self.play(Write(var_title))
        self.play(Write(var_formula))
        self.wait(1)

        # Annotations for Variance
        annotations = VGroup(
            VGroup(MathTex(r"x_i = ", font_size=24), Text("Mỗi giá trị", font="Noto Sans").scale(0.3)).arrange(RIGHT),
            VGroup(MathTex(r"\mu = ", font_size=24), Text("Trung bình", font="Noto Sans").scale(0.3)).arrange(RIGHT),
            VGroup(MathTex(r"N = ", font_size=24), Text("Tổng số", font="Noto Sans").scale(0.3)).arrange(RIGHT)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT, buff=1.5)

        # Draw a box around the squared part to explain why it's squared
        squared_part = SurroundingRectangle(var_formula[0][7:13], color=WHITE, buff=0.1)
        squared_note = Text("Bình phương để khoảng cách trở thành số dương", font="Noto Sans", font_size=20).next_to(squared_part, DOWN, buff=0.5)

        self.play(Write(annotations))
        self.wait(2)
        self.play(Create(squared_part), Write(squared_note))
        self.wait(3)
        coffee = PiCreature().scale(0.25).set_color(DARK_BROWN)
        coffee.next_to(var_title, RIGHT).shift(2*RIGHT)
        squared = Text("2", font_size=36, weight=BOLD).next_to(coffee, UR, SMALL_BUFF)
        self.play(FadeIn(coffee), FadeIn(squared))
        self.wait(2)
        self.play(coffee.animate.change_mode("confused"))
        # self.play(FadeOut(coffee), FadeOut(squared))
        self.wait()
        self.play(FadeOut(squared_part), FadeOut(squared_note))

        # 3. Transition to Standard Deviation
        sd_title = Text("Độ lệch chuẩn (\u03c3)", font="Noto Sans", color=BLUE, font_size=32).shift(UP * 2)
        
        # Show that SD is just the root of Variance
        root_relation = MathTex(
            r"\sigma = \sqrt{\sigma^2}",
            color=BLUE
        ).scale(1.2).move_to(ORIGIN)

        self.play(
            FadeOut(var_title),
            ReplacementTransform(var_formula, root_relation),
            Write(sd_title)
        )
        self.wait(1)

        # Full SD Formula
        sd_formula_full = MathTex(
            r"\sigma = \sqrt{\frac{\sum_{i=1}^{N} (x_i - \mu)^2}{N}}",
            color=BLUE
        ).scale(1.2).move_to(ORIGIN)

        self.play(ReplacementTransform(root_relation, sd_formula_full))
        
        unit_note = Text("Đơn vị hiện đã trở lại bình thường!", font="Noto Sans", color=BLUE, font_size=24).next_to(sd_formula_full, DOWN, buff=0.8)
        self.play(Write(unit_note))
        self.wait(2)
        self.play(FadeOut(squared))
        self.play(coffee.animate.change_mode("happy"))
        
        self.wait(3)

class HistogramSameMeanDifferentStd(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/std4.mp3")
        explain_text = Text("Trung bình, mỗi điểm dữ liệu \nnằm cách giá trị trung bình bao xa", font="Noto Sans")
        self.play(Write(explain_text), run_time=2)
        self.wait()
        self.play(FadeOut(explain_text))
        mu = 0
        sigma1 = 0.8
        sigma2 = 1.8
        samples = 4000
        bins = 35

        data1 = np.random.normal(mu, sigma1, samples)
        data2 = np.random.normal(mu, sigma2, samples)

        counts1, edges = np.histogram(data1, bins=bins, density=True)
        counts2, _ = np.histogram(data2, bins=edges, density=True)
        bin_width = edges[1] - edges[0]

        axes = Axes(
            x_range=[-6, 6, 1],
            y_range=[0, max(max(counts1), max(counts2)) * 1.3, 0.1],
            x_length=10,
            y_length=5,
            y_axis_config={"stroke_opacity": 0},
            x_axis_config={"include_ticks": False, "stroke_opacity": 0},
            tips=False
        )

        bars1 = VGroup()
        bars2 = VGroup()

        for c1, c2, left in zip(counts1, counts2, edges[:-1]):
            bar1 = Rectangle(
                width=axes.x_axis.unit_size * bin_width,
                height=axes.y_axis.unit_size * c1,
                fill_color=BLUE,
                fill_opacity=0.5,
                stroke_width=0
            ).move_to(axes.c2p(left + bin_width / 2, c1 / 2))

            bar2 = Rectangle(
                width=axes.x_axis.unit_size * bin_width,
                height=axes.y_axis.unit_size * c2,
                fill_color=RED,
                fill_opacity=0.5,
                stroke_width=0
            ).move_to(axes.c2p(left + bin_width / 2, c2 / 2))

            bars1.add(bar1)
            bars2.add(bar2)

        # PDF function
        def pdf(x, sigma):
            return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-x**2 / (2 * sigma**2))

        curve1 = axes.plot(lambda x: pdf(x, sigma1), color=BLUE)
        curve2 = axes.plot(lambda x: pdf(x, sigma2), color=RED)
        # Legend
        legend = VGroup(
            Tex(rf"$\sigma = {sigma1}$", color=BLUE),
            Tex(rf"$\sigma = {sigma2}$", color=RED)
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UR)
        # Title
        title = Text("Hai tập dữ liệu: Cùng giá trị trung bình, \nnhưng độ phân tán khác nhau.", font="Noto Sans", font_size=36)
        title.to_corner(UL)

        self.play(FadeIn(title))
        self.play(
            Create(axes),
            LaggedStart(
                *[LaggedStart(GrowFromEdge(bar, edge=DOWN) for bar in bars1)],
                lag_ratio=0.2
            )
        )
        self.wait(2)
        self.play(
            LaggedStart(
                *[LaggedStart(GrowFromEdge(bar, edge=DOWN) for bar in bars2)],
                lag_ratio=0.2
            )
        )
        self.wait()
        self.play(Create(curve1), Create(curve2))
        self.play(FadeIn(legend))
        self.wait(2)

class VarianceAndStandardDeviation(Scene):
    def construct(self):
        self.wait()
        
        # 1. Setup Data & Axes
        data = [15, 20, 25]
        mean_val = np.mean(data) # 20.0
        
        # Use a number line for simplicity
        number_line = NumberLine(
            x_range=[10, 30, 5],
            length=10,
            # include_numbers=True,
            font_size=24
        ).to_edge(DOWN, buff=1.5)
        
        # Plot points
        points = VGroup(*[
            Dot(number_line.n2p(x), color=BLUE, radius=0.12).set_z_index(3)
            for x in data
        ])
        point_labels = VGroup(*[
            Text(str(x), font_size=20).next_to(p, DOWN)
            for x, p in zip(data, points)
        ])

        title = Text("Tính Phương sai và Độ lệch chuẩn", font="Noto Sans", font_size=36).to_edge(UP)
        self.play(FadeIn(title))
        self.add_sound("voiceovers/std5_part1.mp3")
        self.wait(3)
        self.play(Create(number_line), FadeIn(point_labels))
        for point in points:
            self.add_sound("voiceovers/click.wav")
            self.play(FadeIn(point), run_time=0.5)
        self.wait()

        # 2. Show the Mean
        mean_line = Line(
            number_line.n2p(mean_val) + UP*2,
            number_line.n2p(mean_val) + DOWN*0.5,
            color=RED,
            stroke_width=4
        )
        mean_label = Text(f"Trung bình (μ) = {mean_val:.0f}", font="Noto Sans", color=RED, font_size=24).next_to(mean_line, UP)
        
        self.play(Create(mean_line), Write(mean_label))
        self.wait(1)

        # 3. Show Deviations (Step 1)
        self.add_sound("voiceovers/std5_part2.mp3")
        step1_title = Text("Bước 1: Tìm độ lệch (khoảng cách so với giá trị trung bình)", font="Noto Sans", font_size=28, color=YELLOW).next_to(title, DOWN)
        self.play(Write(step1_title))

        deviation_lines = VGroup()
        deviation_labels = VGroup()
        line_indices = [] # To keep track of which point has a line

        for i, (x, p) in enumerate(zip(data, points)):
            diff = x - mean_val
            if diff == 0: continue # Skip the mean point for lines

            start = p.get_center()
            end = number_line.n2p(mean_val)
            # Adjust y-position to be above the number line
            start[1] = number_line.get_y() + 0.5
            end[1] = number_line.get_y() + 0.5
            
            line = Arrow(start, end, buff=0, color=YELLOW, stroke_width=3, tip_length=0.15)
            label = MathTex(f"{diff:+.0f}", color=YELLOW, font_size=24).next_to(line, UP)
            
            deviation_lines.add(line)
            deviation_labels.add(label)
            line_indices.append(i)

        self.play(Create(deviation_lines), Write(deviation_labels))
        self.wait(1)

        # 4. Square the Deviations (Step 2)
        self.add_sound("voiceovers/std5_part3.mp3")
        step2_title = Text("Bước 2: Bình phương các độ lệch (Làm cho chúng trở thành số dương)", font="Noto Sans", font_size=28, color=YELLOW).next_to(title, DOWN)
        self.play(ReplacementTransform(step1_title, step2_title))
        
        # Show why we square: sum of deviations is zero
        sum_of_devs = Text("Tổng độ lệch = -5 + 0 + 5 = 0", font="Noto Sans", font_size=24, color=RED).to_corner(UR).shift(DOWN*0.5)
        self.play(Write(sum_of_devs))
        self.wait(1)
        self.play(FadeOut(sum_of_devs))
        
        squares = VGroup()
        square_labels = VGroup()
        scale_factor = 0.3 # Scale down squares to fit on screen
        
        line_counter = 0
        for i, (x, p) in enumerate(zip(data, points)):
            diff = x - mean_val
            side_length = abs(diff) * scale_factor
            
            if side_length > 0:
                square = Square(side_length=side_length, color=YELLOW, fill_opacity=0.3, stroke_width=2)
                # Position square next to its point
                if diff < 0:
                    square.next_to(number_line.n2p(x), UP, buff=0).shift(RIGHT*side_length/2)
                else:
                    square.next_to(number_line.n2p(x), UP, buff=0).shift(LEFT*side_length/2)
                
                label = MathTex(f"({diff:+.0f})^2 = {diff**2:.0f}", font_size=20, color=YELLOW).next_to(square, UP)
                squares.add(square)
                square_labels.add(label)
                
                # Animate: Fade out line, fade in square
                self.play(
                    FadeOut(deviation_lines[line_counter]),
                    FadeOut(deviation_labels[line_counter]),
                    FadeIn(square),
                    Write(label),
                    run_time=0.5
                )
                line_counter += 1

        self.wait(1)

        # 5. Calculate Variance (Step 3)
        self.add_sound("voiceovers/std5_part4.mp3")
        step3_title = Text("Bước 3: Tìm bình phương trung bình (phương sai)", font="Noto Sans", font_size=28, color=GREEN).next_to(title, DOWN)
        self.play(ReplacementTransform(step2_title, step3_title))
        
        # Formula visual
        variance_formula = MathTex(
            r"\sigma^2 = \frac{25 + 0 + 25}{3} \approx 16.7",
            color=GREEN
        ).to_corner(UR).shift(1.5*DOWN)
        
        # "Gathering" animation: merge squares into one "average" square in the center
        variance_square_side = np.sqrt(16.7) * scale_factor
        variance_square = Square(side_length=variance_square_side, color=GREEN, fill_opacity=0.5)\
            .move_to(number_line.n2p(mean_val) + UP*1.5)
        variance_label = Text("Diện tích trung bình (Phương sai)\n≈ 16.7", font="Noto Sans", font_size=20, color=GREEN).move_to(variance_square)
        
        self.play(
            Write(variance_formula),
            Transform(squares, variance_square),
            FadeOut(square_labels)
        )
        self.play(Write(variance_label))
        
        units_note = Text("Đơn vị được bình phương!", font="Noto Sans", font_size=18, color=GRAY).next_to(variance_square, DOWN)
        self.play(Write(units_note))
        self.wait(2)

        # 6. Calculate Standard Deviation (Step 4)
        self.add_sound("voiceovers/std5_part5.mp3")
        step4_title = Text("Bước 4: Lấy căn bậc hai (Độ lệch chuẩn)", font="Noto Sans", font_size=28, color=BLUE).next_to(title, DOWN)
        self.play(ReplacementTransform(step3_title, step4_title), FadeOut(units_note))
        
        # Formula visual
        std_dev_formula = MathTex(
            r"\sigma = \sqrt{16.7} \approx 4.1",
            color=BLUE
        ).next_to(variance_formula, DOWN)
        
        # "Rooting" animation: transform square area into a side length line
        std_dev_val = np.sqrt(16.7)
        
        # A line representing one std dev length to the right
        std_dev_line_right = Arrow(
            number_line.n2p(mean_val),
            number_line.n2p(mean_val + std_dev_val),
            buff=0, color=BLUE, stroke_width=4
        ).shift(UP*0.2)
        
        std_dev_label_r = Text("+1σ (≈4.1)", font="Noto Sans", font_size=18, color=BLUE).next_to(std_dev_line_right, UP)
        
        self.play(
            Write(std_dev_formula),
            # Visually collapse the square into its side length
            ReplacementTransform(squares, std_dev_line_right), 
            FadeOut(variance_label)
        )
        self.play(Write(std_dev_label_r))
        
        # Final note on units
        final_note = Text("Đơn vị đã trở lại bình thường.\nĐây là khoảng cách 'điển hình' so với giá trị trung bình.", font="Noto Sans", font_size=18, color=GRAY)\
            .next_to(std_dev_line_right, DOWN, buff=0.5).shift(LEFT*1.5).align_to(std_dev_line_right, LEFT)
        self.play(Write(final_note), run_time=3)

        self.wait(5)

class EmpiricalRuleVisualization(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/std6.mp3")
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 0.45, 0.1],
            x_length=12,
            y_length=6,
            y_axis_config={"stroke_opacity": 0},
            axis_config={"include_tip": False, "numbers_to_exclude": range(-4, 5)}
        ).to_edge(DOWN, buff=1)

        # Define Standard Normal PDF (mu=0, sigma=1)
        def normal_pdf(x):
            return (1 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * x**2)

        curve = axes.plot(normal_pdf, color=WHITE, stroke_width=3)

        # Title
        title = Text("Quy tắc 68-95-99,7 (thực nghiệm)", font="Noto Sans", font_size=36).to_edge(UP)
        title[6:8].set_color(BLUE)
        title[9:11].set_color(TEAL)
        title[12:16].set_color(YELLOW)
        explain_text = Text("Là một cách viết tắt dùng để ghi nhớ \ntỷ lệ phần trăm các giá trị \nnằm trong các khoảng cụ thể của Phân phối Chuẩn.", font="Noto Sans").scale(0.65)

        self.play(Write(title))
        self.wait(4)
        self.play(Write(explain_text), run_time=3)
        self.wait()
        self.play(FadeOut(explain_text))
        self.wait()
        self.play(Create(axes), Create(curve), run_time=2)

        mean_line = axes.get_vertical_line(axes.c2p(0, normal_pdf(0)), color=RED, stroke_width=2)
        mean_label = MathTex(r"\mu", color=RED, font_size=32).next_to(axes.c2p(0, 0), DOWN)
        self.play(Create(mean_line), Write(mean_label))
        self.wait()
        self.play(Indicate(mean_label))
        self.wait(3)
        bell = SVGMobject("assets/bell.svg").move_to(curve)
        self.play(FadeIn(bell))
        self.wait()
        self.play(FadeOut(bell))

        # --- 2. The 68% Region (1 Sigma) ---
        # Vertical markers
        line_n1 = axes.get_vertical_line(axes.c2p(-1, normal_pdf(-1)), color=GRAY)
        line_p1 = axes.get_vertical_line(axes.c2p(1, normal_pdf(1)), color=GRAY)
        
        # Axis labels
        label_n1 = MathTex(r"\mu - 1\sigma", font_size=24).next_to(axes.c2p(-1, 0), DOWN)
        label_p1 = MathTex(r"\mu + 1\sigma", font_size=24).next_to(axes.c2p(1, 0), DOWN)

        # Shaded Area
        area_68 = axes.get_area(curve, x_range=[-1, 1], color=BLUE, opacity=0.5)
        text_68 = Text("68%", font_size=28, color=WHITE).move_to(axes.c2p(0, 0.15))

        # Animation Step 1
        self.play(Create(line_n1), Create(line_p1), Write(label_n1), Write(label_p1))
        self.play(FadeIn(area_68), Write(text_68))
        self.wait(1.5)


        # --- 3. The 95% Region (2 Sigma) ---
        # Vertical markers
        line_n2 = axes.get_vertical_line(axes.c2p(-2, normal_pdf(-2)), color=GRAY)
        line_p2 = axes.get_vertical_line(axes.c2p(2, normal_pdf(2)), color=GRAY)
        
        # Axis labels
        label_n2 = MathTex(r"\mu - 2\sigma", font_size=24).next_to(axes.c2p(-2, 0), DOWN)
        label_p2 = MathTex(r"\mu + 2\sigma", font_size=24).next_to(axes.c2p(2, 0), DOWN)

        # Shaded Area (Wider layer on top)
        area_95 = axes.get_area(curve, x_range=[-2, 2], color=TEAL, opacity=0.4)
        text_95 = Text("95%", font_size=28, color=WHITE).move_to(axes.c2p(0, 0.25))
        
        # Use arrows to show the expansion
        arrow_left = Arrow(start=axes.c2p(-1, 0.05), end=axes.c2p(-2, 0.05), buff=0, color=TEAL)
        arrow_right = Arrow(start=axes.c2p(1, 0.05), end=axes.c2p(2, 0.05), buff=0, color=TEAL)

        # Animation Step 2
        self.play(
            Create(line_n2), Create(line_p2), 
            Write(label_n2), Write(label_p2),
            FadeOut(text_68) # Make room for new text
        )
        self.play(
            FadeIn(area_95),
            GrowArrow(arrow_left), GrowArrow(arrow_right),
            Write(text_95)
        )
        self.play(FadeOut(arrow_left), FadeOut(arrow_right))
        self.wait(1.5)


        # --- 4. The 99.7% Region (3 Sigma) ---
        # Vertical markers
        line_n3 = axes.get_vertical_line(axes.c2p(-3, normal_pdf(-3)), color=GRAY)
        line_p3 = axes.get_vertical_line(axes.c2p(3, normal_pdf(3)), color=GRAY)
        
        # Axis labels
        label_n3 = MathTex(r"-3\sigma", font_size=24).next_to(axes.c2p(-3, 0), DOWN)
        label_p3 = MathTex(r"+3\sigma", font_size=24).next_to(axes.c2p(3, 0), DOWN)

        # Shaded Area (Widest layer)
        area_997 = axes.get_area(curve, x_range=[-3, 3], color=YELLOW, opacity=0.3)
        text_997 = Text("99.7%", font_size=28, color=WHITE).move_to(axes.c2p(0, 0.35))

        # Animation Step 3
        self.play(
            Create(line_n3), Create(line_p3),
            Write(label_n3), Write(label_p3),
            FadeOut(text_95)
        )
        self.play(FadeIn(area_997), Write(text_997))
        
        # Final Note
        note = Text("Hầu hết các dữ liệu đều nằm trong phạm vi 3 độ lệch chuẩn.", font="Noto Sans", font_size=20, color=GRAY)\
            .to_edge(DOWN, buff=0.1)
        self.play(Write(note))
        self.wait(2)
        spreadsheet = ImageMobject("assets/spreadsheet.png")
        spreadsheet.scale(0.25).to_corner(UR, LARGE_BUFF).shift(DOWN)
        self.play(FadeIn(spreadsheet))
        self.wait(3)
        self.play(FadeOut(spreadsheet))
        self.play(Indicate(title[6:16]), run_time=3)
        look_closely = SVGMobject("assets/look_closely.svg").to_corner(UR, LARGE_BUFF)
        self.play(FadeIn(look_closely))
        self.wait(3)

class HeightDistribution_std(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/std7_part1.mp3")
        # 1. Setup Parameters
        mu = 175
        sigma = 7
        
        # 2. Define Axes
        # x_range covers roughly 4 standard deviations from the mean
        axes = Axes(
            x_range=[145, 205, 7],
            y_range=[0, 0.07, 0.01],
            x_length=10,
            y_length=5,
            axis_config={"include_tip": False}
        ).to_edge(DOWN, buff=1)
        
        # Add labels to the x-axis for specific cm values
        axes.add_coordinates()
        x_label = Text("Chiều cao (cm)", font="Noto Sans", font_size=24).next_to(axes.x_axis, DOWN, buff=0.7)

        # 3. Define Normal PDF
        def height_pdf(x):
            return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma)**2)

        curve = axes.plot(height_pdf, color=WHITE)
        title = Text("Phân bố chiều cao của nam giới trưởng thành", font="Noto Sans", font_size=36).to_edge(UP)

        self.play(Write(title), Create(axes), Write(x_label))
        self.play(Create(curve), run_time=2)

        # 4. Vertical Line for the Mean
        mean_line = axes.get_vertical_line(axes.c2p(mu, height_pdf(mu)), color=RED)
        mean_text = Text(f"Trung bình = {mu}cm", font="Noto Sans", color=RED, font_size=20).next_to(mean_line, UP)
        self.play(Create(mean_line), Write(mean_text))
        self.wait()
        std_text = Text(f"Độ lệch chuẩn = {sigma}cm", font="Noto Sans", color=BLUE, font_size=20).next_to(mean_text, RIGHT)
        self.play(Write(std_text))
        self.wait()
        rule = Text("Quy tắc 68-95-99,7", font="Noto Sans", font_size=28).next_to(title, DOWN)
        self.play(Write(rule))
        self.wait(3)
        # 5. Highlight 68% (168cm to 182cm)
        area_68 = axes.get_area(curve, x_range=[168, 182], color=BLUE, opacity=0.4)
        label_68 = Text("68% nam giới\n(168 - 182cm)", font="Noto Sans", font_size=20).move_to(axes.c2p(mu, 0.02))
        
        self.play(FadeIn(area_68), Write(label_68))
        self.wait(2.5)

        # 6. Highlight 95% (161cm to 189cm)
        area_95 = axes.get_area(curve, x_range=[161, 189], color=TEAL, opacity=0.3)
        label_95 = Text("95% nam giới\n(161 - 189cm)", font="Noto Sans", font_size=20).move_to(axes.c2p(mu, 0.04))
        
        self.play(
            FadeOut(label_68),
            FadeIn(area_95),
            Write(label_95)
        )
        self.wait(3.5)
        area_99 = axes.get_area(curve, x_range=[154, 196], color=YELLOW, opacity=0.2)
        label_99 = Text("99,7% nam giới\n(154 - 196cm)", font="Noto Sans", font_size=20).move_to(axes.c2p(mu, 0.03))
        
        self.play(
            FadeOut(label_95),
            FadeIn(area_99),
            Write(label_99)
        )
        self.wait(5)
        self.add_sound("voiceovers/std7_part2.mp3")
        outlier_percent = Text("0,3% dân số", font="Noto Sans").to_edge(RIGHT)
        short = Text("< 154 cm", font="Noto Sans").scale(0.65).next_to(outlier_percent, DOWN)
        tall = Text("> 196 cm", font="Noto Sans").scale(0.65).next_to(short, DOWN)
        self.play(Write(outlier_percent))
        self.wait(3)
        self.play(Write(short))
        self.wait()
        self.play(Write(tall))
        self.wait(3)
        self.play(FadeOut(outlier_percent), FadeOut(short), FadeOut(tall))
        you_ming = ImageMobject("assets/yao ming.png").to_edge(RIGHT, LARGE_BUFF)
        basketball = ImageMobject("assets/basketball.png").scale(0.4).to_edge(RIGHT)
        # 7. Highlight the "Tails" (The Outliers)
        # Marking someone very tall
        tall_val = 196
        tall_dot = Dot(axes.c2p(tall_val, height_pdf(tall_val)), color=YELLOW)
        tall_line = axes.get_vertical_line(axes.c2p(tall_val, height_pdf(tall_val)), color=YELLOW)
        tall_text = Text("Giới hạn 99,7%: 196cm", font="Noto Sans", color=YELLOW, font_size=18).next_to(tall_line, UP)

        self.play(FadeIn(basketball), Create(tall_line), Create(tall_dot), Write(tall_text))
        self.wait()
        self.play(FadeOut(basketball))
        self.play(FadeIn(you_ming))
        self.wait(3)

class VarianceAndStandardDeviation2(Scene):
    def construct(self):
        # -----------------------------
        # Title
        # -----------------------------
        title = Text("Variance & Standard Deviation", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # -----------------------------
        # Dataset
        # -----------------------------
        data = np.array([2, 4, 4, 4, 5, 5, 7, 9])
        mean = np.mean(data)

        data_text = Text(f"Data: {list(data)}", font_size=28)
        data_text.next_to(title, DOWN)
        self.play(Write(data_text))
        self.wait(1)

        # -----------------------------
        # Number Line
        # -----------------------------
        number_line = NumberLine(
            x_range=[0, 10, 1],
            length=10,
            include_numbers=True
        )
        number_line.shift(DOWN)
        self.play(Create(number_line))

        # -----------------------------
        # Plot Data Points
        # -----------------------------
        dots = VGroup()
        for x in data:
            dot = Dot(number_line.number_to_point(x), color=BLUE)
            dots.add(dot)

        self.play(FadeIn(dots, scale=0.5))
        self.wait(1)

        # -----------------------------
        # Mean Indicator
        # -----------------------------
        mean_dot = Dot(
            number_line.number_to_point(mean),
            color=RED,
            radius=0.12
        )
        mean_label = Text("Mean", font_size=24, color=RED)
        mean_label.next_to(mean_dot, UP)

        self.play(FadeIn(mean_dot), Write(mean_label))
        self.wait(1)

        # -----------------------------
        # Deviations from Mean
        # -----------------------------
        deviation_lines = VGroup()
        for dot in dots:
            line = Line(
                mean_dot.get_center(),
                dot.get_center(),
                color=YELLOW
            )
            deviation_lines.add(line)

        self.play(Create(deviation_lines))
        self.wait(1)

        # -----------------------------
        # Variance Explanation
        # -----------------------------
        variance_text = MathTex(
            r"\text{Variance} = \frac{1}{N} \sum (x - \mu)^2",
            font_size=36
        )
        variance_text.to_edge(DOWN)
        self.play(Write(variance_text))
        self.wait(2)

        # -----------------------------
        # Squared Deviations (Visual Hint)
        # -----------------------------
        squares = VGroup()
        for line in deviation_lines:
            square = Square(
                side_length=0.25,
                color=ORANGE,
                fill_opacity=0.6
            )
            square.move_to(line.get_end())
            squares.add(square)

        self.play(FadeIn(squares, shift=UP))
        self.wait(1)

        # -----------------------------
        # Standard Deviation
        # -----------------------------
        std_text = MathTex(
            r"\text{Standard Deviation} = \sqrt{\text{Variance}}",
            font_size=36
        )
        std_text.next_to(variance_text, UP)
        self.play(Write(std_text))
        self.wait(2)

        # -----------------------------
        # Intuition Text
        # -----------------------------
        intuition = Text(
            "Standard deviation shows how spread out the data is",
            font_size=26
        )
        intuition.next_to(std_text, UP)
        self.play(FadeIn(intuition))
        self.wait(3)
