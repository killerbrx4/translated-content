# Jolie: anúncios estáticos (V1)

São 5 conceitos, cada um em **feed 1080×1350** e **story 1080×1920**. As fotos são quadros dos vídeos do cliente, com a cor da Jolie (LUT). Seguem o padrão visual das edições 04–09.

| # | Conceito | Ângulo de venda |
|---|---|---|
| 01 | VOCÊ MONTA SEU SORVETE! + selo "pague pelo peso" | autonomia + preço controlado |
| 02 | AÇAÍ DO SEU JEITO + 3 acompanhamentos | oferta do açaí |
| 03 | COMO FUNCIONA NA JOLIE? (6 passos em grade) | tira dúvidas, educa o primeiro cliente |
| 04 | MORA NA ASA SUL OU ASA NORTE? + selo 10% | segmentação por bairro + desconto (**confirmar regra do desconto**) |
| 05 | COISA BOA PERTO DE VOCÊ. | marca / proximidade |

Todas têm a mesma barra de rodapé: logo, "CLN 407 · Asa Norte" e o botão "Como chegar".

Gerar: `python3 -I src/gerar.py <pasta_quadros> <logo.png> saida/` (Playwright + Chromium). Os arquivos de imagem ficam fora do Git.
