
# Various tested raspivid, FFmpeg & MPV commands, arguments

### raspivid TCP H264
``` bash
raspivid -fps 30 -t 0 -l -w 1920 -h 1080 -o tcp://0.0.0.0:3333
```

### raspivid UDP H264
``` bash
raspivid -fps 30 -t 0 -l -w 1920 -h 1080 -o udp://0.0.0.0:3333
```

### raspivid MJPEG to FFmpeg MKV TCP
``` bash
raspivid -vf -hf -fps 30 -t 0 -l -w 1920 -h 1080 --codec MJPEG -o - | ffmpeg -i - -vcodec copy -flush_packets 0 -listen 1 -f matroska tcp://0.0.0.0:3333
```

### MPV low latency arguments TCP
``` bash
mpv --hwdec=auto --cache=no --no-correct-pts --fps=30 --profile=low-latency --opengl-glfinish=yes tcp://<RPi-IP>:3333
```

### MPV low latency arguments UDP
``` bash
mpv --hwdec=auto --cache=no --no-correct-pts --fps=30 --profile=low-latency --opengl-glfinish=yes udp://<RPi-IP>:3333
```

### MPV low latency arguments TCP (testing)
``` bash
mpv --demuxer-thread=no --vd-lavc-threads=1 --untimed --no-correct-pts "tcp://<RPi-IP>:3333
```

### raspivid MJPEG to custom py script (deprecated)
```bash
raspivid -vf -hf -fps 30 -t 0 -l -w 1920 -h 1080 --codec MJPEG -o - | python3 send_mjpeg.py
```