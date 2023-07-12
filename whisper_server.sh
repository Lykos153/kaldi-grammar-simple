podman run -ti --gpus all -p 9000:9000 -e ASR_MODEL=small -e ASR_ENGINE=openai_whisper -v whisper-cache:/root/.cache/whisper  onerahmet/openai-whisper-asr-webservice:latest-gpu
