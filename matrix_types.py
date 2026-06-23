from manim import *
import random
from PIL import Image
import numpy as np

def create_grid():
    window_height = 4
    window_width = 6
    # window_rect = Square(side_length=window_height, color=WHITE, stroke_width=4).set_z_index(12)
    window_rect = Rectangle(
            width=window_width,
            height=window_height,
            color=WHITE
        ).set_z_index(12)
    big_rect = Rectangle(width=20, height=20, fill_color=BLACK, fill_opacity=1, stroke_width=0)
    # hole = Square(side_length=window_height)
    hole = Rectangle(
            width=window_width,
            height=window_height
        )
    wall_with_hole = Difference(big_rect, hole, fill_color=BLACK, fill_opacity=1, stroke_width=0).set_z_index(10)
    
    grid = NumberPlane(
        x_range=[-6, 6, 1],
        y_range=[-4, 4, 1],
        background_line_style={
            "stroke_color": BLUE_E,
            "stroke_width": 1,
            "stroke_opacity": 0.5,
        },
    )
    points = VGroup()
    for x in np.arange(-6, 7, 1):
        for y in np.arange(-4, 5, 1):

            dot = Dot(
                point=[x, y, 0],
                radius=0.05,
                color=YELLOW
            )

            dot.original_position = np.array([x, y, 0])

            points.add(dot)    
    return window_rect, wall_with_hole, grid, points
def create_grid_no_point():
    window_height = 4
    window_width = 6
    window_rect = Square(side_length=window_height, color=WHITE, stroke_width=4).set_z_index(12)
    big_rect = Rectangle(width=20, height=20, fill_color=BLACK, fill_opacity=1, stroke_width=0)
    hole = Square(side_length=window_height)
    wall_with_hole = Difference(big_rect, hole, fill_color=BLACK, fill_opacity=1, stroke_width=0).set_z_index(10)
    
    grid = NumberPlane(
        x_range=[-6, 6, 1],
        y_range=[-4, 4, 1],
        background_line_style={
            "stroke_color": BLUE_E,
            "stroke_width": 1,
            "stroke_opacity": 0.5,
        },
    ) 
    return window_rect, wall_with_hole, grid
def create_grid_double():
    window_height = 4
    window_width = 6
    window_rect_left = Rectangle(
            width=window_width,
            height=window_height,
            color=WHITE
        ).to_edge(LEFT).set_z_index(12)
    window_rect_right = Rectangle(
            width=window_width,
            height=window_height,
            color=WHITE
        ).to_edge(RIGHT).set_z_index(12)
    big_rect = Rectangle(width=20, height=20, fill_color=BLACK, fill_opacity=1, stroke_width=0)
    hole = Union(
        Rectangle(
            width=window_width,
            height=window_height
        ).to_edge(LEFT),
        Rectangle(
            width=window_width,
            height=window_height
        ).to_edge(RIGHT))
    wall_with_hole = Difference(big_rect, hole, fill_color=BLACK, fill_opacity=1, stroke_width=0).set_z_index(10)
    
    grid_left = NumberPlane(
        x_range=[-3, 3, 1],
        y_range=[-2, 2, 1],
        background_line_style={
            "stroke_color": BLUE_E,
            "stroke_width": 1,
            "stroke_opacity": 0.5,
        },
    ).move_to(window_rect_left.get_center())
    grid_right = NumberPlane(
        x_range=[-3, 3, 1],
        y_range=[-2, 2, 1],
        background_line_style={
            "stroke_color": BLUE_E,
            "stroke_width": 1,
            "stroke_opacity": 0.5,
        },
    ).move_to(window_rect_right.get_center())
    return window_rect_left, window_rect_right, wall_with_hole, grid_left, grid_right
def animate_points_matrix(scene, grid, points, matrix, back_to_origin=0):
    positions = []
    for dot in points:
        positions.append(dot.get_center() + back_to_origin*LEFT)

    return [grid.animate.shift(back_to_origin*LEFT).apply_matrix(matrix).shift(back_to_origin*RIGHT),
            *[
                dot.animate.move_to(
                    np.append(matrix @ pos[:2], 0)
                ).shift(back_to_origin*RIGHT)
                for dot, pos in zip(points, positions)
            ]]

class RotateCharacter3D(ThreeDScene):
    def construct(self):
        self.add_sound("voiceovers/RotateCharacter3D.mp3")
        self.set_camera_orientation(phi=70 * DEGREES, theta=45 * DEGREES)
        sphere_radius = 0.3
        cylinder_height = 1.2
        head = Sphere(radius=sphere_radius).move_to(OUT * (cylinder_height/2 + sphere_radius))
        body = Cylinder(radius=0.25, height=cylinder_height)
        left_arm = Cylinder(radius=0.08, height=1).shift(LEFT * 0.5)
        right_arm = Cylinder(radius=0.08, height=1).shift(RIGHT * 0.5)
        left_leg = Cylinder(radius=0.1, height=1).shift(IN * 1 + LEFT * 0.2)
        right_leg = Cylinder(radius=0.1, height=1).shift(IN * 1 + RIGHT * 0.2)

        character = VGroup(head, body, left_arm, right_arm, left_leg, right_leg)
        self.add(character)
        self.add_sound("voiceovers/gear-click.mp3")
        self.play(
            Rotate(
                character,
                angle=2 * PI,
                axis=UP,   
                run_time=6
            )
        )
        self.wait()
class NetflixCinematic(MovingCameraScene):
    def construct(self):
        self.wait()
        logo = Text("NETFLIX", color=RED, weight=BOLD).scale(1.6)
        logo.to_corner(UL)
        self.add_sound("voiceovers/intro_cinematic.mp3")
        self.play(FadeIn(logo, shift=DOWN))
        trending = Text("Đang thịnh hành", font="Noto Sans", font_size=36)
        trending.next_to(logo, DOWN).align_to(logo, LEFT).shift(DOWN*0.5)
        self.play(FadeIn(trending))
        posters = Group(*[
            ImageMobject(f"posters/poster{i}.jpg").stretch_to_fit_width(1.6).stretch_to_fit_height(2.4)
            for i in range(1,9)
        ])
        posters.arrange(RIGHT, buff=0.3)
        posters.next_to(trending, DOWN, aligned_edge=LEFT)
        self.play(LaggedStart(
            *[FadeIn(p, shift=UP*0.3) for p in posters],
            lag_ratio=0.1
        ))
        self.add_sound("voiceovers/spin.mp3")
        self.play(
            posters.animate.shift(LEFT*4),
            run_time=3,
            rate_func=smooth
        )
        focus_movie = posters[5]
        highlight = SurroundingRectangle(
            focus_movie,
            color=YELLOW,
            buff=0.1
        )
        self.add_sound("voiceovers/ding-402325.mp3")
        watched_text = Text("Đã xem", font="Noto Sans", font_size=24, color=YELLOW)
        watched_text.next_to(highlight, UP)
        self.play(
            focus_movie.animate.scale(1.2),
            Create(highlight),
            FadeIn(watched_text)
        )
        self.add_sound("voiceovers/NetflixCinematic.mp3")
        
        self.camera.frame.save_state()

        rec_title = Text("Đề xuất dành cho bạn", font="Noto Sans", font_size=36)
        rec_title.next_to(posters, DOWN, buff=1)
        
        self.play(FadeIn(rec_title, shift=DOWN))
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(self.camera.frame.animate.move_to(rec_title))

        rec_posters = Group(*[
            ImageMobject(f"posters/poster{i}.jpg").stretch_to_fit_width(1.6).stretch_to_fit_height(2.4)
            for i in range(4,10)
        ])

        rec_posters.arrange(RIGHT, buff=0.3)
        rec_posters.next_to(rec_title, DOWN)

        self.play(LaggedStart(
            *[FadeIn(p, shift=UP*0.3) for p in rec_posters],
            lag_ratio=0.1
        ))
        glow = SurroundingRectangle(
            Group(rec_posters[0], rec_posters[1]),
            color=GREEN,
            buff=0.15
        )
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(Create(glow))
        self.wait(2)
def heatmapSweep(scene):
        rows, cols = 6, 6
        cell_size = 0.9

        values = np.arange(rows * cols).reshape(rows, cols)

        grid = VGroup()
        labels = VGroup()

        vmin = values.min()
        vmax = values.max()

        def heat_color(v):
            alpha = (v - vmin) / (vmax - vmin)
            return interpolate_color(BLUE, RED, alpha)

        for r in range(rows):
            row = VGroup()
            label_row = VGroup()

            for c in range(cols):
                val = values[r, c]

                square = Square(side_length=cell_size)
                square.set_fill(heat_color(val), opacity=0.8)
                square.set_stroke(WHITE, width=1)

                square.move_to([c * cell_size, -r * cell_size, 0])

                txt = Text(str(val)).scale(0.35)
                txt.move_to(square.get_center())

                row.add(square)
                label_row.add(txt)

            grid.add(row)
            labels.add(label_row)

        grid.center()
        labels.center()

        scene.play(FadeIn(grid), Write(labels))
        scene.wait()
        scene.play(FadeOut(grid, labels))

