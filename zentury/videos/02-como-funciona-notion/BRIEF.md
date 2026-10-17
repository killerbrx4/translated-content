# ZENTURY 02 — "Como funciona" (estilo Notion)

## Briefing de diretor
- **Duração:** 22,4 s · **Formato:** 9:16, 1080×1920, 30 fps · **Canal:** Instagram Reels (assiste mudo primeiro)
- **Promessa em uma frase:** a ZENTURY organiza o tráfego pago da sua empresa como um plano claro, passo a passo, e você só acompanha.
- **Público:** dono de empresa que ainda não usa (ou usa mal) tráfego pago.
- **Estilo de referência nomeado:** "Notion product film": página branca, tipografia serifada editorial, blocos, comando "/", quadro kanban, toggles e callout, cursor real, uma coisa se move por vez.
- **Marca:** logo vetorizado de `zentury/brand/logo/` (a partir das variações enviadas), preto `#0B0B0C`, dourado `#D4A842` como único destaque, fundo branco-papel.
- **Nada inventado:** nenhum número ou resultado na tela, só o processo.
- **CTA:** perfil `@zentury` (**handle a confirmar**: está em `CONFIG.handle` no topo do script).

## Lista de estados na grade de batidas (100 BPM · batida 0,6 s · compasso 2,4 s)

| # | Tempo | Compasso | Estado na tela | Transição | Som |
| --- | --- | --- | --- | --- | --- |
| 1 | 0,0–2,4 | 1 | Página em branco; o título é digitado: "Sua empresa é ótima." e abaixo, em cinza, "Mas ninguém te encontra." | — | pad suave + tecla por letra |
| 2 | 2,4–3,6 | 2 | Digita "/", abre o menu de blocos, a seleção desce até "Tráfego pago (ZENTURY)" | Enter em 3,55 | tecla, pop, tick |
| 3 | 3,6–4,8 | 2 | O texto sobe e some; a capa preta com o Z dourado desce; o ícone Z entra; título "Como a ZENTURY faz sua empresa aparecer" | elemento compartilhado: o item do menu vira a página | whoosh + thump |
| 4 | 4,8–7,2 | 3 (**drop**) | Quadro "Plano de crescimento": 4 colunas; o card "Sua empresa" nasce em **Diagnóstico**; ☑ "Entender quem é o seu cliente ideal" | — | batida entra; click; check |
| 5 | 7,2–9,6 | 4 | Cursor arrasta o card para **Estratégia**; câmera acompanha; ☑ "Oferta e mensagem certas" | arraste + pan | pick, drop, check |
| 6 | 9,6–12,0 | 5 | Arrasta para **Anúncios no ar**; ☑ "Anúncios no Instagram e no Google" com os ícones reais | arraste + pan | pick, drop, check |
| 7 | 12,0–14,4 | 6 | Arrasta para **Otimização**; ☑ "Ajustes toda semana, com dados"; câmera afasta e mostra o quadro inteiro | arraste + zoom out | pick, drop, check |
| 8 | 14,4–16,8 | 7 | Toggles "O que muda pra você" abrem um por batida (3 frases) | o quadro sobe | 3 clicks |
| 9 | 16,8–19,2 | 8 | Callout preto com o Z dourado: "A ZENTURY cuida de tudo isso pra você." | callout cai | chime |
| 10 | 19,2–22,4 | 9 | Cartão do perfil @zentury; cursor clica em **Seguir** → **Seguindo ✓**; "Siga o perfil" | — | click + success; acorde final |

## Plano de som
Trilha e efeitos **sintetizados em código** (`audio.py`, numpy): pad até o drop, kick/hat a 100 BPM a partir de 4,8 s, cada efeito no tempo exato do estado. Loudness final -14 LUFS.

## Reproduzir
```bash
python3 -I src/build.py . src/template.html   # gera index.html (ícones e logo embutidos)
python3 audio.py                               # trilha + SFX sintetizados → assets/audio/mix.wav
npx --yes hyperframes@0.8.139 render --quality delivery --output renders/zentury-02-como-funciona.mp4
```

## Crítica (loop com nota)
| Rodada | Gancho | Legib. | Movimento | Variedade | Composição | Marca | Som | 3 piores problemas corrigidos |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 7 | 5 | 7 | 8 | 4 | 8 | — | código vazando no texto (`class="gold"`); título sobrepondo toggles/perfil; quadro ilegível |
| 2 | 7,5 | 7 | 8 | 8 | 7,5 | 8,5 | 8 | texto após ícones sumindo (SVG mal fechado); card cortado com 4 etapas; gancho fraco → marca-texto dourado em "ninguém" |
| 3 (final) | 8 | 8 | 8 | 8,5 | 8 | 8,5 | 8 | — |

Pendências: confirmar o @ oficial (`CONFIG.handle`); trilha é sintetizada (trocar por faixa licenciada se quiser).
