# Estudo: 7 repositórios de campanha/criativo com IA (out/2026)

Clonados só para leitura (`/home/user/estudo`, fora do Git). Nenhum código foi executado.

| Repo | O que é | Licença | Nota para nós |
|---|---|---|---|
| **SupercmoHQ/superCMO-skills** | 23 skills de agente (marca → concorrentes → conceitos → copy → roteiro → imagem/vídeo), MCP local, gera por APIs pagas (fal/Wavespeed, ElevenLabs, Gemini) | Apache-2.0 | ⭐⭐⭐⭐⭐ melhor **metodologia** |
| **bitsandbrainsai/ai-ad-creative-strategist** | n8n: pega anúncios vencedores do concorrente (30–60 dias no ar), Gemini disseca, Claude adapta à marca, Sora gera | sem licença (só referência) | ⭐⭐⭐⭐ prompts de **análise** e **adaptação**; tem chave de API vazada no JSON; workflow incompleto |
| **rishidandu/cutagent** | Next.js: URL do produto → 4 cenas (hook/solução/prova/CTA) em Kling/Veo via fal → MP4 | MIT | ⭐⭐⭐⭐ **Hook Lab** (8 tipos de gancho), papéis de cena, regra de 2,8 palavras/s |
| **LichAmnesia/awesome-ad-video-prompts** | 52 prompts de vídeo IA (Veo/Kling/Seedance/Runway), 10 categorias, 5 de comida | CC BY 4.0 (atribuir) | ⭐⭐⭐ padrão de prompt (cena → beats cronometrados → câmera → luz → "fidelity guard") |
| **autonode-x/n8n-ai-short-video-automation** | n8n webhook {tema, tom} → pesquisa, roteiro, storyboard JSON, prompts de imagem, legendas; Groq | MIT | ⭐⭐⭐ esqueleto de agentes com saída estruturada; não gera mídia; pesquisa sem fonte |
| **satyamshivam13/Multi_Agent_Campaign_Creator** | CrewAI: 4 agentes → brief de campanha em Markdown | MIT | ⭐⭐ raso; dados de concorrência falsos; só os **schemas de briefing** servem |
| **Colten1023/ai-content-automation-n8n** | n8n: história → TTS ElevenLabs → 12 imagens DALL·E → ffmpeg | sem licença | ⭐ didático; JSON quebrado; ffmpeg ingênuo |

## O que vamos aproveitar (sem pagar API nenhuma)
1. **Conceito de campanha (superCMO `planning-campaigns/references/finding-concepts.md`)**: comprador (tarefa, gatilho, nível de consciência) + **hipótese falseável** + evidência + formato, pontuados por impacto × confiança. Campanhas separadas por **linha de produto / sazonalidade**, nunca por persona. **Nunca inventar preço, prova ou oferta.**
2. **8 ângulos de copy** (dor, resultado, prova, curiosidade, comparação, urgência real, identidade, contrário). A regra é variar o **argumento**, não as palavras. Guia Meta: ~125 caracteres de texto principal antes do "ver mais", headline ~27; política de atributos pessoais (sem "Solteiro?", "Endividado?").
3. **Hook Lab (cutagent)**: 8 ganchos (Surpresa, Problema, POV, ASMR, Depoimento, Tendência, Luxo, Humor). Fazer N ganchos curtos, testar e expandir o vencedor. Locução cabe em **duração × 2,8 palavras/s × 0,8**.
4. **Ficha de dissecação de anúncio (Strategist)**, 7 seções: visão geral · segundo a segundo · visual · mensagem (hook 3 s, proposta, CTA) · marca · estratégia · "Must-keep × Adaptável". Serve para analisar concorrentes na Meta Ad Library e os nossos vencedores. Heurística: **30–60 dias no ar = vencedor**.
5. **Roteiro cena a cena (tempo, visual, câmera, texto na tela, mood)** como JSON que alimenta direto as composições HyperFrames.
6. **Prompt de vídeo IA (awesome-ad-video-prompts)** só para **atmosfera/b-roll** ou image-to-video a partir de **foto real do prato** (comida gerada por IA = risco de propaganda enganosa).
