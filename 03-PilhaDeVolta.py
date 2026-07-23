from manim import *
import numpy as np

class PilhaDeVolta(Scene):
    def construct(self):
        # Fundo da tela
        self.camera.background_color = "#051a2e"

        # =====================================================
        # PARTE 1: INTRODUÇÃO
        # =====================================================
        
        title = Text("1800: A Fonte Contínua", font_size=40, color=WHITE)
        subtitle = Text("A invenção da Pilha de Volta", font_size=30, color=BLUE_B).next_to(title, DOWN)
        
        self.play(Write(title), FadeIn(subtitle))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle))

        # =====================================================
        # PARTE 2: O PROBLEMA (Eletricidade Estática)
        # =====================================================
        
        static_text = Text("Antes: A eletricidade era rápida e incontrolável...", font_size=28, color=WHITE).to_edge(UP)
        
        # Duas esferas simulando um gerador estático
        sphere1 = Circle(radius=0.6, color=LIGHT_GREY, fill_opacity=1).shift(LEFT * 2)
        sphere2 = Circle(radius=0.6, color=LIGHT_GREY, fill_opacity=1).shift(RIGHT * 2)
        
        self.play(Write(static_text), FadeIn(sphere1), FadeIn(sphere2))
        
        # Criando o visual de um raio / faísca (ZigZag)
        spark = VGroup(
            Line(sphere1.get_right(), LEFT*0.5 + UP*0.5),
            Line(LEFT*0.5 + UP*0.5, RIGHT*0.5 + DOWN*0.5),
            Line(RIGHT*0.5 + DOWN*0.5, sphere2.get_left())
        ).set_color(YELLOW).set_stroke(width=6)
        
        # Piscando o raio rapidamente
        self.play(Create(spark), run_time=0.1)
        self.play(FadeOut(spark), run_time=0.1)
        self.play(Create(spark), run_time=0.1)
        self.play(FadeOut(spark), run_time=0.1)
        self.wait(1)
        
        self.play(FadeOut(static_text), FadeOut(sphere1), FadeOut(sphere2))

        # =====================================================
        # PARTE 3: A SOLUÇÃO (Empilhando metais)
        # =====================================================
        
        volta_text = Text("Alessandro Volta empilha diferentes materiais", font_size=28, color=YELLOW).to_edge(UP)
        self.play(Write(volta_text))
        
        # Grupo para guardar toda a pilha
        discs = VGroup()
        
        # Construindo a primeira camada devagar e com rótulos (usando linhas para não sobrepor)
        cu1 = RoundedRectangle(width=2, height=0.2, corner_radius=0.05, color="#c87b3f", fill_opacity=1).move_to(DOWN*2.5)
        cu_label = Text("Cobre", font_size=24, color="#c87b3f").move_to(RIGHT * 3.5 + DOWN * 3.1)
        cu_line = Line(cu_label.get_left(), cu1.get_right(), color="#c87b3f", stroke_width=2)
        self.play(FadeIn(cu1), Write(cu_label), Create(cu_line))
        
        paper1 = RoundedRectangle(width=2.1, height=0.1, corner_radius=0.02, color="#a1c9f4", fill_opacity=0.9).move_to(DOWN*2.35)
        paper_label = Text("Papel com salmoura", font_size=24, color="#a1c9f4").move_to(RIGHT * 3.5 + DOWN * 2.35)
        paper_line = Line(paper_label.get_left(), paper1.get_right(), color="#a1c9f4", stroke_width=2)
        self.play(FadeIn(paper1), Write(paper_label), Create(paper_line))
        
        zn1 = RoundedRectangle(width=2, height=0.2, corner_radius=0.05, color="#8b959e", fill_opacity=1).move_to(DOWN*2.2)
        zn_label = Text("Zinco", font_size=24, color="#8b959e").move_to(RIGHT * 3.5 + DOWN * 1.6)
        zn_line = Line(zn_label.get_left(), zn1.get_right(), color="#8b959e", stroke_width=2)
        self.play(FadeIn(zn1), Write(zn_label), Create(zn_line))
        
        discs.add(cu1, paper1, zn1)
        self.wait(1.5)
        
        # Apagamos os rótulos e as linhas apontadoras para focar na pilha crescendo
        self.play(
            FadeOut(cu_label), FadeOut(cu_line),
            FadeOut(paper_label), FadeOut(paper_line),
            FadeOut(zn_label), FadeOut(zn_line)
        )
        
        # Loop para construir o resto da pilha rapidamente
        stack_y = -2.2 + 0.15 # Inicia logo acima do zinco
        anims = []
        for i in range(5): # Adicionando mais 5 camadas
            cu = RoundedRectangle(width=2, height=0.2, corner_radius=0.05, color="#c87b3f", fill_opacity=1).move_to(UP * stack_y)
            paper = RoundedRectangle(width=2.1, height=0.1, corner_radius=0.02, color="#a1c9f4", fill_opacity=0.9).move_to(UP * (stack_y + 0.15))
            zn = RoundedRectangle(width=2, height=0.2, corner_radius=0.05, color="#8b959e", fill_opacity=1).move_to(UP * (stack_y + 0.3))
            
            discs.add(cu, paper, zn)
            
            # Animações de "cair" de cima para baixo
            anims.append(FadeIn(cu, shift=DOWN*0.5))
            anims.append(FadeIn(paper, shift=DOWN*0.5))
            anims.append(FadeIn(zn, shift=DOWN*0.5))
            stack_y += 0.45
            
        self.play(LaggedStart(*anims, lag_ratio=0.15), run_time=3)
        
        # Adicionando os sinais de polaridade (Zinco é o Negativo no topo, Cobre é Positivo embaixo)
        minus_sign = Text("-", font_size=40, color=WHITE).next_to(discs, UP, buff=0.2)
        plus_sign = Text("+", font_size=32, color=WHITE).next_to(discs, DOWN, buff=0.2)
        self.play(Write(minus_sign), Write(plus_sign))

        # =====================================================
        # PARTE 4: A CORRENTE ELÉTRICA (Fluxo Contínuo)
        # =====================================================
        
        current_text = Text("Nasce o fluxo contínuo: A Corrente Elétrica", font_size=28, color=YELLOW).to_edge(UP)
        self.play(Transform(volta_text, current_text))
        
        # Identificando o polo negativo e positivo
        top_plate = discs[-1]
        bottom_plate = discs[0]
        
        # Fio conectando o topo (negativo) à base (positivo) formando um arco à esquerda
        wire = ArcBetweenPoints(
            top_plate.get_left(), bottom_plate.get_left(), 
            angle=PI, color=GRAY, stroke_width=4
        )
        self.play(Create(wire))
        
        # Criando os elétrons que vão fluir pelo fio
        electrons = VGroup(*[Dot(radius=0.06, color=YELLOW) for _ in range(12)])
        
        # Função mágica do Manim que atualiza a posição dos elétrons a cada frame
        def update_electron(mob, dt):
            mob.prop += dt * 0.35 # Define a velocidade da corrente
            if mob.prop > 1:
                mob.prop -= 1
            mob.move_to(wire.point_from_proportion(mob.prop))
            
        # Distribuindo os elétrons pelo fio de forma homogênea
        for i, e in enumerate(electrons):
            e.prop = i / 12
            e.move_to(wire.point_from_proportion(e.prop))
            e.add_updater(update_electron)
            
        self.play(FadeIn(electrons))
        
        # Deixando a corrente fluir na tela por alguns segundos
        self.wait(5)
        
        # Limpando a cena (IMPORTANTE: Limpar updaters antes de fazer FadeOut)
        for e in electrons:
            e.clear_updaters()
            
        self.play(*[FadeOut(mob) for mob in self.mobjects])