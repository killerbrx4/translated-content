# ZENTURY EP.01 — "Empresa A vs. Empresa B"

**Formato:** Reels 9:16 · 1080×1920 · 30fps · 26,4s · -13 LUFS
**Fonte:** gravação real do apresentador (WhatsApp, 464×832, 60fps, 31,1s)
**Render:** `renders/zentury-ep01-empresa-a-vs-b.mp4` (fora do Git)

## 1. Conceito criativo
Duas empresas iguais e um único diferencial invisível. O espectador vê a B em todo lugar e a A sozinha, e fica com a pergunta: "eu sou a A?". A resposta (visibilidade/tráfego) **não é dada**. Ela abre o EP.02.

## 2. Hook
"Olha essas duas empresas aqui." O apresentador "segura" uma empresa em cada palma e cada card nasce da mão dele.

## 3. Transcrição (palavra a palavra, corrigida)
| Fonte (s) | Fala |
| --- | --- |
| 0,50–2,05 | Olha essas duas empresas aqui. |
| 3,00–4,40 | Essa daqui é a empresa A. |
| 4,80–6,45 | Essa daqui é a empresa B. |
| 7,10–10,45 | As duas empresas vendem basicamente a mesma coisa, |
| 11,30–13,35 | o mesmo produto e o mesmo preço. |
| 14,00–14,30 | Porém, |
| 15,10–18,05 | essa daqui tem uma diferença dessa daqui. |
| 19,30–21,25 | Essa daqui você já viu, |
| 22,00–24,05 | essa daqui, provavelmente não. |
| 24,90–27,05 | E a pergunta que fica é… por quê? |
| 28,20–30,25 | Isso eu te mostro no próximo vídeo. |

O ASR (Whisper base, local) juntou as frases "empresa A" e "empresa B". A correção veio do mapa de energia do áudio e da leitura dos frames.

## 4. EDL (cortes secos nos silêncios)
| Clip | Fonte | Saída | Câmera |
| --- | --- | --- | --- |
| v1 | 0,42–2,12 | 0,00–1,70 | 1.06 |
| v2 | 2,92–4,48 | 1,70–3,26 | 1.00 |
| v3 | 4,72–6,75 | 3,26–5,29 | 1.00 (pausa mantida) |
| v4 | 7,02–10,55 | 5,29–8,82 | 1.07 |
| v5 | 11,22–13,45 | 8,82–11,05 | 1.00 |
| v6 | 13,92–14,42 | 11,05–11,55 | 1.12 |
| v7 | 15,00–18,15 | 11,55–14,70 | 1.05 |
| freeze | frame 18,12 | 14,70–15,85 | 1.00→1.06 |
| v8 | 19,22–21,35 | 15,85–17,98 | 1.00 |
| v9 | 21,92–24,15 | 17,98–20,21 | 1.07 |
| v10 | 24,82–27,12 | 20,21–22,51 | 1.00→1.32→1.62 (zoom no rosto) |
| preto | — | 22,51–26,40 | voz 28,12–30,35 entra em 23,41 |

## 5. Storyboard

**CENA 01 — Hook** · 0,00–1,70
Fala: "Olha essas duas empresas aqui." · Ação: mãos abertas, palmas para cima · Composição: plano médio, punch-in 1.06, topo escurecido para receber os cards · Texto: legenda no peito, "empresas" em dourado · Câmera: estática · SFX: whoosh curto · Música: drone escuro entra · Ferramenta: HyperFrames

**CENA 02 — Empresa A** · 1,70–3,26
Fala: "Essa daqui é a empresa A." · Ação: o dedo aponta para a palma esquerda (tela) · Elementos 3D: uma faísca dourada nasce na palma (2,30), sobe e vira o card "EMPRESA A" vindo da profundidade (rotY 50→14, escala 0.12→1) · SFX: whoosh + pop · Ferramenta: HyperFrames (CSS 3D + GSAP)

**CENA 03 — Empresa B** · 3,26–5,29
Fala: "Essa daqui é a empresa B." · Ação: aponta para a palma direita · Elementos 3D: mesmo gesto espelhado, card "EMPRESA B" com borda dourada · SFX: whoosh + pop · Pausa de 0,25s mantida

**CENA 04 — Igualdade** · 5,29–11,05
Fala: "As duas empresas vendem basicamente a mesma coisa, o mesmo produto e o mesmo preço." · Os cards flutuam; PRODUTO ✓ entra nos dois em 9,30 e PREÇO ✓ em 10,70 · SFX: dois clicks · Câmera: alterna 1.07/1.00 para esconder o jump cut

