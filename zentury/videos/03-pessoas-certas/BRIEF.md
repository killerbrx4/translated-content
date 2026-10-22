# ZENTURY 03 — "Sua empresa não precisa de mais seguidores"

**Formato:** 9:16 · 1080×1920 · 30 fps · **40,7 s** · -14 LUFS · `renders/zentury-03-pessoas-certas.mp4` · capa `cover/capa-reel.png`

## Roteiro (narração provisória em voz sintética pt-BR; trocar pela gravação do apresentador)
| Bloco | Tempo | Fala | Visual |
| --- | --- | --- | --- |
| Gancho | 0,0–4,7 | "Sua empresa não precisa de mais seguidores. Ela precisa chegar às pessoas certas." | Contador de seguidores sobe e é riscado em dourado → multidão 3D em perspectiva, poucas pessoas acendem em dourado: "PESSOAS CERTAS" |
| Problema | 5,0–9,8 | "Dá pra ter milhares de seguidores e não vender nada. Muita gente vê, curte… e vai embora." | Celular com post (rótulo "Ilustração"), curtidas subindo, selo "Vendas: 0"; pessoas chegam, curtem e saem |
| Explicação · Meta | 10,1–16,7 | "No Meta Ads, seu anúncio aparece no Instagram e no Facebook, para quem tem o perfil do seu cliente: região, idade e interesses." | Anúncio "Patrocinado" no feed + filtros Região/Idade/Interesses estreitando o público |
| Explicação · Google | 17,0–25,6 | "No Google Ads é diferente. Você aparece para quem já está procurando. Uma pessoa pesquisa 'dentista em Campinas', e o seu anúncio aparece como patrocinado." | Barra de pesquisa digitando, selo "Intenção: já está procurando", 1º resultado com rótulo **Patrocinado** (empresa fictícia, "Exemplo ilustrativo"), clique |
| Exemplo | 25,9–33,4 | "Daí começa o caminho: anúncio, clique, contato, atendimento e venda. O resultado depende da oferta, do orçamento, da página e do atendimento." | ANÚNCIO → CLIQUE → CONTATO → ATENDIMENTO → VENDA acendendo palavra a palavra + fatores; nota "o resultado não é garantido: depende desses fatores" |
| Conclusão | 33,7–37,4 | "Não é sobre todo mundo te ver. É sobre quem compra te encontrar." | Multidão inteira acende e apaga; só quem compra sobe em dourado: "QUEM COMPRA." |
| CTA | 37,8–40,7 | "Siga a ZENTURY e entenda o próximo passo." | Logo oficial (vetorizado) + "Siga @zentury" |

## Decisões de edição
- Narração gerada **frase a frase**: cada cena e cada palavra da legenda é cronometrada pelo áudio real (`timings.json`), sem ajuste no olho.
- Uma metáfora visual do começo ao fim (a multidão: alcance × pessoas certas), em vez de efeitos soltos.
- 3D só onde explica: multidão em perspectiva e celular inclinado.
- Interfaces **ilustrativas** (sem copiar a UI do Instagram ou do Google) e rotuladas; empresa do exemplo é fictícia.
- Honestidade: nenhuma estatística; o caminho comercial vem com o aviso de que o resultado depende de oferta, orçamento, página e atendimento.
- Legenda karaokê (palavra acende quando é dita), destaque em amarelo/dourado, zona segura do Reels.
- Trilha escura sintetizada com ducking de ~9 dB sob a voz; SFX discretos (contador, cliques, digitação).

## Controle de qualidade
- Pronúncia verificada transcrevendo o áudio (Whisper): corrigidos "Ads" (→ "Éds") e uma frase que soava "serviço" (reescrita).
- 2 rodadas de crítica: pontuação solta nas legendas, multidão sob a legenda, rótulo "Ilustração" no Meta, 3 vazios de ~0,6 s nas transições. Todos corrigidos.

## Legenda sugerida para o Instagram
> Seguidor não paga boleto. 👀
> Alcance sem intenção de compra enche o perfil, mas não enche a agenda.
> No Meta Ads você aparece para quem tem o perfil do seu cliente. No Google Ads, para quem já está procurando o que você vende.
> E o resultado ainda depende da sua oferta, da página e do atendimento.
> Quer entender qual faz mais sentido para a sua empresa? Comenta "PESSOAS CERTAS" que a gente te explica.
> #trafegopago #googleads #metaads #marketingdigital #empreendedorismo

## CTA recomendado
"Comenta **PESSOAS CERTAS**" (gera conversa para o direct) + seguir o perfil.

## Pendências
1. **Gravação do apresentador** com este roteiro (a voz atual é sintética e provisória).
2. **@ oficial** do Instagram (`CONFIG.handle`; hoje "@zentury").
3. Pronúncia de "ZENTURY" na narração sintética não ficou clara; com a gravação real resolve.
4. Trilha sintetizada; se houver música licenciada da marca, substituir.

## Reproduzir
```bash
python3 narration.py && python3 -I src/build.py . src/template.html && python3 audio.py
npx --yes hyperframes@0.8.139 render --quality delivery --output renders/zentury-03-pessoas-certas.mp4
```
