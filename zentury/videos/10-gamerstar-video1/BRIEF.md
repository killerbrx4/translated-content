# Cliente Gamer Star Informática · Vídeo 1 "RTX 4070 ou 5060 Ti?" (V2)

- **Origem:** vídeo de conteúdo já editado pelo cliente: 53,1 s, 480×854. Tinha legenda queimada, música de fundo e a gravação **espelhada** (as caixas das placas e a camisa "GAMER STAR" apareciam invertidas).
- **Pedido:** "edita esse vídeo, adicione qualidades gráficas e efeitos que vão agregar… cortando os pontos que não são necessários… mostrando sempre os produtos".
- **Entrega:** `renders/gamerstar-4070-vs-5060ti-v2.mp4` (45,9 s, 1080×1920, -14,5 LUFS) e a versão `-celular.mp4`.
- **V2 (pedido do cliente):** a faixa de legenda grande tampava a modelo e os produtos. Agora a legenda é uma etiqueta compacta, do tamanho da legenda antiga daquele trecho.

## Tratamento
1. **Espelhamento corrigido** (`hflip`): agora "GEFORCE RTX 4070/5060 Ti" e o logo na camisa estão legíveis.
2. **Voz isolada com Demucs** (htdemucs_ft): a música do original (de terceiros) sai, e os cortes não dão salto no áudio.
3. **Legenda antiga localizada por OCR** (`src/ocr_burned.py`, RapidOCR no vídeo original, onde ela é legível; resultado em `src/burned.json`). Cada bloco da legenda nova é uma etiqueta escura centrada na legenda antiga daquele trecho e com, no mínimo, o tamanho dela. Assim cobre a legenda invertida sem tampar a modelo e as placas. O texto das caixas e o "INFORMÁTICA" da camisa ficam fora do filtro.
4. **Cortes:** "nós precisamos analisar", "para você determinar qual placa entrega o melhor desempenho", "ou até mesmo a aplicação que você vai utilizá-la" e as pausas (−7,2 s).
5. O efeito cinza do original (8,6–10,8 s) e o fade para preto (44,8 s) ficaram cobertos pelos cartões "50 > 40 SEMPRE?" e "E VOCÊ?".

## Grafismos (todos presos à fala)
| Momento | Grafismo |
|---|---|
| 0 s (já no 1º quadro) | RTX 4070 **VS** RTX 5060 Ti; cada placa pulsa quando é falada |
| "a série 50 é melhor que a 40?" | cartão de tela cheia **SÉRIE 50 > SÉRIE 40 · SEMPRE?** |
| "RTX 4070 série 40 / 5060 Ti série 50" | linha das gerações: nós 40 → 50 acendem, etiquetas com os nomes das placas |
| "Mas, atenção!" | carimbo ATENÇÃO, flash vermelho, tremida, drop da trilha |
| "olhar para geração não é o suficiente" | OLHAR SÓ A GERAÇÃO / **NÃO BASTA!** |
| "para comparar…" | COMO COMPARAR? + checklist (desempenho, memória, recursos, tipo de jogo), cada item marcado quando é dito |
| "geração mais nova não significa automaticamente…" | GERAÇÃO MAIS NOVA **≠ SEMPRE SUPERIOR** |
| pergunta final | cartão E VOCÊ? → enquete A GERAÇÃO / B O DESEMPENHO + "COMENTA AQUI" |
| final (3,2 s) | logo oficial, "Na dúvida entre duas placas?", botão **Enviar mensagem**, endereço e "+ de 1.000 pedidos enviados por mês" (bio do Instagram) |

- **Marca:** logo oficial na versão negativa (o preto virou branco e o vermelho original foi mantido; a forma não foi alterada). Vermelho #cb2129 amostrado do logo. Fontes Bebas Neue e Barlow Condensed (OFL).
- **Trilha própria** (eletrônica, 124 BPM, Lá menor): arpejo até o "atenção!", depois bateria e baixo, com ducking sob a voz. SFX em cada grafismo.

## Pendências / confirmar com o cliente
1. O texto do botão final segue o objetivo do anúncio (mensagem, site ou loja): `CONFIG.cta` no template.
2. Se o vídeo for orgânico, o cartão final pode trocar o botão por "@gamerstar_informatica".
3. Não foram usados preço, especificações nem benchmarks das placas (nada disso foi informado).