class MagicTransform(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/MagicTransform.mp3")
        square = Square(color=BLUE).scale(2)
        star = Star(color=YELLOW).scale(2)
        self.add_sound("voiceovers/click.wav")
        self.play(Create(square))

        self.play(
            square.animate.set_fill(PURPLE, opacity=0.7)
        )
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(Transform(square, star))
        self.add_sound("voiceovers/Matrix.mp3")
        title = Text("Ma trận", font="Noto Sans", font_size=72).set_color(BLUE)
        self.add_sound("voiceovers/magic-034.mp3")
        self.play(Transform(square, title))
        self.wait()
        self.play(FadeOut(square))
        self.matrixDefinition()
        self.wait()
    def matrixDefinition(self):
        self.add_sound("voiceovers/matrixDefinition.mp3")
        matrix = Matrix([[1, 2], [3, 4]])
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(matrix))
        self.wait()
        row_label = Text("Hàng", font="Noto Sans", color=BLUE).scale(0.6)
        row_label.next_to(matrix, LEFT, buff=0.5)
        
        col_label = Text("Cột", font="Noto Sans", color=GREEN).scale(0.6)
        col_label.next_to(matrix, UP, buff=0.5)
        row_rect = SurroundingRectangle(matrix.get_rows()[0], color=BLUE)
        col_rect = SurroundingRectangle(matrix.get_columns()[1], color=GREEN)

        self.play(Create(row_rect), Write(row_label))
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(ReplacementTransform(row_rect, col_rect), Write(col_label))
        self.wait()
        self.play(FadeOut(row_rect, col_rect))

        target_element = matrix.get_entries()[2] 
        focus_rect = SurroundingRectangle(target_element, color=YELLOW)
        
        label = MathTex("a_{2,1}", color=YELLOW).next_to(focus_rect, DOWN)

        self.play(Create(focus_rect))
        self.wait(2)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(label))
        self.wait(2)
        self.play(FadeOut(focus_rect, label, matrix, row_label, col_label))
        self.floatingMatrices()
        self.squareMatrixExplanation()
        self.matrixFamiliesVisualization()
        self.wait()

    def floatingMatrices(self):
        self.add_sound("voiceovers/floatingMatrices.mp3")
        matrices = VGroup(
            Matrix([[1, 2], [3, 4]]),
            Matrix([[5, 6], [7, 8]]),
            Matrix([[9, 1], [2, 3]]),
            Matrix([[4, 5], [6, 7]]),
            Matrix([[8, 9], [1, 2]])
        )

        for m in matrices:
            m.scale(0.8)
            m.move_to([
                random.uniform(-5, 5),
                random.uniform(-3, 3),
                0
            ])

        self.play(LaggedStart(*[FadeIn(m) for m in matrices], lag_ratio=0.2))
        animations = []
        for m in matrices:
            new_pos = [
                random.uniform(-5, 5),
                random.uniform(-3, 3),
                0
            ]
            animations.append(m.animate.move_to(new_pos))

        self.play(*animations, run_time=1)

        for _ in range(2):
            animations = []
            for m in matrices:
                new_pos = [
                    random.uniform(-5, 5),
                    random.uniform(-3, 3),
                    0
                ]
                animations.append(m.animate.move_to(new_pos))
            self.play(*animations, run_time=1)
        self.play(FadeOut(matrices))
    def diagonalMatrix3x3(self):
        matrix = Matrix([
            [3, 0, 0],
            [0, 5, 0],
            [0, 0, 2]
        ])

        self.play(Create(matrix))

        diag_entries = VGroup(
            matrix.get_entries()[0],
            matrix.get_entries()[4],
            matrix.get_entries()[8]
        )

        boxes = VGroup(*[
            SurroundingRectangle(e, color=YELLOW)
            for e in diag_entries
        ])

        self.play(Create(boxes))
        self.wait(2)

        non_diag = VGroup(
            matrix.get_entries()[1],
            matrix.get_entries()[2],
            matrix.get_entries()[3],
            matrix.get_entries()[5],
            matrix.get_entries()[6],
            matrix.get_entries()[7],
        )

        self.play(non_diag.animate.set_opacity(0.2))
        self.wait()
        self.play(FadeOut(matrix, boxes))
    def squareMatrixExplanation(self):
        self.add_sound("voiceovers/squareMatrixExplanation.mp3")
        title = Text("Ma trận vuông", font="Noto Sans").to_edge(UP)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(title))

        matrix = Matrix([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ])
        self.add_sound("voiceovers/click.wav")
        self.play(Create(matrix))
        self.wait()

        dim_text = Text("Ma trận 3 × 3", font="Noto Sans").scale(0.7)
        dim_text.next_to(matrix, DOWN)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(dim_text))
        self.wait()

        row_box = SurroundingRectangle(matrix.get_rows()[0], color=BLUE)
        row_label = Text("Hàng", font="Noto Sans").scale(0.5).next_to(row_box, LEFT, MED_LARGE_BUFF)

        self.play(Create(row_box), Write(row_label))
        self.wait(.5)

        col_box = SurroundingRectangle(matrix.get_columns()[0], color=GREEN)
        col_label = Text("Cột", font="Noto Sans").scale(0.5).next_to(col_box, UP)
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(
            Transform(row_box, col_box),
            Transform(row_label, col_label)
        )
        self.wait(.5)

        property_text = Text("Hàng = Cột", font="Noto Sans").set_color(YELLOW).scale(0.8)
        property_text.next_to(dim_text, DOWN)
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(FadeOut(row_box, row_label), Write(property_text))
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.bitGrid()
    
    def matrixFamiliesVisualization(self):
        self.add_sound("voiceovers/matrixFamiliesVisualization.mp3")
        title = Text("Gia đình Ma trận", font="Noto Sans", font_size=48)
        title.to_edge(UP).set_z_index(12)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(title))

        diag_title = Text("Đường chéo", font="Noto Sans", font_size=32, color=BLUE)

        scalar_text = Text("Ma trận vô hướng", font="Noto Sans", font_size=26)
        identity_text = Text("Ma trận đơn vị", font="Noto Sans", font_size=26)

        diag_items = VGroup(scalar_text, identity_text).arrange(DOWN, aligned_edge=LEFT)

        geo_title = Text("Biến đổi hình học", font="Noto Sans", font_size=32, color=GREEN)

        shear_text = Text("Ma trận trượt", font="Noto Sans", font_size=26)
        ortho_text = Text("Ma trận trực giao", font="Noto Sans", font_size=26)
        proj_text = Text("Ma trận chiếu", font="Noto Sans", font_size=26)

        geo_items = VGroup(shear_text, ortho_text, proj_text).arrange(DOWN, aligned_edge=LEFT)

        checklist = VGroup(
            diag_title,
            diag_items,
            geo_title,
            geo_items
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        checklist.to_edge(LEFT).set_z_index(12)
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(diag_title))
        self.play(FadeIn(scalar_text))
        self.play(FadeIn(identity_text))
        self.wait()
        self.diagonalMatrix3x3()

        window_rect, wall_with_hole, grid, points = create_grid()
        VGroup(window_rect, wall_with_hole, grid, points).shift(2*RIGHT)
        self.play(FadeIn(wall_with_hole))
        self.add_sound("voiceovers/click.wav")
        self.play(Create(window_rect))
        self.play(Create(grid), FadeIn(points))
        
        # ---------------------------------
        # Identity Matrix
        # ---------------------------------
        identity_matrix = np.array([
            [1,0],
            [0,1]
        ])

        identity_check = Text("✓", color=GREEN).next_to(identity_text, RIGHT).set_z_index(12)
        self.add_sound("voiceovers/identity_check.mp3")
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(Write(identity_check))
        self.wait()

        # no transformation since identity
        self.wait()

        # ---------------------------------
        # Scalar Matrix (Scaling)
        # ---------------------------------
        scalar_matrix = np.array([
            [2,0],
            [0,2]
        ])

        scalar_check = Text("✓", color=GREEN).next_to(scalar_text, RIGHT).set_z_index(12)
        self.add_sound("voiceovers/scalar_check.mp3")
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(Write(scalar_check))
        anims = animate_points_matrix(self, grid, points, scalar_matrix, back_to_origin=2)
        self.play(
            *anims,
            run_time=2,
            rate_func=linear
        )
        self.wait()

        # reset grid
        self.play(FadeOut(grid, points))
        window_rect, wall_with_hole, grid, points = create_grid()
        VGroup(window_rect, wall_with_hole, grid, points).shift(2*RIGHT)
        self.play(Create(grid), FadeIn(points))
        self.add_sound("voiceovers/geo_tranform_matrices.mp3")
        self.play(FadeIn(geo_title))
        self.play(FadeIn(geo_items))
        # ---------------------------------
        # Shear Matrix
        # ---------------------------------
        shear_matrix = np.array([
            [1,1],
            [0,1]
        ])

        shear_check = Text("✓", color=GREEN).next_to(shear_text, RIGHT).set_z_index(12)
        self.add_sound("voiceovers/ShearMatrix_title.mp3")
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(Write(shear_check))
        anims = animate_points_matrix(self, grid, points, shear_matrix, back_to_origin=2)
        self.play(
            *anims,
            run_time=2,
            rate_func=linear
        )
        self.wait()
        self.play(FadeOut(grid, points))
        window_rect, wall_with_hole, grid, points = create_grid()
        VGroup(window_rect, wall_with_hole, grid, points).shift(2*RIGHT)
        self.play(Create(grid), FadeIn(points))

        # ---------------------------------
        # Orthogonal Matrix (Rotation)
        # ---------------------------------
        theta = PI/4
        ortho_matrix = np.array([
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)]
        ])

        ortho_check = Text("✓", color=GREEN).next_to(ortho_text, RIGHT).set_z_index(12)
        self.add_sound("voiceovers/RotateMaster.mp3")
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(Write(ortho_check))
        anims = animate_points_matrix(self, grid, points, ortho_matrix, back_to_origin=2)
        self.play(
            *anims,
            run_time=2,
            rate_func=linear
        )
        self.wait()
        self.play(FadeOut(grid, points))
        window_rect, wall_with_hole, grid, points = create_grid()
        VGroup(window_rect, wall_with_hole, grid, points).shift(2*RIGHT)
        self.play(Create(grid), FadeIn(points))

        # ---------------------------------
        # Projection Matrix
        # ---------------------------------
        projection_matrix = np.array([
            [1,0],
            [0,0]
        ])

        proj_check = Text("✓", color=GREEN).next_to(proj_text, RIGHT).set_z_index(12)
        self.add_sound("voiceovers/proj_check.mp3")
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(Write(proj_check))
        anims = animate_points_matrix(self, grid, points, projection_matrix, back_to_origin=2)
        self.play(
            *anims,
            run_time=2,
            rate_func=linear
        )
        self.wait()
        self.play(FadeOut(grid, points))
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.add_sound("voiceovers/by_the_end.mp3")
        heatmapSweep(self)
        self.dNA2D()

    def dNA2D(self):
        amplitude = 1
        length = 10

        strand1 = ParametricFunction(
            lambda t: np.array([t, amplitude * np.sin(t), 0]),
            t_range=[-length, length],
            color=BLUE
        )

        strand2 = ParametricFunction(
            lambda t: np.array([t, -amplitude * np.sin(t), 0]),
            t_range=[-length, length],
            color=RED
        )

        # Base pairs
        base_pairs = VGroup()
        for t in np.linspace(-length, length, 40):
            p1 = np.array([t, amplitude * np.sin(t), 0])
            p2 = np.array([t, -amplitude * np.sin(t), 0])
            base_pairs.add(Line(p1, p2, color=YELLOW))
        self.add_sound("voiceovers/magic-034.mp3")
        self.play(Create(strand1), Create(strand2))
        self.play(LaggedStart(*[Create(bp) for bp in base_pairs], lag_ratio=0.05))
        look_closely = SVGMobject("assets/look_closely.svg").to_edge(UP)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(look_closely))
        self.wait(2)
    def bitGrid(self):
        rows = 10
        cols = 16
        spacing = 0.6
        grid = VGroup()
        for r in range(rows):
            row = VGroup()
            for c in range(cols):
                bit = Text(str(random.randint(0, 1)), font_size=36)
                bit.move_to([c * spacing, -r * spacing, 0])
                row.add(bit)
            grid.add(row)

        grid.move_to(ORIGIN)
        self.add(grid)

        def update_bits(mob, dt):
            for row in mob:
                for bit in row:
                    if random.random() < 0.08:  
                        new_val = str(random.randint(0, 1))
                        bit.become(Text(new_val, font_size=36).move_to(bit.get_center()))

        grid.add_updater(update_bits)
        self.wait(4)
        grid.remove_updater(update_bits)
        self.remove(grid)
def involute_point(rb, t):
    x = rb * (np.cos(t) + t * np.sin(t))
    y = rb * (np.sin(t) - t * np.cos(t))
    return np.array([x, y, 0])

class InvoluteGear(VGroup):
    def __init__(self, teeth=20, module=0.3, pressure_angle=20*DEGREES, **kwargs):
        super().__init__(**kwargs)
        pitch_radius = module * teeth / 2
        base_radius = pitch_radius * np.cos(pressure_angle)
        addendum = module
        dedendum = 1.25 * module
        outer_radius = pitch_radius + addendum
        root_radius = pitch_radius - dedendum
        tooth_angle = TAU / teeth
        gear_points = []
        t_vals = np.linspace(0, 0.7, 10)
        involute = [involute_point(base_radius, t) for t in t_vals]
        involute = np.array(involute)
        for i in range(teeth):
            rot = i * tooth_angle
            left = [
                rotate_vector(p, rot)
                for p in involute
            ]
            right = [
                rotate_vector(np.array([p[0], -p[1], 0]), rot + tooth_angle/2)
                for p in involute[::-1]
            ]
            gear_points.extend(left)
            gear_points.extend(right)

        gear = Polygon(*gear_points, color=WHITE)
        hub = Circle(radius=pitch_radius*0.2, color=GRAY)
        self.add(gear, hub)
        self.pitch_radius = pitch_radius
        self.teeth = teeth

class DiagonalMatrix(Scene):
    def involuteGearSystem(self):
        self.add_sound("voiceovers/scale_machine.mp3")
        gear1 = InvoluteGear(teeth=12, module=0.25).set_color(BLUE)
        gear2 = InvoluteGear(teeth=6, module=0.25).set_color(GREEN)
        center_distance = gear1.pitch_radius + gear2.pitch_radius
        gear1.move_to(LEFT*2)
        gear2.move_to(gear1.get_center() + RIGHT*center_distance)
        self.add(gear1, gear2)
        tracker = ValueTracker(0)
        gear1.angle = 0
        gear2.angle = 0

        def update1(m):
            angle = tracker.get_value()
            m.rotate(angle - m.angle, about_point=m.get_center())
            m.angle = angle

        def update2(m):
            ratio = gear1.teeth / gear2.teeth
            angle = -tracker.get_value() * ratio
            m.rotate(angle - m.angle, about_point=m.get_center())
            m.angle = angle

        gear1.add_updater(update1)
        gear2.add_updater(update2)
        self.add_sound("voiceovers/gear-click.mp3")
        self.play(
            tracker.animate.set_value(6*PI),
            run_time=4,
            rate_func=linear
        )
        self.play(FadeOut(gear1, gear2))  
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/DiagonalMatrixExplanation.mp3")
        title = Text("Ma trận đường chéo", font="Noto Sans").set_z_index(12).to_edge(UP)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(title))

        matrix = Matrix([
            ["a", "b", "c"],
            ["d", "e", "f"],
            ["g", "h", "i"]
        ])
        matrix.scale(1.2)
        self.add_sound("voiceovers/click.wav")
        self.play(Create(matrix))
        self.wait()
        diagonal = VGroup(*[matrix.get_entries()[i*3+i] for i in range(3)])
        self.play(diagonal.animate.set_color(YELLOW))
        self.wait()

        diag_matrix = Matrix([
            ["a", "0", "0"],
            ["0", "e", "0"],
            ["0", "0", "i"]
        ]).scale(1.2)
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(Transform(matrix, diag_matrix))
        self.wait(2)
        entries = matrix.get_entries()

        start = entries[0].get_center()   
        end = entries[8].get_center()     

        diag_line = Line(start, end)
        diag_line.set_stroke(color=YELLOW, width=12)

        diagonal = VGroup(entries[0], entries[4], entries[8])
        explanation = Text(
            "Chỉ các phần tử trên đường chéo chính mới khác 0.", font="Noto Sans"
        ).scale(0.6).next_to(matrix, DOWN)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Create(diag_line), Write(explanation))
        self.wait()
        self.play(diagonal.animate.set_color(YELLOW))
        self.wait()
        self.play(FadeOut(matrix, diag_line, explanation))
        self.involuteGearSystem()
        self.add_sound("voiceovers/DiagonalTransformation.mp3")
        matrix = [[0.5, 0], [0, 2]]
        matrix_tex = MathTex(
            "A = \\begin{bmatrix} 0.5 & 0 \\\\ 0 & 2 \\end{bmatrix}"
        ).to_edge(LEFT).set_z_index(12)
        window_rect, wall_with_hole, grid, points = create_grid()
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(matrix_tex), FadeIn(wall_with_hole), Create(window_rect))
        self.play(Create(grid), FadeIn(points))
        
        square = Square(side_length=2, color=MAROON_E, fill_opacity=0.3)
        self.play(Create(square))
        self.wait(2)
        anims = animate_points_matrix(self, grid, points, matrix) 
        self.add_sound("voiceovers/sci-fi-effect.mp3")   
        self.play(
            square.animate.apply_matrix(matrix),
            *anims,
            run_time=2,
            rate_func=linear
        )
        self.wait(2)
        self.play(FadeOut(matrix_tex, grid, points, square))
        self.add_sound("voiceovers/CircleToEllipseScaling.mp3")
        window_rect, wall_with_hole, grid, points = create_grid()
        self.play(Create(grid), FadeIn(points))
        scaling_matrix = [[3, 0], [0, 1]]
        matrix_tex = MathTex(
            "A = \\begin{bmatrix} 3 & 0 \\\\ 0 & 1 \\end{bmatrix}"
        ).to_edge(LEFT).set_z_index(12)
        unit_circle = Circle(radius=1, color=MAROON_E, stroke_width=2, fill_opacity=0.3)
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(matrix_tex))
        self.play(FadeIn(unit_circle))
        self.wait()
        anims = animate_points_matrix(self, grid, points, scaling_matrix)    
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(
            unit_circle.animate.apply_matrix(scaling_matrix),
            *anims,
            run_time=2,
            rate_func=linear
        )
        self.wait(3)

