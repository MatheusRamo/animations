from manim import *
import numpy as np

class BalancaDeCoulomb(Scene):
    def construct(self):
        # Fundo da tela
        self.camera.background_color = "#051a2e"

        # =====================================================
        # PARTE 1: INTRODUÇÃO
        # =====================================================
        
        title = Text("1785: A Ciência Quantitativa", font_size=40, color=WHITE)
        subtitle = Text("Balança de Torção de Coulomb", font_size=30, color=BLUE_B).next_to(title, DOWN)
        
        self.play(Write(title), FadeIn(subtitle))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle))

        # =====================================================
        # PARTE 2: A BALANÇA (VISTA SUPERIOR)
        # =====================================================
        
        # O centro da nossa balança ficará à esquerda
        center_pos = LEFT * 3.5
        
        # Recipiente de Vidro
        glass_case = Circle(radius=2.2, color="#a1c9f4", stroke_opacity=0.5, stroke_width=4).move_to(center_pos)
        center_dot = Dot(center_pos, color=WHITE)
        
        # Texto de indicação (ajustado para não sobrepor)
        view_text = Text("Vista Superior", font_size=24, color=GRAY).next_to(glass_case, UP, buff=0.2)
        self.play(FadeIn(view_text))

        # Haste móvel (Rotor)
        rod = Line(center_pos + LEFT*1.8, center_pos + RIGHT*1.8, color=LIGHT_GREY, stroke_width=6)
        
        # Carga Q1 (Na ponta direita da haste)
        q1 = Circle(radius=0.25, color="#FF4444", fill_opacity=0.9).move_to(rod.get_end())
        q1_sign = Text("+", font_size=24, color=WHITE).move_to(q1)
        
        # Contrapeso (Na ponta esquerda)
        counter = Circle(radius=0.2, color=GRAY, fill_opacity=1).move_to(rod.get_start())
        
        mobile_part = VGroup(rod, q1, q1_sign, counter)
        
        self.play(Create(glass_case), FadeIn(center_dot))
        self.play(Create(rod), FadeIn(q1), FadeIn(q1_sign), FadeIn(counter))

        # =====================================================
        # PARTE 3: A INTERAÇÃO (CARGA EXTERNA)
        # =====================================================
        
        # Carga Q2 (Fixa, trazida de fora)
        q2 = Circle(radius=0.25, color="#FF4444", fill_opacity=0.9)
        q2_sign = Text("+", font_size=24, color=WHITE)
        fixed_charge = VGroup(q2, q2_sign)
        fixed_charge.move_to(center_pos + RIGHT*5.5) # Começa bem longe
        
        self.play(FadeIn(fixed_charge))

        # Linha pontilhada marcando a posição original (Repouso)
        dashed_line = DashedLine(center_pos, center_pos + RIGHT*1.8, color=GRAY, stroke_opacity=0.5)
        self.add(dashed_line)

        # Linha dinâmica de distância (r) entre as duas esferas
        dist_line = always_redraw(lambda: DashedLine(q1.get_center(), q2.get_center(), color=WHITE, dash_length=0.1))
        r_label = always_redraw(lambda: MathTex("r", font_size=28).next_to(dist_line.get_center(), UP, buff=0.1))
        
        self.play(Create(dist_line), Write(r_label))

        # Explicação (Movida para baixo do vidro para não bater no título)
        explanation = Text("Cargas iguais se repelem,\ntorcendo o fio central.", font_size=26, color=YELLOW)
        explanation.next_to(glass_case, DOWN, buff=0.3)
        self.play(Write(explanation))

        # Tracker para o ângulo (começa em 0.001 para evitar erro matemático no Arc)
        angle_tracker = ValueTracker(0.001)

        # Desenho dinâmico do arco do ângulo Theta
        angle_arc = always_redraw(lambda: Arc(
            radius=0.8, 
            start_angle=0, 
            angle=angle_tracker.get_value(), 
            arc_center=center_pos, 
            color=YELLOW
        ))
        theta = always_redraw(lambda: MathTex(r"\theta", font_size=28, color=YELLOW).move_to(
            center_pos + RIGHT * 1.1 * np.cos(angle_tracker.get_value()/2) + UP * 1.1 * np.sin(angle_tracker.get_value()/2)
        ))

        self.add(angle_arc, theta)

        # Aproximação 1 (Esfera B se aproxima, Haste gira)
        self.play(
            fixed_charge.animate.move_to(center_pos + RIGHT*3.2),
            Rotate(mobile_part, angle=PI/6, about_point=center_pos),
            angle_tracker.animate.set_value(PI/6),
            run_time=2
        )
        self.wait(1)
        self.play(FadeOut(explanation))

        # =====================================================
        # PARTE 4: A FÓRMULA (LEI DE COULOMB)
        # =====================================================
        
        # Fórmula reposicionada para ter mais respiro
        formula = MathTex(
            r"F = k \frac{q_1 \cdot q_2}{r^2}",
            substrings_to_isolate=["F", "q_1", "q_2", "r^2"],
            font_size=50
        ).move_to(RIGHT*3.5 + UP*1.8)
        
        formula.set_color_by_tex("F", YELLOW)
        formula.set_color_by_tex("q_1", "#FF4444")
        formula.set_color_by_tex("q_2", "#FF4444")
        formula.set_color_by_tex("r^2", BLUE_B)
        
        formula_label = Text("Lei de Coulomb", font_size=28, color=WHITE).next_to(formula, UP, buff=0.3)
        
        self.play(Write(formula_label), FadeIn(formula, shift=UP))
        self.wait(1)

        # =====================================================
        # PARTE 5: GRÁFICO (FORÇA x DISTÂNCIA)
        # =====================================================
        
        # Gráfico ligeiramente menor para caber melhor o texto final
        axes = Axes(
            x_range=[0.5, 5, 1], 
            y_range=[0, 12, 3],
            x_length=4.5, 
            y_length=3.0,
            axis_config={"color": WHITE, "include_numbers": False}
        ).move_to(RIGHT*3.5 + DOWN*1.2)
        
        x_label = axes.get_x_axis_label("r").set_color(BLUE_B)
        y_label = axes.get_y_axis_label("F").set_color(YELLOW)
        
        # Curva 1/r^2
        graph = axes.plot(lambda x: 10 / (x**2), color=YELLOW, x_range=[0.9, 4.5])
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(Create(graph), run_time=1.5)

        # Ponto dinâmico no gráfico que acompanha a distância real entre q1 e q2
        dist_tracker_dot = always_redraw(lambda: Dot(
            axes.c2p(
                np.linalg.norm(q1.get_center() - q2.get_center()), 
                10 / (np.linalg.norm(q1.get_center() - q2.get_center())**2)
            ), 
            color=RED, radius=0.08
        ))
        
        self.add(dist_tracker_dot)
        
        # Animação conjunta: O gráfico responde fisicamente à balança!
        self.play(
            fixed_charge.animate.move_to(center_pos + RIGHT*5.5),
            Rotate(mobile_part, angle=-PI/6, about_point=center_pos),
            angle_tracker.animate.set_value(0.001),
            run_time=2.5, rate_func=there_and_back 
        )
        
        self.play(
            fixed_charge.animate.move_to(center_pos + RIGHT*2.5),
            Rotate(mobile_part, angle=PI/3.5, about_point=center_pos),
            angle_tracker.animate.set_value(PI/3.5),
            run_time=3, rate_func=smooth
        )
        self.wait(1)

        # Conclusão (Reposicionada para caber confortavelmente no rodapé)
        conclusion = Text(
            "A eletricidade agora podia\nser estudada matematicamente.",
            font_size=26, color=WHITE
        ).next_to(axes, DOWN, buff=0.5)
        
        self.play(Write(conclusion))
        self.wait(4)

        # Limpando a cena
        self.play(*[FadeOut(mob) for mob in self.mobjects])