# Desafio: anúncio da Jolie feito com o PhotoCraft (V1)

**Pedido:** "estude o repositório storytold/photocraft, diga o que ele pode fazer e faça um anúncio para a Jolie com tudo que já te mandei. Faça o seu melhor."

## O que o PhotoCraft fez neste anúncio (de verdade, pela CLI compilada aqui)
| Etapa | Comandos PhotoCraft | Resultado |
|---|---|---|
| **Look da marca** | `layer.newAdjustmentLayer.curves` + `vibrance` + `photoFilter` → `file.export.colorLookupTables` | `photocraft/jolie-look.cube`, aplicado com `ffmpeg lut3d` nas filmagens dos **2 vídeos usados** (gravados em lugares e luzes diferentes), que ficam com a mesma cor quente e o roxo do açaí mais vivo |
| **Recorte do produto** | `select.object` (área do pote) → `select.inverse` + `edit.clear` → `image.trim` | açaí puro e açaí montado recortados do fundo de granito |
| **Adesivo** | `layer.layerStyle.stroke` (16 px branco) + `dropShadow` | os "stickers" que aparecem no palco roxo |
| **Pôster em PSD** | `layer.newFillLayer.gradient`, `file.placeEmbedded`, `type.create` (Montserrat), `layer.layerStyle.dropShadow` | `jolie-acai-story.psd` (1080×1920) e `jolie-acai-feed.psd` (1080×1350), **em camadas, editáveis no Photoshop** |

Teste que **não** deu certo e ficou de fora: `select.subject` e `select.object` no sorvete (copo na mão sobre a vitrine). A seleção clássica do PhotoCraft (sem IA) pegou o fundo junto. Por isso o adesivo é só do açaí.

## Vídeo: `renders/jolie-photocraft-v1.mp4`, 17,6 s, 1080×1920, -14,0 LUFS
| Saída | Fala real (dos vídeos enviados) | Tela |
|---|---|---|
| 0,0–1,8 | "Você gosta de sorvete?" (tour) | espiada + "VOCÊ GOSTA DE [SORVETE?]" |
| 1,8–3,2 | "Então é porque você ainda não viu…" (açaí) | 3 cortes na batida: vitrine, bola, coberturas (J-cut: voz de um vídeo sobre imagem do outro) |
| 3,2 | "…nosso **açaí**." | **virada:** flash → palco roxo, "AÇAÍ" gigante e o adesivo do açaí puro (PhotoCraft) |
| 3,8–6,6 | "E o melhor é que você pode **montar** do seu **jeito**." | em "montar" o açaí puro gira e **vira o açaí montado**, com brilhos; "DO SEU JEITO" |
| 6,6–10,0 | "Escolha o seu açaí e seus três acompanhamentos." | filmagem real + contador 1·2·3 preenchendo + "+3 ACOMPANHAMENTOS" |
| 10,0–12,1 | "Então vem montar o seu na Jolie!" | mesa + "VEM MONTAR O SEU!" |
| 12,1–14,7 | — | **pôster do PhotoCraft**: o adesivo cai no lugar |
| 14,7–17,6 | — | CTA: logo + "Toque em [Como chegar]" |

Trilha tropical leve (a mesma linguagem do anúncio do açaí), ducking sob as falas, SFX nos adesivos.

## Entregas extras (peças estáticas)
- `photocraft/jolie-acai-story.psd/.png`: story/Reels capa 1080×1920
- `photocraft/jolie-acai-feed.psd/.png`: post do feed 1080×1350
(arquivos do cliente: fora do Git, entregues na conversa)

## Reproduzir
`./photocraft.sh` (etapas PhotoCraft) → ffmpeg com `lut3d` → `python3 -I src/build.py . && python3 -I audio.py` → render HyperFrames → loudnorm.