class EigenvectorInvariantSpan(LinearTransformationScene):
    def __init__(self, **kwargs):
        super().__init__(
            show_basis_vectors=True,
            leave_ghost_vectors=False,
            **kwargs
        )

    def construct(self):
        self.wait()
        self.add_sound("voiceovers/EigenvectorInvariantSpan.mp3")
        self.plane.fade(0.3)
        matrix = [[3, 1],
                  [0, 2]]

        v = np.array([1, -1])

        span_line = Line(
            start=6 * LEFT + 6 * UP,
            end=6 * RIGHT + 6 * DOWN,
            color=MAROON_E
        ).set_z_index(-1)

        vector = Vector(v, color=YELLOW)
        label_v = self.get_vector_label(vector, "v")
        self.wait(2)
        self.add_vector(vector)
        self.wait(2)
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(Create(span_line))
        self.wait()
        self.add_moving_mobject(label_v)
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.apply_matrix(matrix)
        self.wait(2)
        equation = MathTex("Av = \\lambda v", substrings_to_isolate="v"
                           ).to_edge(UP)
        equation.set_color_by_tex("v", YELLOW)
        equation[-2][1].set_color(PURPLE)
        equation.add_background_rectangle()
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(equation))
        self.wait()
        self.play(Indicate(VGroup(equation[2], equation[-1])))
        self.wait()
        self.play(Indicate(equation[-2][1]))
        self.wait(2)
class DiagonalEigen(LinearTransformationScene):
    def __init__(self, **kwargs):
        LinearTransformationScene.__init__(
            self,
            **kwargs
        )

    def construct(self):
        self.wait()
        self.add_sound("voiceovers/DiagonalEigen.mp3")
        self.plane.fade(0.3)
        matrix = [[2, 0],
                  [0, 3]]

        v = self.add_vector([1,1], color=BLUE_E)
        v1_label = self.get_vector_label(self.i_hat, "v1")
        v2_label = self.get_vector_label(self.j_hat, "v2")

        matrix_tex = MathTex(
            r"A=\begin{bmatrix}2 & 0 \\ 0 & 3\end{bmatrix}"
        ).to_corner(UL).add_background_rectangle()
        matrix_tex[1][3].set_color(GREEN)
        matrix_tex[1][-2].set_color(RED)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(matrix_tex))
        self.wait()
        self.add_moving_mobject(v1_label)
        self.add_moving_mobject(v2_label)
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.apply_matrix(matrix)
        self.wait(0.5)
        self.play(Wiggle(VGroup(self.i_hat, self.j_hat)))
        self.wait(4) 
class ColoredDiagonalGrid(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/ColoredDiagonalGrid.mp3")
        n = 6
        cell_size = 0.9
        squares = VGroup()
        numbers = []
        grid = VGroup()
        for i in range(n):
            row = []
            for j in range(n):
                square = Square(side_length=cell_size)
                square.set_fill(BLUE_E, opacity=0.8)
                square.set_stroke(WHITE, width=1)
                num = Integer(i*n + j + 1).scale(0.6)
                cell = VGroup(square, num)
                row.append(num)
                squares.add(square)
                grid.add(cell)
            numbers.append(row)
        grid.arrange_in_grid(rows=n, cols=n, buff=0)
        self.add_sound("voiceovers/game-start.mp3")
        self.play(FadeIn(grid))
        self.wait(1)
        animations = []
        for i in range(n):
            for j in range(n):
                if i != j:
                    zero = Integer(0).scale(0.6)
                    zero.move_to(numbers[i][j])
                    animations.append(Transform(numbers[i][j], zero))
                    animations.append(
                        squares[i*n + j].animate.set_fill(GREY_E, opacity=0.4)
                    )
                else:
                    animations.append(
                        squares[i*n + j].animate.set_fill(YELLOW, opacity=0.9)
                    )
        self.add_sound("voiceovers/click.wav")
        self.play(*animations, run_time=2)
        self.wait()
        self.play(FadeOut(grid))
        self.diagonalMatrixIndependentScaling()
    def diagonalMatrixIndependentScaling(self):
        plane = NumberPlane()
        self.play(Create(plane))
        v = Vector([1, 2], color=YELLOW)
        label_v = MathTex(r"\vec{v}").next_to(v.get_end(), UR)
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(GrowArrow(v), Write(label_v))
        matrix = MathTex(
            r"A=\begin{bmatrix}2 & 0 \\ 0 & 0.5\end{bmatrix}"
        ).to_edge(UP).shift(2*LEFT).add_background_rectangle()
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(matrix))
        self.add_sound("voiceovers/DiagonalMatrixIndependentScaling.mp3")
        step1 = Text("Bước 1: Phóng to x lên 2 lần.", font="Noto Sans", font_size=32).to_edge(DOWN)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(step1))

        v_x_scaled = Vector([2, 2], color=BLUE)
        label_x = MathTex(r"(2,2)").next_to(v_x_scaled.get_end(), UR)
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(
            Transform(v, v_x_scaled),
            Transform(label_v, label_x)
        )

        self.wait(1)

        step2 = Text("Bước 2: Nhân y với hệ số 0,5", font="Noto Sans", font_size=32).to_edge(DOWN)
        self.add_sound("voiceovers/click.wav")
        self.play(Transform(step1, step2))

        v_final = Vector([2, 1], color=RED)
        label_final = MathTex(r"(2,1)").next_to(v_final.get_end(), UR)
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(
            Transform(v, v_final),
            Transform(label_v, label_final)
        )

        self.wait()

        conclusion = Text(
            "Ma trận đường chéo = tỷ lệ trục độc lập", font="Noto Sans",
            font_size=34
        ).to_edge(DOWN)
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(Transform(step1, conclusion))
        self.wait(3)
class ComputationalEfficiency(Scene):
    def diagonalBulb(self):
        n = 6
        cell = 1
        grid = VGroup()
        cells = {}
        for r in range(n):
            for c in range(n):
                sq = Square(side_length=cell, color=GRAY)
                sq.move_to([(c - n/2 + 0.5), (r - n/2 + 0.5), 0])
                grid.add(sq)
                cells[(r, c)] = sq
        self.play(Create(grid))
        bulbs = VGroup()
        for i in range(n):
            r = i
            c = n - 1 - i
            bulb = SVGMobject("assets/lightbulb.svg")
            bulb.set_color(YELLOW)
            bulb.scale(0.35)
            bulb.move_to(cells[(r, c)].get_center())
            bulbs.add(bulb)
        self.add_sound("voiceovers/game-start.mp3")
        self.play(LaggedStart(*[FadeIn(bulb) for bulb in bulbs], lag_ratio=0.03))
        self.wait()
        self.play(FadeOut(bulbs, grid))
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/ComputationalEfficiency.mp3")
        self.diagonalBulb()
        title = Text("Hiệu quả tính toán", color=YELLOW, weight=BOLD, font="Noto Sans")
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(title))
        self.wait(2)
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(title.animate.to_corner(UL))
        self.wait(2)
        A = Matrix([
            ["a","b","c"],
            ["d","e","f"],
            ["g","h","i"]
        ])

        A_label = MathTex("A =")
        A_group = VGroup(A_label, A).arrange(RIGHT)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(A_group))
        self.wait()
        self.add_sound("voiceovers/aww.mp3")
        self.wait(.5)

        D = Matrix([
            ["a","0","0"],
            ["0","e","0"],
            ["0","0","i"]
        ])

        D_label = MathTex("D =")
        D_group = VGroup(D_label, D).arrange(RIGHT)

        D_group.move_to(A_group)
        self.add_sound("voiceovers/shine2.mp3")
        self.play(Transform(A_group, D_group), run_time=1.5)
        self.wait(0.5)

        diag = [0,4,8]
        entries = A_group[1].get_entries()

        self.play(*[
            entries[i].animate.set_color(YELLOW)
            for i in diag
        ])
        self.wait()
        self.play(FadeOut(A_group))
        self.diagonalMatrixMultiplication()
        self.diagonalMatrixInverse()
        self.diagonalMatrixPower()
        self.wait(2)
    def diagonalMatrixMultiplication(self):
        self.add_sound("voiceovers/DiagonalMatrixMultiplication.mp3")
        title = Text("Phép nhân ma trận", font="Noto Sans"
                     ).scale(0.7).to_corner(UR)
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(FadeIn(title))

        D1 = Matrix([
            ["a_1", "0", "0"],
            ["0", "a_2", "0"],
            ["0", "0", "a_3"]
        ])

        D2 = Matrix([
            ["b_1", "0", "0"],
            ["0", "b_2", "0"],
            ["0", "0", "b_3"]
        ])

        result = Matrix([
            ["a_1 b_1", "0", "0"],
            ["0", "a_2 b_2", "0"],
            ["0", "0", "a_3 b_3"]
        ])
        d1 = [D1.get_entries()[0], D1.get_entries()[4], D1.get_entries()[8]]
        d2 = [D2.get_entries()[0], D2.get_entries()[4], D2.get_entries()[8]]
        r  = [result.get_entries()[0], result.get_entries()[4], result.get_entries()[8]]
        for i in range(3):
            d1[i].set_color(YELLOW)
            d2[i].set_color(BLUE)
            r[i].set_color(GREEN)

        mult = MathTex(r"\times")
        eq = MathTex("=")
        group = VGroup(D1, mult, D2, eq, result)
        group.arrange(RIGHT, buff=0.8).scale(0.8)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(D1), Write(mult), Write(D2))
        zeros = [x for x in D1.get_entries() if x not in d1] + \
                [x for x in D2.get_entries() if x not in d2]

        self.play(*[z.animate.set_opacity(0.2) for z in zeros])
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(eq), Write(result.get_brackets()))
        for i in range(3):
            arrow = Arrow(
                d1[i].get_right(),
                d2[i].get_left(),
                buff=0.1,
                color=GREEN
            )
            self.add_sound("voiceovers/sword-swing.wav")
            self.play(GrowArrow(arrow), run_time=0.5)
            pair = VGroup(d1[i].copy(), d2[i].copy())
            pair.arrange(RIGHT, buff=0.2)
            pair.move_to(r[i])
            self.add_sound("voiceovers/whoosh407576.mp3")
            self.play(
                TransformFromCopy(d1[i], pair[0]),
                TransformFromCopy(d2[i], pair[1]),
                run_time=0.5
            )
            self.play(
                FadeOut(pair),
                FadeOut(arrow),
                FadeIn(r[i]), run_time=0.5
            )

        result_zeros = [x for x in result.get_entries() if x not in r]
        for z in result_zeros:
            z.shift(0.3*LEFT)
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(*[FadeIn(z, shift=0.2*DOWN) for z in result_zeros])
        self.wait()
        self.play(FadeOut(group, title))

    def diagonalMatrixInverse(self):
        self.add_sound("voiceovers/DiagonalMatrixInverse.mp3")
        title = Text("Phép nghịch đảo", font="Noto Sans"
                     ).scale(0.7).to_corner(UR)
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(FadeIn(title))

        D = Matrix([
            ["d_1", "0", "0"],
            ["0", "d_2", "0"],
            ["0", "0", "d_3"]
        ])

        inv_symbol = MathTex("^{-1}")
        inv_symbol.next_to(D, UR, buff=0.05) 
        equals = MathTex("=")

        D_inv = Matrix([
            [r"\frac{1}{d_1}", r"\frac{1}{d_2}", r"\frac{1}{d_3}"],
            [r"\frac{1}{d_1}", r"\frac{1}{d_2}", r"\frac{1}{d_3}"],
            [r"\frac{1}{d_1}", r"\frac{1}{d_2}", r"\frac{1}{d_3}"]
        ])

        D_entries = D.get_entries()
        Dinv_entries = D_inv.get_entries()

        diag_indices = [0, 4, 8]

        for i in diag_indices:
            D_entries[i].set_color(YELLOW)
            Dinv_entries[i].set_color(GREEN)
        off_diag = [i for i in range(9) if i not in diag_indices]

        for i in off_diag:
            Dinv_entries[i].set_opacity(0)

        left = VGroup(D, inv_symbol)
        group = VGroup(left, equals, D_inv)
        group.arrange(RIGHT, buff=0.8).shift(UP*0.5)
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(D),
                  FadeIn(inv_symbol, shift=0.2*RIGHT))

        diag = [D.get_entries()[0], D.get_entries()[4], D.get_entries()[8]]
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(equals), FadeIn(D_inv.get_brackets()))

        result_diag = [Dinv_entries[i] for i in diag_indices]
        for item in result_diag:
            item.scale(0.6)

        for i in range(3):
            self.add_sound("voiceovers/whoosh407576.mp3")
            self.play(TransformFromCopy(diag[i], result_diag[i]), run_time=0.5)

        zero_anims = []
        for i in off_diag:
            zero = MathTex("0").move_to(Dinv_entries[i])
            zero_anims.append(Transform(Dinv_entries[i], zero))
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(*zero_anims)
        self.wait()
        self.play(FadeOut(group, title))

    def diagonalMatrixPower(self):
        self.add_sound("voiceovers/DiagonalMatrixPower.mp3")
        title = Text("Lũy thừa", font="Noto Sans"
                     ).scale(0.7).to_corner(UR)
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(FadeIn(title))
        D = Matrix([
            ["d_1", "0", "0"],
            ["0", "d_2", "0"],
            ["0", "0", "d_3"]
        ])

        power_symbol = MathTex("^{100}")
        power_symbol.next_to(D, UR, buff=0.05)

        equals = MathTex("=")

        D_pow = Matrix([
            [r"d_1^{100}", r"d_2^{100}", r"d_3^{100}"],
            [r"d_1^{100}", r"d_2^{100}", r"d_3^{100}"],
            [r"d_1^{100}", r"d_2^{100}", r"d_3^{100}"]
        ])

        D_entries = D.get_entries()
        pow_entries = D_pow.get_entries()

        diag_indices = [0,4,8]
        off_diag = [i for i in range(9) if i not in diag_indices]

        for i in diag_indices:
            D_entries[i].set_color(YELLOW)
            pow_entries[i].set_color(GREEN)

        for i in off_diag:
            pow_entries[i].set_opacity(0)

        left = VGroup(D, power_symbol)
        group = VGroup(left, equals, D_pow)
        group.arrange(RIGHT, buff=0.8).shift(UP*0.5)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(D))
        self.wait(1.5)
        self.add_sound("voiceovers/click.wav")
        self.play(FadeIn(power_symbol, shift=0.1*UP))
        self.wait()
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(equals), Write(D_pow.get_brackets()))

        diag = [D_entries[i] for i in diag_indices]
        result_diag = [pow_entries[i] for i in diag_indices]

        for i in range(3):
            self.add_sound("voiceovers/whoosh407576.mp3")
            self.play(TransformFromCopy(diag[i], result_diag[i]), run_time=0.5)
            self.wait(0.3)

        zero_anims = []
        for i in off_diag:
            zero = MathTex("0").move_to(pow_entries[i])
            zero_anims.append(Transform(pow_entries[i], zero))
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(*zero_anims)
        self.wait(2)
        self.play(FadeOut(group, title))
