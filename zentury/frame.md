---
name: ZENTURY
status: provisório — tipografia aguardando as fontes oficiais da marca
colors:
  background: "#0B0B0C"     # preto matte (fundo único em todas as cenas)
  surface: "#141416"        # cards e painéis
  line: "#2A2A2E"           # bordas e réguas
  on-background: "#F5F3EE"  # branco quente (nunca #FFF puro)
  muted: "#9A968F"          # kickers e texto secundário
  accent: "#D4A842"         # dourado ZENTURY: 1 foco por tela
  accent-on-video: "#E9C977" # dourado mais claro para texto sobre vídeo
  accent-deep: "#8A6A1F"    # bordas douradas
typography:
  display:                  # palavras de impacto (VISIBILIDADE, POR QUÊ?)
    fontFamily: Montserrat  # embutida no renderer; trocar pela fonte oficial
    fontWeight: 900
    textTransform: uppercase
    letterSpacing: -0.03em
  caption:                  # legendas faladas
    fontFamily: Montserrat
    fontWeight: 700
    fontSize: 54px
  label:                    # kickers, metadados, "EP. 02", nomes de plataforma
    fontFamily: JetBrains Mono
    fontWeight: 400
    textTransform: uppercase
    letterSpacing: 0.24em
rounded:
  card: 28px
  chip: 999px
spacing:
  safe-top: 220px           # UI do Instagram
  safe-bottom: 1600px       # nada importante abaixo desta linha
  safe-right: 140px         # botões de curtir/comentar
  gutter: 60px
motion:
  energy: controlada, cinematográfica
  easing:
    entry: "expo.out"       # confiança
    exit: "power2.in"
    impact: "power4.out"    # palavras que batem
    ambient: "sine.inOut"
  duration:
    impact: 0.25
    entrance: 0.5
    luxury: 0.9
  transitions:
    disruption: hard-cut    # virada, revelação, corte para preto
    continuity: match-cut   # do gesto para o elemento
  atmosphere:
    - grain-sutil
    - vinheta
    - réguas-douradas
---

# ZENTURY — frame.md

## Overview
Estratégia, posicionamento e performance falando com empresários que ainda não usam tráfego pago. O tom é de **marca global**: confiante, calmo e editorial. Nada de "guru", e o vídeo não pode parecer anúncio.

## The Frame
- 9:16, 1080×1920. O apresentador ocupa o centro e a metade inferior. O **terço superior** (y 220–720) é o palco dos elementos.
- Legendas no peito (y ≈ 1290–1430), nunca sobre a boca e nunca abaixo de y=1600.
- Um único dourado por tela. O resto é preto, branco quente e cinza.

## Composition Rules
1. Todo elemento nasce de um gesto, de um olhar ou de uma palavra (regra Humano + Design).
2. Hard cut quer dizer "acorda": use na virada e no final. Crossfade quer dizer "continua": use pouco.
3. Cada cena passa por construção (0–30%), respiração (30–70%) e resolução (70–100%). As saídas são mais rápidas que as entradas.
4. Varie as eases e as direções de entrada. Nunca entre tudo com `y:30, opacity:0`.
5. Nada de gradiente linear de tela inteira sobre o preto (ele cria faixas no H.264). Use radial ou cor sólida.

## Do
- Cards de vidro escuro com borda fina, e dourado só no foco.
- Tipografia grande (títulos com 64–150px) e kickers em mono espaçado.
- Silêncio e frame congelado como impacto.

## Don't
- Glow neon, gradiente roxo/azul, texto com gradiente, emoji como ícone.
- Inter, Poppins, Playfair, Syne (fontes genéricas de IA, segundo o guia de tipografia do HyperFrames).
- Mais de 6 elementos na tela ao mesmo tempo, salvo quando a poluição é o próprio argumento (ex.: "B em todo lugar").
