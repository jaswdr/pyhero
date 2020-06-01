import sys
import logging as _log
import math
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile as wav
from youtube_dl import YoutubeDL
import ffmpeg
import pickle
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import calendar
import json

LOG_DIR = os.path.join(os.getcwd(), "logs")
now = datetime.utcnow()
LOG_FILE = os.path.join(LOG_DIR, "{:4d}_{:02d}_{:02d}_{:02d}.log".format(
    now.year,
    now.month,
    now.day,
    now.hour
    ))

_log.basicConfig(
        format="%(asctime)s|%(module)s|%(filename)s:%(lineno)d|%(levelname)s:%(message)s",
        level=_log.DEBUG,
        filename=LOG_FILE,
        filemode='a+')

CACHE_DIR = os.path.join(os.getcwd(), "cache")

def handle(video_id):
    # downloading video file
    video_ext = "mp4"
    video_file = os.path.join(CACHE_DIR, "{}.{}".format(video_id, video_ext))
    if not os.path.isfile(video_file):
        _log.info("Downloding youtube file")
        video_url = "https://www.youtube.com/watch?v={}".format(video_id)
        ydl_opts = {
                "outtmpl": os.path.join(CACHE_DIR, "%(id)s.%(ext)s"),
                "format": "18",
                "writeinfojson": True
                }
        ydl = YoutubeDL(ydl_opts)
        result = ydl.download([video_url])
        _log.info("Successfully downloaded video file to {}".format(video_file))

    # convert to wav
    wav_file = os.path.join(CACHE_DIR, "{}.wav".format(video_id))
    if not os.path.isfile(wav_file):
        _log.info("Converting to WAV file")
        ffmpeg.input(video_file).filter("loudnorm").output(wav_file).run()
        _log.info("Successfully converted to WAV file {}".format(wav_file))

    # plotting
    data_file = os.path.join(CACHE_DIR, "{}.data".format(video_id))
    if not os.path.isfile(data_file):
        _log.info("Generating data")
        rate, raw_data = wav.read(wav_file)
        considered = int(len(raw_data)/rate)
        seconds = math.fmod(considered, 60)
        minutes = (considered-seconds)/60

        _log.info("Time {}m{}s".format(minutes, seconds))
        _log.info("Seconds {}".format(considered))
        _log.info("Rate {}hz".format(rate))
        _log.info("Samples {}".format(len(raw_data)))
        _log.info("Blocks {}".format(considered/rate))

        data = np.zeros(considered)
        last_percent = 0;
        for i in range(len(data)):
            current_percent = (i/len(data))*100
            current_percent = math.floor(current_percent)
            if current_percent > last_percent and current_percent % 5 == 0:
                _log.info("Data generation is {:3d}% complete".format(current_percent))
            data[i] = np.median(raw_data[i:(i*rate)+rate])
            last_percent = current_percent
        pickle.dump(data, open(data_file, "wb"))
        _log.info("Successfully generated data file {}".format(data_file))
    else:
        data = pickle.load(open(data_file, "rb"))
        _log.info("Successfully loadded data file {}".format(data_file))

    hero_file = os.path.join(CACHE_DIR, "{}.hero".format(video_id))
    if not os.path.isfile(hero_file):
        _log.info("Generating hero file")
        hero = np.zeros(len(data))
        for i in range(1, len(hero)):
            limit = 3
            previous = data[i-1] 
            current = data[i]
            if current > previous:
                hero[i] = hero[i-1]+1
                if hero[i] > limit:
                    hero[i] = limit
            if current < previous:
                hero[i] = hero[i-1]-1
                if hero[i] < -limit:
                    hero[i] = -limit
            if current == previous:
                hero[i] = hero[i-1]
        pickle.dump(hero, open(hero_file, "wb"))
        _log.info("Successfully generated hero file {}".format(hero_file))
    else:
        hero = pickle.load(open(hero_file, "rb"))
        _log.info("Successfully loadded hero file {}".format(hero_file))
    hero_json_file = os.path.join(CACHE_DIR, "{}.hero.json".format(video_id))
    if not os.path.isfile(hero_json_file):
        _log.info("Saving hero array to {}".format(hero_json_file))
        json.dump(hero.tolist(), open(hero_json_file, "w+"))
        _log.info("Saved hero array to {}".format(hero_json_file))

    return [video_file, wav_file, data_file, hero_file, hero_json_file]

if __name__ == "__main__":
    args = sys.argv
    if len(args) != 2:
        print("Usage: {} <youtube_video_url>".format(__file__))
        sys.exit(1)

    video_id = args[1]
    video_url = args[1]
    if video_url.startswith("http"):
        # full url used
        parsed = urlparse(video_url)
        query_parsed = parse_qs(parsed.query)
        video_id = query_parsed["v"][0]
    if video_id == "":
        print("Invalid Youtube URL")
        sys.exit(2)
    list_of_files = handle(video_id)
    print("Files:")
    print("\n".join(list_of_files ))
