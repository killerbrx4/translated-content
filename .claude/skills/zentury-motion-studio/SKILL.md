---
name: zentury-motion-studio
description: Estúdio de motion da ZENTURY — o método "o prompt é 10%, o estúdio é 90%" (Felipe Borges / guia Movez Opus 5.5) aplicado a Reels, showreels, vídeos de lançamento e edições sobre gravação real. Use sempre que pedirem para criar, editar, refazer ou melhorar um vídeo, Reels, showreel, motion graphics, vinheta ou lançamento para a ZENTURY ou para uma marca de cliente. Define as 7 peças obrigatórias (regras, marca real, referência, lista de estados na grade de batidas, som na batida, loop de crítica com nota, skill/briefing), a ordem do trabalho e os critérios de entrega.
---

# ZENTURY Motion Studio

> O Claude não gera vídeo: ele escreve um programa (HTML/CSS/JS com tempo determinístico) que vira MP4.
> A qualidade vem das **regras**, da **marca real**, da **referência** e da **revisão**, não de um prompt esperto.

Motor padrão: **HyperFrames** (`/hyperframes`, `/hyperframes-core`, `/hyperframes-cli`), porque já resolve render, áudio, legendas, recorte (`remove-background`) e checagem (`lint`/`check`/`snapshot`). Alternativa bare-metal `window.seek(t)` + Playwright + ffmpeg: `.claude/skills/motion-design/` (Howseen, MIT). Use as técnicas dela (molas, câmera em escala log, floods, motion blur por subframes, áudio por pico) dentro do HyperFrames quando couber.

Leia antes de começar: `zentury/CLAUDE.md` (manual), `zentury/frame.md` (marca), `zentury/docs/biblioteca-motion.md` (momento → técnica), `zentury/docs/referencias-showreels.md`.

## As 7 peças do estúdio (todas obrigatórias, nesta ordem)

### 1. Regras do estúdio
`zentury/CLAUDE.md` + `frame.md` valem para todo vídeo. Proibido ("AI slop"):
- título centralizado sobre gradiente; tudo entrando com fade; `y:30, opacity:0` em tudo;
- **rótulos de canto e molduras decorativas** (marca registrada de vídeo feito por IA; só use se a referência da marca exigir);
- glow em interface, partículas genéricas, gradiente arco-íris, emoji como ícone, lorem ipsum, flips 3D gratuitos;
- texto pequeno demais para celular; movimento linear; frame morto (nada parado > 1 s, exceto o hold final);
- fontes genéricas de IA (Inter, Poppins, Syne, Playfair...) quando a marca tem fonte própria;
- telas, números ou recursos inventados.
Obrigatório: uma cor de destaque, uma fonte display + uma de UI, **uma coisa se move por vez**, algo novo a cada 2–4 s, molas com amortecimento ≥ 0,72 (sem bounce de desenho animado), determinismo total (sem `Math.random` sem seed, sem relógio).

### 2. Marca real
Pasta `brand/` do projeto: logo SVG, paleta (hex exato, amostrado de pixels), fontes (arquivos), **capturas reais** (`npx hyperframes capture <url>` ou Playwright) e `facts.md` (todo número com fonte e data). Sem `facts.md`, nenhum número na tela. Dado ilustrativo leva o rótulo "Exemplo". Logos: `simple-icons` (npm, CC0) ou svgl.app; nunca redesenhar logo.

### 3. Referência
Com vídeo de referência: extrair 1 frame a cada 0,5 s (ou storyboard do YouTube via `yt-dlp --write-info-json` + fragmentos `sb0` quando o download é bloqueado), montar contact sheet, escrever `docs/style_guide.md` (paleta, tipografia, duração dos planos, transições, câmera, textura, entrada/saída de texto) e `docs/shotlist.md`. **Pegar a gramática, nunca o conteúdo nem os logos.** Esperar OK antes do código.

### 4. Lista de estados na grade de batidas
Antes de qualquer HTML: BPM → duração da batida → tabela de estados.

