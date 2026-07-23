from manim import *

class EletronicaAnimadaIntro(Scene):
    def construct(self):
        # Cor de fundo elegante e moderna
        self.camera.background_color = "#0B0F19"

        # =========================
        # 1. ENTRADA DO TÍTULO
        # =========================
        titulo = Text("Eletrônica Animada", font_size=55, weight=BOLD)
        # Degradê de cor no título
        titulo.set_color_by_gradient(GREEN_C, TEAL_C) 
        
        subtitulo = Text("Circuitos ganhando vida", font_size=28, color=LIGHT_GREY)
        subtitulo.next_to(titulo, DOWN, buff=0.3)

        self.play(Write(titulo), run_time=1.5)
        self.play(FadeIn(subtitulo, shift=UP), run_time=1)
        self.wait(1.5)

        # Recolhe o texto para cima para dar espaço
        self.play(
            FadeOut(subtitulo),
            titulo.animate.scale(0.6).to_edge(UP).set_opacity(0),
            run_time=1
        )

        # =========================
        # 2. CRIANDO A TRILHA DE PCB (Placa de Circuito)
        # =========================
        # Coordenadas com ângulos de PCB (45 graus e retas)
        pontos_trilha = [
            [-5, 0.5, 0],
            [-3, 0.5, 0],
            [-2, 1.5, 0],
            [1, 1.5, 0],
            [2, 0.5, 0],
            [4, 0.5, 0]
        ]
        
        caminho_pcb = VMobject(color=GREEN_C, stroke_width=6)
        caminho_pcb.set_points_as_corners(pontos_trilha)

        # Função para criar "Pads" de solda realistas
        def criar_pad(pos):
            pad = VGroup(
                Circle(radius=0.2, color=GREEN_C, fill_opacity=1),
                Circle(radius=0.08, color="#0B0F19", fill_opacity=1, stroke_width=0)
            )
            return pad.move_to(pos)

        pad_inicio = criar_pad(pontos_trilha[0])
        pad_fim = criar_pad(pontos_trilha[-1])

        circuito = VGroup(pad_inicio, caminho_pcb, pad_fim)
        circuito.shift(UP * 0.5) # Ajusta posição na tela

        # Anima a criação do circuito
        self.play(FadeIn(pad_inicio, scale=0.5))
        self.play(Create(caminho_pcb), run_time=1.5)
        self.play(FadeIn(pad_fim, scale=0.5))
        self.wait(0.5)

        # =========================
        # 3. ELÉTRON COM EFEITO "GLOW"
        # =========================
        eletron_core = Dot(color=WHITE, radius=0.08)
        eletron_glow = Dot(color=YELLOW, radius=0.25, fill_opacity=0.4)
        eletron = VGroup(eletron_glow, eletron_core)
        
        # Posição inicial no pad de entrada
        eletron.move_to(pontos_trilha[0] + UP * 0.5)

        self.play(FadeIn(eletron, scale=0))

        # Percorrer o caminho
        self.play(
            MoveAlongPath(eletron, caminho_pcb),
            run_time=2.5)
        
        # Explosãozinha quando chega no final
        brilho_fim = Flash(eletron, color=YELLOW_A, line_length=0.3, num_lines=8)
        self.play(brilho_fim, FadeOut(eletron, scale=2), run_time=0.5)

        # =========================
        # 4. ONDA SENOIDAL DINÂMICA E ENCERRAMENTO
        # =========================
        # Tracker para animar a fase da onda continuamente
        fase_onda = ValueTracker(0)

        # Cria a onda que se desenha com base no valor de fase_onda
        onda = always_redraw(lambda: FunctionGraph(
            lambda x: 0.6 * np.sin(3 * x + fase_onda.get_value()),
            x_range=[-5, 5],
            color=YELLOW
        ).shift(DOWN * 1.2))

        self.play(Create(onda), run_time=1.5)
        
        # Faz a onda oscilar e o título voltar simultaneamente
        slogan_final = Text("Aprenda • Construa • Entenda", font_size=30, color=WHITE)
        slogan_final.shift(DOWN * 2.8)

        self.play(
            fase_onda.animate.set_value(2 * PI), # Anima a onda
            FadeIn(slogan_final, shift=UP),
            titulo.animate.set_opacity(1).scale(1/0.6), # Retorna o título ao tamanho normal
            run_time=3
        )

        self.wait(2)

        # Transição de saída suave
        self.play(FadeOut(Group(*self.mobjects)))