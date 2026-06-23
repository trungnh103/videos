from manim import *
import random
import numpy as np

class EndingScreen1(Scene):
    def construct(self):
        # Background color (optional)
        self.camera.background_color = "#0f172a"  # dark blue-gray
        
        # Main thank you text
        thank_you = Text("Thanks for Watching!", font_size=72, weight=BOLD)
        thank_you.set_color_by_gradient(BLUE, PURPLE)
        
        # Subtitle
        subtitle = Text("Like • Share • Subscribe", font_size=36)
        subtitle.next_to(thank_you, DOWN, buff=0.5)
        
        # Channel name
        channel_name = Text("Your Channel Name", font_size=40)
        channel_name.set_color(YELLOW)
        channel_name.to_edge(DOWN)

        # Animate
        self.play(FadeIn(thank_you, shift=UP), run_time=2)
        self.play(Write(subtitle), run_time=1.5)
        self.play(FadeIn(channel_name), run_time=1.5)
        
        self.wait(3)
        
        # Fade everything out
        self.play(
            FadeOut(thank_you),
            FadeOut(subtitle),
            FadeOut(channel_name),
            run_time=2
        )
        self.wait()
from manim import *

class EndingScreen(Scene):
    def construct(self):
        self.camera.background_color = "#111827"

        # Title
        title = Text("Thanks for Watching!", font_size=64)
        title.set_color_by_gradient(TEAL, BLUE)
        title.to_edge(UP)

        # Subscribe button
        button = RoundedRectangle(
            corner_radius=0.2,
            width=4,
            height=1.2,
            color=RED,
            fill_opacity=1
        )

        button_text = Text("SUBSCRIBE", font_size=36, color=WHITE)
        button_group = VGroup(button, button_text)

        # Position text in center of button
        button_text.move_to(button.get_center())

        # Animation
        self.play(Write(title))
        self.wait(0.5)

        self.play(FadeIn(button, scale=0.8))
        self.play(Write(button_text))

        # Pulse effect
        self.play(button.animate.scale(1.1), run_time=0.4)
        self.play(button.animate.scale(1/1.1), run_time=0.4)

        self.wait(3)

        self.play(FadeOut(VGroup(title, button_group)))
        self.wait()

class MatChanEnding(Scene):
    def construct(self):
        # Background
        self.camera.background_color = "#0b1020"  # deep navy

        # Main Title
        title = Text("Thanks for Watching!", font_size=64, weight=BOLD)
        title.set_color_by_gradient(BLUE, PURPLE)
        title.to_edge(UP)

        # Channel Name (Styled)
        channel = Text("Mat-chan", font_size=72, weight=BOLD)
        channel.set_color(YELLOW)

        # Add subtle glow effect
        glow = channel.copy()
        glow.set_stroke(YELLOW, width=8, opacity=0.4)
        glow.set_fill(opacity=0)

        channel_group = VGroup(glow, channel)

        # Math formula decoration
        formula = MathTex(r"\int_a^b f(x)\,dx", font_size=48)
        formula.set_color(GREEN)
        formula.next_to(channel_group, DOWN, buff=0.8)

        # Subscribe Button
        button = RoundedRectangle(
            width=4,
            height=1.2,
            corner_radius=0.3,
            color=RED,
            fill_opacity=1
        )

        button_text = Text("SUBSCRIBE", font_size=34, color=WHITE)
        button_group = VGroup(button, button_text)
        button_text.move_to(button.get_center())
        button_group.to_edge(DOWN)

        # Animations
        self.play(FadeIn(title, shift=UP), run_time=1.5)
        self.play(Write(channel), FadeIn(glow), run_time=1.5)
        self.play(Write(formula), run_time=1.2)

        self.wait(0.5)

        self.play(FadeIn(button, scale=0.8))
        self.play(Write(button_text))

        # Button pulse effect
        self.play(button_group.animate.scale(1.1), run_time=0.4)
        self.play(button_group.animate.scale(1/1.1), run_time=0.4)

        self.wait(3)

        self.play(FadeOut(VGroup(title, channel_group, formula, button_group)))
        self.wait()