| # | Tempo | Batida | Estado (o que é verdade na tela) | Transição para o próximo | Som |
| --- | --- | --- | --- | --- | --- |

Regras: cada mudança cai numa batida; o **drop da música cai no momento-chave** (revelação, logo, virada); "estado → estado" (transformação contínua, elemento compartilhado) vale mais que corte. Showreel de 15 s de referência: ~102 BPM, ~24 cortes. Com gravação real: os estados também respeitam o transcript palavra a palavra (`CUE` no topo do script).

### 5. Som na batida
Trilha licenciada (Mixkit, catálogo HeyGen via `/media-use`) ou **sintetizada em código** (numpy/ffmpeg: click = seno curto decaindo, pop = seno subindo, thump = seno caindo, whoosh = ruído janelado). Achar o drop pela energia por banda (nunca confiar só no grid automático). Cada SFX posicionado pelo **pico medido**. Voz com ducking da trilha. Loudness final **-14 LUFS** (duas passadas de loudnorm).

### 6. Loop de crítica com nota (juiz ≠ autor)
Antes do render final e depois dele:
```bash
ffmpeg -i out.mp4 -vf "fps=2,scale=270:-1,tile=6x5" -frames:v 1 contact.png   # visão geral
ffmpeg -i out.mp4 -vf "fps=1,scale=360:-1,tile=5x3" -frames:v 1 phone.png     # legibilidade no celular
npx hyperframes snapshot --at <cada estado>                                    # frames exatos
```
Dar nota 1–10 para: **gancho nos 2 primeiros s · legibilidade a 360 px · qualidade do movimento · variedade (novo a cada 2–4 s) · composição · fidelidade à marca/dados · sincronia com o som**. Listar os **3 piores problemas com timestamp**, corrigir, re-renderizar só o trecho, dar nota de novo. **Repetir até tudo ≥ 8.** Quando possível, a crítica é feita por um subagente separado, só leitura, que começa rejeitando. Teste mudo: alguém resume o vídeo numa frase só pelas imagens?

### 7. Briefing de diretor (vídeos > 20 s ou de cliente)
Primeira mensagem, antes do código: duração · formato mestre e derivados (9:16, 1:1, 16:9 do MESMO timeline, recompondo, nunca cortando) · assunto + promessa em uma frase · público · canal · **estilo de referência nomeado** ("Apple bumper", "Linear launch", nunca "premium moderno") · estados com tempo · lista de camadas · plano de som. Depois PARAR e pedir OK.

## Fluxo de trabalho
1. Entradas (perguntar o que falta; senão, defaults ditos em voz alta).
2. Peças 2 e 3 (marca e referência) → `style_guide.md`.
3. Peça 4 (estados na grade) → aprovação.
4. **4 stills** (`hyperframes snapshot`) → olhar → corrigir.
5. Composição HyperFrames → `lint` → `check` (0 erros) → render `draft`.
6. Peça 6 (crítica com nota) até ≥ 8 em tudo.
7. Render `--quality delivery`, verificar duração, resolução, -14 LUFS, contact sheet final.
8. Entregar com legenda verdadeira (sem "feito com um prompt só" se houve iterações).

## Com gravação real do apresentador (padrão ZENTURY)
- Transcrição palavra a palavra + mapa de energia → EDL que corta só o silêncio morto.
- Recorte: `npx hyperframes remove-background` → texto atrás da pessoa, troca de fundo.
- Mão: `python3 -I zentury/tools/track_hands.py <video> <hand_landmarker.task> hands.json` → elementos presos à palma.
- Legenda no peito, nunca sobre a boca, nunca abaixo de y=1600 (UI do Reels).

## Entrega (checklist)
☐ 7 peças feitas ☐ estados aprovados ☐ notas ≥ 8 ☐ 0 erros no `check` ☐ drop no momento-chave ☐ -14 LUFS ☐ nada inventado ☐ legenda verdadeira ☐ versão registrada no BRIEF.md
