from manim import *
import numpy as np
import random

class MatrixIntro(Scene):
    def construct(self):
        self.add_sound("voiceovers/MatrixIntro.mp3")
        look_closely = SVGMobject("assets/look_closely.svg").to_edge(UP)
        self.play(FadeIn(look_closely))  
        pixel = SVGMobject("assets/Pixel-Guy.svg").shift(3*LEFT+UP)
        self.play(DrawBorderThenFill(pixel))
        tetris = SVGMobject("assets/Tetris_block.svg").shift(3*RIGHT+UP)
        self.play(FadeIn(tetris))
        spacetime = SVGMobject("assets/astronaut.svg").shift(3*LEFT+2*DOWN)
        self.spacetime = spacetime
        self.play(FadeIn(spacetime))
        nn = self.get_nn().scale(0.6).shift(3*RIGHT+2*DOWN)
        self.play(FadeIn(nn))
        self.play(FadeOut(look_closely))
        question_label = Label(
            label=Text('???', font='sans-serif'),
            box_config = {
                "color" : BLUE,
                "fill_opacity" : 0.75
            }
        )
        self.play(Transform(VGroup(pixel, tetris, nn, spacetime), question_label))
        self.wait()
        all_objects = Group(*self.mobjects)
        self.play(FadeOut(all_objects))
        self.wait()
        self.matrix_title_intro()
        self.wait(13)
        
    def matrix_title_intro(self):
        title = "MA-TRẬN"
        size = 7
        matrix_data = []
        for i in range(size):
            row = []
            for j in range(size):
                if i == j:
                    row.append(title[i])
                else:
                    # Fill with numbers, e.g., row*size + col + 1
                    row.append(str(i * size + j + 1))
            matrix_data.append(row)

        # Manually define the matrix for full control
        def cell_mobject(cell):
            # Use Text for non-ASCII, MathTex for numbers
            if cell.isnumeric():
                return MathTex(cell)
            else:
                return Text(cell, font="Noto Sans", font_size=36)
        matrix_mob = MobjectTable(
            [[cell_mobject(cell) for cell in row] for row in matrix_data],
            include_outer_lines=True
        ).scale(0.7)
        self.play(FadeIn(matrix_mob))
        self.wait(1)

        # Step 2: Animate the diagonal letters to move and form the word "MATRİSLER"
        diagonal_letters = [
            matrix_mob.get_entries()[i * size + i] for i in range(size)
        ]
        matrisler_group = VGroup(
            *[Text(title[i], font="Noto Sans", font_size=36) for i in range(size)]
        ).arrange(RIGHT, buff=0.3).move_to(matrix_mob)

        # Animate diagonal letters to their new positions, fade out only the non-diagonal elements and lines
        non_diagonal_entries = [
            entry for i, entry in enumerate(matrix_mob.get_entries())
            if (i // size) != (i % size)
        ]

        # Animate each diagonal letter to its new position using Transform, keeping the original objects
        self.play(
            *[
                Transform(diagonal_letters[i], matrisler_group[i], run_time=1.2)
                for i in range(size)
            ],
            FadeOut(VGroup(*non_diagonal_entries), shift=DOWN, lag_ratio=0.1, run_time=1.5),
            FadeOut(matrix_mob.get_horizontal_lines(), run_time=1.5),
            FadeOut(matrix_mob.get_vertical_lines(), run_time=1.5),
        )
        self.wait(0.5)
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

class WhatIsAMatrix(Scene):
    def construct(self):
        self.wait(3)
        self.add_sound("voiceovers/WhatIsAMatrix_part1.mp3")
        matrix = Matrix([
            [1, 2, 3],
            [4, 5, 6]
        ])
        self.play(Create(matrix))
        self.wait(2)
        row_rects = VGroup()
        for row in range(2):
            rect = SurroundingRectangle(matrix.get_rows()[row], color=YELLOW, buff=0.1)
            row_rects.add(rect)
        self.play(FadeIn(row_rects))
        rows_text = Text("2 hàng", font="Noto Sans", color=YELLOW).next_to(matrix, DOWN)
        row_num = rows_text[:1]
        self.play(FadeIn(rows_text))     
        self.play(FadeOut(row_rects))     
        self.add_sound("voiceovers/WhatIsAMatrix_part2.mp3")
        col_rects = VGroup()
        for col in range(3):
            rect = SurroundingRectangle(matrix.get_columns()[col], color=BLUE, buff=0.1)
            col_rects.add(rect)
        self.play(FadeIn(col_rects))
        cols_text = Text("3 cột", font="Noto Sans", color=BLUE).next_to(matrix, RIGHT)
        col_num = cols_text[:1]
        self.play(FadeIn(cols_text))
        self.play(FadeOut(col_rects))
        self.add_sound("voiceovers/WhatIsAMatrix_part3.mp3")
        self.wait(5)
        self.play(Indicate(rows_text))
        self.play(Indicate(cols_text))
        matrix_text = Text("Ma trận 2x3", font="Noto Sans").next_to(matrix, UP)
        matrix_row = matrix_text[-3:-2]
        matrix_row.set_color(YELLOW)
        matrix_col = matrix_text[-1:]
        matrix_col.set_color(BLUE)
        matrix_row.target, matrix_col.target = row_num, col_num
        for mob in matrix_row, matrix_col:
            mob.save_state()
            mob.move_to(mob.target)
        self.play(Write(matrix_text))
        self.play(*[Restore(mob) for mob in (matrix_row, matrix_col)])
        self.wait()
        self.play(FadeOut(matrix_text), FadeOut(rows_text), FadeOut(cols_text))
        
        self.add_sound("voiceovers/WhatIsAMatrix_part4a1.mp3")
        matrix_name = Text("A=").next_to(matrix, LEFT)
        self.play(Write(matrix_name))
        self.wait(2)
        self.play(Indicate(matrix_name))
        self.wait(2)

        aij_text = MathTex(r"A_{ij}", font_size=42).to_corner(UL)
        element_text = Text(" = phần tử ", font="Noto Sans", font_size=32).next_to(aij_text, RIGHT)
        element_text[1:].set_color_by_gradient(YELLOW, BLUE)
        equal_element = element_text[0]
        equal_i = Text("=", font="Noto Sans", font_size=32).next_to(equal_element, DOWN)
        equal_j = Text("=", font="Noto Sans", font_size=32).next_to(equal_i, DOWN)
        i_text = Text("i", font="Noto Sans", font_size=32).next_to(equal_i, LEFT)
        j_text = Text("j", font="Noto Sans", font_size=32).next_to(equal_j, LEFT)
        row_text = Text("hàng", font="Noto Sans", font_size=32, color=YELLOW).next_to(equal_i, RIGHT)
        col_text = Text("cột ", font="Noto Sans", font_size=32, color=BLUE).next_to(equal_j, RIGHT)
        ij_text = VGroup(i_text, equal_i, row_text, j_text, equal_j, col_text)
        
        self.play(Write(aij_text), Write(element_text))
        self.wait(3)
        self.play(Write(VGroup(i_text, equal_i, row_text)))
    
        i_labels = VGroup(
            Text("i=1", font_size=28).next_to(matrix.get_rows()[0], RIGHT, buff=0.6),
            Text("i=2", font_size=28).next_to(matrix.get_rows()[1], RIGHT, buff=0.6)
        )
        i_rects = VGroup(
            SurroundingRectangle(matrix.get_rows()[0], color=YELLOW, buff=0.1),
            SurroundingRectangle(matrix.get_rows()[1], color=YELLOW, buff=0.1)
        )
        self.play(FadeIn(i_rects), FadeIn(i_labels))
        self.play(FadeOut(i_rects), FadeOut(i_labels))
        self.add_sound("voiceovers/WhatIsAMatrix_part4a2.mp3")
        self.play(Write(VGroup(j_text, equal_j, col_text)))

        j_labels = VGroup(
            Text("j=1", font_size=28).next_to(matrix.get_columns()[0], UP, buff=0.3),
            Text("j=2", font_size=28).next_to(matrix.get_columns()[1], UP, buff=0.3),
            Text("j=3", font_size=28).next_to(matrix.get_columns()[2], UP, buff=0.3)
        )
        j_rects = VGroup(
            SurroundingRectangle(matrix.get_columns()[0], color=BLUE, buff=0.1),
            SurroundingRectangle(matrix.get_columns()[1], color=BLUE, buff=0.1),
            SurroundingRectangle(matrix.get_columns()[2], color=BLUE, buff=0.1)
        )
        self.play(FadeIn(j_rects), FadeIn(j_labels))
        self.play(FadeOut(j_rects), FadeOut(j_labels))

        row2_rect = SurroundingRectangle(matrix.get_rows()[1], color=YELLOW, buff=0.1)
        col3_rect = SurroundingRectangle(matrix.get_columns()[2], color=BLUE, buff=0.1)
        element_23 = matrix.get_entries()[5]  # (2,3) element in 2x3 matrix (row-major order)
        element_rect = SurroundingRectangle(element_23, color=RED, buff=0.15)
        self.play(Create(row2_rect), Create(col3_rect))
        self.add_sound("voiceovers/WhatIsAMatrix_part4b.mp3")
        self.play(Create(element_rect))    
        arrow = Arrow(0.5*UP, 0.5*DOWN, color=GOLD).next_to(element_23, DOWN)
        a23_result = MathTex(r"A_{23} = 6", font_size=42).next_to(arrow, DOWN)       
        self.play(GrowArrow(arrow), Write(a23_result))
        self.wait(2)
        element_label = Text("i=2, j=3", font_size=32).next_to(element_23, RIGHT, buff=0.6)
        self.play(Write(element_label), run_time=3)
        self.wait(6)
        self.play(FadeOut(row2_rect), FadeOut(col3_rect), FadeOut(element_rect), FadeOut(element_label), FadeOut(ij_text))
        self.play(FadeOut(matrix), FadeOut(matrix_name), FadeOut(aij_text), FadeOut(element_text), FadeOut(arrow), FadeOut(a23_result))
# ---------------------------------------------------------
class VectorReview(Scene):
    def construct(self):
        title = Text("Review Vectơ", font="Noto Sans", color=YELLOW)
        title.scale(0.7).to_edge(UP)
        title.add_background_rectangle()
        self.play(Write(title))
        self.add_sound("voiceovers/VectorReview.mp3")
        axes = NumberPlane()
        axes.set_opacity(0.3)
        v = Vector([3,2], color=YELLOW)
        label = v.coordinate_label(color=YELLOW)
        self.play(Create(axes))
        self.play(GrowArrow(v))
        self.play(Write(label))     
        self.play(FadeOut(axes), FadeOut(v)) 
        
        col_vec = Matrix([[3], [2]])
        row_vec = Matrix([[3, 2]]).set_row_colors(BLUE)     
        VGroup(col_vec, row_vec).arrange(RIGHT, buff=2)
        col_vec_text = Text("Vectơ \ncột", font="Noto Sans").scale(0.65).next_to(col_vec, LEFT)
        row_vec_text = Text("Vectơ hàng", font="Noto Sans").scale(0.65).next_to(row_vec, DOWN)
        self.play(label.animate.move_to(col_vec))
        self.play(Write(col_vec_text))
        self.play(Transform(col_vec, row_vec))
        self.play(Write(row_vec_text))
        self.wait(3)
        
class MatrixAddition(Scene):
    def construct(self):
        self.add_sound("voiceovers/MatrixAddition_part1.mp3")
        title_operations = Text("Các phép toán ma trận cơ bản", font="Noto Sans", color=YELLOW)
        self.play(Write(title_operations), run_time=1.5)      
        self.play(FadeOut(title_operations))
        title = Text("Cộng hoặc trừ ma trận", font="Noto Sans")
        title.scale(0.7).to_edge(UP)
        line = Line(LEFT * 6, RIGHT * 6, color=WHITE).set_stroke(width=3)
        line.next_to(title, DOWN, buff=0.1)
        self.play(Write(title))
        self.add_sound("voiceovers/MatrixAddition_part2.mp3")
        self.play(Create(line))
        self.wait()
        A_different_size = Matrix([[1, 2], [3, 4]])
        B_different_size = Matrix([[5], [6], [7]])
        plus_different_size = MathTex("+")
        addition__different_size = VGroup(A_different_size, plus_different_size, B_different_size).arrange(RIGHT)
        matrix_text_A = Text("Ma trận 2x2", font="Noto Sans").scale(0.65).next_to(A_different_size, LEFT)
        matrix_text_B = Text("Ma trận 3x1", font="Noto Sans").scale(0.65).next_to(B_different_size, RIGHT)
        self.play(Create(A_different_size), FadeIn(plus_different_size), Create(B_different_size))
        self.play(Write(matrix_text_A), Write(matrix_text_B))
        self.wait(2)
        cross = Cross(addition__different_size).set_stroke(RED, 8)
        self.add_sound("voiceovers/error.wav")
        self.play(Create(cross))
        self.wait(2)
        self.play(FadeOut(A_different_size), FadeOut(B_different_size), 
                  FadeOut(plus_different_size), FadeOut(cross),
                  FadeOut(matrix_text_A), FadeOut(matrix_text_B))
        self.wait()
        deftext = Text(
            "Nếu ta có hai ma trận A và B có cùng kích thước, \nphép cộng ma trận A+B và phép trừ ma trận A-B được định nghĩa như sau:",
        font="Noto Sans").scale(0.65)
        deftext.next_to(line, DOWN, buff=0.5)
        self.play(Write(deftext), run_time=7)
        self.wait()
        
        #A+B=[aij+bij]
        addition = MathTex(r"A + B = [a_{ij} + b_{ij}]")
        addition.next_to(deftext, DOWN, buff=0.5)
        addition.set_color(BLUE)
        self.play(Write(addition), run_time=2)
        self.wait(1)
        #A−B=[aij−bij]
        subtraction = MathTex(r"A - B = [a_{ij} - b_{ij}]")
        subtraction.set_color(GREEN)
        subtraction.next_to(addition, DOWN, buff=0.5)
        self.play(Write(subtraction), run_time=2)
        self.wait(1)
        # Fade out all the text
        self.play(
            FadeOut(addition),
            FadeOut(subtraction),
            FadeOut(deftext)
        )
        self.add_sound("voiceovers/MatrixAddition_part3.mp3")
        A = Matrix([[1, 6, 4], [2, 0, 3]])
        B = Matrix([[7, 5, -1], [2, 3, 7]])
        plus = MathTex("+")
        minus = MathTex("-")
        plus_minus = VGroup(plus, minus).arrange(DOWN)
        equals = MathTex("=")
        C = Matrix([[8, 11, 3], [4, 3, 10]])

        group = VGroup(A, plus_minus, B, equals, C).arrange(RIGHT)
        self.play(Create(A), FadeIn(plus_minus), Create(B))        
        element_11_A = A.get_entries()[0]
        element_11_A_rect = SurroundingRectangle(element_11_A, buff=0.15)
        element_11_B = B.get_entries()[0]
        element_11_B_rect = SurroundingRectangle(element_11_B, buff=0.15)
        self.play(Create(element_11_A_rect))   
        self.wait()   
        self.play(Create(element_11_B_rect))
        self.wait()
        self.play(FadeOut(element_11_A_rect), FadeOut(element_11_B_rect))
        self.wait()
        element_12_A = A.get_entries()[1]
        element_12_A_rect = SurroundingRectangle(element_12_A, buff=0.15)
        element_12_B = B.get_entries()[1]
        element_12_B_rect = SurroundingRectangle(element_12_B, buff=0.15)
        self.play(Create(element_12_A_rect))
        self.wait()
        self.play(Create(element_12_B_rect))
        self.wait()
        self.play(FadeOut(minus))
        self.play(FadeIn(equals), Create(C))
        self.wait(4)

class ScalarMultiplication(Scene):
    def construct(self):
        title = Text("Nhân ma trận với một số", font="Noto Sans")
        title.scale(0.7).to_edge(UP)
        line = Line(LEFT * 6, RIGHT * 6, color=WHITE).set_stroke(width=3)
        line.next_to(title, DOWN, buff=0.1)
        self.play(Write(title))
        self.add_sound("voiceovers/ScalarMultiplication.mp3")
        self.play(Create(line))
        self.wait()
        scalar_multiply = MathTex("k \\times ")
        scalar = scalar_multiply[0][:1]
        scalar.set_color(BLUE)
        matrix = MobjectMatrix([[MathTex("a"), MathTex("b")], [MathTex("c"), MathTex("d")]])
        equal = MathTex("=")
        result = MobjectMatrix([[MathTex("ka"), MathTex("kb")], [MathTex("kc"), MathTex("kd")]])
        group = VGroup(scalar_multiply, matrix, equal, result).arrange(RIGHT)
        matrix_entries = matrix.get_entries()
        matrix_entries.set_color(YELLOW)
        result_entries = result.get_entries()

        self.play(Write(scalar_multiply), Create(matrix))
        self.wait(1)      
        self.play(Write(equal), Create(result.get_brackets()))
        for matrix_entry, result_entry in zip(matrix_entries, result_entries):
            scalar_result = result_entry[0][:1]
            scalar_result.set_color(BLUE)
            element_result = result_entry[0][1:]
            element_result.set_color(YELLOW)
            scalar_result.target, element_result.target = scalar, matrix_entry
            for mob in scalar_result, element_result:
                mob.save_state()
                mob.move_to(mob.target)
            self.play(*[mob.animate.restore() for mob in (scalar_result, element_result)], run_time=1.5)            
        result_entries.set_color(GREEN)
        self.wait()
        self.play(FadeOut(group))

        scalar_multiply_ex = MathTex("2 \\times")
        scalar_ex = scalar_multiply_ex[0][:1]
        scalar_ex.set_color(BLUE)
        matrix_ex = Matrix([[1, 2], [3, 4]])
        equal_ex = MathTex("=")
        result_ex = Matrix([[2, 4], [6, 8]])
        group_ex = VGroup(scalar_multiply_ex, matrix_ex, equal_ex, result_ex).arrange(RIGHT)
        matrix_ex_entries = matrix_ex.get_entries()
        matrix_ex_entries.set_color(YELLOW)
        result_ex_entries = result_ex.get_entries()
        result_ex_entries.set_color(GREEN)
        self.play(Write(scalar_multiply_ex), Create(matrix_ex))
        self.play(Indicate(matrix_ex))
        self.wait(1)
        self.play(Write(equal_ex), Create(result_ex.get_brackets()))

        for matrix_entry, result_entry in zip(matrix_ex_entries, result_ex_entries):
            self.play(Transform(VGroup(scalar_ex.copy(), matrix_entry.copy()), result_entry)) 
        self.wait()
        self.play(FadeOut(group_ex))
# ---------------------------------------------------------
class TransformJustOneVector(Scene):
    def construct(self):
        self.add_sound("voiceovers/TransformJustOneVector.mp3")
        title = Text("Từ các con số đến Phép biến đổi", font="Noto Sans", color=YELLOW)
        title.scale(0.7).to_corner(UL)
        title.add_background_rectangle()
        self.play(Write(title))
        
        container = SVGMobject("assets/container.svg")
        self.play(DrawBorderThenFill(container))
        self.wait()
        self.play(FadeOut(container))
        plane = NumberPlane()
        plane.set_opacity(0.3)
        self.add(plane)

        # Vector and transformation
        v1_coords = np.array([-3, 1])
        t_matrix = np.array([[0, -1], [2, -1]])

        v1 = Vector(v1_coords, color=GOLD)
        v2_coords = t_matrix.T @ v1_coords
        v2 = Vector(v2_coords, color=MAROON)

        v1_label = Text("Vectơ đầu vào", font="Noto Sans", color=v1.get_color()).scale(0.65)
        v1_label.next_to(v1.get_end(), UP)

        v2_label = Text("Vectơ đầu ra", font="Noto Sans", color=v2.get_color()).scale(0.65)
        v2_label.next_to(v2.get_end(), UP)

        # Animate input vector
        self.play(Create(v1))
        self.play(Write(v1_label))

        self.play(Create(v2))
        self.play(Write(v2_label))

        self.remove(v2)
        self.play(
            Transform(v1.copy(), v2, path_arc=-PI / 2, run_time=3),
            v1.animate.set_opacity(0.4)
        )
        self.wait()
class MatrixVectorMultiplication(Scene):
    def construct(self):           
        title = Text("Phép nhân ma trận với một vectơ", font="Noto Sans", color=YELLOW)
        title.scale(0.7).to_edge(UP)
        line = Line(LEFT * 6, RIGHT * 6, color=YELLOW).set_stroke(width=3)
        line.next_to(title, DOWN, buff=0.1)
        self.play(Write(title)) 
        self.add_sound("voiceovers/MatrixVectorMultiplication_part1.mp3")       
        self.play(Create(line))
        explainer1 = Text("Lấy từng hàng của ma trận và tìm tích vô hướng của nó với vectơ", font="Noto Sans")
        explainer1.scale(0.65).next_to(line, DOWN, aligned_edge=LEFT)
        self.play(FadeIn(explainer1))
        explainer2 = Text("(Tổng các tích của các phần tử tương ứng)", font="Noto Sans")
        explainer2.scale(0.65).next_to(explainer1, DOWN, aligned_edge=LEFT)
         
        A = Matrix([[2, 1], [1, 3]])
        v = Matrix([[1], [2]])
        
        equals = MathTex("=")
        result = MobjectMatrix([[MathTex("(2)(1)+(1)(2)")], [MathTex("(1)(1)+(3)(2)")]])
        result_entries = result.get_entries()
        result_entries.set_color(YELLOW)
         
        VGroup(A, v, equals, result).arrange(RIGHT)
        
        result_final = Matrix([[4], [7]]).next_to(result, DOWN, aligned_edge=LEFT)
        equals_final = MathTex("=").next_to(result_final, LEFT)
        group_final = VGroup(equals_final, result_final)
        self.play(Create(A), Create(v))
        row_A_first = A.get_rows()[0]
        row_A_second = A.get_rows()[1]
        rect_A_first = SurroundingRectangle(row_A_first, color=YELLOW, buff=0.1)
        self.play(Create(rect_A_first)) 
 
        rect_v = SurroundingRectangle(v.get_columns(), color=YELLOW, buff=0.1)
        self.play(Create(rect_v))
        arrow = Arrow(row_A_first.get_right(), rect_v.get_left(), color=YELLOW, buff=SMALL_BUFF)
        self.play(FadeIn(arrow))
        self.play(FadeOut(arrow))
        rect_A_second = SurroundingRectangle(row_A_second, color=YELLOW, buff=0.1)
        self.add_sound("voiceovers/slidecard03.wav")
        self.play(ReplacementTransform(rect_A_first, rect_A_second))  
        arrow = Arrow(rect_A_second.get_right(), rect_v.get_left(), color=YELLOW, buff=SMALL_BUFF)
        self.play(FadeIn(arrow))
        self.play(FadeOut(arrow))
        self.play(FadeOut(rect_A_first), FadeOut(rect_A_second), FadeOut(rect_v))     
        
        self.play(FadeIn(equals), FadeIn(result.get_brackets()))
        self.play(FadeIn(explainer2))
        self.add_sound("voiceovers/MatrixVectorMultiplication_part2.mp3")
        
        v_entries = v.get_entries()
        v_entries.set_color(YELLOW)
        for row_index in range(2):
            row_A = A.get_rows()[row_index]
            row_A.set_color(YELLOW)
            result_entry = result_entries[row_index]
            result_left = result_entry[0][:6]
            result_right = result_entry[0][6:]
            circ_A = Circle(color=GREEN).surround(row_A[0], buffer_factor=2.0)
            circ_v = Circle(color=GREEN).surround(v_entries[0], buffer_factor=2.0)
            self.play(Create(circ_A), Create(circ_v))    
            group_left = VGroup(row_A[0].copy(), v_entries[0].copy())   
            self.play(Transform(group_left, result_left))
            group_left.set_color(WHITE)
            circ2_A = Circle(color=GREEN).surround(row_A[1], buffer_factor=2.0)
            circ2_v = Circle(color=GREEN).surround(v_entries[1], buffer_factor=2.0)
            self.play(ReplacementTransform(circ_A, circ2_A), ReplacementTransform(circ_v, circ2_v))
            group_right = VGroup(row_A[1].copy(), v_entries[1].copy())
            self.play(Transform(group_right, result_right))
            self.remove(circ_A, circ_v, circ2_A, circ2_v)
            group_right.set_color(WHITE)
            row_A.set_color(WHITE)
         
        v_entries.set_color(WHITE)
        result_entries.set_color(WHITE)
        self.play(FadeIn(group_final))
        self.add_sound("voiceovers/victory.wav") 
        self.play(Flash(result_final))
        self.wait()


# ---------------------------------------------------------
class MatrixMultiplication(Scene):
    def construct(self):
        self.add_sound("voiceovers/MatrixMultiplication_part1.mp3") 
        title = Text("Phép nhân ma trận với ma trận", font="Noto Sans", color=YELLOW)
        title.scale(0.7).to_edge(UP)
        line = Line(LEFT * 6, RIGHT * 6, color=YELLOW).set_stroke(width=3)
        line.next_to(title, DOWN, buff=0.1)
        self.play(Write(title))        
        self.play(Create(line))
        explainer = Text("Tìm tích vô hướng của mỗi hàng trong ma trận thứ nhất \n và mỗi cột của ma trận thứ hai.", font="Noto Sans")
        explainer.scale(0.65).next_to(line, DOWN, aligned_edge=LEFT)
        self.play(FadeIn(explainer))
        
        A = Matrix([[2, 3], [1, -5]])
        B = Matrix([[4, 3, 6], [1, -2, 3]])
        C = Matrix([[11, 0, 21], [-1, 13, -9]])
        C.get_entries().set_color(YELLOW)
        result = [[MathTex("(2)(4)+(3)(1)"), MathTex("(2)(3)+(3)(-2)"), MathTex("(2)(6)+(3)(3)")],
                  [MathTex("(1)(4)+(-5)(1)"), MathTex("(1)(3)+(-5)(-2)"), MathTex("(1)(6)+(-5)(3)")]]
        
        time = MathTex("\\times ")
        equals = MathTex("=")

        matrix_group = VGroup(A, time, B, equals, C).arrange(RIGHT)
        matrix_text_A = Text("2x2", font="Noto Sans").scale(0.65).next_to(A, DOWN)
        rowNo_A = matrix_text_A[:1].set_color(RED)
        colNo_A = matrix_text_A[2:].set_color(BLUE)
        matrix_text_B = Text("2x3", font="Noto Sans").scale(0.65).next_to(B, DOWN)
        rowNo_B = matrix_text_B[:1].set_color(BLUE)
        colNo_B = matrix_text_B[2:].set_color(RED)
        matrix_text_C = Text("2x3", font="Noto Sans").scale(0.65).next_to(C, DOWN)
        self.play(FadeIn(VGroup(A, time, B)))
        rect_A_moving = SurroundingRectangle(A.get_rows()[0], buff=0.1)      
        self.play(FadeIn(rect_A_moving))
        for row_index in range(2):
            row_A = A.get_rows()[row_index]
            rect_A = SurroundingRectangle(row_A, color=YELLOW, buff=0.1)
            if row_index is not 0:
                self.add_sound("voiceovers/slidecard03.wav")
                self.play(ReplacementTransform(rect_A_moving, rect_A))
            rect_B_moving = SurroundingRectangle(B.get_columns()[0], buff=0.1)
            self.play(FadeIn(rect_B_moving))
            for col_index in range(3):
                col_B = B.get_columns()[col_index]
                rect_B = SurroundingRectangle(col_B, color=YELLOW, buff=0.1)
                if col_index is not 0:
                    self.add_sound("voiceovers/slidecard03.wav")
                    self.play(ReplacementTransform(rect_B_moving, rect_B))
                arrow = Arrow(rect_A_moving.get_right(), rect_B_moving.get_left(), color=YELLOW, buff=SMALL_BUFF)
                self.play(FadeIn(arrow))
                self.play(FadeOut(arrow))
                self.remove(rect_B)
            self.remove(rect_B_moving, rect_A)
        self.remove(rect_A_moving)
        self.add_sound("voiceovers/MatrixMultiplication_part2.mp3")
        self.play(Write(matrix_text_A), Write(matrix_text_B))
        self.wait()
        self.play(Indicate(colNo_A))
        self.wait(0.5)
        self.play(Indicate(rowNo_B))
        self.wait()
        
        dot = r"\cdot"
        matrix_dot = Matrix([[dot, dot, dot], [dot, dot, dot]], element_to_mobject_config={"color": GREEN})
        matrix_dot.move_to(C.get_center())
        self.play(Write(equals), Create(C.get_brackets()), FadeIn(matrix_dot.get_entries())) 
        self.wait()
        rowNo_C = matrix_text_C[:1].set_color(RED)
        colNo_C = matrix_text_C[2:].set_color(RED)
        rowNo_C.target, colNo_C.target = rowNo_A, colNo_B
        for mob in rowNo_C, colNo_C:
            mob.save_state()
            mob.move_to(mob.target)
     
        self.play(rowNo_C.animate.restore())
        self.play(FadeIn(matrix_text_C[1:2]))
        self.play(colNo_C.animate.restore())
       
        self.wait(2)
        self.add_sound("voiceovers/MatrixMultiplication_part3.mp3")          
        self.wait(2) 
        groups = VGroup()
        for row_index in range(2):
            row_A = A.get_rows()[row_index]
            row_A.set_color(YELLOW)
            for col_index in range(3):
                col_B = B.get_columns()[col_index]
                col_B.set_color(YELLOW)
                result_entry = result[row_index][col_index]
                result_left = result_entry[0][:6]
                result_right = result_entry[0][6:]
                VGroup(result_left, result_right).arrange(RIGHT).next_to(C, UP).set_color(YELLOW)
                circ_A = Circle(color=GREEN).surround(row_A[0][0][-1:], buffer_factor=2.0)
                circ_B = Circle(color=GREEN).surround(col_B[0][0][-1:], buffer_factor=2.0)
                self.play(Create(circ_A), Create(circ_B)) 
                group_left = VGroup(row_A[0].copy(), col_B[0]).copy()   
                self.play(Transform(group_left, result_left))
                if row_index==0 and col_index==0:
                    self.wait(0.5)
                circ2_A = Circle(color=GREEN).surround(row_A[1][0][-1:], buffer_factor=2.0)
                circ2_B = Circle(color=GREEN).surround(col_B[1][0][-1:], buffer_factor=2.0)
                self.play(ReplacementTransform(circ_A, circ2_A), ReplacementTransform(circ_B, circ2_B))
                group_right = VGroup(row_A[1].copy(), col_B[1].copy())
                self.play(Transform(group_right, result_right))
                self.play(FadeOut(matrix_dot.get_rows()[row_index][col_index]))
                group = VGroup(group_left, group_right)
                self.play(Transform(group, C.get_rows()[row_index][col_index]))
                groups.add(group)
                self.play(FadeOut(circ_A), FadeOut(circ_B), 
                          FadeOut(circ2_A), FadeOut(circ2_B))
                col_B.set_color(WHITE)
            row_A.set_color(WHITE)
        self.add_sound("voiceovers/victory.wav") 
        self.play(Flash(C))
         
        self.play(
            FadeOut(matrix_group), FadeOut(explainer), 
            FadeOut(matrix_text_A), FadeOut(matrix_text_B), FadeOut(matrix_text_C),
            FadeOut(C), FadeOut(groups))
        
        explainer_not_commutative = Text("Phép nhân ma trận không có tính chất giao hoán.", font="Noto Sans")
        explainer_not_commutative.scale(0.65).next_to(line, DOWN, aligned_edge=LEFT)
        explainer_not_identity = Text("Nhân một ma trận với ma trận đơn vị thu được chính ma trận đó.", font="Noto Sans")
        explainer_not_identity.scale(0.65).next_to(explainer_not_commutative, DOWN, aligned_edge=LEFT)
        not_commutative = MathTex(r"A \times B \neq B \times A")
        not_commutative[0][:1].set_color(YELLOW)
        not_commutative[0][2:3].set_color(BLUE)
        not_commutative[0][5:6].set_color(BLUE)
        not_commutative[0][-1:].set_color(YELLOW)
        identity = MathTex(r"A \times I = A")
        identity[0][:1].set_color(YELLOW)
        identity[0][-1:].set_color(YELLOW)
        VGroup(not_commutative, identity).arrange(DOWN)
        self.add_sound("voiceovers/MatrixMultiplication_properties.mp3")
        self.play(Write(explainer_not_commutative))
        self.wait()       
        self.play(Write(not_commutative),run_time=2)
        self.wait(2)       
        self.play(Write(explainer_not_identity))
        self.play(Write(identity),run_time=2)
        self.wait(3)


# --------------------------------------------------------
class IntroduceLinearTransformations(LinearTransformationScene):
    def __init__(self, **kwargs):
        LinearTransformationScene.__init__(
            self,
            show_basis_vectors = False,
            **kwargs
        )
    def construct(self):       
        title = Text("Trực quan hóa các phép biến đổi tuyến tính", font="Noto Sans", color=YELLOW)
        title.scale(0.7).to_corner(UL).add_background_rectangle()
        self.play(Write(title))     
        self.add_sound("voiceovers/IntroduceLinearTransformations_part1a.mp3") 
        self.wait()
        self.apply_matrix([[2, 1], [1, 2]])
        self.wait()

        self.add_sound("voiceovers/IntroduceLinearTransformations_part1b.mp3") 
        lines_rule = Text("Đường thẳng vẫn thẳng", font="Noto Sans").scale(0.7)
        lines_rule.shift(2*UP).to_edge(LEFT)

        origin_rule = Text("Gốc tọa độ vẫn cố định", font="Noto Sans").scale(0.7)
        origin_rule.shift(2*UP).to_edge(RIGHT)

        arrow = Arrow(
            origin_rule.get_bottom(),
            ORIGIN,
            color=YELLOW,
            buff=0.1
        )
        dot = Dot(ORIGIN, radius=0.1, color=RED)

        for rule in (lines_rule, origin_rule):
            rule.add_background_rectangle()

        self.play(
            Write(lines_rule),
            run_time=1.0
        )

        self.play(
            Write(origin_rule),
            Create(arrow),
            GrowFromCenter(dot),
            run_time=2
        )
        self.wait()

class LinearTransformationShear(LinearTransformationScene):
    def __init__(self, **kwargs):
        LinearTransformationScene.__init__(
            self,
            show_coordinates=True,
            leave_ghost_vectors=True,
            **kwargs
        )

    def construct(self):
        self.add_sound("voiceovers/IntroduceLinearTransformations_part2.mp3")
        title = Text("Lực cắt ngang (shear) với m = 1,25", font="Noto Sans", color=YELLOW)
        title.scale(0.7).to_corner(UL).add_background_rectangle()
        self.play(Write(title))
        matrix_values = [[1, 0], [1.25, 1]]
        matrix = Matrix(matrix_values).next_to(title, DOWN)
        matrix.set_color(PINK).add_background_rectangle()
        self.play(FadeIn(matrix))
        self.wait()
        self.apply_matrix(matrix_values)
        self.wait()

class LinearTransformationReflection(LinearTransformationScene):
    def __init__(self, **kwargs):
        LinearTransformationScene.__init__(
            self,
            show_coordinates=True,
            leave_ghost_vectors=True,
            **kwargs
        )

    def construct(self):
        self.add_sound("voiceovers/IntroduceLinearTransformations_part3.mp3")
        title = Text("Phép phản xạ qua trục thẳng đứng", font="Noto Sans", color=YELLOW)
        title.scale(0.7).to_corner(UL).add_background_rectangle()
        self.play(Write(title)) 
        matrix_values = [[-1, 0], [0, 1]]
        matrix = Matrix(matrix_values).next_to(title, DOWN)
        matrix.set_color(PINK).add_background_rectangle()
        self.play(FadeIn(matrix))
        self.wait()
        self.apply_matrix(matrix_values)
        self.wait()

class LinearTransformationSqueeze(LinearTransformationScene):
    def __init__(self, **kwargs):
        LinearTransformationScene.__init__(
            self,
            show_coordinates=True,
            leave_ghost_vectors=True,
            **kwargs
        )

    def construct(self):
        self.add_sound("voiceovers/IntroduceLinearTransformations_part4.mp3") 
        title = Text("Ánh xạ nén với r = 3/2", font="Noto Sans", color=YELLOW)
        title.scale(0.7).to_corner(UL).add_background_rectangle()
        self.play(Write(title)) 
        matrix_values = [[3/2, 0], [0, 2/3]]
        matrix = MobjectMatrix([[MathTex(r"\frac{3}{2}"), MathTex("0")],
                               [MathTex("0"), MathTex(r"\frac{2}{3}")]])
        matrix.next_to(title, DOWN)
        matrix.get_rows()[0][1].shift(0.65*UP)
        matrix.set_color(PINK).add_background_rectangle()
        self.play(FadeIn(matrix))
        self.wait()
        self.apply_matrix(matrix_values)
        self.wait()

class LinearTransformationSceneScaling(LinearTransformationScene):
    def __init__(self, **kwargs):
        LinearTransformationScene.__init__(
            self,
            show_coordinates=True,
            leave_ghost_vectors=True,
            **kwargs
        )

    def construct(self):
        self.add_sound("voiceovers/IntroduceLinearTransformations_part5.mp3")
        title = Text("Phóng to theo hệ số 3/2", font="Noto Sans", color=YELLOW)
        title.scale(0.7).to_corner(UL).add_background_rectangle()
        self.play(Write(title))        
        matrix_values = [[3/2, 0], [0, 3/2]]
        matrix = MobjectMatrix([[MathTex(r"\frac{3}{2}"), MathTex(r"\text{0}")],
                               [MathTex("0"), MathTex(r"\frac{3}{2}")]])
        matrix.next_to(title, DOWN)
        matrix.get_entries()[1].shift(0.65*UP)
        matrix.set_color(PINK).add_background_rectangle()
        self.play(FadeIn(matrix))
        self.wait()
        self.apply_matrix(matrix_values)
        self.wait()

class RotationByThirtyDegrees(LinearTransformationScene):
    def __init__(self, **kwargs):
        LinearTransformationScene.__init__(
            self,
            show_coordinates=True,
            leave_ghost_vectors=True,
            **kwargs
        )
    def construct(self):
        self.add_sound("voiceovers/IntroduceLinearTransformations_part6.mp3")
        title = Text("Xoay một góc π/6 = 30°", font="Noto Sans", color=YELLOW)
        title.scale(0.7).to_corner(UL).add_background_rectangle()
        self.play(Write(title)) 
        theta = PI / 6
        rotation_matrix = [
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta),  np.cos(theta)]
        ]
        matrix = MobjectMatrix([[MathTex(r"\cos \frac{\pi}{6}"), MathTex(r"-\sin \frac{\pi}{6}")],
                               [MathTex(r"\sin \frac{\pi}{6}"), MathTex(r"\cos \frac{\pi}{6}")]])
        matrix.next_to(title, DOWN)
        matrix.get_rows()[0].shift(0.3*UP)
        matrix.get_rows()[1].shift(0.3*DOWN)
        VGroup(matrix.get_columns()[1], matrix.get_brackets()[1]).shift(0.6*RIGHT)
        matrix.set_color(PINK).add_background_rectangle()
        self.play(FadeIn(matrix))
        self.wait()
        self.apply_matrix(rotation_matrix)
        self.wait()

