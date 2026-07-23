from manim import *
import random
import numpy as np

class EraDoMisterio(Scene):
    def construct(self):
        # Fundo da tela
        self.camera.background_color = "#051a2e"

        # =====================================================
        # PARTE 1: O PRESENTE - MULTÍMETRO
        # =====================================================
        
        multimeter_body = RoundedRectangle(width=3, height=4.5, corner_radius=0.3, color=DARK_GRAY, fill_opacity=1)
        screen = Rectangle(width=2.5, height=1.2, color="#7ea37e", fill_opacity=1).move_to(multimeter_body.get_top() + DOWN * 0.9)
        dial = Circle(radius=0.6, color=LIGHT_GREY, fill_opacity=0.2).move_to(multimeter_body.get_center() + DOWN * 0.6)
        dial_knob = Line(dial.get_center(), dial.get_boundary_point(UP + RIGHT), color=RED, stroke_width=6)
        
        multimeter = VGroup(multimeter_body, screen, dial, dial_knob)
        multimeter.shift(LEFT * 3)
        
        text_v = Text("5.00 V", font_size=28, color=BLACK).move_to(screen.get_center() + UP * 0.3)
        text_i = Text("200 mA", font_size=28, color=BLACK).move_to(screen.get_center())
        text_r = Text("1.0 kΩ", font_size=28, color=BLACK).move_to(screen.get_center() + DOWN * 0.3)
        
        screen_texts = VGroup(text_v, text_i, text_r)
        
        intro_text = Text("Hoje, medir eletricidade parece natural...", font_size=32, color=WHITE)
        intro_text.next_to(multimeter, RIGHT, buff=1)
        
        self.play(FadeIn(multimeter), Write(intro_text))
        self.play(FadeIn(screen_texts, shift=UP), run_time=1.5)
        self.wait(1)
        
        intro_text_2 = Text("Mas e antes de sabermos medir?", font_size=32, color=YELLOW)
        intro_text_2.next_to(multimeter, RIGHT, buff=1)
        
        self.play(Transform(intro_text, intro_text_2))
        self.wait(2)
        
        self.play(FadeOut(multimeter), FadeOut(screen_texts), FadeOut(intro_text))

        # =====================================================
        # PARTE 2: O PASSADO - O MISTÉRIO DO ÂMBAR
        # =====================================================
        
        amber = Circle(radius=1.2, color=ORANGE, fill_opacity=0.8)
        amber_label = Text("O Mistério do Âmbar", font_size=32).next_to(amber, DOWN)
        
        papers = VGroup(*[Rectangle(width=0.2, height=0.1, color=WHITE, fill_opacity=1) for _ in range(5)])
        papers.arrange(RIGHT, buff=0.5).next_to(amber, DOWN, buff=2)
        
        self.play(FadeIn(amber), Write(amber_label))
        self.play(FadeIn(papers))
        
        self.play(
            *[
                p.animate.move_to(amber.get_boundary_point(DOWN) + UP * random.uniform(0, 0.5) + RIGHT * random.uniform(-0.5, 0.5)).rotate(random.uniform(-0.5, 0.5))
                for p in papers
            ],
            run_time=1.5
        )
        
        mystery_text = Text("O que causa essa atração?", font_size=32, color=YELLOW).to_edge(UP)
        self.play(Write(mystery_text))
        self.wait(2)
        
        self.play(FadeOut(amber), FadeOut(amber_label), FadeOut(papers), FadeOut(mystery_text))

        # =====================================================
        # PARTE 3: O ELETROSCÓPIO - DESIGN CORRIGIDO
        # =====================================================
        
        # 1. Desenhando o frasco de vidro
        glass_color = "#a1c9f4"
        flask_lines = VGroup(
            Line(LEFT * 1.5, RIGHT * 1.5), # Base
            Line(LEFT * 1.5, LEFT * 0.6 + UP * 2.5), # Lateral esq
            Line(RIGHT * 1.5, RIGHT * 0.6 + UP * 2.5), # Lateral dir
            Line(LEFT * 0.6 + UP * 2.5, LEFT * 0.6 + UP * 3.2), # Pescoço esq
            Line(RIGHT * 0.6 + UP * 2.5, RIGHT * 0.6 + UP * 3.2), # Pescoço dir
            Line(LEFT * 0.7 + UP * 3.2, RIGHT * 0.7 + UP * 3.2) # Borda superior
        ).set_color(glass_color).set_stroke(width=4, opacity=0.7)
        flask_lines.move_to(ORIGIN)
        
        # 2. Rolha
        stopper = Rectangle(width=1.2, height=0.4, color="#5c4033", fill_opacity=1)
        stopper.move_to(flask_lines[5].get_center() + DOWN * 0.2)
        
        # 3. Haste de metal e Esfera (Altura ajustada para caber no vidro)
        sphere = Circle(radius=0.4, color=LIGHT_GREY, fill_opacity=1)
        stem = Rectangle(width=0.08, height=2.0, color=LIGHT_GREY, fill_opacity=1) # Ajustado
        
        sphere.next_to(stopper, UP, buff=0)
        stem.next_to(sphere, DOWN, buff=0)
        
        # Z-index para a haste parecer passar por dentro da rolha e do vidro
        stem.set_z_index(0)
        stopper.set_z_index(1)
        flask_lines.set_z_index(2)
        sphere.set_z_index(3)
        
        # 4. Folhas de Ouro (Proporções menores para não vazar o fundo)
        pivot_point = stem.get_bottom()
        leaf_l = Rectangle(width=0.1, height=0.8, color="#FFD700", fill_opacity=1) # Ajustado
        leaf_r = Rectangle(width=0.1, height=0.8, color="#FFD700", fill_opacity=1) # Ajustado
        
        leaf_l.move_to(pivot_point + DOWN * 0.4 + LEFT * 0.05).set_z_index(1)
        leaf_r.move_to(pivot_point + DOWN * 0.4 + RIGHT * 0.05).set_z_index(1)
        
        electroscope = VGroup(flask_lines, stopper, stem, sphere, leaf_l, leaf_r)
        electroscope.shift(DOWN * 1.5 + RIGHT * 2)
        
        title_electroscope = Text("Eletroscópio de Folhas", font_size=36, color=WHITE).to_edge(UP)
        desc_electroscope = Text("Detecta eletricidade por repulsão", font_size=28, color=BLUE_B).next_to(title_electroscope, DOWN)
        
        self.play(Write(title_electroscope), FadeIn(desc_electroscope))
        self.play(Create(flask_lines), FadeIn(stopper), run_time=1)
        self.play(FadeIn(stem), FadeIn(sphere), FadeIn(leaf_l), FadeIn(leaf_r))
        self.wait(1)
        
        # =====================================================
        # PARTE 4: A POLARIZAÇÃO E ROTAÇÃO
        # =====================================================
        
        rod = RoundedRectangle(width=0.4, height=2.5, corner_radius=0.1, color=RED, fill_opacity=0.8)
        rod.rotate(PI/4).move_to(sphere.get_center() + LEFT * 3 + UP * 2)
        rod_signs = VGroup(*[Text("-", font_size=24, color=WHITE).move_to(rod.point_from_proportion(i/5)) for i in range(1, 5)])
        charged_rod = VGroup(rod, rod_signs)

        self.play(FadeIn(charged_rod))
        self.play(charged_rod.animate.next_to(sphere, LEFT, buff=0.2), run_time=1.5)
        
        polarization_text = Text("Elétrons fogem para o fundo!", font_size=26, color=YELLOW).next_to(electroscope, LEFT, buff=1)
        self.play(Write(polarization_text))
        
        actual_pivot = stem.get_bottom()
        actual_sphere_center = sphere.get_center()
        
        pos_charges = VGroup(*[Text("+", font_size=28, color="#FF4444").move_to(actual_sphere_center + UP*random.uniform(-0.2,0.2) + RIGHT*random.uniform(-0.2,0.2)) for _ in range(6)])
        neg_charges = VGroup(*[Text("-", font_size=32, color="#4444FF").move_to(actual_sphere_center) for _ in range(6)])
        
        self.play(FadeIn(pos_charges), FadeIn(neg_charges))
        
        down_animations = []
        for charge in neg_charges:
            # Posição de destino ajustada para caber na nova folha
            target = actual_pivot + DOWN * random.uniform(0.1, 0.7)
            down_animations.append(charge.animate.move_to(target))
            
        self.play(*down_animations, run_time=1.5)
        
        leaf_angle = PI/6
        self.play(
            Rotate(leaf_l, angle=leaf_angle, about_point=actual_pivot),
            Rotate(leaf_r, angle=-leaf_angle, about_point=actual_pivot),
            neg_charges.animate.scale(1.5).shift(DOWN*0.1),
            run_time=1
        )
        
        self.wait(1)
        self.play(FadeOut(polarization_text))
        
        conclusion = VGroup(
            Text('"Existe carga elétrica aqui!"', font_size=30, color=YELLOW),
            Text('(Mas o aparelho não dava números...)', font_size=30, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT)
        conclusion.move_to(LEFT * 3)
        
        self.play(Write(conclusion))
        self.wait(4)
        
        # Fim da cena
        self.play(*[FadeOut(mob) for mob in self.mobjects])