class MatChanEnding(Scene):
    def construct(self):
        self.camera.background_color = "#0b1020"  # deep navy

        # --- Floating Math Symbols ---
        formulas = [
            r"\int_a^b f(x)\,dx",
            r"e^{i\pi} + 1 = 0",
            r"\frac{d}{dx}x^2 = 2x",
            r"\sum_{n=1}^{\infty} \frac{1}{n^2}",
            r"\nabla \cdot \vec{F}",
            r"\lim_{x \to 0} \frac{\sin x}{x}"
        ]

        floating_group = VGroup()

        for formula in formulas:
            tex = MathTex(formula, font_size=36)
            tex.set_color(random.choice([BLUE, GREEN, PURPLE, TEAL]))
            
            # Random starting position
            tex.move_to([
                random.uniform(-6, 6),
                random.uniform(-3.5, 3.5),
                0
            ])
            
            tex.set_opacity(0.25)  # subtle background look
            floating_group.add(tex)

        self.add(floating_group)

        # Animate floating motion
        for tex in floating_group:
            direction = random.choice([UP, DOWN]) * 0.5
            self.play(
                tex.animate.shift(direction),
                rate_func=there_and_back,
                run_time=random.uniform(4, 6),
            )

        # --- Main Branding ---
        channel = Text("Mat-chan", font_size=80, weight=BOLD)
        channel.set_color_by_gradient(YELLOW, ORANGE)

        glow = channel.copy()
        glow.set_stroke(YELLOW, width=10, opacity=0.4)
        glow.set_fill(opacity=0)

        branding = VGroup(glow, channel)

        # Subscribe text
        subscribe = Text("Subscribe for more math!", font_size=36)
        subscribe.next_to(branding, DOWN)

        # Animate branding
        self.play(FadeIn(branding, scale=0.8), run_time=2)
        self.play(Write(subscribe), run_time=1.5)

        self.wait(3)

        # Fade out everything
        self.play(FadeOut(VGroup(branding, subscribe, floating_group)))
        self.wait()

class MatChanEnergeticEnding(Scene):
    def construct(self):
        # self.camera.background_color = "#0f0f1f"

        # ----------------------------
        # Floating Math Symbols
        # ----------------------------
        formulas = [
            r"\int_a^b f(x)\,dx",
            r"e^{i\pi}+1=0",
            r"\frac{d}{dx}x^2=2x",
            r"\sum_{n=1}^{\infty}\frac{1}{n^2}",
            r"\lim_{x\to0}\frac{\sin x}{x}",
            r"\nabla \cdot \vec{F}",
        ]

        floating_group = VGroup()

        for formula in formulas:
            tex = MathTex(formula, font_size=42)
            tex.set_color(random.choice([BLUE, GREEN, TEAL, PURPLE]))
            tex.set_opacity(0.35)

            tex.move_to([
                random.uniform(-7, 7),
                random.uniform(-4, 4),
                0
            ])

            floating_group.add(tex)

        self.add(floating_group)

        # Continuous floating animation
        for tex in floating_group:
            tex.add_updater(
                lambda m, dt: m.shift(UP * 0.3 * dt)
            )

        # ----------------------------
        # Main Channel Name
        # ----------------------------
        channel = Text("Mat-chan", font_size=96, weight=BOLD)
        channel.set_color_by_gradient(YELLOW, ORANGE)

        glow = channel.copy()
        glow.set_stroke(YELLOW, width=12, opacity=0.5)
        glow.set_fill(opacity=0)

        branding = VGroup(glow, channel)

        # Energetic entrance (zoom punch)
        self.play(
            FadeIn(branding, scale=0.3),
            run_time=1.2,
            rate_func=rush_from
        )

        # Bounce effect
        self.play(
            branding.animate.scale(1.15),
            run_time=0.2
        )
        self.play(
            branding.animate.scale(1/1.15),
            run_time=0.2
        )

        # ----------------------------
        # Subscribe Text
        # ----------------------------
        subscribe = Text("SUBSCRIBE FOR MORE MATH!", font_size=40)
        subscribe.set_color(RED)
        subscribe.next_to(branding, DOWN)

        self.play(
            Write(subscribe),
            run_time=1,
            rate_func=there_and_back_with_pause
        )

        # Pulse animation loop
        for _ in range(2):
            self.play(subscribe.animate.scale(1.1), run_time=0.25)
            self.play(subscribe.animate.scale(1/1.1), run_time=0.25)

        self.wait(3)

        # Clean up
        self.play(FadeOut(VGroup(branding, subscribe, floating_group)))
        self.wait()

