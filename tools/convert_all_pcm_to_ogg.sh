#/bin/bash
    return f"ffmpeg -f {fformat} -ar {framerate} -ac {channels} -i {input} {output}"

find .. -name \"*.pcm\" | parallel -I % --max-args 1 --jobs 8 ffmpeg -f s16le -ac 1 -ar 44100 % %.ogg
