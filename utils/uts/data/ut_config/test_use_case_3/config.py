__author__ = "Marcin Matula"
__copyright__ = "Copyright (C) 2022, Marcin Matula"
__credits__ = ["Marcin Matula"]
__license__ = "Apache License"
__version__ = "2.0"
__maintainer__ = "Marcin Matula"

VATF = {"branch" : "develop_20220815"}

session_dir = "/tmp/data/session_{config_loading_time}"

AUDIO  = {
    "path" : f"{session_dir}/audio"
}

ASSETS = {
    "audio" : {
        "path":"./assets/audio_files",
        "files":[
            {
                "name": "alexa_are_you_there.wav",
                "tags":["verification"]
            },
            {
                "name":"alexa_tell_me_a_joke.wav",
                "tags":["joke"]
            }]
    }
}

log_path = f"{session_dir}/log/session.log"
date_format = "%Y-%m-%d %H:%M:%S.%f"
date_regex = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]"

VA_LOG = {
    "path" : log_path,
    "timedelta" : { "hours" : -1 },
    "date_format" : date_format,
    "date_regex" : date_regex
}

WAIT_FOR_REGEX = {
    "path" : log_path,
    "date_format" : date_format,
    "date_regex" : date_regex
}

UTTERANCE_FROM_VA = {
    "regexes" : [
        {
            "begin" : "DialogUXStateAggregator:executeSetState:from=THINKING,to=SPEAKING,validTransition=true",
            "end" : "DialogUXStateAggregator:executeSetState:from=SPEAKING,to=IDLE,validTransition=true"
        }
    ]
}
