# PyHero

> Extract information from Youtube videos

### Quick Start

```
$ git clone https://github.com/jaswdr/pyhero
$ cd pyhero
$ pip install -r ./requirements.txt
$ python main.py https://www.youtube.com/watch?v=jNQXAC9IVRw
Files:
    ./cache/jNQXAC9IVRw.mp4
    ./cache/jNQXAC9IVRw.wav
    ./cache/jNQXAC9IVRw.data
    ./cache/jNQXAC9IVRw.hero
    ./cache/jNQXAC9IVRw.hero.json
```

Generated files:
- MP4 video file extracted from the url
- INFO information related to the video
- WAV audio file extracted from MP4, used to generate data
- DATA file with numpy array of median frequency per second
- HERO file with number array, starting at zero and going up or down dependending if the frequency increase or decrease, also available in JSON format using the `*.hero.json` file

# Docker

```
$ docker run -v $PWD:/app/cache jaschweder/pyhero https://www.youtube.com/watch?v=jNQXAC9IVRw
```

### Disclaimer

All content downloaded from Youtube belongs to Youtube