class DiagonalizationIntro(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/DiagonalizationIntro_title.mp3")
        title = Text("Chéo hóa ma trận", font="Noto Sans")
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(title))
        self.wait()
        eq = MathTex(
            "A", "=",
            "P",
            "D",
            "P^{-1}"
        ).scale(1.8)

        eq[2].set_color(BLUE)
        eq[3].set_color(YELLOW)
        eq[4].set_color(GREEN)
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(title.animate.to_edge(UP))
        self.add_sound("voiceovers/DiagonalizationIntro.mp3")
        self.wait(4)
        find_coordinates_text = Text("Tìm một hệ tọa độ mà tại đó ma trận trở thành ma trận đường chéo", font="Noto Sans"
                     ).scale(0.7)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(find_coordinates_text), run_time=2)
        self.wait(2)
        self.play(FadeOut(find_coordinates_text))
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(eq), run_time=2)
        self.wait(3)

        p_text = VGroup(
            MathTex("P:"),
            Text("ma trận các vectơ riêng", font="Noto Sans").scale(0.7)
        ).arrange(RIGHT).set_color(BLUE)

        d_text = VGroup(
            MathTex("D:"),
            Text("ma trận đường chéo của các giá trị riêng", font="Noto Sans").scale(0.7)
        ).arrange(RIGHT).set_color(YELLOW)

        pinv_text = VGroup(
            MathTex("P^{-1}:"),
            Text("nghịch đảo của P", font="Noto Sans").scale(0.7)
        ).arrange(RIGHT).set_color(GREEN)

        explanation = VGroup(
            p_text,
            d_text,
            pinv_text
        ).arrange(DOWN, aligned_edge=LEFT).next_to(eq, DOWN, buff=1)
        for text in explanation:
            self.add_sound("voiceovers/writin.mp3")
            self.play(Write(text))
            self.wait(0.5)
        self.wait()
        self.play(FadeOut(explanation, eq, title))
        self.diagonalizationVis()
    def perform_step(self, matrix, label_text, plane, i_hat, j_hat):
        title = Text(label_text, font="Noto Sans", font_size=30).to_corner(UL)
        self.add(title)
        curr_i = i_hat.get_end()[:2]
        curr_j = j_hat.get_end()[:2]
        
        new_i = np.dot(matrix, curr_i)
        new_j = np.dot(matrix, curr_j)
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(
            plane.animate.apply_matrix(matrix),
            i_hat.animate.put_start_and_end_on(ORIGIN, [new_i[0], new_i[1], 0]),
            j_hat.animate.put_start_and_end_on(ORIGIN, [new_j[0], new_j[1], 0]),
            run_time=2
        )
        self.wait()
        self.remove(title)

    def diagonalizationVis(self):
        self.add_sound("voiceovers/DiagonalizationVis.mp3")
        P_inv = np.array([[0.5, 0.5], [0.5, -0.5]])
        D = np.array([[3, 0], [0, 1]])
        P = np.array([[1, 1], [1, -1]])

        plane = NumberPlane()
        
        i_hat = Vector(RIGHT, color=RED)
        j_hat = Vector(UP, color=GREEN)
        
        self.add(plane, i_hat, j_hat)
        self.perform_step(P_inv, "Bước 1: P⁻¹ (Thay đổi cơ sở)", plane, i_hat, j_hat)
        self.perform_step(D, "Bước 2: D (Điều chỉnh tỷ lệ theo đường chéo)", plane, i_hat, j_hat)
        self.perform_step(P, "Bước 3: P (Quay trở lại cơ sở tiêu chuẩn)", plane, i_hat, j_hat)
        self.play(*[mob.animate.set_opacity(0.1) for mob in self.mobjects])
        
        final_text = Text("Hoàn thành biến đổi A = PDP⁻¹", font="Noto Sans", color=YELLOW)
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(FadeIn(final_text))
        self.wait(3)
def svdCompression(scene):
        img = Image.open("assets/lenna_color.png").convert("L")  # grayscale
        A = np.array(img)
        U, S, VT = np.linalg.svd(A)
        ranks = [1, 5, 20, 50]
        for k in ranks:
            Ak = U[:, :k] @ np.diag(S[:k]) @ VT[:k, :]
            # Normalize for display
            Ak = np.clip(Ak, 0, 255).astype(np.uint8)
            im = Image.fromarray(Ak)
            im.save("assets/temp.png")
            img_obj = ImageMobject("assets/temp.png").scale(2)
            label = Text(f"Rank {k} approximation").scale(0.6).next_to(img_obj, DOWN)
            scene.play(FadeIn(img_obj), FadeIn(label))
            scene.play(FadeOut(img_obj), FadeOut(label))
class SVDIntro(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/SVDIntro_title.mp3")
        title = Text("Giảm chiều dữ liệu và phân tích giá trị đơn (SVD)", 
                     font="Noto Sans").scale(0.7)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(title), run_time=3)
        self.wait()

        eq = MathTex(
            "A", "=",
            "U",
            "\\Sigma",
            "V^T"
        ).scale(1.8)

        eq[2].set_color(BLUE)    # U
        eq[3].set_color(YELLOW)  # Sigma
        eq[4].set_color(GREEN)   # V^T
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(title.animate.to_edge(UP))
        self.add_sound("voiceovers/SVDIntro.mp3")
        self.wait()
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(eq))
        self.wait(0.5)
        self.add_sound("voiceovers/wiggle.mp3")
        self.play(Wiggle(eq[3]))
        self.wait()
       
        u_text = VGroup(
            MathTex("U:"),
            Text("ma trận trực giao", font="Noto Sans").scale(0.7)
        ).arrange(RIGHT).set_color(BLUE)

        s_text = VGroup(
            MathTex("\\Sigma:"),
            Text("giá trị đơn", font="Noto Sans").scale(0.7)
        ).arrange(RIGHT).set_color(YELLOW)

        v_text = VGroup(
            MathTex("V^T:"),
            Text("ma trận trực giao", font="Noto Sans").scale(0.7)
        ).arrange(RIGHT).set_color(GREEN)

        explanations = VGroup(
            u_text, s_text, v_text
        ).arrange(DOWN, aligned_edge=LEFT).next_to(eq, DOWN, buff=1)

        for text in explanations:
            self.add_sound("voiceovers/writin.mp3")
            self.play(Write(text))
            self.wait(0.5)
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(Flash(eq[3]))
        self.wait()
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.svdVisualization()
        svdCompression(self)
        self.wait(2)   
    def svdVisualization(self):
        self.add_sound("voiceovers/SVDVisualization.mp3")
        points = VGroup(*[Dot(point=RIGHT * np.cos(t) + UP * np.sin(t), radius=0.03) 
                          for t in np.linspace(0, 2*PI, 100)])
        
        matrix = [[2.5, 0], [0, 0.8]]
        
        self.add(points)
        title = Text("SVD: Kéo giãn dữ liệu", font="Noto Sans", font_size=36).to_edge(UP)
        self.add_sound("voiceovers/game-start.mp3")
        self.play(FadeIn(title))
        self.wait(0.5)
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(
            *[p.animate.apply_matrix(matrix) for p in points]
        )

        v1 = Vector([2.5, 0], color=YELLOW)
        v2 = Vector([0, 0.8], color=RED)
        
        label1 = MathTex("\\sigma_1 = 2.5", color=YELLOW).next_to(v1.get_end(), RIGHT)
        label2 = MathTex("\\sigma_2 = 0.8", color=RED).next_to(v2.get_end(), UP)
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(Create(v1), Write(label1))
        self.wait()
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(Create(v2), Write(label2))
        self.wait()
        self.play(*[FadeOut(mob) for mob in self.mobjects])

