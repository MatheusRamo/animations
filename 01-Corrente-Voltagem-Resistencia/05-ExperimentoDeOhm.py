from manim import *

class ExperimentoDeOhm(Scene):
    def construct(self):
        # 1. Título (Ajustado para não sobrepor)
        title = Text("O Experimento de Ohm", font_size=40).to_edge(UP, buff=0.5)
        self.play(Write(title))

        # --- PARTE 1: O CIRCUITO SEM BLOCOS DE FUNDO ---
        circuit_group = VGroup()

        # Fios do Amperímetro (Topo)
        wire_top_l = Line([-5.5, 1.0, 0], [-3.9, 1.0, 0])
        wire_top_r = Line([-3.1, 1.0, 0], [-1.5, 1.0, 0])
        
        amm_bg = Circle(radius=0.4, color=WHITE).move_to([-3.5, 1.0, 0])
        amm_label = Text("A", font_size=24).move_to([-3.5, 1.0, 0])
        ammeter = VGroup(amm_bg, amm_label)

        # Fios e Resistor (Lado Direito)
        wire_right_t = Line([-1.5, 1.0, 0], [-1.5, 0.3, 0])
        wire_right_b = Line([-1.5, -1.1, 0], [-1.5, -2.0, 0])
        
        # Desenhando o Zig-Zag (Padrão Americano, perfeitamente alinhado)
        p0 = [-1.5, 0.3, 0]
        p1 = [-1.2, 0.16, 0]
        p2 = [-1.8, -0.12, 0]
        p3 = [-1.2, -0.4, 0]
        p4 = [-1.8, -0.68, 0]
        p5 = [-1.2, -0.96, 0]
        p6 = [-1.5, -1.1, 0]
        resistor = VGroup(Line(p0,p1), Line(p1,p2), Line(p2,p3), Line(p3,p4), Line(p4,p5), Line(p5,p6))
        resistor.set_color(YELLOW)
        r_label = Text("R", font_size=24, color=YELLOW).next_to(resistor, RIGHT, buff=0.2)

        # Fios e Bateria (Lado Esquerdo)
        wire_left_t = Line([-5.5, 1.0, 0], [-5.5, -0.3, 0])
        wire_left_b = Line([-5.5, -0.7, 0], [-5.5, -2.0, 0])
        
        # Bateria - Padrão Americano correto (Placas horizontais cruzando o fio vertical)
        bat_pos = Line([-5.9, -0.3, 0], [-5.1, -0.3, 0], color=WHITE) # Longa
        bat_neg = Line([-5.7, -0.7, 0], [-5.3, -0.7, 0], color=WHITE, stroke_width=8) # Curta e grossa
        
        plus_label = Text("+", font_size=16).next_to(bat_pos, UP, buff=0.1).shift(LEFT*0.3)
        minus_label = Text("-", font_size=16).next_to(bat_neg, DOWN, buff=0.1).shift(LEFT*0.3)
        battery = VGroup(bat_pos, bat_neg, plus_label, minus_label)

        # Fio Inferior
        wire_bottom = Line([-1.5, -2.0, 0], [-5.5, -2.0, 0])

        circuit_group.add(
            wire_top_l, wire_top_r, ammeter, 
            wire_right_t, wire_right_b, resistor, r_label,
            wire_left_t, wire_left_b, battery, 
            wire_bottom
        )
        
        # Sistema de Variação de Valores (Resistência constante R = 2)
        r_value = 2.0
        v_tracker = ValueTracker(0)
        
        # Textos dos medidores com tamanho reduzido para não encavalar
        v_text = always_redraw(lambda: Text(f"V = {v_tracker.get_value():.1f} V", font_size=20).next_to(battery, LEFT, buff=0.3))
        i_text = always_redraw(lambda: Text(f"I = {v_tracker.get_value()/r_value:.1f} A", font_size=20).next_to(ammeter, UP, buff=0.2))
        
        # --- PARTE 2: O GRÁFICO CARTESIANO ---
        # Gráfico ligeiramente menor para dar mais respiro à cena
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 10, 2],
            x_length=4.5,
            y_length=4.0,
            axis_config={"include_numbers": True, "font_size": 20}
        ).shift(RIGHT * 2.8 + DOWN * 0.5)
        
        axes_labels = axes.get_axis_labels(x_label="I (A)", y_label="V (V)")
        graph_group = VGroup(axes, axes_labels)

        # Animação inicial
        self.play(Create(circuit_group), FadeIn(v_text), FadeIn(i_text), run_time=2)
        self.play(Create(graph_group), run_time=1.5)
        self.wait(1)

        # --- PARTE 3: EXECUTANDO O EXPERIMENTO ---
        medicoes = [(1, 2), (2, 4), (3, 6), (4, 8)]
        
        for i, v in medicoes:
            # 1. Aumenta a tensão na fonte
            self.play(v_tracker.animate.set_value(v), run_time=1.5)
            self.wait(0.3)
            
            # 2. Plota o ponto
            dot = Dot(axes.c2p(i, v), color=RED, radius=0.08)
            h_line = axes.get_horizontal_line(axes.c2p(i, v), color=GRAY, line_func=DashedLine)
            v_line = axes.get_vertical_line(axes.c2p(i, v), color=GRAY, line_func=DashedLine)
            
            self.play(Create(h_line), Create(v_line), FadeIn(dot), run_time=1)
            
        self.wait(1)

        # --- PARTE 4: A CONCLUSÃO ---
        graph_line = axes.plot(lambda x: r_value * x, x_range=[0, 4.5], color=YELLOW)
        self.play(Create(graph_line), run_time=1.5)
        
        # Fórmula da proporção logo acima do gráfico
        razao_text = MathTex(r"\frac{V}{I} = \text{Constante}").next_to(axes, UP, buff=0.4)
        self.play(Write(razao_text))
        self.wait(1)
        
        # Fórmula final fixada na base da tela
        eq_final = MathTex("V", "=", "R", "\\cdot", "I", font_size=44).to_edge(DOWN, buff=0.4)
        eq_final[2].set_color(YELLOW) 
        
        self.play(TransformFromCopy(razao_text, eq_final), run_time=1.5)
        
        box = SurroundingRectangle(eq_final, color=YELLOW, buff=0.2)
        self.play(Create(box))
        
        self.wait(3)