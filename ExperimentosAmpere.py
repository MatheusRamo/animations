from manim import *
import numpy as np

class ExperimentosAmpere(Scene):
    def construct(self):
        self.camera.background_color = "#051a2e"

        # =====================================================
        # PARTE 1: INTRODUÇÃO
        # =====================================================
        title = Text("1820: O Magnetismo", font_size=40, color=WHITE)
        subtitle = Text("A resposta de Ampère: Fios Paralelos", font_size=30, color=BLUE_B).next_to(title, DOWN)
        
        self.play(Write(title), FadeIn(subtitle))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle))

        # =====================================================
        # PARTE 2: CONFIGURAÇÃO INICIAL (FIOS PARALELOS)
        # =====================================================
        desc_text = Text("Ampère percebeu que fios com corrente se comportam como ímãs.", font_size=28, color=YELLOW).to_edge(UP)
        self.play(Write(desc_text))
        
        # Criando os dois fios paralelos
        wire1 = Line(UP*3 + LEFT*1.5, DOWN*3 + LEFT*1.5, color=DARK_GRAY, stroke_width=8)
        wire2 = Line(UP*3 + RIGHT*1.5, DOWN*3 + RIGHT*1.5, color=DARK_GRAY, stroke_width=8)
        
        self.play(Create(wire1), Create(wire2))
        self.wait(1)

        # =====================================================
        # PARTE 3: CORRENTES NO MESMO SENTIDO (ATRAÇÃO)
        # =====================================================
        desc_text_2 = Text("Correntes no MESMO sentido: Os fios se ATRAEM.", font_size=28, color=GREEN_C).to_edge(UP)
        self.play(Transform(desc_text, desc_text_2))
        
        # Setas indicando a direção da corrente (para baixo em ambos)
        arrow1 = Arrow(start=UP*2 + LEFT*2.2, end=DOWN*2 + LEFT*2.2, color=GREEN_C, stroke_width=4, max_tip_length_to_length_ratio=0.1)
        arrow2 = Arrow(start=UP*2 + RIGHT*2.2, end=DOWN*2 + RIGHT*2.2, color=GREEN_C, stroke_width=4, max_tip_length_to_length_ratio=0.1)
        
        label_i1 = MathTex("I_1", color=GREEN_C).next_to(arrow1, LEFT)
        label_i2 = MathTex("I_2", color=GREEN_C).next_to(arrow2, RIGHT)
        
        self.play(GrowArrow(arrow1), GrowArrow(arrow2), Write(label_i1), Write(label_i2))
        
        # Elétrons se movendo (corrente convencional para baixo, logo elétrons para cima, mas vamos animar a corrente para facilitar)
        # Animaremos "cargas positivas" para manter a lógica das setas
        charges_w1 = VGroup(*[Dot(radius=0.08, color=GREEN_C) for _ in range(8)])
        charges_w2 = VGroup(*[Dot(radius=0.08, color=GREEN_C) for _ in range(8)])
        
        for i, c in enumerate(charges_w1):
            c.move_to(wire1.point_from_proportion(i / 8))
        for i, c in enumerate(charges_w2):
            c.move_to(wire2.point_from_proportion(i / 8))
            
        def update_charges_down(mob, dt):
            for c in mob:
                y = c.get_y() - dt * 3
                if y < -3:
                    y = 3
                c.move_to(np.array([c.get_x(), y, 0]))

        self.play(FadeIn(charges_w1), FadeIn(charges_w2))
        charges_w1.add_updater(update_charges_down)
        charges_w2.add_updater(update_charges_down)
        self.wait(1)
        
        # Forças de atração
        force_arrow1 = Arrow(start=LEFT*1.5, end=LEFT*0.3, color=YELLOW, buff=0)
        force_arrow2 = Arrow(start=RIGHT*1.5, end=RIGHT*0.3, color=YELLOW, buff=0)
        
        label_f = MathTex("F", color=YELLOW)
        label_f1 = label_f.copy().next_to(force_arrow1, UP, buff=0.1)
        label_f2 = label_f.copy().next_to(force_arrow2, UP, buff=0.1)
        
        self.play(GrowArrow(force_arrow1), GrowArrow(force_arrow2), Write(label_f1), Write(label_f2))
        
        # Animando a curvatura (atração)
        # Usaremos curvas bezier para simular a flexão dos fios
        wire1_bent = ParametricFunction(lambda t: np.array([-1.5 + 0.8 * np.sin(t * PI), 3 - 6*t, 0]), t_range=[0, 1], color=DARK_GRAY, stroke_width=8)
        wire2_bent = ParametricFunction(lambda t: np.array([1.5 - 0.8 * np.sin(t * PI), 3 - 6*t, 0]), t_range=[0, 1], color=DARK_GRAY, stroke_width=8)
        
        # Para que os updaters funcionem nos fios curvados, precisamos mudar a lógica,
        # ou simplesmente removê-los durante a transformação para simplificar.
        charges_w1.clear_updaters()
        charges_w2.clear_updaters()
        self.play(FadeOut(charges_w1), FadeOut(charges_w2))
        
        self.play(Transform(wire1, wire1_bent), Transform(wire2, wire2_bent), run_time=1.5)
        self.wait(2)
        
        # Restaurando os fios
        self.play(
            Transform(wire1, Line(UP*3 + LEFT*1.5, DOWN*3 + LEFT*1.5, color=DARK_GRAY, stroke_width=8)),
            Transform(wire2, Line(UP*3 + RIGHT*1.5, DOWN*3 + RIGHT*1.5, color=DARK_GRAY, stroke_width=8)),
            FadeOut(force_arrow1), FadeOut(force_arrow2), FadeOut(label_f1), FadeOut(label_f2)
        )

        # =====================================================
        # PARTE 4: CORRENTES EM SENTIDOS OPOSTOS (REPULSÃO)
        # =====================================================
        desc_text_3 = Text("Correntes em sentidos OPOSTOS: Os fios se REPELEM.", font_size=28, color=RED).to_edge(UP)
        self.play(Transform(desc_text, desc_text_3))
        
        # Mudando a direção da corrente 2 (para cima)
        arrow2_new = Arrow(start=DOWN*2 + RIGHT*2.2, end=UP*2 + RIGHT*2.2, color=RED, stroke_width=4, max_tip_length_to_length_ratio=0.1)
        label_i2_new = MathTex("I_2", color=RED).next_to(arrow2_new, RIGHT)
        
        self.play(
            Transform(arrow2, arrow2_new),
            Transform(label_i2, label_i2_new),
            arrow1.animate.set_color(RED),
            label_i1.animate.set_color(RED)
        )
        
        # Novas cargas animadas
        charges_w1_opp = VGroup(*[Dot(radius=0.08, color=RED) for _ in range(8)])
        charges_w2_opp = VGroup(*[Dot(radius=0.08, color=RED) for _ in range(8)])
        
        for i, c in enumerate(charges_w1_opp):
            c.move_to(wire1.point_from_proportion(i / 8))
        for i, c in enumerate(charges_w2_opp):
            c.move_to(wire2.point_from_proportion(i / 8))
            
        def update_charges_up(mob, dt):
            for c in mob:
                y = c.get_y() + dt * 3
                if y > 3:
                    y = -3
                c.move_to(np.array([c.get_x(), y, 0]))

        self.play(FadeIn(charges_w1_opp), FadeIn(charges_w2_opp))
        charges_w1_opp.add_updater(update_charges_down) # Fio 1 continua pra baixo
        charges_w2_opp.add_updater(update_charges_up)   # Fio 2 agora vai pra cima
        self.wait(1)
        
        # Forças de repulsão
        force_arrow1_rep = Arrow(start=LEFT*1.5, end=LEFT*2.7, color=YELLOW, buff=0)
        force_arrow2_rep = Arrow(start=RIGHT*1.5, end=RIGHT*2.7, color=YELLOW, buff=0)
        
        label_f1_rep = label_f.copy().next_to(force_arrow1_rep, UP, buff=0.1)
        label_f2_rep = label_f.copy().next_to(force_arrow2_rep, UP, buff=0.1)
        
        self.play(GrowArrow(force_arrow1_rep), GrowArrow(force_arrow2_rep), Write(label_f1_rep), Write(label_f2_rep))
        
        # Animando a curvatura (repulsão)
        charges_w1_opp.clear_updaters()
        charges_w2_opp.clear_updaters()
        self.play(FadeOut(charges_w1_opp), FadeOut(charges_w2_opp))
        
        wire1_bent_rep = ParametricFunction(lambda t: np.array([-1.5 - 0.8 * np.sin(t * PI), 3 - 6*t, 0]), t_range=[0, 1], color=DARK_GRAY, stroke_width=8)
        wire2_bent_rep = ParametricFunction(lambda t: np.array([1.5 + 0.8 * np.sin(t * PI), 3 - 6*t, 0]), t_range=[0, 1], color=DARK_GRAY, stroke_width=8)
        
        self.play(Transform(wire1, wire1_bent_rep), Transform(wire2, wire2_bent_rep), run_time=1.5)
        self.wait(3)

        # Encerramento
        self.play(*[FadeOut(mob) for mob in self.mobjects])