class ScalarMatrix(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/scalar_check.mp3")
        title = Text("Ma trận vô hướng", font="Noto Sans", font_size=42).set_z_index(12)
        number_one_text = Text("Sự giãn nở đồng đều", font="Noto Sans", font_size=24)
        VGroup(title, number_one_text).arrange(DOWN)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(title))
        self.wait(0.5)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(number_one_text, shift=DOWN))
        self.wait()
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(
            title.animate.to_edge(UP),
            LaggedStart(*[FadeOut(obj, shift=DOWN) for obj in number_one_text]),
        )
        self.wait()
        self.add_sound("voiceovers/ScalarMatrix_.mp3")
        diag_matrix = Matrix([
            ["a", "0", "0"],
            ["0", "e", "0"],
            ["0", "0", "i"]
        ])

        diag_text = Text("Ma trận đường chéo", font="Noto Sans").scale(0.6)
        diag_group = VGroup(diag_matrix, diag_text).arrange(DOWN)
        diag_group.shift(UP*0.5)
        self.add_sound("voiceovers/click.wav")
        self.play(Create(diag_matrix))
        self.play(FadeIn(diag_text))
        self.wait()

        diag_entries = VGroup(
            diag_matrix.get_entries()[0],
            diag_matrix.get_entries()[4],
            diag_matrix.get_entries()[8]
        )

        self.play(diag_entries.animate.set_color(YELLOW))
        self.wait()

        scalar_matrix = Matrix([
            ["k", "0", "0"],
            ["0", "k", "0"],
            ["0", "0", "k"]
        ])

        scalar_text = Text("Ma trận vô hướng", font="Noto Sans").scale(0.6)
        scalar_group = VGroup(scalar_matrix, scalar_text).arrange(DOWN)
        scalar_group.move_to(diag_group)
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(Transform(diag_matrix, scalar_matrix))
        self.wait()

        new_entries = VGroup(
            diag_matrix.get_entries()[0],
            diag_matrix.get_entries()[4],
            diag_matrix.get_entries()[8]
        )
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(new_entries.animate.set_color(GREEN),
                  Transform(diag_text, scalar_text))
        self.wait()
        self.add_sound("voiceovers/UniformScaler.mp3")
        self.wait(2)
        self.play(FadeOut(diag_matrix, diag_text))
        pixel_guy = SVGMobject("assets/Pixel-Guy.svg")
        self.add_sound("voiceovers/energy-up.mp3")
        self.play(FadeIn(pixel_guy))
        self.wait()
        scalar_k = 2
        matrix = [[scalar_k, 0], [0, scalar_k]]
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(ApplyMatrix(matrix, pixel_guy))
        self.wait()
        self.play(FadeOut(pixel_guy))
        self.add_sound("voiceovers/ScalarTransformation.mp3")
        matrix_tex = MathTex(
            "S = \\begin{bmatrix} 2 & 0 \\\\ 0 & 2 \\end{bmatrix}"
        ).to_edge(LEFT).set_z_index(12)
        window_rect, wall_with_hole, grid, points = create_grid()
        self.add_sound("voiceovers/game-start.mp3")
        self.play(FadeIn(matrix_tex), FadeIn(wall_with_hole), Create(window_rect))
        self.play(FadeIn(grid), FadeIn(points))
        
        square = Square(side_length=2, color=MAROON_E, fill_opacity=0.3)
        self.play(FadeIn(square))
        anims = animate_points_matrix(self, grid, points, matrix)    
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(
            square.animate.apply_matrix(matrix),
            *anims,
            run_time=3,
            rate_func=linear
        )
        self.wait(3)

class IdentityMatrix(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/IdentityMatrix.mp3")
        title = Text("Ma trận đơn vị (I)", color=GREEN, font="Noto Sans", font_size=42).set_z_index(12)
        number_one_text = Text("\"Số 1\"", font="Noto Sans", font_size=24)
        VGroup(title, number_one_text).arrange(DOWN)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(title))
        self.wait(0.5)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(number_one_text, shift=DOWN))
        self.wait()
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(
            title.animate.to_edge(UP),
            LaggedStart(*[FadeOut(obj, shift=DOWN) for obj in number_one_text]),
        )
        self.wait()

        matrix = Matrix([
            ["k", "0", "0"],
            ["0", "k", "0"],
            ["0", "0", "k"]
        ])
        entries = matrix.get_entries()
        k1, k2, k3 = entries[0], entries[4], entries[8]
        k_diag = VGroup(k1, k2, k3)
        k_diag.set_color(BLUE)
        definition = Text("Ma trận vô hướng trong đó k=1", font="Noto Sans"
                          ).scale(0.7)
        iden_group = VGroup(matrix, definition).arrange(DOWN)
        iden_group.shift(UP*0.5)

        one1 = MathTex("1", color=YELLOW).move_to(k1)
        one2 = MathTex("1", color=YELLOW).move_to(k2)
        one3 = MathTex("1", color=YELLOW).move_to(k3)
        self.add_sound("voiceovers/IdentityMatrix_define.mp3")
        self.add_sound("voiceovers/game-start.mp3")
        self.play(Create(matrix))
        self.wait()
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(k_diag.animate.set_color(BLUE))
        self.wait()
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(definition))
        self.wait()
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(
            Transform(k1, one1),
            Transform(k2, one2),
            Transform(k3, one3),
        )

        self.wait(2)
        self.add_sound("voiceovers/do_nothing.mp3")
        self.play(FadeOut(matrix, definition))
        do_nothing = SVGMobject("assets/40.svg")
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(do_nothing))
        self.wait()
        self.play(FadeOut(do_nothing))
        self.add_sound("voiceovers/IdentityMatrix_tranform.mp3")
        identity_matrix = [[1, 0], [0, 1]]
        matrix_tex = MathTex(
            "I = \\begin{bmatrix} 1 & 0 \\\\ 0 & 1 \\end{bmatrix}"
        ).to_edge(LEFT).set_z_index(12)
        window_rect, wall_with_hole, grid, points = create_grid()
        self.add_sound("voiceovers/game-start.mp3")
        self.play(FadeIn(wall_with_hole), Create(window_rect))
        self.play(FadeIn(grid), FadeIn(points))
        self.play(FadeIn(matrix_tex))
        
        circle = Circle(radius=1, color=MAROON_E, fill_opacity=0.2)
        text = Text("Không thay đổi", font="Noto Sans", font_size=24, color=GREEN
                    ).next_to(circle, UP).shift(1.3*RIGHT).set_z_index(12)
        self.play(FadeIn(circle))
        anims = animate_points_matrix(self, grid, points, identity_matrix)    
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(
            circle.animate.apply_matrix(identity_matrix),
            *anims,
            run_time=2,
            rate_func=linear
        )
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(FadeIn(text))
        self.add_sound("voiceovers/NeutralElement.mp3")
        self.wait(2)
        self.play(FadeOut(grid, points))
        self.play(FadeOut(matrix_tex, wall_with_hole, window_rect, text, circle))    
        scalar_eq = MathTex("5", r"\times", "1", "=", "5")
        matrix_A = MathTex("A")
        times = MathTex(r"\dot")
        identity = MathTex("I")
        equals = MathTex("=")
        result = MathTex("A")

        equation = VGroup(matrix_A, times, identity, equals, result).arrange(RIGHT)
        eq_group = VGroup(scalar_eq, equation).arrange(DOWN)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(scalar_eq))
        self.wait()
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(equation))
        self.wait()
        box = SurroundingRectangle(equation, color=YELLOW)
        self.add_sound("voiceovers/click.wav")
        self.play(Create(box))
        self.wait(2)
        self.play(FadeOut(eq_group, box))
        self.add_sound("voiceovers/north-star.mp3")
        north_star = ImageMobject("assets/north-star.png").scale(0.3)
        self.add_sound("voiceovers/shooting-star.mp3")
        self.play(FadeIn(north_star))
        self.wait()
        self.play(FadeOut(north_star))
        nn = self.get_nn().scale(0.6).shift(3*LEFT)
        self.add_sound("voiceovers/beep.mp3")
        self.play(FadeIn(nn))
        self.wait()
        multiply_expr = MathTex("A", r"\cdot", "I", "=", "A")
        multiply_expr.shift(3*RIGHT)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(multiply_expr))
        self.wait()

        inverse_eq = MathTex("A", r"\cdot", "A^{-1}", "=", "I")
        inverse_eq.move_to(multiply_expr)
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(Transform(multiply_expr, inverse_eq))
        self.wait(3)
    def get_nn(self):
        matrix_tex = MathTex(
            r"W^{[l]} =",
            r"\begin{bmatrix}"
            r"w^{[l]}_{11} & w^{[l]}_{12} & \cdots & w^{[l]}_{1n^{[l-1]}} \\"
            r"w^{[l]}_{21} & w^{[l]}_{22} & \cdots & w^{[l]}_{2n^{[l-1]}} \\"
            r"\vdots & \vdots & \ddots & \vdots \\"
            r"w^{[l]}_{n^{[l]}1} & w^{[l]}_{n^{[l]}2} & \cdots & w^{[l]}_{n^{[l]}n^{[l-1]}}"
            r"\end{bmatrix}",
            font_size=36
        )

        matrix_tex.to_edge(LEFT, buff=1)
        matrix_tex.shift(DOWN * 0.5)

        def layer(n, x_pos):
            return VGroup(*[
                Circle(radius=0.25, color=BLUE_D, fill_opacity=1)
                for _ in range(n)
            ]).arrange(DOWN, buff=0.35).move_to([x_pos, 0, 0])

        input_layer = layer(5, 2)
        hidden_layer = layer(6, 3.8)
        output_layer = layer(3, 5.6)

        for neuron in hidden_layer:
            neuron.set_color(BLUE_C)
        for neuron in output_layer:
            neuron.set_color(BLUE_B)

        def connect_layers(layer1, layer2):
            return VGroup(*[
                Line(
                    n1.get_center(),
                    n2.get_center(),
                    stroke_color=BLUE_C,
                    stroke_width=2
                )
                for n1 in layer1
                for n2 in layer2
            ])

        connections_1 = connect_layers(input_layer, hidden_layer)
        connections_2 = connect_layers(hidden_layer, output_layer)
        return VGroup(matrix_tex, connections_1, connections_2, input_layer, hidden_layer, output_layer)
class Transformers(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/Transformers_title.mp3")
        title = Text("Ma trận Biến dạng", font="Noto Sans", font_size=42).set_z_index(12)
        subtitle = Text("Ma trận Trượt và Ma trận Trực giao", font="Noto Sans", font_size=24)
        VGroup(title, subtitle).arrange(DOWN)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(title))
        self.wait(0.5)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(subtitle, shift=DOWN))
        self.wait()
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(
            FadeOut(title, shift=UP),
            LaggedStart(*[FadeOut(obj, shift=DOWN) for obj in subtitle]),
        )
        self.add_sound("voiceovers/Transformers1.mp3")
        self.wait()
        window_rect_left, window_rect_right, wall_with_hole, grid_left, grid_right = create_grid_double()
        self.add_sound("voiceovers/game-start.mp3")
        self.play(FadeIn(wall_with_hole, window_rect_left))
        left_guy = SVGMobject("assets/Pixel-Guy.svg").move_to(window_rect_left.get_center())
        scalar_lbl = Text("Phóng to", font="Noto Sans"
                          ).scale(0.7).set_z_index(12).next_to(window_rect_left, UP)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(left_guy))
        self.wait()
        
        scalar_matrix = [[2,0],[0,2]]
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(FadeIn(scalar_lbl),
                  left_guy.animate.center().apply_matrix(scalar_matrix).move_to(window_rect_left.get_center()))
        self.wait()
        self.add_sound("voiceovers/game-start.mp3")
        self.play(FadeIn(window_rect_right))
        self.add_sound("voiceovers/Transformers2.mp3")
        right_guy = SVGMobject("assets/Pixel-Guy.svg").move_to(window_rect_right.get_center())
        ortho_lbl = Text("Xoay", font="Noto Sans"
                          ).scale(0.7).set_z_index(12).next_to(window_rect_right, UP)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(right_guy))
        self.wait()
        theta = PI/4
        ortho_matrix = np.array([
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)]
        ])
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(FadeIn(ortho_lbl),
                  right_guy.animate.center().apply_matrix(ortho_matrix).move_to(window_rect_right.get_center()))
        self.wait()
        self.play(FadeOut(right_guy))
        right_guy = SVGMobject("assets/Pixel-Guy.svg").move_to(window_rect_right.get_center())
        shear_lbl = Text("Nghiêng", font="Noto Sans"
                          ).scale(0.7).set_z_index(12).next_to(window_rect_right, UP)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(right_guy))
        self.wait()
        shear_matrix = np.array([
            [1,1],
            [0,1]
        ])
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(Transform(ortho_lbl, shear_lbl),
                  right_guy.animate.center().apply_matrix(shear_matrix).move_to(window_rect_right.get_center()))
        self.wait(3)
