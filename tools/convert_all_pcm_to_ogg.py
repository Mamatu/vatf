if __name__ == "__main__":
    import toolsargs
    import os
    args = toolsargs.parse()
    root = args["root"]
    jobs = args["jobs"]
    os.system(f"find {root} -name \"*.pcm\" -not -path \"./vatf/*\" | parallel -I % --max-args 1 --jobs {jobs} PYTHONPATH=. python3 vatf/utils/papy.py --convert --input % --output %.ogg --tool ffmpeg --audio_config s16le,1,44100")
