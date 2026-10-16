# VoiceStudio (OmniVoice) · clonagem de voz

Repositório: https://github.com/debpalash/VoiceStudio (app AGPL-3.0). Motor padrão: **k2-fsa/OmniVoice**.

> ⚠️ **Licença do modelo: CC-BY-NC (não comercial)**, conforme o card do modelo no Hugging Face ("The pre-trained model is licensed under the CC-BY-NC due to constraints from its training data"). Serve para **teste interno**. Para anúncio pago de cliente, use uma voz gravada de verdade ou um motor com licença comercial (ex.: HeyGen/ElevenLabs com plano comercial).

## Instalação no ambiente da nuvem (sem GPU, só CPU)
O app desktop (Electron) não roda aqui; usamos o CLI Python do mesmo motor.
```bash
S=<scratchpad>
git clone --depth 1 https://github.com/debpalash/VoiceStudio $S/repos/VoiceStudio
uv venv --python 3.12 $S/vsenv
VIRTUAL_ENV=$S/vsenv uv pip install torch torchaudio torchcodec transformers accelerate soundfile pydub numpy safetensors huggingface_hub
$S/vsenv/bin/hf download k2-fsa/OmniVoice --local-dir $S/models/OmniVoice   # 3,3 GB
```
- `download.pytorch.org` é bloqueado pela rede → o torch vem do PyPI (versão CUDA, ~5 GB, roda em CPU).
- Sem `torchcodec` a geração roda, mas falha ao salvar o WAV.

## Gerar
```bash
PYTHONPATH=$S/repos/VoiceStudio $S/vsenv/bin/python -m omnivoice.cli.infer \
  --model $S/models/OmniVoice --device cpu --language pt \
  --ref_audio voz-ref.wav --ref_text "transcrição exata da referência" \
  --text "Texto novo" --output saida.wav
```
- `--ref_text` é obrigatório aqui (a transcrição automática precisa de um modelo de ASR do app). Use a transcrição da referência feita com Whisper.
- Outras opções: `--speed`, `--duration` (força a duração, útil para encaixar na EDL) e `--num_step` (32 por padrão).
- Velocidade medida em CPU de 4 núcleos: **~65 s para 3 s de áudio** (inclui ~10 s de carga do modelo).

## Referência ideal da voz
- 10–20 s de fala contínua, sem música, sem eco, um só falante, no tom do vídeo.
- Celular a ~20 cm da boca, cômodo com cortinas/sofá, sem ventilador ou ar-condicionado.
- Arquivo de voz pessoal **não vai para o Git** (`videos/*/assets/audio/voice-*` está no `.gitignore`).

## Uso ético
Só clonar a voz de quem autorizou, e informar quando a fala for sintética, se a plataforma ou o contexto exigir.
