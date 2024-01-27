#/bin/bash
find ${WORKSPACE_PATH} -name "*.pcm" | parallel -I % --max-args 1 --jobs 8 ffmpeg -f s16le -ac 1 -ar 44100 % %.ogg
