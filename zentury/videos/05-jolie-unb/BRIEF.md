# Cliente Jolie Sorveteria e Café — anúncio "UnB 10%" (V1, padrão criativo de vendas)

- **Origem:** vídeo do cliente (16,3 s, 576×1024, WhatsApp). Sem arte final no vídeo: reaproveitada a arte do cliente do anúncio 04 (sem alteração).
- **Entrega:** `renders/jolie-unb-v1.mp4`: 20,0 s, 1080×1920, -14,0 LUFS.

## Fala (Whisper small + revisão)
"Você é professor ou aluno da UnB? Sabia que você tem 10% de desconto na sorveteria Jolie? E não é só no sorvete não! É no sorvete, no açaí e no nosso cardápio. Ou seja, deu aquela fome depois da aula? Vem na Jolie aproveitar os seus 10% de desconto!"
(confirmar a abertura: o áudio soa como "você é professor(a)…")

## Estados
| Saída | Fala | Tela |
|---|---|---|
| 0,0–2,3 | professor ou aluno da UnB? | "PROFESSOR OU ALUNO DA" + **"UnB?" gigante ATRÁS das meninas** (recorte `remove-background`), zoom de entrada |
| 2,3–5,7 | Sabia que você tem 10%… | selo 10% bate no "10%" (**drop da música**) |
| 5,7–9,6 | Não é só sorvete… cardápio | adesivo 10% fixo · "NÃO É SÓ SORVETE!" · cartões Sorvete / Açaí / Cardápio |
| 9,6–12,6 | deu fome depois da aula? | fusão para a loja · "DEU FOME DEPOIS DA AULA?" |
| 12,6–15,1 | Vem na Jolie… 10% | "VEM PRA JOLIE!" + pino "CLN 407 · Asa Norte" · **adesivo pulsa quando falam "10%" de novo** |
| 15,1–17,1 | — | arte do cliente |
| 17,1–20,0 | — | CTA "Toque em [Como chegar]" com a mão clicando |

## O que melhorou em relação ao anúncio 04 V2
1. **Texto atrás das apresentadoras** no gancho (profundidade, efeito de marca grande).
2. **Adesivo de oferta reage à fala** (pulsa no segundo "10%").
3. Um título por cena, sem repetir a legenda.
4. Corte mais enxuto: 16 s de fala em 15 s de vídeo + 5 s de marca/CTA.

## Legenda do anúncio (sugestão)
Professor ou aluno da UnB? 🎓🍦 Você tem 10% de desconto na Jolie, no sorvete, no açaí e em todo o cardápio.
Deu fome depois da aula? 📍 CLN 407, Bloco A, Lojas 1 e 5, Asa Norte.

**Público sugerido:** raio de 2–3 km da UnB (campus Darcy Ribeiro) + interesses universitários, 18–35 anos. Botão "Como chegar".

## Pendências
1. **Regra do desconto UnB:** precisa mostrar carteirinha/crachá? Validade? Se sim, entra na tela ("apresente sua carteirinha").
2. Confirmar "professor ou aluno" (a fala soa como "professora").
3. Vídeo original e arte em qualidade máxima.

## Reproduzir
```bash
./preprocess.sh /caminho/video.mov   # footage, voz, recorte do gancho (~70 s em CPU)
python3 -I src/build.py . && python3 -I audio.py
npx --yes hyperframes@0.8.139 render --quality delivery --output renders/raw.mp4   # + loudnorm -14 LUFS
```
