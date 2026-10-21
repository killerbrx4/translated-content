# Jolie · gravação 20/10/2026 · V1 "Não é só sorvete" (venda de lanche: tapioca e cuscuz)

- **Material:** 31 vídeos (WhatsApp, 464×832, 60 fps), 13 fotos, 10 falas gravadas no celular (.m4a), logo oficial.
- **Entrega:** `renders/jolie-nao-e-so-sorvete-v1.mp4` (37,1 s, 1080×1920, -14,2 LUFS) + `-celular.mp4`.

## Sincronia das falas (celular ↔ câmera)
Encontrada por correlação da forma de onda (passa-faixa 300–3000 Hz), com precisão de amostra:
v23↔Pato_2 (+1,5665 s), v22↔Avenida_Cln (+2,1068 s), v25↔Pato_5 (+2,3417 s), v26↔Pato_6 (+2,3080 s), v29↔Pato_7 (+2,0780 s).
As falas sem par na câmera (Pato_4, Avenida_Cln_2, Avenida_Cln_3) viraram narração sobre o preparo. Textos conferidos com Whisper large-v3-turbo.

## Roteiro montado
| Saída | Imagem | Fala |
|---|---|---|
| 0–3,7 | ela à mesa (v23) + cubas de sorvete em "só sorvete?" | "Você achou que a Jolie era só sorvete? Então deixa eu te mostrar uma coisa." |
| 3,7–7,2 | ela com o cardápio (v25) + close do cardápio | "São tantas opções gostosas, que fica até difícil escolher uma só." |
| 7,2–10,7 | tapioca na mesa (v26) | "E hoje eu escolhi uma das minhas favoritas." |
| 10,7–15,7 | preparo da tapioca (goma → disco → mussarela → frango → prato) | "E uma dessas opções é a nossa tapioca…" |
| 15,7–20,4 | tapioca aberta, servida, foto | "Tapioca de frango com mussarela. Olha só essa combinação deliciosa." |
| 20,4–28,5 | preparo do cuscuz → desenformar → **queijo derretido escorrendo** (2,4 s, sem fala) | "Aqui na Jolie você encontra várias opções de cuscuz…" |
| 28,5–33,5 | ela recebe o cuscuz (v29) | "Gente, olha só esse cuscuz da Jolie. Quem aí também ama?" |
| 33,5–37,1 | foto do pôr do sol com o cuscuz + logo + "Como chegar" + endereço | — |

## Acabamento (padrão profissional)
- Um grafismo por vez, só no topo: gancho "era só sorvete?" no 1º quadro; depois "Tapioca", "Frango com mussarela", "Cuscuz" e "Quem aí também ama?". Cada um entra na palavra e sai pouco depois.
- Legenda palavra a palavra embaixo (sem caixa), palavras-chave em laranja. Ken Burns suave em todos os planos. Logo pequeno no canto.
- Som: falas limpas do celular + som ambiente da cozinha baixinho nos planos de preparo + trilha pop leve própria (100 BPM) com ducking.
- Upscale 464→1080 com nitidez leve e cor quente uniforme.

## Pendências
1. **Preços:** o cardápio aparece, mas os valores não foram usados (não estão legíveis com certeza).
2. **Botão do anúncio:** `CONFIG.cta` no template ("Como chegar"; pode trocar por "Enviar mensagem").
3. **Material não usado ainda:** v02 (coberturas), v03 (picolés e bombons), v04/v28 (fachada), v15 (cozinheira explicando, horizontal), v21, v22 (2º take do gancho) e mais 11 fotos. Dá para fazer cortes curtos só de tapioca, só de cuscuz e de sorvete.

## V2 (ajustes pedidos pelo cliente: organização dos blocos + novo encerramento)
- `renders/jolie-nao-e-so-sorvete-v2.mp4` (38,1 s, -14,2 LUFS).
- **Blocos:** apresentação da Laura → cardápio (agora um bloco próprio de 2 s, até o fim de "escolher uma só") → Laura com a tapioca → preparo da tapioca → preparo do cuscuz → Laura com o cuscuz → final.
- **Transições:** fusão suave de 0,3 s **só na troca de bloco** (`edl.json → xfade`). Dentro de cada bloco, os cortes continuam secos, no ritmo da fala. O cardápio entra e sai em fusão.
- **Sem repetição:** a tapioca servida (v27) aparece uma vez só; a foto da tapioca ficou mais tempo.
- **Encerramento:** mesma foto, mesma entrada da logo e mesmo degradê. Saíram o botão, o ícone e "Como chegar". Texto: "Sorvete, tapioca, cuscuz e muito mais." / **"Venha conhecer a Jolie!"** (destaque laranja) / "CLN 407, Bloco A, Lojas 1 e 5 — Asa Norte". O endereço fica 3,7 s na tela; o encerramento passou de 3,6 para 4,6 s.
- A logo oficial já traz "Jolie · sorveteria e café", por isso esse texto não foi repetido embaixo dela.