class ShearMatrix(Scene):
    def deckShear(self):
        self.add_sound("voiceovers/deckShear.mp3")
        table = Rectangle(
            width=10,
            height=6,
            fill_color=GREEN_D,
            fill_opacity=0.8
        ).shift(DOWN)

        card_width = 2.5
        card_height = 3.5
        num_cards = 30
        thickness = 0.03
        shear_amount = 1.5 

        deck = VGroup()

        for i in range(num_cards):
            card = Rectangle(
                width=card_width,
                height=card_height,
                stroke_color=GRAY,
                fill_color=WHITE,
                fill_opacity=1
            )

            card.shift(UP * i * thickness)
            deck.add(card)

        deck.move_to(table.get_center() + UP * 0.2)
        top_label = Text("A♠", font_size=28, color=RED).set_z_index(10)
        top_label.move_to(deck[-1].get_center())
        deck[-1].add(top_label)
        card_group = VGroup(table, deck).scale(0.6)
        self.add_sound("voiceovers/click.wav")
        self.play(Create(table))
        self.add_sound("voiceovers/game-start.mp3")
        self.play(LaggedStart(*[FadeIn(c) for c in deck], lag_ratio=0.03))
        self.wait(0.5)

        animations = []
        for i, card in enumerate(deck):
            t = i / (num_cards - 1)  
            shift = RIGHT * shear_amount * t
            animations.append(card.animate.shift(shift))
        self.add_sound("voiceovers/slidecard03.wav")
        self.play(LaggedStart(*animations, lag_ratio=0.02), run_time=3)
        self.wait(3)
        self.play(FadeOut(card_group))
    def define(self):      
        matrix = Matrix([
            ["1", "?"],
            ["?", "1"]
        ])
        diag_text = Text("Đường chéo đơn vị", font="Noto Sans", color=BLUE).scale(0.6)
        diag_group = VGroup(matrix, diag_text).arrange(DOWN)
        diag_group.shift(UP*0.5)
        entries = matrix.get_entries()
        self.add_sound("voiceovers/click.wav")
        self.play(Create(matrix.get_brackets()))
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(entries[0]), Write(entries[3]), Write(diag_text))
        self.add_sound("voiceovers/ShearMatrix.mp3")
        self.wait()
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(entries[1]), Write(entries[2]))
        self.wait()
        k = MathTex("k", color=YELLOW).move_to(entries[1])
        zero = MathTex("0").move_to(entries[2])
        start = entries[0].get_center()   
        end = entries[3].get_center()     
        diag_line = Line(start, end)
        diag_line.set_stroke(color=YELLOW, width=12)
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(Create(diag_line))
        self.wait()
        self.play(FadeOut(diag_line))
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(Indicate(entries[1]))
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(Indicate(entries[2]))
        self.wait(0.5)
        horizontal_arrow = Arrow(0.5*LEFT, 0.5*RIGHT).next_to(matrix, LEFT)
        horizontal_shear_text = Text("Trượt ngang", font="Noto Sans"
                                     ).scale(0.7).next_to(horizontal_arrow, LEFT)
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(FadeIn(horizontal_shear_text), GrowArrow(horizontal_arrow))
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(
            Transform(entries[1], k),
            Transform(entries[2], zero)
        )
        self.wait(0.5)
        box = SurroundingRectangle(entries[1], color=YELLOW, buff=0.15)
        label = Text("Hệ số trượt", font="Noto Sans", color=YELLOW).scale(0.6).next_to(box, UR)
        self.add_sound("voiceovers/click.wav")
        self.play(Create(box), Write(label))
        self.wait(2)
        self.play(FadeOut(box, label, diag_group, horizontal_arrow, horizontal_shear_text))
    def shearDeterminant(self):
        self.add_sound("voiceovers/shearDeterminant.mp3")
        matrix = Matrix([
            ["1", "k"],
            ["0", "1"]
        ]).shift(UP*0.5)
        self.add_sound("voiceovers/click.wav")
        self.play(Create(matrix))
        self.wait()

        det_formula = MathTex(
            r"\det(S) = (1)(1) - (k)(0)"
        ).next_to(matrix, DOWN, buff=1)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(det_formula))
        self.wait()

        result = MathTex(r"\det(S) = 1").next_to(det_formula, DOWN)
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(Transform(det_formula.copy(), result))
        self.wait(2)

        box = SurroundingRectangle(result, color=YELLOW)
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(Create(box))
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/ShearMatrix_title.mp3")
        title = Text("Ma trận Trượt (Shear)", font="Noto Sans", font_size=42,
                     gradient=[BLUE, YELLOW]).to_edge(UP).set_z_index(12)
        title_itatlic = Text("Ma trận Trượt (Shear)", font="Noto Sans", font_size=42,
                     gradient=[BLUE, YELLOW], slant=ITALIC).to_edge(UP).set_z_index(12)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(title))
        self.wait()
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(Transform(title, title_itatlic))
        self.wait()
        self.deckShear()
        self.define()
        shear_factor = 1
        matrix_right = [[1, shear_factor], [0, 1]]
        matrix_tex = MathTex(
            "S = \\begin{bmatrix} 1 & 1 \\\\ 0 & 1 \\end{bmatrix}"
        ).to_edge(LEFT).set_z_index(12)
        window_rect, wall_with_hole, grid, points = create_grid()
        self.add_sound("voiceovers/game-start.mp3")
        self.play(FadeIn(matrix_tex), FadeIn(wall_with_hole), Create(window_rect))
        self.play(FadeIn(grid), FadeIn(points))
        
        square = Square(side_length=2, color=MAROON_E, fill_opacity=0.3)
        self.play(FadeIn(square))
        self.add_sound("voiceovers/ShearGeometry.mp3")
        anims = animate_points_matrix(self, grid, points, matrix_right)    
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(
            square.animate.apply_matrix(matrix_right),
            *anims,
            run_time=2,
            rate_func=linear
        )
        self.wait()
        self.play(FadeOut(grid, points, matrix_tex, square))
        matrix_left = [[1, 0], [shear_factor, 1]]
        matrix_tex = MathTex(
            "S = \\begin{bmatrix} 1 & 0 \\\\ 1 & 1 \\end{bmatrix}"
        ).to_edge(LEFT).set_z_index(12)
        window_rect, wall_with_hole, grid, points = create_grid()
        self.play(FadeIn(matrix_tex))
        self.play(FadeIn(grid), FadeIn(points))
        
        square = Square(side_length=2, color=MAROON_E, fill_opacity=0.3)
        self.play(FadeIn(square))
        anims = animate_points_matrix(self, grid, points, matrix_left)    
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(
            square.animate.apply_matrix(matrix_left),
            *anims,
            run_time=2,
            rate_func=linear
        )
        self.wait()
        self.play(FadeOut(grid, points, matrix_tex, square))
        matrix_tex = MathTex(
            "S = \\begin{bmatrix} 1 & 1 \\\\ 0 & 1 \\end{bmatrix}"
        ).to_edge(LEFT).set_z_index(12)
        window_rect, wall_with_hole, grid, points = create_grid()
        self.play(FadeIn(matrix_tex))
        self.play(FadeIn(grid), FadeIn(points))
        unit_circle = Circle(radius=1, color=GREEN_E, stroke_width=2, fill_opacity=0.3)
        self.play(FadeIn(unit_circle))
        anims = animate_points_matrix(self, grid, points, matrix_right)    
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(
            unit_circle.animate.apply_matrix(matrix_right),
            *anims,
            run_time=2,
            rate_func=linear
        )
        self.wait()
        self.play(FadeOut(grid, points, matrix_tex, unit_circle))
        self.play(*[
            FadeOut(mob) for mob in self.mobjects
            if mob is not title
        ])
        self.shearDeterminant()
        self.wait(3)

class TransposeMatrix(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/TransposeMatrix.mp3")
        word = "Ma trận Chuyển vị"
        vertical = VGroup(Text("Ma", font="Noto Sans"),
                          Text("trận", font="Noto Sans"),
                          Text("Chuyển", font="Noto Sans"),
                          Text("vị", font="Noto Sans"),).arrange(DOWN)
        horizontal = Text(word, font="Noto Sans")
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(vertical))
        self.wait()
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(Transform(vertical, horizontal))
        self.wait()
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(vertical.animate.to_edge(UP))
        matrix = Matrix([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ])
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(matrix))
        self.wait()

        entries = matrix.get_entries()

        diag_indices = [0, 4, 8]
        diag = VGroup(*[entries[i] for i in diag_indices])
        self.add_sound("voiceovers/click.wav")
        self.play(diag.animate.set_color(YELLOW))
        self.wait()

        swaps = [
            (1, 3),  # (0,1) <-> (1,0)
            (2, 6),  # (0,2) <-> (2,0)
            (5, 7)   # (1,2) <-> (2,1)
        ]
        animations = []
        for i, j in swaps:
            animations.append(Swap(entries[i], entries[j]))
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(*animations)
        self.wait()
        self.play(FadeOut(matrix))
        matrix_a = Matrix([
            [1, 2, 3],
            [4, 5, 6]
        ]).shift(3*LEFT)
        label_a = MathTex("A").next_to(matrix_a, UP)
        row1 = matrix_a.get_rows()[0]
        row2 = matrix_a.get_rows()[1]
        row1.set_color(BLUE)
        row2.set_color(ORANGE)
        matrix_t = Matrix([
            [1, 4],
            [2, 5],
            [3, 6]
        ]).shift(3*RIGHT)
        label_t = MathTex("A^T").next_to(matrix_t, UP)
        col1 = matrix_t.get_columns()[0]
        col2 = matrix_t.get_columns()[1]
        col1.set_color(BLUE)
        col2.set_color(ORANGE)
        arrow = Arrow(matrix_a.get_right(), matrix_t.get_left())
        transpose_text = Text("Chuyển vị", font="Noto Sans"
                              ).scale(0.6).next_to(arrow, UP)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(matrix_a, label_a))
        self.wait(2)
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(GrowArrow(arrow), FadeIn(transpose_text))
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(label_t))
        self.wait()

        a_entries = matrix_a.get_entries()
        t_entries = matrix_t.get_entries()

        animations = []
        for i in range(len(a_entries)):
            animations.append(TransformFromCopy(a_entries[i], t_entries[i]))
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(*animations, Create(matrix_t.get_brackets()))
        self.wait(2)
        rule = MathTex("A_{ij} \\rightarrow A_{ji}")
        rule.to_edge(DOWN, LARGE_BUFF)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(rule))
        self.wait(3)

class RotateMaster(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/RotateMaster.mp3")
        title = Text("Ma trận trực giao", font="Noto Sans", font_size=42).to_edge(UP)
        planet = ImageMobject("assets/planet.png").scale(.15)
        satellite = ImageMobject("assets/satellite.png").scale(.05)
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(SpinInFromNothing(title))
        self.add_sound("voiceovers/radar-ping.mp3")
        self.play(
            Rotate(
                satellite.shift(UP * 2),
                angle=2*PI,
                about_point=ORIGIN,
                rate_func=linear,
            ),
            Rotate(planet, angle=2*PI, rate_func=linear),
            run_time=6
            )
class OrthogonalMatrix(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/OrthogonalMatrix.mp3")
        Q = Matrix([
            ["\\frac{1}{\\sqrt{2}}", "-\\frac{1}{\\sqrt{2}}"],
            ["\\frac{1}{\\sqrt{2}}",  "\\frac{1}{\\sqrt{2}}"]
        ]).set_z_index(12)
        entries = Q.get_entries()
        for e in entries:
            e.scale(0.6)
        title = MathTex("Q")
        title.set_z_index(12).to_edge(UP)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(title, Q))
        self.wait()

        col1 = VGroup(entries[0], entries[2])
        col2 = VGroup(entries[1], entries[3])

        divider = Line(UP, DOWN).scale(1.3)
        divider.move_to(Q.get_center())
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(Create(divider))
        self.wait(0.5)
        self.play(FadeOut(Q.get_brackets()))
        col1_target = col1.copy().shift(LEFT*.4)
        col2_target = col2.copy().shift(RIGHT*.4)
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(
            Transform(col1, col1_target),
            Transform(col2, col2_target),
            FadeOut(divider)
        )
        col1_br = Matrix([
            ["\\frac{1}{\\sqrt{2}}"],
            ["\\frac{1}{\\sqrt{2}}"]
        ]).move_to(col1).get_brackets().set_z_index(12)

        col2_br = Matrix([
            ["-\\frac{1}{\\sqrt{2}}"],
            ["\\frac{1}{\\sqrt{2}}"]
        ]).move_to(col2).get_brackets().set_z_index(12)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(
            FadeIn(col1_br),
            FadeIn(col2_br)
        )

        labels = VGroup(
            MathTex("q_1").next_to(col1, DOWN),
            MathTex("q_2").next_to(col2, DOWN),
        ).set_z_index(12)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(labels))
        window_rect, wall_with_hole, grid = create_grid_no_point()
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(VGroup(col1, col1_br, col2, col2_br, labels, title).animate.to_edge(LEFT),
                  FadeIn(wall_with_hole, window_rect))
        self.play(Create(grid))
        
        q1 = np.array([1/np.sqrt(2), 1/np.sqrt(2), 0])
        q2 = np.array([-1/np.sqrt(2), 1/np.sqrt(2), 0])

        v1 = Vector(q1, color=YELLOW)
        v2 = Vector(q2, color=PINK)

        label1 = MathTex("q_1").next_to(v1.get_end(), RIGHT)
        label2 = MathTex("q_2").next_to(v2.get_end(), LEFT)
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(ReplacementTransform(col1.copy(), v1), FadeIn(label1),
                  ReplacementTransform(col2.copy(), v2), FadeIn(label2))
        self.add_sound("voiceovers/perpendicular.mp3")
        self.wait()
        right_angle = RightAngle(v1, v2, length=0.2)
        self.add_sound("voiceovers/click.wav")
        self.play(Create(right_angle))
        self.wait()
        
        dot_formula = MathTex(
            r"q_1 \cdot q_2 =",
            r"\frac{1}{\sqrt2}\left(-\frac{1}{\sqrt2}\right)",
            "+",
            r"\frac{1}{\sqrt2}\left(\frac{1}{\sqrt2}\right)"
        ).to_edge(DOWN).set_z_index(12)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(dot_formula), run_time=0.5)
        self.wait(0.5)

        simplify = MathTex(
            r"q_1 \cdot q_2 = -\frac12 + \frac12"
        ).to_edge(DOWN).set_z_index(12)
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(Transform(dot_formula, simplify), run_time=0.5)
        self.wait(0.5)

        result = MathTex(
            r"q_1 \cdot q_2 = 0"
        ).to_edge(DOWN).set_z_index(12)
        self.add_sound("voiceovers/soccer-ball-kick.mp3")
        self.play(Transform(dot_formula, result), run_time=0.5)
        self.wait()
        self.add_sound("voiceovers/Normalized.mp3")
        circle = Circle(radius=1, color=WHITE, stroke_opacity=0.3)
        norm_text = MathTex(
            r"\|q_1\| = \|q_2\| = 1"
        ).to_edge(RIGHT).set_z_index(12)
        self.add_sound("voiceovers/click.wav")
        self.play(Create(circle))
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(norm_text))
        self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.orthogonalMatrixDefinition()
        self.wait(3)
    def orthogonalMatrixDefinition(self):
        self.add_sound("voiceovers/OrthogonalMatrixDefinition.mp3")
        title = Text("Ma trận trực giao", font="Noto Sans").to_edge(UP)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(title))
        self.wait()

        eq1 = MathTex(
            r"Q^T Q = I",
            font_size=72
        )
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(eq1))
        self.wait(1.5)
        explain_transpose = VGroup(
            Tex(r"$Q^T$ :", font_size=36),
            Text("ma trận chuyển vị của", font="Noto Sans").scale(0.5),
            Tex(r"$Q$", font_size=36)
            ).arrange(RIGHT)

        explain_identity = VGroup(
            Tex(r"$I$ :", font_size=36),
            Text("ma trận đơn vị", font="Noto Sans").scale(0.5)
            ).arrange(RIGHT)

        explanations = VGroup(
            explain_transpose,
            explain_identity
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        explanations.next_to(eq1, DOWN, buff=1)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(explain_transpose, shift=DOWN))
        self.wait(1.5)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(explain_identity, shift=DOWN))
        self.wait(2)
        self.add_sound("voiceovers/radio-wave.mp3")
        self.play(ApplyWave(eq1))
        self.wait(3)

        eq2 = MathTex(
            r"Q^T = Q^{-1}",
            font_size=72
        )
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(
            TransformMatchingTex(eq1, eq2),
            run_time=2
        )
        self.wait(2)
        box = SurroundingRectangle(eq2, color=YELLOW)
        self.add_sound("voiceovers/click.wav")
        self.play(Create(box))
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.rotationTransposeInverse()
    def rotationTransposeInverse(self):
        self.add_sound("voiceovers/RotationTransposeInverse.mp3")
        plane = NumberPlane()
        self.add(plane)
        eq = MathTex(r"Q^T = Q^{-1}")
        eq.add_background_rectangle().to_edge(UP)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(eq))
        v = np.array([2, 1, 0])
        vec = Arrow(ORIGIN, v, buff=0, color=BLUE)
        vec_label = MathTex(r"\vec{v}").next_to(vec.get_end(), RIGHT)
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(GrowArrow(vec), Write(vec_label))
        self.wait()
        theta = PI/4

        Q = np.array([
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta),  np.cos(theta)]
        ])
        QT = Q.T
        v_rot = np.dot(Q, v[:2])
        v_rot = np.append(v_rot, 0)
        vec_rot = Arrow(ORIGIN, v_rot, buff=0, color=GREEN)
        label_rot = MathTex(r"Q\vec{v}").next_to(vec_rot.get_end(), RIGHT)
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(Transform(vec, vec_rot), Transform(vec_label, label_rot))
        self.wait()
        v_back = np.dot(QT, v_rot[:2])
        v_back = np.append(v_back, 0)
        vec_back = Arrow(ORIGIN, v_back, buff=0, color=RED)
        label_back = MathTex(r"Q^T(Q\vec{v}) = \vec{v}").next_to(vec_back.get_end(), RIGHT)
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(Transform(vec, vec_back), Transform(vec_label, label_back))
        
