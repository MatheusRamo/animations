from manim import *

class LogoCanal(Scene):
    def construct(self):
        # Cor de fundo solicitada
        self.camera.background_color = "#051a2e"

        # =========================
        # 1. ÍCONE PRINCIPAL (Hexágono)
        # =========================
        # Hexágono central apontando para cima
        hexagono = RegularPolygon(n=6, stroke_width=12).scale(2.2)
        hexagono.rotate(PI / 2) 
        hexagono.set_color_by_gradient("#00FFFF", GREEN_C)

        # Efeito de brilho sutil (glow) atrás do hexágono
        hex_glow = hexagono.copy().set_stroke(width=40, opacity=0.15)
        hex_glow.set_color_by_gradient("#00FFFF", GREEN_C)

        # =========================
        # 2. PULSO ELÉTRICO (Sinal)
        # =========================
        pulso = VMobject(stroke_width=12)
        pulso.set_points_as_corners([
            [-1.5, 0, 0],
            [-0.8, 0, 0],
            [-0.3, 1.0, 0],
            [0.3, -1.0, 0],
            [0.8, 0, 0],
            [1.5, 0, 0]
        ])
        pulso.set_color_by_gradient(WHITE, "#00FFFF")

        # Pontos de conexão (ilhas de solda) nas extremidades do pulso
        ponto_esq = Dot(pulso.get_points()[0], radius=0.15, color=WHITE)
        ponto_dir = Dot(pulso.get_points()[-1], radius=0.15, color="#00FFFF")
        
        # Efeito de elétron brilhando na ponta direita
        brilho_dir = Dot(pulso.get_points()[-1], radius=0.4, color="#00FFFF", fill_opacity=0.3)

        icone_completo = VGroup(hex_glow, hexagono, pulso, ponto_esq, ponto_dir, brilho_dir)
        icone_completo.shift(UP * 0.8) # Sobe um pouco para dar espaço ao texto

        # =========================
        # 3. TEXTO DO CANAL
        # =========================
        texto_eletronica = Text("ELETRÔNICA", font_size=50, weight=BOLD, color=WHITE)
        texto_animada = Text("ANIMADA", font_size=50, weight=BOLD, color="#00FFFF")
        
        # Junta os dois textos com um pequeno espaço entre eles
        nome_canal = VGroup(texto_eletronica, texto_animada).arrange(RIGHT, buff=0.25)
        nome_canal.next_to(icone_completo, DOWN, buff=1)

        # Adiciona tudo à cena estática
        self.add(icone_completo, nome_canal)