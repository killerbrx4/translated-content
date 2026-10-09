# Biblioteca de Motion ZENTURY

Mapa de cada momento narrativo para a técnica pronta do HyperFrames: os blueprints (formatos de cena já testados), os blocos do catálogo (`npx hyperframes catalog --query "..."`) e os SFX. Antes de desenhar um efeito do zero, procure aqui.

## Momento narrativo → técnica

| Momento ZENTURY | Blueprint HyperFrames | Blocos do catálogo | Som |
| --- | --- | --- | --- |
| **Hook com pergunta** ("Por que a sua empresa…?") | `kinetic-type-beats` (palavras trocando no lugar) | `headline-slam`, `kinetic-type-swap`, `char-slam-explode` | bass hit no golpe |
| **Comparação A vs B** | `comparison-split` (dois itens em "livro abrindo" 3D) | `split-tilt-cards`, `before-after-wipe`, `comparison-split` | whoosh por lado |
| **"Você está cercado de concorrentes"** | `overwhelm-surround` (elementos fecham o cerco) | `notification-pileup`, `avatar-cloud`, `radial-surround` | notificações empilhando |
| **"Ela aparece em todo lugar"** | `constellation-hub` (nós orbitando um centro) | `orbit-card`, `three-orbiting-cards`, `social-proof-card` | pops escalonados |
| **Número que choca** ("8 de cada 10…") | `dataviz-countup` | `count-up`, `number-wheel`, `conic-progress-ring`, `apple-money-count` | riser → impacto |
| **Mostrar anúncio / celular** | `device-surface-showcase` | `vfx-iphone-device`, `device-frame-stage`, `scroll-feed`, `ios26-liquid-glass` | click + swipe |
| **Busca no Google** | `prompt-type-submit-generate` | `typed-prompt`, `typewriter`, `streaming-text` | teclado |
| **Virada / congelamento** | — (hard cut + freeze) | `freeze-frame-dressing`, `beat-freeze-cut`, `rack-focus`, `focus-blur-resolve` | silêncio + sub |
| **Revelação de conceito** | `titlecard-reveal` | `glass-shard-title`, `light-sweep-pass`, `svg-mask-reveal` | ping/chime |
| **Câmera dramática** | `camera-journey`, `zoom-out-workspace-reveal` | `cinematic-zoom`, `camera-dolly-zoom`, `push-in`, `pull-back-reveal`, `whip-pan` | whoosh cinematográfico |
| **Lista do que muda** | `grid-card-assemble` | `marker-checklist-card`, `success-check`, `stagger-cascade` | clicks |
| **Assinatura ZENTURY** | `logo-assemble-lockup` | `logo-sting`, `logo-brand-close`, `wordmark-tiles`, `cta-lockup` | impacto + cauda |
| **CTA "comenta A ou B"** | `cta-morph-press` | `instagram-follow`, `badge-pop`, `press-ripple` | pop |
| **Textura premium** | — | `grain-overlay`, `light-leak`, `vfx-anamorphic-flare` (com moderação), `vignette` | — |

## Regras de movimento (do guia de motion do HyperFrames, aplicadas à ZENTURY)

- **Ease é emoção:** `expo.out` transmite confiança (entrada de card), `power4.out` é impacto (palavra que bate), `sine.inOut` é respiração (flutuação). No máximo 2 tweens com a mesma ease por cena.
- **Velocidade é peso:** de 0,15 a 0,3s é urgência, de 0,5 a 0,8s é luxo, de 0,8 a 2s é cinematográfico. A cena mais lenta deve ser 3× mais lenta que a mais rápida.
- **Coreografia é hierarquia:** o que se move primeiro é o mais importante. Escalonamento total abaixo de 500ms.
- **Assimetria:** a entrada leva cerca de 0,4s e a saída cerca de 0,25s.
- **Cada elemento tem um verbo:** BATE, DESLIZA, CONSTRÓI, FLUTUA, TRAVA. Se não dá para nomear o verbo, o elemento ainda não foi desenhado.
- **Escala de vídeo:** títulos com 64–150px, corpo com 28–42px, rótulos com no mínimo 18–24px, bordas de 2–4px e decorativos com 12–25% de opacidade.

## Autocrítica do EP.01 (para aplicar nos próximos)

1. **Tipografia:** usei Inter, que está na lista de fontes genéricas de IA. Do EP.02 em diante, use o `frame.md` (display + mono) ou a fonte oficial da marca.
2. **Cards:** a borda de 1px some depois da compressão do Instagram. Use 2px.
3. **Monotonia de ease:** A e B entram com a mesma ease e a mesma direção. Dá para variar (A em `expo.out`, B em `back.out` com leve atraso).
4. **Textura:** falta grão sutil, e o fundo do apresentador é o ponto fraco. Nas próximas gravações, use fundo escuro de verdade, ou remova o fundo (`npx hyperframes remove-background`, que exige baixar o modelo).
5. **Trilha:** a provisória é sintetizada. Defina uma assinatura sonora fixa da ZENTURY (mesmo impacto e mesma cauda no logo em todo episódio) para criar memória de marca.