class OrthogonalPreservesAngle(Scene):
    def construct(self):
        self.wait()
        plane = NumberPlane()
        self.play(Create(plane))
        self.add_sound("voiceovers/OrthogonalPreservesAngle.mp3")
        v1_end = np.array([3, 1, 0])
        v2_end = np.array([1, 2, 0])

        v1 = Arrow(ORIGIN, v1_end, color=BLUE, buff=0)
        v2 = Arrow(ORIGIN, v2_end, color=GREEN, buff=0)
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(GrowArrow(v1), GrowArrow(v2))
        angle = Angle(v1, v2, radius=0.6, color=YELLOW)
        self.add_sound("voiceovers/click.wav")
        self.play(Create(angle))
        theta = 2*PI

        matrix_text = MathTex(
            r"Q=\begin{bmatrix}\cos\theta & -\sin\theta \\ \sin\theta & \cos\theta\end{bmatrix}"
        ).scale(0.8).add_background_rectangle().to_corner(UL)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(matrix_text))
        group = VGroup(v1, v2, angle)
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(
            Rotate(group, angle=theta, about_point=ORIGIN),
            run_time=2
        )
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.orthogonalTransformations()
        self.wait(3)
    def orthogonalTransformations(self):
        window_rect, wall_with_hole, grid = create_grid_no_point()
        self.play(FadeIn(wall_with_hole, window_rect), run_time=.5)
        squares = VGroup()
        centers = [
            np.array([-0.5, -0.5, 0]),
            np.array([0.5, -0.5, 0]),
            np.array([-0.5, 0.5, 0]),
            np.array([0.5, 0.5, 0])
        ]

        colors = [BLUE, GREEN, ORANGE, PURPLE]

        for c, col in zip(centers, colors):
            sq = Square(side_length=1, color=col, fill_opacity=0.2)
            sq.move_to(c)
            squares.add(sq)
        self.play(FadeIn(grid), run_time=.5)
        self.play(FadeIn(squares), run_time=.5)

        theta = PI/4
        rotation_matrix = np.array([
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta),  np.cos(theta)]
        ])

        rot_text = MathTex(
            r"R = \begin{bmatrix}\cos\theta & -\sin\theta \\ \sin\theta & \cos\theta\end{bmatrix}"
        ).set_z_index(12).to_corner(UL)
        self.add_sound("voiceovers/rotate.mp3")
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(rot_text))
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(
            grid.animate.apply_matrix(rotation_matrix),
            squares.animate.apply_matrix(rotation_matrix),
            run_time=2
        )
        self.wait()
        self.add_sound("voiceovers/reflect.mp3")
        reflection_matrix = np.array([
            [1,0],
            [0,-1]
        ])

        ref_text = MathTex(
            r"Q=\begin{bmatrix}1 & 0 \\ 0 & -1\end{bmatrix}"
        ).set_z_index(12).to_corner(UL)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(Transform(rot_text, ref_text))
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(
            grid.animate.apply_matrix(reflection_matrix),
            squares.animate.apply_matrix(reflection_matrix),
            run_time=2
        )
class MagicCircle(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/orthogonal_app.mp3")
        circle = Circle(radius=2, color=PURPLE)
        circle.set_stroke(width=6)
        symbols = VGroup(*[
            Star(n=5, color=BLUE).scale(0.3).move_to(
                circle.point_at_angle(i * TAU / 6)
            )
            for i in range(6)
        ])
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(Create(circle))
        self.add_sound("voiceovers/game-start.mp3")
        self.play(LaggedStart(*[FadeIn(s) for s in symbols]))
        self.add_sound("voiceovers/twinklesparkle.mp3")
        self.play(
            Rotate(symbols, angle=TAU, run_time=6),
            circle.animate.set_color(GOLD),
            rate_func=linear
        )
        self.wait(2)

class RotateOrthogonalProof(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/RotateOrthogonalProof.mp3")
        QT = Matrix([
            [r"\cos\theta", r"\sin\theta"],
            [r"-\sin\theta", r"\cos\theta"]
        ])
        
        Q = Matrix([
            [r"\cos\theta", r"-\sin\theta"],
            [r"\sin\theta", r"\cos\theta"]
        ])

        result = Matrix([
            ["?", "?"],
            ["?", "?"]
        ])

        qt = QT.get_entries()
        q = Q.get_entries()
        res = result.get_entries()

        for e in qt:
            e.scale(0.6)
        for e in q:
            e.scale(0.6)

        matrices = VGroup(QT, Q, result).arrange(RIGHT, buff=1)
        qt_text = MathTex("Q^T").next_to(QT, UP, LARGE_BUFF)
        q_text = MathTex("Q").next_to(Q, UP, LARGE_BUFF)

        equal = MathTex("=").next_to(Q, RIGHT)
        result.next_to(equal, RIGHT)

        group = VGroup(QT, Q, equal, result)
        group.move_to(UP*0.5)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(Q, q_text))
        self.wait(2)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(QT, qt_text, equal, result))
        row1 = VGroup(qt[0], qt[1])
        col1 = VGroup(q[0], q[2])

        row_box = SurroundingRectangle(row1, color=YELLOW, buff=0.05)
        col_box = SurroundingRectangle(col1, color=BLUE, buff=0.05)
        calc = MathTex(
            r"\cos\theta\cos\theta + \sin\theta\sin\theta = 1"
        ).scale(0.8)
        calc.to_edge(DOWN)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Create(row_box), Create(col_box),
                  Write(calc), run_time=0.5)
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(
            Transform(res[0], MathTex("1").scale(0.8).move_to(res[0])),
            run_time=0.5
        )
        self.play(FadeOut(row_box, col_box, calc), run_time=0.5)
        col2 = VGroup(q[1], q[3])
        row_box = SurroundingRectangle(row1, color=YELLOW, buff=0.05)
        col_box = SurroundingRectangle(col2, color=BLUE, buff=0.05)
        calc = MathTex(
            r"\cos\theta(-\sin\theta)+\sin\theta\cos\theta=0"
        ).scale(0.8)
        calc.to_edge(DOWN)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Create(row_box), Create(col_box),
                  Write(calc), run_time=0.5)
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(
            Transform(res[1], MathTex("0").scale(0.8).move_to(res[1])),
            run_time=0.5
        )
        self.play(FadeOut(row_box, col_box, calc), run_time=0.5)
        row2 = VGroup(qt[2], qt[3])
        row_box = SurroundingRectangle(row2, color=YELLOW, buff=0.05)
        col_box = SurroundingRectangle(col1, color=BLUE, buff=0.05)
        calc = MathTex(
            r"-\sin\theta\cos\theta+\cos\theta\sin\theta=0"
        ).scale(0.8)
        calc.to_edge(DOWN)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Create(row_box), Create(col_box),
                  Write(calc), run_time=0.5)
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(
            Transform(res[2], MathTex("0").scale(0.8).move_to(res[2])),
            run_time=0.5
        )
        self.play(FadeOut(row_box, col_box, calc), run_time=0.5)
        row_box = SurroundingRectangle(row2, color=YELLOW, buff=0.05)
        col_box = SurroundingRectangle(col2, color=BLUE, buff=0.05)
        calc = MathTex(
            r"\sin^2\theta+\cos^2\theta=1"
        ).scale(0.8)
        calc.to_edge(DOWN)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Create(row_box), Create(col_box), 
                  Write(calc), run_time=0.5)
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(
            Transform(res[3], MathTex("1").scale(0.8).move_to(res[3])),
            run_time=.5
        )
        self.play(FadeOut(row_box, col_box, calc), run_time=0.5)
        final = MathTex(r"Q^T Q = I").scale(0.9)
        final.next_to(result, DOWN)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(final))
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(Flash(final))
        self.wait()
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.identityColumnsOrthonormal()
        self.wait(3)

    def identityColumnsOrthonormal(self):
        self.add_sound("voiceovers/IdentityColumnsOrthonormal.mp3")
        matrix = MathTex(
            r"I = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}"
        ).to_corner(UL).add_background_rectangle()
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(matrix))

        plane = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            },
        )
        self.play(Create(plane))
        v1 = Arrow(ORIGIN, RIGHT, buff=0, color=BLUE)
        v2 = Arrow(ORIGIN, UP, buff=0, color=GREEN)
        label1 = MathTex(r"v_1 = \begin{bmatrix}1\\0\end{bmatrix}").add_background_rectangle()
        label2 = MathTex(r"v_2 = \begin{bmatrix}0\\1\end{bmatrix}").add_background_rectangle()
        label1.next_to(v1, RIGHT)
        label2.next_to(v2, UP)
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(GrowArrow(v1), GrowArrow(v2))
        self.wait()
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(label1), Write(label2))
        self.wait()

        norm_text = MathTex(
            r"\|v_1\| = 1,\quad \|v_2\| = 1"
        ).add_background_rectangle().shift(1.5*DOWN+3*LEFT)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(norm_text))
        self.wait()

        dot_text = MathTex(
            r"v_1 \cdot v_2 = 0"
        ).next_to(norm_text, DOWN).add_background_rectangle()
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(dot_text))
        
