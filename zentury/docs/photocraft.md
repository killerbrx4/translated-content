# PhotoCraft no estúdio ZENTURY (estudado em out/2026)

Repositório: https://github.com/storytold/photocraft (MIT / Apache-2.0, early alpha). É uma reimplementação clean-room do Photoshop em Rust puro, do time ArtCraft. Desktop (macOS/Windows/Linux/FreeBSD) e web (WebAssembly).

## O que ele faz
- **Camadas como no Photoshop:** grupos, máscaras de pixel e vetor, clipping, 27 modos de mesclagem, smart objects com filtros editáveis.
- **16 camadas de ajuste não destrutivas:** Curves, Levels, Vibrance, Hue/Sat, Photo Filter, Selective Color, Gradient Map, Color Lookup (.cube/.3dl/.look) etc. Também Camera Raw (`filter.cameraRaw`).
- **Exporta um LUT `.cube`** a partir das camadas de ajuste (`file.export.colorLookupTables`). Essa é a ponte para vídeo: o "look" criado na foto é aplicado igual em todas as filmagens com `ffmpeg lut3d`.
- **Seleção inteligente local** (sem nuvem): Select Subject, Object Selection, Quick Selection, Select and Mask. Gera **recortes de produto** com alpha.
- **Estilos de camada:** Drop Shadow, Stroke, Outer Glow, Bevel, Gradient Overlay… em qualquer camada, inclusive texto.
- **Texto e vetores:** formas, caneta, operações booleanas, texto editável.
- **Filtros com preview:** blurs (gaussiano, movimento, tilt-shift), sharpen, Reduce Noise, distorções, Lens Flare.
- **PSD de verdade:** abre e salva PSD/PSB em camadas. Entregamos ao cliente um arquivo editável no Photoshop.
- **Feito para agentes:** são 500+ comandos, e tudo que existe no menu é um comando. Funciona headless pela CLI (`photocraft-cli run … --cmd <id> --params <json> --out`), em `batch` sobre uma pasta, e via servidor **MCP** (`photocraft-cli mcp`) e protocolo JSON.

## Limites (honestos)
- Early alpha: ainda não substitui o Photoshop no trabalho profissional diário (está no README do próprio projeto).
- Sem IA generativa (não "cria" imagem nem preenche com IA).
- Vídeo é básico (camadas de vídeo e exportação de sequência PNG/GIF). Animação e motion continuam no HyperFrames.
- Texto depende de fontes instaladas no sistema.

## Como usamos (pipeline)
1. **Look da marca:** Curves + Vibrance + Photo Filter num frame de referência → `file.export.colorLookupTables` → `jolie-look.cube` → `ffmpeg -vf lut3d=jolie-look.cube` em toda a filmagem. Garante consistência entre vídeos gravados em dias e luzes diferentes.
2. **Recortes de produto:** `select.subject` → máscara → PNG com alpha → "stickers" e efeito pop-out no vídeo.
3. **Peças estáticas em PSD:** pôster/feed 1080×1350 e story 1080×1920 em camadas, editáveis pelo cliente.
4. **Lote:** `photocraft-cli batch --actions grade.json --in frames --out graded` para tratar dezenas de frames iguais.
