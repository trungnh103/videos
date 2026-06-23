from manim import *
import numpy as np

class IntroScene(Scene):
    def construct(self):
        self.prismDispersionWithScreen()
        self.chordDecomposition()
        self.showCloud()
        self.animatedRainbow()
        title = Text("Spectral Decomposition", font="Noto Sans", color=YELLOW, font_size=42)
        self.play(Write(title))
        self.wait()
        leds = VGroup(SVGMobject("assets/led.svg")).next_to(title, DOWN)
        self.play(FadeIn(leds))
        self.wait(2)
    def showCloud(self):
        # Cloud parts
        cloud_color = LIGHT_GREY

        c1 = Circle(radius=0.6, fill_opacity=1, color=cloud_color).shift(LEFT * 0.8)
        c2 = Circle(radius=0.8, fill_opacity=1, color=cloud_color)
        c3 = Circle(radius=0.6, fill_opacity=1, color=cloud_color).shift(RIGHT * 0.8)

        cloud_base = RoundedRectangle(
            width=3,
            height=0.9,
            corner_radius=0.4,
            fill_opacity=1,
            color=cloud_color
        ).shift(DOWN * 0.4)

        cloud = VGroup(c1, c2, c3, cloud_base)
        self.play(FadeIn(cloud))
        self.wait()
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def animatedRainbow(self):
        # Sky background
        sky = Rectangle(width=14, height=8, fill_color=BLUE_E, fill_opacity=1)
        self.add(sky)

        # Rainbow colors (inner → outer for gradient effect)
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]

        # Base parameters
        base_radius = 3.5
        stroke_width = 0.25
        arcs = VGroup()

        # Create arcs
        for i, color in enumerate(colors):
            arc = Arc(
                radius=base_radius - i * 0.3,
                start_angle=PI,
                angle=-PI,
                stroke_color=color,
                stroke_width=20,
            )
            arcs.add(arc)

        # Clouds
        def create_cloud(center, scale=1):
            cloud = VGroup(
                *[Circle(radius=0.5*scale, color=WHITE, fill_opacity=1) for _ in range(3)]
            )
            cloud.arrange(RIGHT, buff=-0.2*scale)
            cloud.move_to(center)
            return cloud

        cloud1 = create_cloud(LEFT*3 + DOWN*1)
        cloud2 = create_cloud(RIGHT*3 + DOWN*1.2, scale=1.2)
        self.add(cloud1, cloud2)

        # Animate rainbow
        self.play(LaggedStart(*[GrowFromCenter(arc) for arc in arcs], lag_ratio=0.2))
        self.wait(1)

        # Animate clouds floating slightly
        self.play(cloud1.animate.shift(RIGHT*0.5), cloud2.animate.shift(LEFT*0.5), run_time=2)
        self.wait()
        self.play(*[FadeOut(mob) for mob in self.mobjects])
    def prismDispersionWithScreen(self):
        # 1. Create the glass prism
        prism = Polygon(
            UP * 2, 
            DOWN * 1.5 + LEFT * 2.5, 
            DOWN * 1.5 + RIGHT * 2.5,
            color=WHITE,
            fill_color=BLUE,
            fill_opacity=0.1,
            stroke_width=2
        )
        
        # Add a subtle glow to the prism
        self.play(Create(prism), run_time=1.5)
        self.wait(0.5)

        # 2. Setup the incident white light beam
        p_start = LEFT * 6 + UP * 1.5
        p_incident = LEFT * 1.25 + UP * 0.25
        
        white_beam = Line(p_start, p_incident, color=WHITE, stroke_width=4)
        
        # Animate the white beam entering
        self.play(Create(white_beam), run_time=1)

        # 3. Setup the colors and screen details
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
        screen_x_pos = 5.5 # Fixed horizontal position for the screen
        
        inside_rays = VGroup()
        outside_rays = VGroup()
        screen_spots = VGroup() # For the colorful dots on the screen

        # 4. Calculate rays and prepare screen spots
        for i, color in enumerate(colors):
            alpha = i / (len(colors) - 1)
            
            # Exit points on the right face of the prism
            p_exit_top = np.array([0.9, 0.65, 0])
            p_exit_bottom = np.array([1.4, -0.1, 0])
            p_exit = interpolate(p_exit_top, p_exit_bottom, alpha)
            
            # Destinations on the vertical screen
            # Red bends least (lands higher), purple bends most (lands lower)
            screen_y_top = 0.5
            screen_y_bottom = -3.5
            p_final = np.array([screen_x_pos, interpolate(screen_y_top, screen_y_bottom, alpha), 0])
            
            # Create the line segments
            inside_ray = Line(p_incident, p_exit, color=color, stroke_width=3)
            outside_ray = Line(p_exit, p_final, color=color, stroke_width=4)
            
            inside_rays.add(inside_ray)
            outside_rays.add(outside_ray)

            # Create colorful spots/shimmers on the screen surface
            spot = Dot(p_final, color=color, radius=0.12).set_opacity(0.8)
            screen_spots.add(spot)

        # 5. Create the screen object
        screen_rect = Rectangle(
            height=5, width=0.2, 
            fill_color=GREY_A, fill_opacity=0.5, 
            stroke_color=WHITE
        ).move_to([screen_x_pos + 0.1, -1.5, 0])
        
        screen_label = Text("Screen", font_size=20).next_to(screen_rect, UP)
        screen_group = VGroup(screen_rect, screen_label)

        # 6. Animation Sequence
        # Fade in the screen before the light reaches it
        self.play(FadeIn(screen_group), run_time=1)
        self.wait(0.3)

        # Draw rays inside the prism
        self.play(Create(inside_rays), run_time=0.8)
        
        # Draw rays emerging and hitting the screen simultaneously
        self.play(
            Create(outside_rays),
            FadeIn(screen_spots, lag_ratio=0.1), # Spots appear as rays arrive
            run_time=1.5
        )
        
        # Add labels and shimmer effect
        white_label = Text("White Light", font_size=24).next_to(p_start, UP)
        dispersion_label = Text("Dispersion", font_size=24).next_to(prism, DOWN * 2)
        
        self.play(Write(white_label), Write(dispersion_label))

        # Subtle "shimmer" on the screen for effect
        self.play(screen_spots.animate.set_opacity(0.4), run_time=0.5)
        self.play(screen_spots.animate.set_opacity(0.8), run_time=0.5)
        self.wait()
        self.play(*[FadeOut(mob) for mob in self.mobjects])
    def chordDecomposition(self):
        # Frequencies for a chord (C major: C, E, G)
        freqs = [1, 1.25, 1.5]
        colors = [RED, GREEN, BLUE]
        labels = ["C", "E", "G"]

        # Create axes
        axes = Axes(
            x_range=[0, 4 * PI, PI],
            y_range=[-3, 3, 1],
            axis_config={"include_tip": False},
        ).scale(0.8).shift(0.5*UP)

        self.play(Create(axes))

        # Individual waves
        waves = [
            axes.plot(lambda x, f=f: np.sin(f * x), color=c)
            for f, c in zip(freqs, colors)
        ]

        # Combined chord (sum of waves)
        combined_wave = axes.plot(
            lambda x: sum(np.sin(f * x) for f in freqs),
            color=YELLOW
        )

        combined_label = Text("Chord", color=YELLOW).next_to(axes, UP)

        # Show combined chord
        self.play(Create(combined_wave), Write(combined_label))
        self.wait(1)

        # Fade in individual components on top
        self.play(
            *[Create(w) for w in waves],
            FadeOut(combined_label)
        )
        self.wait(1)

        # Move waves apart vertically
        separated_waves = VGroup()
        separated_labels = VGroup()

        for i, (wave, label, color) in enumerate(zip(waves, labels, colors)):
            new_wave = axes.plot(
                lambda x, f=freqs[i]: np.sin(f * x),
                color=color
            ).shift(DOWN * (i + 1.5))

            text = Text(label, color=color).scale(0.6)
            text.next_to(new_wave, LEFT)

            separated_waves.add(new_wave)
            separated_labels.add(text)

        self.play(
            ReplacementTransform(VGroup(*waves), separated_waves),
            FadeOut(combined_wave)
        )

        self.play(Write(separated_labels))
        self.wait()
        self.play(*[FadeOut(mob) for mob in self.mobjects])
class SlidingMatrices(Scene):
    def construct(self):
        # List of matrices with different sizes
        matrices_data = [
            [[1, 2], [3, 4]],          # 2x2 square
            [[5, 6, 7], [8, 9, 10]],   # 2x3 rectangle
            [[1], [2], [3]],           # 3x1 column vector
            [[1, 2, 3, 4]],            # 1x4 row vector
            [[i + j*4 for i in range(4)] for j in range(4)]  # 4x4 square
        ]

        # Create Matrix objects
        matrices = [Matrix(data) for data in matrices_data]

        # Initial matrix (centered)
        current_matrix = matrices[0]
        current_matrix.move_to(ORIGIN)
        self.play(Write(current_matrix))
        self.wait(1)

        # Animate the rest
        for next_matrix in matrices[1:]:
            next_matrix.move_to(RIGHT * 10)  # start off-screen right
            # Animate current sliding out left and next sliding in
            self.play(
                current_matrix.animate.shift(LEFT * 10),  # move current off-screen
                next_matrix.animate.move_to(ORIGIN),    # move next to center
                run_time=1.0,
                rate_func=smooth
            )
            current_matrix = next_matrix
            self.wait(0.5)

        # Fade out the last matrix
        self.play(FadeOut(current_matrix))