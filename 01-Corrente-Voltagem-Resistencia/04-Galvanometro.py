from manim import *
import numpy as np

class Galvanometro(Scene):
    def construct(self):
        self.camera.background_color = "#051a2e"

        # =====================================================
        # PARTE 1: INTRODUÇÃO
        # =====================================================
        title = Text("1820: O Magnetismo", font_size=40, color=WHITE)
        subtitle = Text("A descoberta de Ørsted e o Galvanômetro", font_size=30, color=BLUE_B).next_to(title, DOWN)
        
        self.play(Write(title), FadeIn(subtitle))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle))

        # =====================================================
        # PARTE 2: A DESCOBERTA DE ØRSTED (FIO RETO)
        # =====================================================
        
        # Bússola com fundo transparente para vermos o fio por baixo
        compass_body = Circle(radius=1.5, color=WHITE, stroke_width=4, fill_opacity=0.1)
        compass_center = Dot(color=WHITE)
        
        # Agulha da bússola (Vermelho pro Norte, Branco pro Sul)
        needle_n = Polygon(ORIGIN, LEFT*0.1 + UP*0.2, UP*1.2, RIGHT*0.1 + UP*0.2, color=RED, fill_opacity=1)
        needle_s = Polygon(ORIGIN, LEFT*0.1 + DOWN*0.2, DOWN*1.2, RIGHT*0.1 + DOWN*0.2, color=WHITE, fill_opacity=1)
        needle = VGroup(needle_n, needle_s)
        
        compass = VGroup(compass_body, compass_center, needle)
        compass.shift(DOWN * 1)
        
        # Fio Reto (Passa por trás/baixo da bússola)
        straight_wire = Line(LEFT*6, RIGHT*6, color=DARK_GRAY, stroke_width=8).shift(DOWN * 1)
        
        # DEFININDO AS CAMADAS (O Segredo para a clareza)
        straight_wire.set_z_index(0)    # Fio fica no fundo
        compass_body.set_z_index(1)     # Vidro da bússola
        needle.set_z_index(2)           # Agulha acima de tudo
        compass_center.set_z_index(3)
        
        self.play(Create(straight_wire))
        self.play(FadeIn(compass_body), FadeIn(compass_center), Create(needle))
        
        desc_text = Text("Um fio com corrente desvia a agulha", font_size=30, color=YELLOW).to_edge(UP)
        self.play(Write(desc_text))
        self.wait(1)
        
        # Criando Elétrons (Corrente) - Ficam no z_index 0 junto com o fio
        electrons_straight = VGroup(*[Dot(radius=0.08, color=YELLOW).set_z_index(0) for _ in range(10)])
        for i, e in enumerate(electrons_straight):
            e.move_to(straight_wire.point_from_proportion(i / 10))
            
        def update_straight_current(mob, dt):
            for e in mob:
                x = e.get_x() + dt * 4
                if x > 6:
                    x = -6
                e.move_to(np.array([x, straight_wire.get_y(), 0]))
                
        # Ligando a corrente
        self.play(FadeIn(electrons_straight))
        electrons_straight.add_updater(update_straight_current)
        
        # A agulha desvia devido ao campo magnético
        self.play(Rotate(needle, angle=-PI/4, about_point=compass_center.get_center()), run_time=1.5)
        self.wait(2)
        
        # Desligando a corrente
        electrons_straight.clear_updaters()
        self.play(FadeOut(electrons_straight))
        self.play(Rotate(needle, angle=PI/4, about_point=compass_center.get_center()), run_time=1)

        # =====================================================
        # PARTE 3: O GALVANÔMETRO (A BOBINA EXTERNA)
        # =====================================================
        
        desc_text_2 = Text("Enrolando o fio, o efeito magnético se multiplica!", font_size=30, color=YELLOW).to_edge(UP)
        self.play(Transform(desc_text, desc_text_2))
        
        # Desenhando a bobina (como um anel EM VOLTA da bússola para não cobrir a agulha)
        coil = VGroup(
            Circle(radius=1.70, color=GRAY, stroke_width=4),
            Circle(radius=1.75, color=GRAY, stroke_width=4),
            Circle(radius=1.80, color=GRAY, stroke_width=4)
        ).shift(DOWN * 1).set_z_index(0)
            
        self.play(Transform(straight_wire, coil))
        self.wait(1)

        # =====================================================
        # PARTE 4: A ESCALA DE MEDIÇÃO
        # =====================================================
        
        desc_text_3 = Text("Nasce o Galvanômetro: O Medidor de Corrente", font_size=30, color=WHITE).to_edge(UP)
        self.play(Transform(desc_text, desc_text_3))
        
        # Escala Graduada (Fica na borda interna da bússola)
        scale_arc = Arc(radius=1.2, start_angle=PI/4, angle=PI/2, arc_center=compass_center.get_center(), color=WHITE)
        ticks = VGroup()
        for i in range(9):
            angle = PI/4 + i * (PI/16)
            tick_start = compass_center.get_center() + np.array([1.1 * np.cos(angle), 1.1 * np.sin(angle), 0])
            tick_end = compass_center.get_center() + np.array([1.3 * np.cos(angle), 1.3 * np.sin(angle), 0])
            ticks.add(Line(tick_start, tick_end, color=WHITE, stroke_width=2))
            
        scale = VGroup(scale_arc, ticks).set_z_index(1)
        self.play(FadeIn(scale))
        self.wait(1)

        # =====================================================
        # PARTE 5: COMPARANDO CORRENTES
        # =====================================================
        
        # Cenário A: Corrente Pequena
        label_small = Text("Corrente Pequena", font_size=24, color=BLUE_B).next_to(coil, DOWN, buff=0.5)
        self.play(Write(label_small))
        
        # Elétrons lentos rodando na bobina circular
        electrons_coil = VGroup(*[Dot(radius=0.06, color=YELLOW).set_z_index(0) for _ in range(12)])
        
        def update_coil_current_slow(mob, dt):
            for e in mob:
                e.prop = (e.prop + dt * 0.2) % 1.0 # Velocidade lenta
                e.move_to(coil[1].point_from_proportion(e.prop)) # Roda no círculo do meio

        for i, e in enumerate(electrons_coil):
            e.prop = i / 12
            e.move_to(coil[1].point_from_proportion(e.prop))
            
        electrons_coil.add_updater(update_coil_current_slow)
        self.play(FadeIn(electrons_coil))
        
        # Pequeno desvio (ex: 30 graus)
        self.play(Rotate(needle, angle=-PI/6, about_point=compass_center.get_center()), run_time=1.5)
        self.wait(2)
        
        # Cenário B: Corrente Grande
        label_large = Text("Corrente Grande", font_size=24, color="#FF4444").next_to(coil, DOWN, buff=0.5)
        self.play(Transform(label_small, label_large))
        
        electrons_coil.clear_updaters()
        
        # Mais elétrons e mais rápidos
        electrons_coil_fast = VGroup(*[Dot(radius=0.08, color=YELLOW).set_z_index(0) for _ in range(30)])
        def update_coil_current_fast(mob, dt):
            for i, e in enumerate(mob):
                e.prop = (e.prop + dt * 0.8) % 1.0 # Velocidade rápida
                # Distribui os elétrons entre os 3 aros da bobina
                e.move_to(coil[i % 3].point_from_proportion(e.prop))

        for i, e in enumerate(electrons_coil_fast):
            e.prop = i / 30
            
        electrons_coil_fast.add_updater(update_coil_current_fast)
        
        self.play(FadeOut(electrons_coil), FadeIn(electrons_coil_fast))
        
        # Grande desvio (ex: 75 graus)
        self.play(Rotate(needle, angle=-PI/3.5, about_point=compass_center.get_center()), run_time=1)
        self.wait(3)

        # Desligando e limpando
        electrons_coil_fast.clear_updaters()
        self.play(*[FadeOut(mob) for mob in self.mobjects])