**CENA 05 — Virada** · 11,05–14,70
Fala: "Porém, essa daqui tem uma diferença dessa daqui." · Os cards se viram de frente no "Porém"; em "diferença" (13,42) a imagem vai para P&B e escurece, os cards apagam e a música **para** · SFX: glitch sutil

**CENA 06 — Congela** · 14,70–15,85
Frame congelado (zoom lento 1.06) + flash branco de 40ms · Surge um olho em traço dourado e a palavra **VISIBILIDADE**, com uma régua dourada · SFX: bass hit + ping · Silêncio de música

**CENA 07 — B em todo lugar** · 15,85–17,98
Fala: "Essa daqui você já viu." · Cor volta, música volta · Seis "aparições" da B entram em cascata ao redor do rosto (Instagram, Google, Outdoor, Celular, Maps, YouTube) enquanto a A aparece pequena, tracejada e cinza · SFX: pops, clicks e notificação em sequência

**CENA 08 — A invisível** · 17,98–20,21
Fala: "Essa daqui… provavelmente não." · As aparições da B desfocam e somem; a A ganha foco por um instante e depois apaga

**CENA 09 — Pergunta** · 20,21–22,51
Fala: "E a pergunta que fica é… por quê?" · Câmera aproxima lentamente no rosto (1.00→1.32) e dá um snap 1.62 no "por quê" · SFX: riser · Legenda some antes do snap para não cobrir a boca

**CENA 10 — Corte seco** · 22,51–26,40
Tela preta: **POR QUÊ?** (o "?" dourado pulsa) com bass hit · A voz continua no preto (J-cut): "Isso eu te mostro no próximo vídeo." · "EP. 02 · EM BREVE" · ZENTURY com régua dourada · SFX: impact final

## 6. Direção do apresentador (para as próximas gravações)
- Gravar em 1080p ou 4K (a câmera do celular direto, **não** o vídeo enviado pelo WhatsApp, que chega com 464×832).
- Fundo mais escuro ou parede neutra, luz principal a 45° e contraluz leve; evitar luminária no quadro.
- Manter os gestos na altura do peito, com pausa de 0,3s no ápice do gesto. É nesse quadro que o elemento nasce.
- Uma frase por respiração, com 0,5s de silêncio entre frases (facilita a EDL).
- O roteiro foi seguido com pequenas variações ("Isso eu te mostro no próximo vídeo" no lugar de "A gente vai descobrir"). Funcionou e foi mantido.

## 7. Sound design e trilha
- Voz: highpass 80Hz, compressor 3:1, loudnorm -14 LUFS.
- Trilha: **placeholder** sintetizado (drone em Lá + pulso grave), em `assets/audio/bed.m4a`. Para publicar, troque por uma faixa licenciada (`npx hyperframes media-use resolve --type bgm --intent "dark minimal corporate tension pulse"`), mantendo os mesmos cortes: para em 13,45 e volta em 15,85.
- SFX: biblioteca local do HyperFrames (licença Pixabay, ver `assets/sfx/CREDITS.md`).

## 8. Ferramentas usadas
ffmpeg (pré-tratamento, espelhamento, grade, loudnorm), Whisper base ONNX local (transcrição), HyperFrames 0.8.139 (composição, lint/check/snapshot/render). HeyGen não foi usado: o apresentador é real.

## 9. Auditoria de qualidade
| Item | Status |
| --- | --- |
| Hook | ✓ gesto + promessa de comparação em 1,7s |
| Curiosidade | ✓ "tem uma diferença" sem revelar o quê |
| Retenção | ✓ uma mudança visual a cada 1,5–2,5s, congelamento no meio |
| Narrativa | ✓ igualdade → diferença → pergunta → cliffhanger |
| Visual premium | ✓ preto, branco e dourado, cards de vidro escuro, sem glow excessivo |
| Movimento com propósito | ✓ cada elemento nasce de um gesto ou de uma palavra |
| 3D | ✓ cards emergem da profundidade a partir da palma |
| Apresentador natural | ✓ gravação real; jump cuts escondidos com punch-in |
| Voz | ✓ -13 LUFS integrado |
| Marca | ✓ ZENTURY só na assinatura final |
| Conversão | ✓ cria a pergunta, deixa a resposta para o EP.02 |
| Limitações | ⚠ fonte em 464×832 (upscale perde nitidez); trilha é placeholder |

## 10. Reproduzir
```bash
cd zentury/videos/01-empresa-a-vs-b
# coloque assets/footage/presenter.mp4, assets/audio/voice.m4a e assets/img/freeze.jpg (ver pré-tratamento no CLAUDE.md)
npx --yes hyperframes@0.8.139 check
npx --yes hyperframes@0.8.139 preview
npm run render
```
