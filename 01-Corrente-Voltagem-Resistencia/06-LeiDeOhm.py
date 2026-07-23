from manim import *
import numpy as np

class LeiDeOhm(Scene):
    def construct(self):
        self.camera.background_color = "#051a2e"

        # =====================================================
        # PARTE 1: INTRODUÇÃO
        # =====================================================
        title = Text("1827: A Lei de Ohm", font_size=42, color=WHITE)
        subtitle = Text("A relação entre Tensão, Corrente e Resistência", font_size=30, color=BLUE_B).next_to(title, DOWN)
        
        self.play(Write(title), FadeIn(subtitle))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle))

        # =====================================================
        # PARTE 2: DESENHANDO O CIRCUITO (Padrão Americano)
        # =====================================================
        
        # Parâmetros do circuito
        w = 7.0  # Largura (x vai de -3.5 a 3.5)
        h = 4.0  # Altura (y vai de -2 a 2)
        
        b_x = -3.5
        r_x = 3.5
        
        # 1. Bateria (Fonte de Tensão) - Padrão Americano (Esquerda)
        # Linha longa (Positivo) em cima, Linha curta e grossa (Negativo) embaixo
        pos_line = Line([b_x - 0.6, 0.2, 0], [b_x + 0.6, 0.2, 0], color=YELLOW, stroke_width=4)
        neg_line = Line([b_x - 0.3, -0.2, 0], [b_x + 0.3, -0.2, 0], color=YELLOW, stroke_width=10)
        battery = VGroup(pos_line, neg_line)
        
        label_v = MathTex("V", color=YELLOW, font_size=48).next_to(battery, LEFT, buff=0.4)
        desc_v = Text("Tensão\n(Empurra)", font_size=20, color=YELLOW).next_to(label_v, DOWN)

        # 2. Resistor - Padrão Americano Zigue-zague (Direita)
        r_pts = [[r_x, 1, 0]]
        num_zigs = 8
        for i in range(1, num_zigs):
            x_val = r_x + (0.3 if i % 2 != 0 else -0.3)
            y_val = 1 - i * (2 / num_zigs)
            r_pts.append([x_val, y_val, 0])
        r_pts.append([r_x, -1, 0])
        
        resistor = VMobject(color=RED, stroke_width=4)
        resistor.set_points_as_corners(r_pts)
        
        label_r = MathTex("R", color=RED, font_size=48).next_to(resistor, RIGHT, buff=0.4)
        desc_r = Text("Resistência\n(Freia)", font_size=20, color=RED).next_to(label_r, DOWN)

        # 3. Fios de Conexão
        # Topo e Base
        wire_top = Line([b_x, h/2, 0], [r_x, h/2, 0], color=WHITE)
        wire_bot = Line([b_x, -h/2, 0], [r_x, -h/2, 0], color=WHITE)
        
        # Conexões da Bateria (Esquerda)
        wire_l_top = Line([b_x, h/2, 0], [b_x, 0.2, 0], color=WHITE)
        wire_l_bot = Line([b_x, -0.2, 0], [b_x, -h/2, 0], color=WHITE)
        
        # Conexões do Resistor (Direita)
        wire_r_top = Line([r_x, h/2, 0], [r_x, 1, 0], color=WHITE)
        wire_r_bot = Line([r_x, -1, 0], [r_x, -h/2, 0], color=WHITE)
        
        wires = VGroup(wire_top, wire_bot, wire_l_top, wire_l_bot, wire_r_top, wire_r_bot)

        # Animação de criação do circuito
        self.play(Create(wires))
        self.play(FadeIn(battery), Write(label_v), FadeIn(desc_v))
        self.play(Create(resistor), Write(label_r), FadeIn(desc_r))
        self.wait(1)

        # =====================================================
        # PARTE 3: A CORRENTE ELÉTRICA (I)
        # =====================================================
        
        # Caminho oculto para os elétrons seguirem (Retângulo de -3.5 a 3.5 em X, -2 a 2 em Y)
        # O Rectangle do Manim desenha no sentido anti-horário começando do canto superior direito.
        # Para fluir do Positivo (cima) para o Negativo (baixo), faremos movimento horário (-dt)
        electron_path = Rectangle(width=w, height=h)
        
        num_electrons = 25
        electrons = VGroup(*[Dot(radius=0.08, color=GREEN_C) for _ in range(num_electrons)])
        
        for i, e in enumerate(electrons):
            e.prop = i / num_electrons
            e.move_to(electron_path.point_from_proportion(e.prop))

        # Variável para controlar a velocidade dinamicamente
        speed_tracker = ValueTracker(0.15)
        
        def update_electrons(mob, dt):
            speed = speed_tracker.get_value()
            for e in mob:
                # Subtraindo para mover no sentido horário (sai do + em cima, vai pro - embaixo)
                e.prop = (e.prop - dt * speed) % 1.0 
                e.move_to(electron_path.point_from_proportion(e.prop))

        self.play(FadeIn(electrons))
        electrons.add_updater(update_electrons)
        
        label_i = MathTex("I", color=GREEN_C, font_size=48).next_to(wire_top, UP, buff=0.2)
        desc_i = Text("Corrente (Fluxo)", font_size=20, color=GREEN_C).next_to(label_i, RIGHT, buff=0.2)
        self.play(Write(label_i), FadeIn(desc_i))
        self.wait(2)

        # =====================================================
        # PARTE 4: A FÓRMULA E AS PROPORÇÕES
        # =====================================================
        self.play(FadeOut(desc_v), FadeOut(desc_r), FadeOut(desc_i))
        
        formula = MathTex("V", "=", "R", "\\cdot", "I", font_size=64).to_edge(UP)
        formula[0].set_color(YELLOW)  # V
        formula[2].set_color(RED)     # R
        formula[4].set_color(GREEN_C) # I
        
        self.play(
            Transform(label_i, MathTex("I", color=GREEN_C, font_size=48).move_to(ORIGIN)),
            Write(formula)
        )
        self.wait(1)

        # -----------------------------------------------------
        # CENA A: Aumentando a Tensão (V)
        # -----------------------------------------------------
        action_text_1 = Text("Aumentando a Tensão (V)...", font_size=28, color=YELLOW).next_to(formula, DOWN)
        self.play(Write(action_text_1))
        
        # Efeito de aumento na bateria (Pulsar/Brilhar)
        glow_battery = battery.copy().set_stroke(width=8).set_color(WHITE).set_opacity(0.5)
        
        self.play(
            FadeIn(glow_battery),
            formula[0].animate.scale(1.5),
            label_v.animate.scale(1.5),
            formula[4].animate.scale(1.5),
            label_i.animate.scale(1.5),
            speed_tracker.animate.set_value(0.4), # Corrente fica rápida
            run_time=2
        )
        self.wait(2)
        
        # Retornando ao normal
        self.play(FadeOut(action_text_1), FadeOut(glow_battery))
        self.play(
            formula[0].animate.scale(1/1.5),
            label_v.animate.scale(1/1.5),
            formula[4].animate.scale(1/1.5),
            label_i.animate.scale(1/1.5),
            speed_tracker.animate.set_value(0.15),
            run_time=1
        )

        # -----------------------------------------------------
        # CENA B: Aumentando a Resistência (R)
        # -----------------------------------------------------
        action_text_2 = Text("Aumentando a Resistência (R)...", font_size=28, color=RED).next_to(formula, DOWN)
        self.play(Write(action_text_2))
        
        # Criando um resistor com picos mais longos (maior amplitude para simbolizar mais resistência)
        new_r_pts = [[r_x, 1, 0]]
        for i in range(1, num_zigs):
            x_val = r_x + (0.7 if i % 2 != 0 else -0.7) # Maior variação lateral
            y_val = 1 - i * (2 / num_zigs)
            new_r_pts.append([x_val, y_val, 0])
        new_r_pts.append([r_x, -1, 0])
        
        new_resistor = VMobject(color=RED, stroke_width=5)
        new_resistor.set_points_as_corners(new_r_pts)
        
        self.play(
            formula[2].animate.scale(1.5),
            label_r.animate.scale(1.5),
            formula[4].animate.scale(0.6),
            label_i.animate.scale(0.6),
            Transform(resistor, new_resistor),
            speed_tracker.animate.set_value(0.04), # Corrente fica bem lenta
            run_time=2
        )
        self.wait(2)

        # =====================================================
        # PARTE 5: CONCLUSÃO
        # =====================================================
        self.play(FadeOut(action_text_2))
        conclusion = Text("Corrente (I) obedece à Tensão (V)\nmas é barrada pela Resistência (R).", 
                          font_size=28, color=WHITE).next_to(formula, DOWN)
        
        self.play(Write(conclusion))
        self.wait(4)

        # Encerramento
        electrons.clear_updaters()
        self.play(*[FadeOut(mob) for mob in self.mobjects])