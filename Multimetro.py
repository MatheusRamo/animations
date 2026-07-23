from manim import *
import numpy as np

class Multimetro(MovingCameraScene):
    def construct(self):
        # ==========================================
        # CONFIGURAÇÃO DA CÂMERA E FUNDO
        # ==========================================
        self.camera.background_color = "#051a2e"
        self.camera.frame_width = 16
        self.camera.frame_height = 9

        # Área segura para textos (evita sobreposição)
        SAFE_TOP = 3.8
        SAFE_BOTTOM = -3.8
        SAFE_LEFT = -7
        SAFE_RIGHT = 7

        # ==========================================
        # HELPERS MELHORADOS
        # ==========================================
        def caption(txt, color=WHITE, size=28):
            """Cria legenda na área inferior segura"""
            text = Text(txt, font_size=size, color=color, line_spacing=1.3)
            text.move_to([0, SAFE_BOTTOM + 0.8, 0])
            # Background semi-transparente para legibilidade
            bg = Rectangle(
                width=text.width + 0.6,
                height=text.height + 0.4,
                fill_color="#051a2e",
                fill_opacity=0.85,
                stroke_width=0
            )
            bg.move_to(text.get_center())
            return VGroup(bg, text)

        def info_bubble(txt, color=YELLOW, size=22, pos=UP*2.5):
            """Balão informativo que aparece próximo aos elementos"""
            text = Text(txt, font_size=size, color=color, line_spacing=1.2)
            text.move_to(pos)
            bg = RoundedRectangle(
                width=text.width + 0.5,
                height=text.height + 0.3,
                corner_radius=0.15,
                fill_color="#0a2a4a",
                fill_opacity=0.9,
                stroke_color=color,
                stroke_width=2
            )
            bg.move_to(text.get_center())
            return VGroup(bg, text)

        def zigzag(width=1.4, height=0.28, n_peaks=3):
            step = width / (2 * n_peaks)
            pts, x, up = [LEFT * (width / 2)], -width / 2, True
            for _ in range(2 * n_peaks):
                x += step
                pts.append(RIGHT * x + UP * (height if up else -height))
                up = not up
            pts.append(RIGHT * (width / 2))
            return pts

        def make_resistor(width=1.4, color=WHITE):
            body = VMobject(color=color, stroke_width=5).set_points_as_corners(zigzag(width=width))
            # Glow sutil
            glow = VMobject(color=color, stroke_width=12, stroke_opacity=0.2).set_points_as_corners(zigzag(width=width))
            return VGroup(glow, body)

        def make_battery(glow=False):
            plus = Line(UP * 0.5, DOWN * 0.5, color=WHITE, stroke_width=4)
            minus = Line(UP * 0.25, DOWN * 0.25, color=WHITE, stroke_width=10).next_to(plus, RIGHT, buff=0.2)
            group = VGroup(plus, minus)
            if glow:
                glow_plus = Line(UP * 0.5, DOWN * 0.5, color=YELLOW, stroke_width=10, stroke_opacity=0.3)
                glow_minus = Line(UP * 0.25, DOWN * 0.25, color=YELLOW, stroke_width=16, stroke_opacity=0.3).next_to(glow_plus, RIGHT, buff=0.2)
                return VGroup(glow_plus, glow_minus, plus, minus)
            return group

        def make_multimeter(scale=1.0):
            """Corpo esquemático de um multímetro digital com melhorias visuais."""
            body = RoundedRectangle(
                width=3.0 * scale, height=4.2 * scale, corner_radius=0.25 * scale,
                color=GREY_B, fill_color=GREY_E, fill_opacity=1, stroke_width=4
            )
            screen = RoundedRectangle(
                width=2.3 * scale, height=0.9 * scale, corner_radius=0.1 * scale,
                color=GREEN, fill_color=BLACK, fill_opacity=1, stroke_width=3
            )
            screen.move_to(body.get_top() + DOWN * 0.9 * scale)
            display = Text("0.00", font="monospace", color=GREEN, font_size=int(34 * scale)).move_to(screen)

            dial_circle = Circle(radius=0.55 * scale, color=WHITE, stroke_width=3).move_to(body.get_center() + DOWN * 0.2 * scale)

            # Labels com posições melhores
            labels = VGroup(
                Text("V", font_size=int(18 * scale), color=YELLOW).move_to(dial_circle.get_top() + UP * 0.28 * scale),
                Text("A", font_size=int(18 * scale), color=RED).move_to(dial_circle.point_at_angle(-40 * DEGREES) * 1.35 * scale),
                Text("Ω", font_size=int(18 * scale), color=BLUE).move_to(dial_circle.point_at_angle(220 * DEGREES) * 1.35 * scale),
            )
            pointer = Line(
                dial_circle.get_center(),
                dial_circle.get_center() + UP * 0.42 * scale,
                color=WHITE, stroke_width=5
            )

            com_port = Circle(radius=0.12 * scale, color=BLACK, fill_color=BLACK, fill_opacity=1, stroke_color=WHITE)
            v_port = Circle(radius=0.12 * scale, color=RED, fill_color=RED, fill_opacity=1, stroke_color=WHITE)
            ports = VGroup(com_port, v_port).arrange(RIGHT, buff=0.6 * scale)
            ports.move_to(body.get_bottom() + UP * 0.5 * scale)
            com_lbl = Text("COM", font_size=int(14 * scale), color=WHITE).next_to(com_port, DOWN, buff=0.1 * scale)
            v_lbl = Text("VΩmA", font_size=int(14 * scale), color=WHITE).next_to(v_port, DOWN, buff=0.1 * scale)

            # Pontas com pontas de prova visíveis
            probe_len = 2.2 * scale
            black_probe = Line(com_port.get_center(), com_port.get_center() + DOWN * probe_len, color=GREY_A, stroke_width=6)
            red_probe = Line(v_port.get_center(), v_port.get_center() + DOWN * probe_len, color=RED, stroke_width=6)

            # Pontas metálicas
            black_tip = Triangle(color=GREY_A, fill_color=GREY_A, fill_opacity=1).scale(0.12 * scale)
            black_tip.move_to(black_probe.get_end()).rotate(PI)
            red_tip = Triangle(color=RED, fill_color=RED, fill_opacity=1).scale(0.12 * scale)
            red_tip.move_to(red_probe.get_end()).rotate(PI)

            mm = VGroup(body, screen, display, dial_circle, labels, pointer,
                       ports, com_lbl, v_lbl, black_probe, red_probe, black_tip, red_tip)
            mm.display = display
            mm.pointer = pointer
            mm.dial_circle = dial_circle
            mm.black_probe = black_probe
            mm.red_probe = red_probe
            mm.black_tip = black_tip
            mm.red_tip = red_tip
            mm.com_port = com_port
            mm.v_port = v_port
            return mm

        def set_display(mm, text, color=GREEN):
            new_txt = Text(text, font="monospace", color=color, font_size=mm.display.font_size).move_to(mm.display)
            return Transform(mm.display, new_txt)

        def point_dial(mm, angle):
            target = Line(
                mm.dial_circle.get_center(),
                mm.dial_circle.get_center() + 0.42 * np.array([np.cos(angle), np.sin(angle), 0]) * (mm.dial_circle.width / 1.1),
                color=WHITE, stroke_width=5
            )
            return Transform(mm.pointer, target)

        def create_arrow(start, end, color=YELLOW, buff=0.3):
            """Seta animada para indicar direção"""
            arrow = Arrow(start, end, color=color, buff=buff, stroke_width=3, max_tip_length_to_length_ratio=0.15)
            return arrow

        def highlight_zone(target, color=YELLOW, opacity=0.2):
            """Cria um halo de destaque ao redor de um objeto"""
            halo = SurroundingRectangle(target, color=color, buff=0.2, stroke_width=0)
            halo.set_fill(color, opacity=opacity)
            return halo

        # ==========================================
        # TÍTULO INTRODUTÓRIO
        # ==========================================
        title = Text("Como Funciona um", font_size=46, weight=BOLD, color=YELLOW)
        subtitle = Text("Multímetro", font_size=60, weight=BOLD, color=WHITE)
        header = VGroup(title, subtitle).arrange(DOWN, buff=0.25).to_edge(UP, buff=1.2)

        self.play(FadeIn(title, shift=UP * 0.3), Write(subtitle), run_time=1.2)
        self.wait(0.5)
        self.play(header.animate.scale(0.55).to_corner(UP + LEFT, buff=0.4))

        # ==========================================
        # APRESENTAÇÃO DO APARELHO
        # ==========================================
        mm = make_multimeter(scale=1.1).move_to(ORIGIN)

        # Legenda com fundo
        text_intro = caption("Mede Tensão (V), Corrente (A) e Resistência (Ω)")

        self.play(FadeIn(mm, shift=UP * 0.3), run_time=1.2)
        self.play(FadeIn(text_intro[0]), Write(text_intro[1]), run_time=0.8)

        # Destaque nos componentes principais
        self.play(
            Indicate(mm.dial_circle, color=YELLOW, scale_factor=1.15),
            Indicate(mm.display, color=GREEN, scale_factor=1.1),
            run_time=1.0
        )
        self.wait(0.8)
        self.play(FadeOut(text_intro))

        # ==========================================
        # CENA 1: MEDINDO TENSÃO (PARALELO)
        # ==========================================
        self.play(
            mm.animate.scale(0.6).move_to(DOWN * 2.5 + RIGHT * 4.5),
            run_time=1.0
        )

        # Construir circuito na área superior
        bat = make_battery()
        res = make_resistor(width=1.6, color=YELLOW)
        VGroup(bat, res).arrange(RIGHT, buff=1.6)

        wtop = Line(bat.get_center() + UP * 0.9, res.get_center() + UP * 0.9, color=WHITE, stroke_width=4)
        wbot = Line(bat.get_center() + DOWN * 0.9, res.get_center() + DOWN * 0.9, color=WHITE, stroke_width=4)
        left_up = Line(bat.get_top(), wtop.get_start(), color=WHITE, stroke_width=4)
        left_down = Line(bat.get_bottom(), wbot.get_start(), color=WHITE, stroke_width=4)
        right_up = Line(res.get_top(), wtop.get_end(), color=WHITE, stroke_width=4)
        right_down = Line(res.get_bottom(), wbot.get_end(), color=WHITE, stroke_width=4)

        circuito_v = VGroup(bat, res, wtop, wbot, left_up, left_down, right_up, right_down)
        circuito_v.move_to(UP * 2.0).scale(0.9)

        # Labels do circuito
        label_bat = Text("9V", font_size=20, color=YELLOW).next_to(bat, LEFT, buff=0.3)
        label_res = Text("R", font_size=20, color=WHITE).next_to(res, RIGHT, buff=0.3)

        text_v = caption("TENSÃO: pontas em PARALELO com o componente", color=YELLOW)

        # Animação de entrada do circuito
        self.play(
            FadeIn(circuito_v, shift=UP * 0.3),
            FadeIn(label_bat), FadeIn(label_res),
            run_time=1.0
        )
        self.play(FadeIn(text_v[0]), Write(text_v[1]), run_time=0.8)

        # Zoom na área de medição
        self.play(
            self.camera.frame.animate.move_to(res.get_center() + DOWN * 0.5).set_width(8),
            run_time=1.0
        )

        # Mostrar conexão em paralelo com setas indicativas
        node_a = right_up.get_end()
        node_b = right_down.get_end()

        # Linhas de conexão das pontas
        probe_black = Line(mm.black_tip.get_center(), node_b, color=GREY_A, stroke_width=4)
        probe_red = Line(mm.red_tip.get_center(), node_a, color=RED, stroke_width=4)

        # Setas indicando paralelo
        arrow_par1 = create_arrow(res.get_left() + LEFT * 0.5, res.get_left(), color=YELLOW)
        arrow_par2 = create_arrow(res.get_right() + RIGHT * 0.5, res.get_right(), color=YELLOW)

        parallel_text = info_bubble("Mesmos pontos = Mesma tensão", color=YELLOW, size=20, pos=res.get_center() + UP * 1.5)

        self.play(
            Transform(mm.black_probe.copy().clear_updaters(), probe_black),
            Transform(mm.red_probe.copy().clear_updaters(), probe_red),
            FadeIn(arrow_par1), FadeIn(arrow_par2),
            run_time=1.2
        )
        self.play(FadeIn(parallel_text[0]), Write(parallel_text[1]))

        # Atualizar display
        self.play(
            set_display(mm, "9.00V"),
            point_dial(mm, 90 * DEGREES),
            run_time=0.8
        )
        self.wait(1.0)

        # Reset zoom
        self.play(
            self.camera.frame.animate.move_to(ORIGIN).set_width(16),
            FadeOut(arrow_par1), FadeOut(arrow_par2), FadeOut(parallel_text),
            run_time=0.8
        )

        # ==========================================
        # CENA 2: MEDINDO CORRENTE (SÉRIE)
        # ==========================================
        text_a = caption("CORRENTE: circuito é ABERTO e o medidor entra em SÉRIE", color=RED)

        # Preparar corte no circuito
        gap = 0.6
        cut_point = right_up.get_center()
        cut_l = Line(
            right_up.get_start(),
            cut_point + LEFT * gap / 2,
            color=WHITE, stroke_width=4
        )
        cut_r = Line(
            cut_point + RIGHT * gap / 2,
            right_up.get_end(),
            color=WHITE, stroke_width=4
        )

        # Mover multímetro para posição de medição de corrente
        mm_a = mm.copy()

        self.play(
            FadeOut(text_v),
            FadeIn(text_a[0]), Write(text_a[1]),
            run_time=0.8
        )

        # Animar o corte do fio
        self.play(
            Transform(right_up, VGroup(cut_l, cut_r)),
            run_time=0.8
        )

        # Zoom no ponto de corte
        self.play(
            self.camera.frame.animate.move_to(cut_point + UP * 0.5).set_width(6),
            run_time=0.8
        )

        # Mover multímetro para série
        self.play(
            mm_a.animate.move_to(cut_point + UP * 1.2),
            run_time=0.8
        )

        # Conectar em série
        probe_a_black = Line(mm_a.black_tip.get_center(), cut_l.get_end(), color=GREY_A, stroke_width=4)
        probe_a_red = Line(mm_a.red_tip.get_center(), cut_r.get_start(), color=RED, stroke_width=4)

        # Seta indicando fluxo
        flux_arrow = Arrow(
            cut_l.get_end() + UP * 0.3,
            cut_r.get_start() + UP * 0.3,
            color=RED, buff=0.1
        )
        serie_text = info_bubble("Mesmo caminho = Mesma corrente", color=RED, size=20, pos=cut_point + UP * 2.2)

        self.play(
            Transform(mm_a.black_probe.copy().clear_updaters(), probe_a_black),
            Transform(mm_a.red_probe.copy().clear_updaters(), probe_a_red),
            FadeIn(flux_arrow),
            run_time=1.0
        )
        self.play(FadeIn(serie_text[0]), Write(serie_text[1]))

        self.play(
            set_display(mm_a, "0.50A", color=RED),
            point_dial(mm_a, -30 * DEGREES),
            run_time=0.8
        )
        self.wait(1.0)

        # Reset
        self.play(
            self.camera.frame.animate.move_to(ORIGIN).set_width(16),
            FadeOut(flux_arrow), FadeOut(serie_text),
            run_time=0.8
        )

        # ==========================================
        # CENA 3: MEDINDO RESISTÊNCIA
        # ==========================================
        text_r = caption("RESISTÊNCIA: componente FORA do circuito, sem energia!", color=BLUE)

        self.play(
            FadeOut(text_a),
            FadeOut(circuito_v),
            FadeOut(mm_a),
            FadeOut(label_bat), FadeOut(label_res),
            FadeIn(text_r[0]), Write(text_r[1]),
            run_time=1.0
        )

        # Resistor isolado
        res_iso = make_resistor(width=2.2, color=BLUE).move_to(UP * 1.5)
        wl = Line(res_iso.get_left() + LEFT * 1.0, res_iso.get_left(), color=WHITE, stroke_width=4)
        wr = Line(res_iso.get_right(), res_iso.get_right() + RIGHT * 1.0, color=WHITE, stroke_width=4)
        res_setup = VGroup(wl, res_iso, wr)

        # Símbolo de "desligado"
        power_off = Text("⚡ OFF", font_size=24, color=GREY_C).next_to(res_setup, UP, buff=0.5)

        mm_r = mm.copy().scale(0.9).next_to(res_setup, DOWN, buff=1.2)

        self.play(
            FadeIn(res_setup, shift=UP * 0.3),
            FadeIn(power_off),
            FadeIn(mm_r, shift=UP * 0.3),
            run_time=1.0
        )

        # Zoom
        self.play(
            self.camera.frame.animate.move_to(res_setup.get_center()).set_width(8),
            run_time=0.8
        )

        probe_r_black = Line(mm_r.black_tip.get_center(), wl.get_start(), color=GREY_A, stroke_width=4)
        probe_r_red = Line(mm_r.red_tip.get_center(), wr.get_end(), color=RED, stroke_width=4)

        # Destaque no resistor
        halo = highlight_zone(res_iso, color=BLUE, opacity=0.15)

        self.play(
            Transform(mm_r.black_probe.copy().clear_updaters(), probe_r_black),
            Transform(mm_r.red_probe.copy().clear_updaters(), probe_r_red),
            FadeIn(halo),
            run_time=1.0
        )

        self.play(
            set_display(mm_r, "220Ω", color=BLUE),
            point_dial(mm_r, 210 * DEGREES),
            Indicate(res_iso, color=BLUE, scale_factor=1.1),
            run_time=0.8
        )
        self.wait(1.0)

        # ==========================================
        # RESUMO FINAL
        # ==========================================
        self.play(
            self.camera.frame.animate.move_to(ORIGIN).set_width(16),
            FadeOut(res_setup), FadeOut(mm_r), FadeOut(text_r),
            FadeOut(power_off), FadeOut(halo),
            run_time=1.0
        )

        resumo_title = Text("Resumindo:", font_size=42, weight=BOLD, color=YELLOW).move_to(UP * 3.5)

        # Cards de resumo
        card_v = RoundedRectangle(width=6, height=1.2, corner_radius=0.2, fill_color="#1a1a2e", fill_opacity=1, stroke_color=YELLOW, stroke_width=2)
        card_v.move_to(UP * 1.5)
        item_v = Text("V  →  Paralelo com o componente", font_size=28, color=YELLOW).move_to(card_v)

        card_a = RoundedRectangle(width=6, height=1.2, corner_radius=0.2, fill_color="#1a1a2e", fill_opacity=1, stroke_color=RED, stroke_width=2)
        card_a.move_to(ORIGIN)
        item_a = Text("A  →  Em série, circuito interrompido", font_size=28, color=RED).move_to(card_a)

        card_o = RoundedRectangle(width=6, height=1.2, corner_radius=0.2, fill_color="#1a1a2e", fill_opacity=1, stroke_color=BLUE, stroke_width=2)
        card_o.move_to(DOWN * 1.5)
        item_o = Text("Ω  →  Componente sem energia", font_size=28, color=BLUE).move_to(card_o)

        self.play(Write(resumo_title))
        self.play(
            FadeIn(card_v), Write(item_v),
            run_time=0.6
        )
        self.play(
            FadeIn(card_a), Write(item_a),
            run_time=0.6
        )
        self.play(
            FadeIn(card_o), Write(item_o),
            run_time=0.6
        )

        # Pulso final nos cards
        self.play(
            card_v.animate.set_stroke(width=4),
            card_a.animate.set_stroke(width=4),
            card_o.animate.set_stroke(width=4),
            run_time=0.5
        )
        self.play(
            card_v.animate.set_stroke(width=2),
            card_a.animate.set_stroke(width=2),
            card_o.animate.set_stroke(width=2),
            run_time=0.5
        )

        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)