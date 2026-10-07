# Capacidades verificadas — HeyGen × HyperFrames

Pesquisa feita em 2026-10-07 no repositório oficial `heygen-com/hyperframes` (skills e CLI v0.8.139, testados neste ambiente) e em fontes públicas sobre o HeyGen. A documentação do HeyGen (developers.heygen.com e heygen.com) estava bloqueada na rede deste ambiente, então os itens do HeyGen marcados (†) vêm de resultados de busca e devem ser conferidos no painel antes de cada produção.

## HyperFrames (verificado no código e na CLI)

- **O que é:** framework open source que transforma HTML, CSS, mídia e animação "seekable" em MP4 determinístico, renderizado frame a frame. Node 22+ e FFmpeg.
- **Contrato da composição:** a raiz tem `data-composition-id`, `data-width`, `data-height` e `data-duration`. Os clips usam `data-start`, `data-duration`, `data-track-index` (só a lane do Studio, não afeta a ordem), `data-media-start` (offset na mídia) e `data-volume`. Há uma única `gsap.timeline({paused:true})`, registrada em `window.__timelines[id]`.
- **Regras que quebram o render se ignoradas:** nada de `Math.random` sem seed, relógio ou rede; não animar `visibility`/`display` de um `.clip`; não dar `transform` em CSS a um elemento que o GSAP anima (use `fromTo`); todo `<audio>` precisa de `id`; nunca usar `crossorigin` em mídia; nunca colocar `<video data-start>` dentro de um wrapper que também tenha `data-start`; não animar `letterSpacing` (dá "pulo" de pixel).
- **Runtimes:** GSAP (padrão), Three.js, Lottie, Anime.js, CSS keyframes, WAAPI, TypeGPU. Perspectiva 3D com CSS (`perspective` + `rotationY`/`z`) resolve a maioria dos cards e telas sem precisar de Three.js.
- **Subcomposições:** `data-composition-src` + `<template>`. O lint recomenda uma subcomposição por cena em projetos grandes.
- **Catálogo:** cerca de 400 blocos e componentes (`npx hyperframes catalog --query "..."`, `npx hyperframes add <nome>`). Exemplos: transições (`transitions-3d`, `whip-pan`, `zoom-through-transition`), lower-thirds, `count-up`, `iphone-device`, `light-leak`, `glitch`, `logo-sting`, `caption-*`, `x-post`, `instagram-follow`. Consulte antes de criar um efeito do zero.
- **CLI:** `init`, `lint`, `check` (lint + layout + motion + contraste WCAG), `snapshot --at`, `preview` (Studio), `render` (`--quality draft|looks|delivery`, `--format mp4|webm|mov|png-sequence`; WebM/MOV com transparência), `transcribe` (Whisper local), `tts`, `remove-background`, `timeline`, `cloud render`, `lambda`.
- **Áudio:** mixer próprio com automação de volume (`data-automation`), "voiceover carve" (ducking por bandas) e cadeia de efeitos. A ferramenta `/media-use` busca BGM/SFX/imagem/ícone/voz no catálogo HeyGen (exige login no `heygen` CLI) e traz uma biblioteca local de 19 SFX (licença Pixabay).
- **Ponte com o HeyGen:** `/media-use` → `resolve --type video` gera um vídeo de avatar HeyGen pela CLI `heygen` (`heygen video create`, tipos `avatar` e `image`). Campos disponíveis: `resolution`, `aspect_ratio`, `remove_background`, `background`, `voice_settings`, `motion_prompt`, `expressiveness`. O esquema atualizado está em `heygen video create --request-schema`.

## HeyGen (†)

- **Avatar IV:** lip-sync fotorrealista, enquadramentos de meio corpo e corpo inteiro, microexpressões e gestos de mão sincronizados com o tempo da fala.
- **Gesture Control (desde jun/2025):** gestos por prompt no Avatar IV. Em **Digital Twins**, os gestos gravados no treino (por exemplo apontar, joinha, acenar) podem ser atribuídos a palavras exatas do roteiro, com preview.
- **Digital Twin:** desde ago/2025 roda no Avatar IV, com "gesture detection" ligada no treino.
- **Fundo transparente:** `output_format: "webm"` em `POST /v3/videos` gera um vídeo com canal alpha. Só funciona com avatar treinado com matting, e não pode ser combinado com o objeto `background`.
- **Limitação que importa para a ZENTURY:** a direção exata de um "apontar" não é garantida em avatares de estoque. Para a coreografia apontar → aparecer, use um **Digital Twin com os gestos gravados** ou a **gravação real** (como no EP.01) e cronometre os elementos pelo transcript.

## Divisão de responsabilidades

| Elemento | Ferramenta |
| --- | --- |
| Rosto, fala, presença humana | Gravação real ou HeyGen |
| Cards 3D, celulares, telas, tipografia cinética, legendas | HyperFrames (HTML/CSS 3D + GSAP) |
| Cenas 3D de verdade (cidade, objetos, partículas volumétricas) | HyperFrames + Three.js |
| Fotos e texturas | `/media-use` (catálogo) ou um gerador de imagem externo, com prompt entregue |
| Música licenciada | `/media-use --type bgm` (catálogo HeyGen) ou biblioteca licenciada |
| Mix final e loudness | HyperFrames (automação) + ffmpeg loudnorm |

## Fontes

- [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) (skills `hyperframes-core`, `hyperframes-cli`, `media-use`, `talking-head-recut`)
- [HeyGen gesture control guide](https://www.heygen.com/blog/heygen-gesture-control-guide)
- [June 2025 product updates — Avatar IV gesture control](https://community.heygen.com/public/resources/june-2025-product-updates-webinar-recap-avatar-iv-gesture-control-product-placement-and-more-2025-07-01)
- [How to create a Digital Twin](https://www.heygen.com/academy/avatars/how-to-create-a-Digital-Twin)
- [Create Transparent Avatar Videos in WebM](https://docs.heygen.com/docs/create-webm-avatar-videos)
