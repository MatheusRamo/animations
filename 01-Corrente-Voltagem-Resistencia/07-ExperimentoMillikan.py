from manim import *
import numpy as np

class ExperimentoMillikan(Scene):
    def construct(self):
        # 1. Configuração do Fundo e Título Inicial
        self.camera.background_color = "#051a2e"
        
        title = Text("1909: O Experimento de Millikan", font_size=40, color=WHITE)
        subtitle = Text("A Descoberta da Carga Elementar", font_size=28, color="#11caa0").next_to(title, DOWN)
        
        self.play(Write(title), FadeIn(subtitle))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle))

        # =2. MONTAGEM DA CÂMARA DE PLACAS METÁLICAS =
        # Placa Superior (Positiva) e Placa Inferior (Negativa)
        plate_top = Rectangle(width=8.0, height=0.3, color=WHITE, fill_opacity=0.8).shift(UP * 2.2)
        plate_bot = Rectangle(width=8.0, height=0.3, color=WHITE, fill_opacity=0.8).shift(DOWN * 2.2)
        
        label_plus = MathTex("+ + + + + + + +", color=RED, font_size=28).next_to(plate_top, UP, buff=0.1)
        label_minus = MathTex("- - - - - - - -", color=BLUE, font_size=28).next_to(plate_bot, DOWN, buff=0.1)
        
        chamber_group = VGroup(plate_top, plate_bot, label_plus, label_minus)
        self.play(Create(chamber_group), run_time=1.5)

        # 3. A GOTA DE ÓLEO CAINDO
        drop = Dot(radius=0.12, color=YELLOW).shift(UP * 2.0)
        drop_label = Text("Gota de Óleo", font_size=20, color=YELLOW).next_to(drop, RIGHT, buff=0.2)
        
        self.play(FadeIn(drop), Write(drop_label))
        
        # Gota caindo até o centro da câmara
        self.play(drop.animate.shift(DOWN * 2.0), drop_label.animate.shift(DOWN * 2.0), run_time=1.5, rate_func=rate_functions.ease_in_sine)
        self.wait(0.5)

        # 4. SURGEM AS FORÇAS (Gravidade e Força Elétrica)
        # Força da Gravidade (mg) para baixo
        arrow_mg = Arrow(start=ORIGIN, end=DOWN*1.2, color=RED, stroke_width=4, buff=0).move_to(drop.get_center() + DOWN*0.6)
        label_mg = MathTex(r"\vec{F}_g = m\vec{g}", color=RED, font_size=24).next_to(arrow_mg, RIGHT, buff=0.1)
        
        self.play(GrowArrow(arrow_mg), Write(label_mg))
        self.wait(0.8)

        # Campo elétrico ligado: Força Elétrica (qE) para cima equilibrando a gravidade
        arrow_qe = Arrow(start=ORIGIN, end=UP*1.2, color=GREEN_C, stroke_width=4, buff=0).move_to(drop.get_center() + UP*0.6)
        label_qe = MathTex(r"\vec{F}_e = q\vec{E}", color=GREEN_C, font_size=24).next_to(arrow_qe, RIGHT, buff=0.1)
        
        # A gota para (levita perfeitamente no centro)
        self.play(
            GrowArrow(arrow_qe), 
            Write(label_qe),
            drop.animate.set_color(GREEN),
            run_time=1.2
        )
        
        levita_text = Text("Equilíbrio: A gota levita!", font_size=24, color=YELLOW).to_edge(UP)
        self.play(Write(levita_text))
        self.wait(1.5)

        # 5. A EQUAÇÃO DE EQUILÍBRIO
        # Limpando a câmara e subindo os elementos para abrir espaço para a matemática
        self.play(
            FadeOut(levita_text),
            FadeOut(arrow_mg), FadeOut(label_mg),
            FadeOut(arrow_qe), FadeOut(label_qe),
            FadeOut(drop_label),
            chamber_group.animate.shift(UP * 0.8),
            drop.animate.shift(UP * 0.8),
            run_time=1
        )
        
        eq_title = Text("Igualando as forças:", font_size=26, color=WHITE).to_edge(DOWN).shift(UP * 2.2)
        eq_step1 = MathTex("qE = mg", font_size=40).next_to(eq_title, DOWN, buff=0.3)
        
        self.play(Write(eq_title), Write(eq_step1))
        self.wait(1)
        
        # Isolando a Carga (q)
        eq_step2 = MathTex(r"q = \frac{mg}{E}", font_size=48, color="#11caa0").move_to(eq_step1.get_center())
        
        self.play(Transform(eq_step1, eq_step2), run_time=1.2)
        
        box_eq = SurroundingRectangle(eq_step1, color="#11caa0", buff=0.2)
        self.play(Create(box_eq))
        self.wait(1.5)

        # 6. MÚLTIPLOS E O VALOR FINAL DA CARGA ELEMENTAR
        # Limpando a tela para focar nos números e na quantização
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob != title]
        )
        
        quant_title = Text("Os valores nunca eram aleatórios...", font_size=32, color=WHITE).to_edge(UP, buff=1.0)
        self.play(Write(quant_title))
        
        # Mostrando divisões de valores que sempre resultam em múltiplos inteiros
        calc_sequence = MathTex(
            r"q_1 = 3.2 \times 10^{-19}\text{ C } (= 2 \times e)",
            r"\\ q_2 = 4.8 \times 10^{-19}\text{ C } (= 3 \times e)",
            r"\\ q_3 = 6.4 \times 10^{-19}\text{ C } (= 4 \times e)",
            font_size=28
        ).shift(UP * 0.2)
        
        for line in calc_sequence:
            self.play(Write(line), run_time=1)
            self.wait(0.5)
            
        self.wait(1)

        # O Gran Finale: A Carga Elementar do Elétron
        final_result_box = Rectangle(width=8.5, height=1.4, color="#11caa0", fill_color="#005088", fill_opacity=0.9).shift(DOWN * 2.2)
        final_text = MathTex(r"e = 1.602 \times 10^{-19}\text{ C}", font_size=44, color=WHITE).move_to(final_result_box.get_center())
        final_label = Text("A Carga Elementar do Elétron!", font_size=20, color="#11caa0").next_to(final_result_box, UP, buff=0.1)
        
        self.play(Create(final_result_box), Write(final_label), Write(final_text))
        self.wait(3)