class MatChanLongEnergeticEnding(ZoomedScene):
    def construct(self):
        self.camera.background_color = "#0f1025"

        # ---------------------------------
        # Floating Background Math Symbols
        # ---------------------------------
        formulas = [
            r"\int_a^b f(x)\,dx",
            r"e^{i\pi}+1=0",
            r"\frac{d}{dx}x^2=2x",
            r"\sum_{n=1}^{\infty}\frac{1}{n^2}",
            r"\lim_{x\to0}\frac{\sin x}{x}",
            r"\nabla \cdot \vec{F}",
            r"\oint_C \vec{F}\cdot d\vec{r}",
            r"\Delta x \to 0"
        ]

        floating_group = VGroup()

        for _ in range(15):
            formula = random.choice(formulas)
            tex = MathTex(formula, font_size=random.randint(30, 48))
            tex.set_color(random.choice([BLUE, TEAL, PURPLE, GREEN]))
            tex.set_opacity(0.25)

            tex.move_to([
                random.uniform(-8, 8),
                random.uniform(-4.5, 4.5),
                0
            ])

            # Continuous upward drift
            tex.add_updater(
                lambda m, dt: m.shift(UP * 0.4 * dt)
            )

            floating_group.add(tex)

        self.add(floating_group)

        # ---------------------------------
        # Camera subtle movement
        # ---------------------------------
        self.camera.frame.save_state()
        self.play(
            self.camera.frame.animate.scale(0.95),
            run_time=10,
            rate_func=linear
        )

        # ---------------------------------
        # Main Channel Branding
        # ---------------------------------
        channel = Text("Mat-chan", font_size=100, weight=BOLD)
        channel.set_color_by_gradient(YELLOW, ORANGE)

        glow = channel.copy()
        glow.set_stroke(YELLOW, width=15, opacity=0.4)
        glow.set_fill(opacity=0)

        branding = VGroup(glow, channel)

        # Punch entrance
        self.play(
            FadeIn(branding, scale=0.2),
            run_time=1.5,
            rate_func=rush_from
        )

        # Impact bounce
        self.play(branding.animate.scale(1.2), run_time=0.3)
        self.play(branding.animate.scale(1/1.2), run_time=0.3)

        # ---------------------------------
        # Radial Burst Effect
        # ---------------------------------
        burst_lines = VGroup()
        for angle in np.linspace(0, TAU, 20):
            line = Line(ORIGIN, RIGHT * 3)
            line.rotate(angle)
            line.set_color(YELLOW)
            line.set_opacity(0.4)
            burst_lines.add(line)

        self.play(
            LaggedStartMap(GrowFromCenter, burst_lines),
            run_time=1
        )
        self.play(FadeOut(burst_lines), run_time=1)

        # ---------------------------------
        # Subscribe Call-To-Action
        # ---------------------------------
        subscribe_box = RoundedRectangle(
            width=5,
            height=1.4,
            corner_radius=0.3,
            color=RED,
            fill_opacity=1
        )

        subscribe_text = Text("SUBSCRIBE FOR MORE MATH!", font_size=40, color=WHITE)
        subscribe_text.move_to(subscribe_box.get_center())

        subscribe_group = VGroup(subscribe_box, subscribe_text)
        subscribe_group.next_to(branding, DOWN, buff=1)

        self.play(FadeIn(subscribe_group, scale=0.5), run_time=1)

        # Continuous pulsing for ~10 seconds
        for _ in range(6):
            self.play(subscribe_group.animate.scale(1.08), run_time=0.4)
            self.play(subscribe_group.animate.scale(1/1.08), run_time=0.4)

        # Hold ending (floating continues)
        self.wait(8)

        # ---------------------------------
        # Fade Out (Clean Ending)
        # ---------------------------------
        self.play(
            FadeOut(VGroup(branding, subscribe_group, floating_group)),
            run_time=2
        )

        self.wait()