class OutroScene(Scene):
    def construct(self):
        self.add_sound("voiceovers/OutroScene.mp3")
        matrix = SVGMobject("assets/rubiks-cube.svg")
        self.play(DrawBorderThenFill(matrix))
        # arrows = VGroup(*[
        #     Arrow(ORIGIN, RIGHT*1.5).rotate(i*PI/6).set_color(random_bright_color())
        #     for i in range(12)
        # ])
        # self.play(LaggedStart(*[GrowArrow(arrow) for arrow in arrows]))
        text = Text("Ma trận là ngôn ngữ của sự biến đổi.", font="Noto Sans", color=YELLOW, font_size=40).next_to(matrix, DOWN)
        self.play(Write(text))
        thank = SVGMobject("assets/ThankYou.svg").to_corner(UL)
        
        self.wait(4)
        self.play(DrawBorderThenFill(thank))
        self.wait() 
        self.play(FadeOut(matrix), FadeOut(text))
class MatrixTypes(Scene):
    def construct(self):
        self.add_sound("voiceovers/MatrixTypes.mp3")
        title = Text("Các loại ma trận khác nhau", font="Noto Sans", color=YELLOW)
        self.play(Write(title))
        self.play(title.animate.scale(0.7).to_corner(UL))
        # Show a 3x3 square matrix with random numbers
        random_matrix_3x3 = Matrix([
            [random.randint(1, 9) for _ in range(3)] for _ in range(3)
        ])
        random_matrix_3x3.next_to(title, DOWN)
        self.play(FadeIn(random_matrix_3x3))
        description_square = Text("Ma trận Vuông", font="Noto Sans").scale(0.65)
        description_square[6:].set_color(RED)
        description_square.next_to(random_matrix_3x3, DOWN, buff=SMALL_BUFF)
        self.play(FadeIn(description_square))
        row_rects = VGroup()
        for row in range(3):
            rect = SurroundingRectangle(random_matrix_3x3.get_rows()[row], color=YELLOW, buff=0.1)
            row_rects.add(rect)
        self.play(FadeIn(row_rects))
        self.remove(row_rects)
        col_rects = VGroup()
        for col in range(3):
            rect = SurroundingRectangle(random_matrix_3x3.get_columns()[col], color=BLUE, buff=0.1)
            col_rects.add(rect)
        self.play(FadeIn(col_rects))
        self.play(FadeOut(col_rects))
        self.play(Circumscribe(random_matrix_3x3))
        self.wait()

        # Initial 2x3 zero matrix
        matrix_2x3 = Matrix([[0, 0, 0],
                             [0, 0, 0]])
        matrix_2x3.next_to(description_square, DOWN, buff=LARGE_BUFF)
        self.play(Write(matrix_2x3))
        description_zero = Text("Ma trận Không", font="Noto Sans").scale(0.65)
        description_zero[6:].set_color(RED)
        description_zero.next_to(matrix_2x3, DOWN, buff=SMALL_BUFF)
        self.play(Write(description_zero))
        self.wait(1.5)
        self.play(Indicate(matrix_2x3.get_entries()))
        self.wait(2)

        # Create 3x3 identity matrix
        identity_3x3 = Matrix([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])
        
        identity_2x2 = Matrix([[1, 0], [0, 1]])
        identity_2x2.next_to(random_matrix_3x3, RIGHT).shift(3.5*RIGHT)
        diagonal1 = VGroup(identity_2x2.get_rows()[0][0], identity_2x2.get_rows()[1][1])
        diagonal1.set_color(YELLOW)
        diagonal2 = VGroup(identity_2x2.get_rows()[0][1], identity_2x2.get_rows()[1][0])
        diagonal2.set_color(BLUE)
        description_id_2x2 = Text("Ma trận Đơn vị", font="Noto Sans").scale(0.65)
        description_id_2x2[6:].set_color(RED)
        size_2x2 = Text("Kích thước 2", font="Noto Sans")
        size_2x2.next_to(identity_2x2, RIGHT, buff=SMALL_BUFF).scale(0.55)
        size_2x2.shift(0.6*LEFT)
        description_id_2x2.next_to(identity_2x2, DOWN, buff=SMALL_BUFF)
        self.play(Write(identity_2x2))
        
        self.play(Write(description_id_2x2))
        self.wait(2.5)
        
        self.play(Wiggle(diagonal1))
        self.play(Wiggle(diagonal2))
        self.play(Circumscribe(identity_2x2))
        self.wait()      
        self.play(Write(size_2x2))
        
        identity_3x3.next_to(description_id_2x2, DOWN, buff=LARGE_BUFF)
        for row_index in range(3):
            for col_index in range(3):
                if row_index == col_index:
                    identity_3x3.get_rows()[row_index][col_index].set_color(YELLOW)
                else:
                    identity_3x3.get_rows()[row_index][col_index].set_color(BLUE)
        
        description_id_3x3 = Text("Ma trận Đơn vị", font="Noto Sans").scale(0.65)
        description_id_3x3[6:].set_color(RED)
        size_3x3 = Text("Kích thước 3", font="Noto Sans")
        size_3x3.next_to(identity_3x3, RIGHT, buff=SMALL_BUFF).scale(0.55)
        size_3x3.shift(0.6*LEFT)
        description_id_3x3.next_to(identity_3x3, DOWN, buff=SMALL_BUFF)          
        
        self.play(Write(identity_3x3))
        self.play(Write(description_id_3x3)) 
        self.play(Write(size_3x3))
        self.wait()

class MatrixThumbnail(Scene):
    def construct(self):
        matrix = Matrix([[1, 1], [0, 1]])
        matrix.scale(1.6)
        matrix.shift(LEFT * 4)

        arrow = Arrow(start=LEFT, end=RIGHT, stroke_width=8)
        arrow.scale(2)
        arrow.shift(UP * 0.3)

        # Transformed grid
        plane = NumberPlane(
            x_range=[-2, 2], y_range=[-2, 2],
            background_line_style={"stroke_opacity": 0.4}
        )
        plane.apply_matrix([[1, 1], [0, 1]])
        plane.scale(0.7)
        plane.shift(RIGHT * 3)

        # Big title text
        title = Text("Ma trận", font="Noto Sans", font_size=96, weight=BOLD)
        subtitle = Text("A - Z", font_size=48)
        title.shift(UP * 2.4)
        subtitle.next_to(title, DOWN, buff=0.2)

        title.set_color(YELLOW)
        subtitle.set_color(WHITE)

        matrix_svg = SVGMobject("assets/matrix.svg")
        matrix_svg.to_corner(UL)

        self.add(matrix, arrow, plane, title, subtitle, matrix_svg)
         
