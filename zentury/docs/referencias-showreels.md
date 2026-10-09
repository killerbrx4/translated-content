# Referências — 4 showreels analisados (out/2026)

**Fonte da análise:** os storyboards do YouTube, aproximadamente 1 frame por segundo e em baixa resolução, mais os metadados. O YouTube bloqueia o download do vídeo completo vindo de servidor na nuvem, então **não ouvi o áudio** e não vi a fluidez exata dos movimentos. Para estudar ritmo e som, use a gravação de tela.

| # | Vídeo | Autor | Duração | Estilo dominante |
| --- | --- | --- | --- | --- |
| 1 | Video Editor Showreel 2025 | J's Cuts (`mhCpZMwM9Xg`) | 53s | Tipografia cinética sobre footage, desfoque de movimento, cartelas de categoria |
| 2 | Video Editor Showreel 2025 | rystal (`Y9LYuqb4uYA`) | 30s | UI escura minimalista, números de prova social, ícones 3D, setas desenhadas à mão |
| 3 | 3D artist – Blender Showreel 2025 | Aurelien Thomas (`d09twkNJSOM`) | 65s | Tipografia 3D em material, renders de produto, campos de cor dominantes |
| 4 | Motion Design Showreel 2025 | Bohdan Martovskyi (`hszNZTElIzE`) | 35s | Moldura editorial com metadados nos cantos, chips, cursor, palavras em volta da pessoa, parede de logos |

## O que cada um ensina

### 1. J's Cuts — a frase que se constrói em cortes
- O texto conduz o vídeo como uma **frase dividida em telas**: "LOOKING FOR" → "VIDEO EDITOR" → "EASY TO UNDERSTAND" → "TAILORED FOR ALL PLATFORMS" → "HOOK YOUR AUDIENCE" → "THROUGH storytelling". Cada tela traz uma ideia, e o espectador lê a frase inteira sem perceber.
- Título com **textura metálica/cromada**, em caixa alta e condensado.
- **Transições com desfoque de movimento e whip pan**: cada corte "puxa" para o próximo.
- **Cartelas de categoria** ("TALKING HEAD", "MUSIC", "SPORTS", "PROMO", "PODCAST") sobre o footage do tema.
- **Recortes diagonais (vidro quebrado)** com silhuetas em cada fatia.
- Fecha com o logo em desfoque e o contato.

### 2. rystal — provas com números e ícones (o mais útil para a ZENTURY)
- Fundo **cinza-grafite único** do começo ao fim, com wordmark branco em minúsculas e um brilho suave.
- **A linha do tempo de edição vira um túnel 3D**: o "bastidor" do trabalho virou espetáculo.
- **Números gigantes como prova**: "914k views" → "1.4M views" → "**10M+ views generated**", com prints de comentários e da interface **desfocados atrás**.
- **Ícones 3D brilhantes** das ferramentas (DaVinci, Premiere, Photoshop) surgindo com selos curtos ("4+ years").
- **Setas e linhas desenhadas à mão, em branco**, ligando rótulos ("CUTTING", "MOTION GRAPHICS", "AUDIO DESIGN", "3D ANIMATION") às telas inclinadas em 3D.

### 3. Aurelien Thomas — material e cor
- Abertura com **tipografia 3D em material** (laranja derretido e metálico), com a câmera passando por dentro das letras.
- **Uma cor dominante por cena** (laranja, azul-petróleo, branco). A troca de cor marca a troca de assunto.
- Produto sempre **sozinho, com luz de estúdio** e muito espaço vazio. Close extremo (olho) como respiro.

### 4. Bohdan Martovskyi — acabamento editorial
- **Moldura de "revista"**: metadados minúsculos em mono nos 4 cantos ("PRODUCER · @MARTOVSKYI · MOTION DESIGNER · ART DIRECTOR"). Custa pouco e passa muito profissionalismo.
- **Tipografia gigante e deformada** ("SHOWREEL", "2025") que se dobra e se transforma.
- **Chips/pílulas** coloridas ("Token", "RGB", "Design System", "#7B61FF") como rótulos de ideias.
- **Cursor clicando** num botão ("OPEN ACCOUNT"): a ação vira o clímax.
- **Palavras em neon ao redor da pessoa** ("FAMILY · TECH · SUPPORT"): o texto **orbita o apresentador**.
- **Número de impacto com brilho dourado** ("200 MBт") e **gráfico de barras crescendo**.
- Fecha com a **parede de logos de clientes**: prova social sem precisar dizer nada.

## Como aplicar na ZENTURY (técnica → bloco do catálogo HyperFrames)

| Técnica | Uso na ZENTURY | Bloco do catálogo |
| --- | --- | --- |
| Metadados editoriais nos cantos | "ZENTURY · EP.02 · ESTRATÉGIA · 2026" em mono dourado, em todo vídeo | (CSS próprio, fonte mono do `frame.md`) |
| Frase dividida em telas | Hook: "SUA EMPRESA" → "É BOA" → "MAS NINGUÉM" → "VÊ." | `kinetic-center-build`, `variable-font-flex`, `texture-mask-text` |
| Palavras orbitando a pessoa | Palavras-chave em dourado em volta do apresentador ("CLIENTE · HORA CERTA · LUGAR CERTO") | `three-orbiting-cards`, `badge-pop` |
| Ícones 3D + setas desenhadas à mão | Sequência "B em todo lugar" com ícones reais (Instagram, Google, Maps) e setas ligando à empresa | `hw-arrow`, `hw-callout-circle`, `hw-underline`, `ui-3d-reveal` |
| Número gigante com prova atrás | Resultado de cliente ("+312% de contatos") com o painel desfocado atrás | `count-up`, `social-proof-card`, `data-chart`, `animated-bar-chart` |
| Chips/pílulas | Conceitos sem jargão: "Aparecer", "Pessoa certa", "Hora certa" | `state-chip-rail`, `spring-pop` |
| Cursor clicando | Fim do vídeo: um cursor clica em "FALE COM A ZENTURY" | `oversized-cursor`, `gesture-tap`, `press-ripple` |
| Transição com desfoque/whip | Troca de assunto | `transitions-blur`, `whip-pan`, `motion-blur` |
| Telas inclinadas em 3D | Mostrar anúncio, painel e Google em perspectiva | `multi-device-splay`, `parallax-device-dive`, `split-tilt-cards` |
| Tipografia com brilho/material | Palavra de impacto ("VISIBILIDADE", "POR QUÊ?") com reflexo dourado | `gloss-sweep`, `light-sweep-pass`, `glass-shard-title` |
| Parede de logos | Clientes atendidos (quando tiver autorização) | `logo-wall`, `wordmark-tiles` |

## O que NÃO copiar
- O excesso de cores do Bohdan e do Aurelien: a ZENTURY fica em **preto, branco e dourado**.
- A troca de estilo a cada 2 segundos de um showreel: isso serve para mostrar portfólio. Nos Reels da ZENTURY, a **narrativa** manda, e os efeitos servem a ela.
- O cromado colorido do J's Cuts: o equivalente na ZENTURY é **dourado escovado sobre preto**, com moderação.

## Como obter referências do YouTube nesta sessão
O ambiente libera o YouTube, mas o YouTube bloqueia o download de vídeo vindo de servidor. O que funciona:
```bash
yt-dlp --skip-download --ignore-no-formats-error --write-info-json \
  --extractor-args "youtube:player_client=mweb" -o "%(id)s" "<URL>"
# depois baixar os fragmentos do formato 'sb0' (storyboard) listados no .info.json
```
Para análise completa (movimento fluido + áudio), mande o vídeo como arquivo (gravação de tela).
