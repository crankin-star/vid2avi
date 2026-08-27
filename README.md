# vid2avi

A python script for quickly converting entire folders of videos to .avi extensions with ffmpeg.

## installation

- Install ffmpeg with preferred method. I would suggest running `winget install ffmpeg` in a terminal.
- clone this repository with `gh clone https://github.com/crankin-star/vid2avi.git`
- Make a local environment with uv or pip:
  - `uv venv; uv .\.venv\Scripts\activate`
  - `python3 -m venv .venv; .\.venv\Scripts\activate`
- install with uv or pip `[uv] pip install -e .` into an environment.
- Set up your terminal to access the script with a function for ease of use:

### zsh

```{shell}
run_my_script() {
    "/path/to/venv/bin/python" "/path/to/script.py" "$@"
}
```

Copy into your .zshrc file and replace `/path/to/venv` with your environment's _absolute_ path and `/path/to/script` with your script's _absolute_ path

### bash

```{bash}
vid2avi() {
    "/path/to/venv/bin/python" "/path/to/script.py" "$@"
}
```

Copy into your .bashrc file and replace `/path/to/venv` with your environment's _absolute_ path and `/path/to/script` with your script's _absolute_ path

### fish

```{fish}
function vid2avi
    # Change the paths below to the correct venv and script
    "/path/to/venv/bin/python" "/path/to/script.py" $argv
end

funcsave vid2avi
```

Or save into `~/.config/fish/config.fish` after changing.

### PowerShell

```{PowerShell}
function vid2avi {
    # Change the paths below to the correct venv and script
    & "C:\path\to\venv\Scripts\python.exe" "C:\path\to\script.py" @args
}
```

Copy the run function into your `PROFILE` (access with `notepad $PROFILE`)

You can then invoke them, for example, like:

## intended use

Open the folder with videos to convert in file explorer or navigate into the folder with terminal. If in file explorer, right click in the folder and select "Open in Terminal".

In the terminal window type `vid2avi`. If you want to include file extensions other than .mts and .mp4, use the `--formats` flag. If you want to convert videos in a subdirectory, use the `--dir` flag.

```{shell}
run_my_script --dir ./some-directory --format foo bar baz
```

Everything after the function name gets passed through to Python, unchanged.