class MatChanYouTubeEndCard(Scene):
    def construct(self):
        # self.camera.background_color = "#0f1025"

        # ---------------------------------
        # Floating Background Math Symbols
        # ---------------------------------
        formulas = [
            r"\int_a^b f(x)\,dx",
            r"e^{i\pi}+1=0",
            r"\frac{d}{dx}x^2=2x",
            r"\sum_{n=1}^{\infty}\frac{1}{n^2}",
            r"\lim_{x\to0}\frac{\sin x}{x}",
            r"\nabla \cdot \vec{F}"
        ]

        floating_group = VGroup()

        for _ in range(18):
            tex = MathTex(random.choice(formulas), font_size=random.randint(28, 44))
            tex.set_color(random.choice([BLUE, TEAL, PURPLE, GREEN]))
            tex.set_opacity(0.2)

            tex.move_to([
                random.uniform(-8, 8),
                random.uniform(-4.5, 4.5),
                0
            ])

            tex.add_updater(lambda m, dt: m.shift(UP * 0.3 * dt))
            floating_group.add(tex)

        self.add(floating_group)

        # ---------------------------------
        # Channel Branding (Top Center)
        # ---------------------------------
        title = Text("Mat-chan", font_size=80, weight=BOLD)
        title.set_color_by_gradient(YELLOW, ORANGE)
        title.to_edge(UP)

        glow = title.copy()
        glow.set_stroke(YELLOW, width=12, opacity=0.4)
        glow.set_fill(opacity=0)

        branding = VGroup(glow, title)

        self.play(FadeIn(branding, scale=0.5), run_time=1.5)

        # ---------------------------------
        # Two Video Placeholder Boxes
        # ---------------------------------
        box_width = 5
        box_height = 3

        left_box = RoundedRectangle(
            width=box_width,
            height=box_height,
            corner_radius=0.2,
            color=WHITE
        )

        right_box = left_box.copy()

        left_box.shift(LEFT * 3.5 + DOWN * 0.5)
        right_box.shift(RIGHT * 3.5 + DOWN * 0.5)

        left_label = Text("Previous Video", font_size=28)
        right_label = Text("Recommended", font_size=28)

        left_label.next_to(left_box, DOWN)
        right_label.next_to(right_box, DOWN)

        self.play(
            FadeIn(left_box, scale=0.8),
            FadeIn(right_box, scale=0.8),
            run_time=1.5
        )

        self.play(Write(left_label), Write(right_label))

        # ---------------------------------
        # Subscribe Button (Center Bottom)
        # ---------------------------------
        subscribe_box = RoundedRectangle(
            width=4.5,
            height=1.2,
            corner_radius=0.3,
            color=RED,
            fill_opacity=1
        )

        subscribe_text = Text("SUBSCRIBE", font_size=36, color=WHITE)
        subscribe_text.move_to(subscribe_box.get_center())

        subscribe_group = VGroup(subscribe_box, subscribe_text)
        subscribe_group.next_to(title, DOWN, buff=1.8)

        self.play(FadeIn(subscribe_group, scale=0.5), run_time=1)

        # Pulsing subscribe animation (~8 seconds)
        for _ in range(8):
            self.play(subscribe_group.animate.scale(1.06), run_time=0.3)
            self.play(subscribe_group.animate.scale(1/1.06), run_time=0.3)

        # Hold screen so YouTube end elements can appear
        self.wait(10)

        # Fade out cleanly
        self.play(FadeOut(VGroup(
            branding,
            left_box, right_box,
            left_label, right_label,
            subscribe_group,
            floating_group
        )), run_time=2)

        self.wait()

class MatChanYouTubeSafeEndCard(Scene):
    def construct(self):
        self.camera.background_color = "#0f1025"

        # ---------------------------------
        # Floating Background
        # ---------------------------------
        formulas = [
            r"\int_a^b f(x)\,dx",
            r"e^{i\pi}+1=0",
            r"\frac{d}{dx}x^2=2x",
            r"\sum_{n=1}^{\infty}\frac{1}{n^2}",
            r"\lim_{x\to0}\frac{\sin x}{x}"
        ]

        floating_group = VGroup()

        for _ in range(20):
            tex = MathTex(random.choice(formulas), font_size=32)
            tex.set_color(random.choice([BLUE, TEAL, PURPLE, GREEN]))
            tex.set_opacity(0.15)

            tex.move_to([
                random.uniform(-8, 8),
                random.uniform(-4.5, 4.5),
                0
            ])

            tex.add_updater(lambda m, dt: m.shift(UP * 0.25 * dt))
            floating_group.add(tex)

        self.add(floating_group)

        # ---------------------------------
        # Branding (Top)
        # ---------------------------------
        title = Text("Mat-chan", font_size=80, weight=BOLD)
        title.set_color_by_gradient(YELLOW, ORANGE)
        title.to_edge(UP)

        self.play(FadeIn(title, scale=0.5), run_time=1.5)

        # ---------------------------------
        # Safe Video Placeholder Frames
        # ---------------------------------
        left_frame = RoundedRectangle(
            width=5,
            height=3,
            corner_radius=0.2,
            stroke_width=4,
            color=WHITE
        ).set_opacity(0.5)

        right_frame = left_frame.copy()

        left_frame.shift(LEFT * 3.5 + DOWN * 0.5)
        right_frame.shift(RIGHT * 3.5 + DOWN * 0.5)

        self.play(
            FadeIn(left_frame),
            FadeIn(right_frame),
            run_time=1.5
        )

        # ---------------------------------
        # Subscribe Area (center)
        # ---------------------------------
        subscribe = Text("Subscribe for more math!", font_size=40)
        subscribe.set_color(RED)
        subscribe.next_to(title, DOWN, buff=1.5)

        self.play(Write(subscribe))

        # Energetic pulse for ~10 seconds
        for _ in range(8):
            self.play(subscribe.animate.scale(1.05), run_time=0.3)
            self.play(subscribe.animate.scale(1/1.05), run_time=0.3)

        # Hold for YouTube elements
        self.wait(10)

        self.play(FadeOut(VGroup(title, left_frame, right_frame, subscribe, floating_group)))
        self.wait()

