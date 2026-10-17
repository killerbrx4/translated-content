# Cliente Jolie Sorveteria e Café — anúncio "10% de desconto" (V1)

- **Origem:** vídeo enviado pelo cliente (30,4 s, 576×1024, comprimido pelo WhatsApp), com a fala das duas apresentadoras e a arte final de endereço.
- **Entrega:** `renders/jolie-desconto-v1.mp4`: 24,2 s, 1080×1920, -14,2 LUFS.
- **Marca:** cores amostradas da arte do cliente (azul-marinho #0B1D47, vermelho #E61A27, laranja #F39A1E, creme #F6ECE3). Fonte Montserrat (a mesma família da arte). A arte final do cliente entra sem alteração.

## Fala (transcrita palavra a palavra, Whisper small + revisão)
"Você mora na Asa Sul ou na Asa Norte? Então essa é pra você. A Jolie está com 10% de desconto pra você aproveitar! Nos sorvetes, no açaí e também no nosso **café** (confirmar). Tá pela Asa Sul ou pela Asa Norte? Então você já sabe onde parar quando bater aquela vontade. Porque coisa boa tem que estar perto de você!"

## EDL (origem → saída)
| Corte | Origem (s) | Saída (s) | Zoom | Grafismo |
|---|---|---|---|---|
| c1 | 0,80–4,10 | 0,00 | 1,00→1,04 | chips "Asa Sul" / "Asa Norte" saltam em cada palavra |
| c2 | 4,45–8,10 | 3,30 | 1,16 (punch-in esconde o jump cut) | selo "10% de desconto" bate como carimbo no "10%" |
| c3 | 8,18–11,00 | 6,95 | 1,00→1,05 | cartões Sorvetes · Açaí · Café, um por palavra |
| c4 | 11,30–14,00 | 9,77 | 1,08 | chips voltam entrando pelas laterais |
| c5 | 15,75–19,93 | 12,47 | 1,00→1,08 | pino "Jolie · Asa Norte" cai em "parar" |
| c6 | 20,35–21,75 | 16,65 | 1,04→1,10 | cartão de endereço (texto igual ao da arte) |
| c7 | 22,60–25,70 | 18,05 | 1,00→1,06 | legenda no topo (rostos ficam livres) |
| card | arte do cliente | 21,15 (3 s) | 1,00→1,03 | flash creme + acorde final |

Cortado: silêncio inicial, a fusão lenta 14,0–15,7 s, 1 s da fachada e a pausa antes de "Porque coisa boa". Resultado: 30,4 s → 24,2 s.

## Som
Voz original (mesma EDL, fades de 15 ms) + trilha pop solar sintetizada (112 BPM, I–V–vi–IV) com ducking de ~10 dB sob a fala + SFX presos a cada grafismo (pop, carimbo, brilho, whoosh, acorde final). Loudness -14 LUFS.

## Crítica (V1)
Gancho 8 · legibilidade 8,5 · movimento 8 · variedade 8,5 (novo elemento a cada 1,5–3 s) · composição 8 · marca 8,5 · som 8. `check`: 0 erros, contraste 19/19 AA.

## Legenda do anúncio (sugestão)
Asa Sul ou Asa Norte? 🍦 A Jolie está com 10% de desconto em sorvetes, açaí e café.
📍 CLN 407, Bloco A, Lojas 1 e 5, Asa Norte.
Coisa boa tem que estar perto de você. Vem pra Jolie!

**CTA recomendado:** botão "Como chegar" (anúncio com objetivo de visita/tráfego local) ou "Enviar mensagem" se o pedido for pelo WhatsApp.

## Pendências
1. Confirmar a palavra "café" (o áudio diz algo como "no nosso ca-fé"; o ASR ficou em dúvida).
2. Regras do desconto: validade, se vale para tudo e se precisa de cupom. Se houver condição, ela entra na legenda/tela.
3. Arquivos originais em qualidade máxima (vídeo da câmera e arte final em PNG/PDF). O WhatsApp reduziu para 576×1024.
4. @ do Instagram da Jolie, se quiserem "Siga" no final.

## Reproduzir
```bash
./preprocess.sh /caminho/video.mov     # footage 1080x1920, voz, arte final
python3 -I src/build.py .              # index.html + timeline.json a partir de edl.json
python3 -I audio.py                    # mix -14 LUFS
npx --yes hyperframes@0.8.139 render --quality delivery --output renders/jolie-desconto-v1.mp4
```

---

# V2: criativo de vendas (`renders/jolie-desconto-v2.mp4`, 26,1 s, 1080×1920, -14,0 LUFS)

Pedido: "edite de forma profissional para ser um criativo de vendas… tem que ter uma boa conversão".
Gerar: `python3 -I src/build.py . edl-v2.json src/template-v2.html && python3 -I audio.py` + render + loudnorm final.

| O que mudou | Por que converte mais |
|---|---|
| **Título fixo no topo já no 1º quadro** ("MORA NA ASA SUL OU ASA NORTE?") + zoom de entrada | para o dedo antes da fala começar; segmenta o público pelo bairro no 1º segundo |
| **Gramática da referência:** título no mesmo lugar, só a palavra troca ("TÁ PELA ASA SUL? → ASA NORTE?") | leitura sem som; o olho não precisa procurar |
| **Oferta sempre visível:** o selo 10% bate no centro e vira adesivo no canto até o fim | quem entra no meio do vídeo também vê a oferta |
| **Drop da música no carimbo do 10%** (antes só pluck; riser de 0,9 s) | o pico de energia cai no momento-chave da oferta |
| "SUA PARADA CERTA:" + pino Jolie · Asa Norte | transforma a fala em destino concreto |
| Arte do cliente 2 s (era 3 s) | menos tempo parado |
| **Tela de CTA nova:** selo + "Toque em [Como chegar]" com a mão clicando e o endereço | espelha o botão real do anúncio; diz exatamente o que fazer (`CONFIG.cta` troca para "Enviar mensagem") |
| Legendas duplicadas do título removidas; legenda da mesa abaixo do adesivo | uma informação por vez |

Crítica V2: gancho 9 · legibilidade 8,5 · movimento 8,5 · variedade 9 · composição 8 · marca 8,5 · som 8,5.

**Configuração recomendada no Gerenciador de Anúncios:** objetivo Tráfego/Reconhecimento com raio de 3–5 km da CLN 407 (Asa Norte + Asa Sul), botão "Como chegar"; se o pedido for por WhatsApp, objetivo Engajamento → mensagens e `CONFIG.cta = "Enviar mensagem"`. Testar V1 × V2 com o mesmo público e orçamento por 3–4 dias antes de escalar.
