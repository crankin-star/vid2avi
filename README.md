# vid2avi

A python script for quickly converting entire folders of videos to .avi extensions with ffmpeg.

## installation

- Install ffmpeg with preferred method
- clone this repository with `gh clone https://github.com/crankin-star/vid2avi.git`
- install with uv or pip `[uv] pip install -e .` into an environment or into the global scope for easy use.

## intended use

Open the folder with videos to convert in file explorer or navigate into the folder with terminal. If in file explorer, right click in the folder and select "Open in Terminal".

In the terminal window type `vid2avi .`. If you want to include file extensions other than .mts and .mp4, use the `--formats` flag.