class ProjectionMatrix(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/ProjectionMatrix_title.mp3")
        bg = Rectangle(width=14, height=8, fill_color=BLACK, fill_opacity=1)
        self.add(bg)
        target = Circle(radius=0.4, color=YELLOW, fill_opacity=1).shift(DOWN*1.5)
        self.add(target)
        source = Dot(point=UP*3 + LEFT*2, color=WHITE)
        beam = Polygon(
            source.get_center(),
            target.get_center() + LEFT*1.2,
            target.get_center() + RIGHT*1.2,
            color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.35,
            stroke_width=0
        )
        self.add_sound("voiceovers/light-switch.mp3")
        self.play(FadeIn(source, beam))
        title = Text("Ma trận chiếu", font="Noto Sans", font_size=42).move_to(source)
        self.add_sound("voiceovers/shine2.mp3")
        self.play(Transform(source, title))
        self.wait()
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.projectionExample()
        self.wait(5)

    def projectionExample(self):
        self.add_sound("voiceovers/ProjectionMatrix.mp3")
        axes = NumberPlane()
        u_basis = np.array([3, 1, 0])
        line = Line(start=u_basis * -2, end=u_basis * 2, color=GRAY)
        line_label = Text("Không gian con (đường thẳng)", font="Noto Sans", font_size=24
                          ).add_background_rectangle().next_to(line, DOWN)

        v_coord = np.array([1, 2, 0])
        v_vec = Vector(v_coord, color=YELLOW)
        v_label = MathTex(r"\mathbf{v}").next_to(v_vec.get_end(), UP)

        proj_coord = (np.dot(v_coord, u_basis) / np.dot(u_basis, u_basis)) * u_basis
        proj_vec = Vector(proj_coord, color=PINK)
        proj_label = MathTex(r"P\mathbf{v}", color=PINK).next_to(proj_vec.get_end(), DOWN)

        error_line = DashedLine(start=v_vec.get_end(), end=proj_vec.get_end(), color=WHITE)
        
        right_angle = RightAngle(
            Line(proj_vec.get_end(), v_vec.get_end()),
            Line(proj_vec.get_end(), [0, 0, 0]),
            length=0.2, color=WHITE
        )

        self.add(axes, line, line_label)
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(GrowArrow(v_vec), Write(v_label))
        self.wait()
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(Create(error_line))
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(GrowArrow(proj_vec), Write(proj_label))
        self.add_sound("voiceovers/click.wav")
        self.play(Create(right_angle))
        self.wait(2)
        self.add_sound("voiceovers/wiggle.mp3")
        self.play(Wiggle(proj_vec))
        self.wait()
        self.add_sound("voiceovers/whoosh407576.mp3")
        self.play(
            proj_label.animate.set_color(WHITE),
            Text("Áp dụng ma trận lần thứ hai sẽ không thay đổi gì", font="Noto Sans", font_size=24
                 ).add_background_rectangle().animate.to_edge(UP)
        )
        
class Projection3D(ThreeDScene):
    def construct(self):
        self.wait()
        rank_text = Text("Trực giác Hình học", font="Noto Sans", font_size=24).to_corner(UL)
        self.add_fixed_in_frame_mobjects(rank_text)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(rank_text))
        self.wait()
        self.add_sound("voiceovers/Projection3D.mp3")
        axes = ThreeDAxes()
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        
        plane = Rectangle(
            width=6, height=6, 
            fill_opacity=0.2, 
            fill_color=BLUE, 
            stroke_color=BLUE
        )

        v_coord = np.array([2, 2, 3])
        v_vec = Arrow3D(start=ORIGIN, end=v_coord, color=YELLOW)
        v_label = MathTex(r"\mathbf{v}").next_to(v_vec.get_end(), UP)
        self.add_fixed_in_frame_mobjects(v_label)

        proj_coord = np.array([2, 2, 0])
        proj_vec = Arrow3D(start=ORIGIN, end=proj_coord, color=PINK)
        proj_label = MathTex(r"P\mathbf{v}", color=PINK).shift(.5*DOWN+1.5*RIGHT)
        
        error_line = DashedLine(
            start=v_coord, 
            end=proj_coord, 
            color=WHITE,
            stroke_width=2
        )

        self.add(axes)
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(Create(v_vec), Write(v_label))
        self.wait()
        self.add_sound("voiceovers/click.wav")
        self.play(Create(plane))
        self.wait()
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(Create(error_line))
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(Create(proj_vec))
        self.add_fixed_in_frame_mobjects(proj_label)

        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(5)
        self.stop_ambient_camera_rotation()     
        self.wait(3)
class ProjectionFormula(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/ProjectionFormula.mp3")
        title = Text("Công thức", font="Noto Sans", font_size=36).to_edge(UP)
        formula = MathTex(
            "P", "=", "A", "(A^T A)^{-1}", "A^T",
            font_size=48
        )
        formula.set_color_by_tex("A", BLUE)
        formula.set_color_by_tex("P", PINK)
        self.add_sound("voiceovers/pop-268648.mp3")
        self.play(FadeIn(title))
        self.wait(3)
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(formula))
        self.wait()
        explanation = VGroup(
            Text("A: Ma trận có các cột trải rộng trên không gian con", font="Noto Sans", font_size=20, color=BLUE),
            Text("(AᵀA)⁻¹ Aᵀ: Logic 'ngược giả'", font_size=20, font="Noto Sans"),
            Text("P: Chiếu bất kỳ vectơ nào lên Col(A)", font="Noto Sans", font_size=20, color=PINK)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(formula, DOWN, buff=1)

        for line in explanation:
            self.add_sound("voiceovers/ding-402325.mp3")
            self.play(FadeIn(line, shift=UP * 0.2))
            self.wait(0.5)
        self.wait(3)
class LinearRegressionProjection(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/LinearRegressionProjection.mp3")
        title = Text("Hồi quy tuyến tính", font="Noto Sans"
                     ).scale(0.8).to_edge(UP)
        axes = Axes(
            x_range=[-1,5,1],
            y_range=[-1,5,1],
            x_length=6,
            y_length=6,
            axis_config={"include_numbers": True}
        )
        self.add_sound("voiceovers/writin.mp3")
        self.play(Write(title))
        self.add_sound("voiceovers/click.wav")
        self.play(Create(axes))
        self.wait()
        u = np.array([2, 1, 0])
        y_vec = np.array([3, 4, 0])
        proj = (np.dot(y_vec[:2], u[:2]) / np.dot(u[:2], u[:2])) * u
        y_vector = Arrow(
            axes.c2p(0,0),
            axes.c2p(*y_vec[:2]),
            buff=0,
            color=BLUE
        )

        proj_vector = Arrow(
            axes.c2p(0,0),
            axes.c2p(*proj[:2]),
            buff=0,
            color=GREEN
        )

        residual_vector = Arrow(
            axes.c2p(*proj[:2]),
            axes.c2p(*y_vec[:2]),
            buff=0,
            color=RED
        )
        y_label = MathTex("y").next_to(y_vector.get_end(), RIGHT)
        yhat_label = MathTex(r"\hat{y}").next_to(proj_vector.get_end(), DOWN)
        residual_label = MathTex(r"y - \hat{y}").next_to(residual_vector, RIGHT)
        line = Line(
            axes.c2p(-1, -0.5),
            axes.c2p(5, 2.5),
            color=YELLOW
        )
        line_label = Text("Không gian cột của X", color=YELLOW, font="Noto Sans").scale(0.5).next_to(line, RIGHT)
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(Create(line), FadeIn(line_label))
        self.wait()
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(GrowArrow(y_vector), Write(y_label))
        self.wait()
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(GrowArrow(proj_vector), Write(yhat_label))
        self.wait()
        self.add_sound("voiceovers/sword-swing.wav")
        self.play(GrowArrow(residual_vector), Write(residual_label))
        self.wait()
        right_angle = RightAngle(
            Line(axes.c2p(*proj[:2]), axes.c2p(*y_vec[:2])),
            line,
            length=0.2,
            quadrant=(1,-1)
        )
        self.add_sound("voiceovers/click.wav")
        self.play(Create(right_angle))
        self.wait(2)

class HiddenStructure(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/HiddenStructure.mp3")
        window_rect_left, window_rect_right, wall_with_hole, grid_left, grid_right = create_grid_double()
        self.add_sound("voiceovers/game-start.mp3")
        self.play(FadeIn(wall_with_hole, window_rect_left))
        squares_left = VGroup()
        centers = [
            np.array([-0.25, -0.25, 0]),
            np.array([0.25, -0.25, 0]),
            np.array([-0.25, 0.25, 0]),
            np.array([0.25, 0.25, 0])
        ]

        colors = [BLUE, GREEN, ORANGE, PURPLE]

        for c, col in zip(centers, colors):
            sq = Square(side_length=.5, color=col, fill_opacity=0.2)
            sq.move_to(c)
            squares_left.add(sq)
        squares_left.move_to(window_rect_left.get_center())
        squares_right = squares_left.copy().move_to(window_rect_right.get_center())
        self.play(FadeIn(squares_left))
        self.wait()
        A = np.array([[3, 1],
                      [1, 2]])

        U, S, VT = np.linalg.svd(A)
        Sigma = np.array([
            [S[0], 0],
            [0, S[1]]
        ])
        label_A = Text("Áp dụng A", font="Noto Sans").set_z_index(12).next_to(window_rect_left, UP)
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(squares_left.animate.center().apply_matrix(A).move_to(window_rect_left.get_center()),
                  FadeIn(label_A), run_time=3)
        self.wait(2)
        self.add_sound("voiceovers/click.wav")
        self.play(Create(window_rect_right))
        self.wait()
        self.play(Create(squares_right))

        self.wait(2)
        # Step 1: apply V^T
        self.add_sound("voiceovers/svd_VT.mp3")
        label1 = Text("Áp dụng Vᵀ (xoay)", font="Noto Sans").set_z_index(12).next_to(window_rect_right, UP)

        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(
            FadeIn(label1),
            squares_right.animate.center().apply_matrix(VT).move_to(window_rect_right.get_center()),
            run_time=3)
        self.wait()
        self.add_sound("voiceovers/svd_Sigma.mp3")
        # Step 2: apply Sigma (stretch)
        label2 = Text("Áp dụng Σ (kéo giãn)", font="Noto Sans").set_z_index(12).next_to(window_rect_right, UP)
        # self.add_sound("voiceovers/happy-coin.wav")
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(
            Transform(label1, label2),
            squares_right.animate.center().apply_matrix(Sigma).move_to(window_rect_right.get_center()),
            run_time=3)
        self.wait()
        # Step 3: apply U
        self.add_sound("voiceovers/svd_U.mp3")
        label3 = Text("Áp dụng U (xoay)", font="Noto Sans").set_z_index(12).next_to(window_rect_right, UP)
        # self.add_sound("voiceovers/happy-coin.wav")
        self.add_sound("voiceovers/sci-fi-effect.mp3")
        self.play(
            Transform(label1, label3),
            squares_right.animate.center().apply_matrix(U).move_to(window_rect_right.get_center()),
            run_time=3)
        self.wait()
        self.add_sound("voiceovers/svd_final.mp3")
        final_text = Text("A = U Σ Vᵀ", font="Noto Sans").set_z_index(12).next_to(window_rect_right, UP)
        self.add_sound("voiceovers/happy-coin.wav")
        self.play(Transform(label1, final_text))
        self.wait()
        self.add_sound("voiceovers/ding-402325.mp3")
        self.play(Indicate(label1))
        self.wait(4)

class Closing(Scene):
    def construct(self):
        self.wait()
        self.add_sound("voiceovers/Closing.mp3")
        heatmapSweep(self)
        svdCompression(self)
        particles = VGroup()
        for _ in range(60):
            dot = Dot(radius=0.05, color=random.choice([BLUE, PURPLE, GOLD]))
            dot.move_to([random.uniform(-0.1,0.1), random.uniform(-0.1,0.1),0])
            particles.add(dot)
        self.add_sound("voiceovers/start-computer.mp3")
        self.play(LaggedStart(*[
            dot.animate.shift([
                random.uniform(-4,4),
                random.uniform(-2,2),
                0
            ])
            for dot in particles
        ], lag_ratio=0.1))
        self.wait()
        
        eq = MathTex(
            "A", "=",
            "U",
            "\\Sigma",
            "V^T"
        ).scale(1.8)
        eq[2].set_color(BLUE)    # U
        eq[3].set_color(YELLOW)  # Sigma
        eq[4].set_color(GREEN)   # V^T
        self.add_sound("voiceovers/shine2.mp3")
        self.play(Transform(particles, eq))
        self.wait(2)
        self.play(FadeOut(particles))
class MatrixThumbnail(Scene):
    def construct(self):
        bg = ImageMobject("assets/neo_artemis-matrix.png")
        bg.scale_to_fit_height(config.frame_height)  
        bg.scale_to_fit_width(config.frame_width)    
        bg.move_to(ORIGIN)
        bg.animate.set_opacity(0.3)
        # Title
        title = Text(
            "Các loại ma trận",
            font_size=96, font="Noto Sans",
            weight=BOLD
        ).set_z_index(10)

        title.to_edge(UP)
        rust = ImageMobject("assets/rust.png").scale(0.5).to_edge(DOWN)
        self.add(title, bg, rust)