class MatChanMusicSyncedEnd(Scene):
    def construct(self):

        # Add your music file (place in same folder)
        # self.add_sound("end_music.mp3")

        self.camera.background_color = "#0f1025"

        # ---------------------------------
        # Floating Math Background
        # ---------------------------------
        formulas = [
            r"\int_a^b f(x)\,dx",
            r"e^{i\pi}+1=0",
            r"\frac{d}{dx}x^2=2x",
            r"\sum_{n=1}^{\infty}\frac{1}{n^2}",
            r"\lim_{x\to0}\frac{\sin x}{x}"
        ]

        floating = VGroup()
        for _ in range(25):
            tex = MathTex(random.choice(formulas), font_size=30)
            tex.set_color(random.choice([BLUE, TEAL, PURPLE, GREEN]))
            tex.set_opacity(0.12)
            tex.move_to([
                random.uniform(-8, 8),
                random.uniform(-4.5, 4.5),
                0
            ])
            tex.add_updater(lambda m, dt: m.shift(UP * 0.25 * dt))
            floating.add(tex)

        self.add(floating)

        # ---------------------------------
        # 0–4s : Music Intro (Slow Build)
        # ---------------------------------
        # title = Text("Mat-chan", font_size=90, weight=BOLD)
        title = Text("Thanks for Watching!", font_size=64)
        title.set_color_by_gradient(TEAL, BLUE)
        title.to_edge(UP)

        # Subscribe button
        button = RoundedRectangle(
            corner_radius=0.2,
            width=4,
            height=1.2,
            color=RED,
            fill_opacity=1
        )

        button_text = Text("SUBSCRIBE", font_size=36, color=WHITE)
        button_group = VGroup(button, button_text)

        # Position text in center of button
        button_text.move_to(button.get_center())

        # Animation
        self.play(Write(title))
        self.wait(0.5)

        self.play(FadeIn(button, scale=0.8))
        self.play(Write(button_text))

        # ---------------------------------
        # 4s : BEAT DROP
        # ---------------------------------
        self.play(title.animate.scale(1.6), run_time=0.2)
        self.play(title.animate.scale(1/1.6), run_time=0.2)

        # Flash effect
        flash = FullScreenRectangle(fill_color=WHITE, fill_opacity=0.3)
        self.play(FadeOut(flash), run_time=0.3)

        # ---------------------------------
        # Subscribe Text
        # ---------------------------------
        # subscribe = Text("SUBSCRIBE FOR MORE MATH!", font_size=42)
        # subscribe.set_color(RED)
        # subscribe.next_to(title, DOWN, buff=1.2)

        # self.play(Write(subscribe), run_time=1)

        # ---------------------------------
        # 8–18s : Beat Pulses
        # (Assuming ~120 BPM → pulse every 0.5 sec)
        # ---------------------------------
        for _ in range(16):  # ~8 seconds
            self.play(
                title.animate.scale(1.05),
                button.animate.scale(1.08),
                run_time=0.25
            )
            self.play(
                title.animate.scale(1/1.05),
                button.animate.scale(1/1.08),
                run_time=0.25
            )

        # ---------------------------------
        # Outro Hold (YouTube overlay time)
        # ---------------------------------
        self.wait(6)

        # Fade out with music ending
        self.play(FadeOut(VGroup(title, button, floating)), run_time=2)
        self.wait()