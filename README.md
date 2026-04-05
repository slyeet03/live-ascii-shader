# ASCII Webcam

A real-time webcam feed rendered as ASCII art directly in your terminal.

## Demo

```
@@@@@&#&#GPGP555JJY77?~~::^^..  ..^^::~~7?YYJ55PGPG&#&#@@@@@
@@&#&GPGP55JJY77?~~::^^..      ..^^::~~7?YYJ55PGPG&#&#@@@@@
&#GPG5JY7?~:^.  ⠀              ⠀  .^:~?7YJ5GPG&#@@@@@@@@@
```

## Features

- Live webcam capture rendered as ASCII art
- Auto-scales to your terminal size
- Debug window showing the pre-processed grayscale feed
- Configurable FPS and threshold controls

## Requirements

- Python 3.7+
- A webcam

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ascii-webcam.git
   cd ascii-webcam
   ```

2. Install dependencies:
   ```bash
   pip install opencv-python numpy Pillow rich
   ```

## Usage

```bash
python src/main.py
```

Press **Ctrl+C** to exit.

A second window will also open showing the live grayscale/thresholded debug feed.

## Configuration

Two constants at the top of `main.py` can be tuned to your liking:

| Variable        | Default | Description                                                  |
|-----------------|---------|--------------------------------------------------------------|
| `threshold_val` | `80`    | Brightness cutoff — higher values drop more detail           |
| `fps`           | `15`    | Target frames per second for the ASCII render loop           |

## How It Works

Each frame goes through a small pipeline before being printed:

1. **Resize** — shrinks the frame to fit the current terminal dimensions (width halved, height corrected for character aspect ratio)
2. **Grayscale** — converts BGR to a single luminance channel
3. **Blur** — a light 1×1 blur smooths out sensor noise
4. **Threshold** — pixels below `threshold_val` are zeroed out to reduce visual noise
5. **Map to ASCII** — each pixel's brightness is mapped to a character from the density string `@B&#GP5JY7?~:^.⠀` and printed via [Rich](https://github.com/Textualize/rich)

## Known Limitations / TODO

- Output can be noisy in low-light conditions (threshold tuning helps)
- No support yet for saving the ASCII output as a video file

## License

MIT
