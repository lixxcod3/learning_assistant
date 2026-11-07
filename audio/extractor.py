import subprocess
from pathlib import Path
import imageio_ffmpeg

SUPPORTED_FORMATS = {
    ".mp3", ".wav", ".m4a", ".aac",
    ".flac", ".ogg", ".mp4", ".mov", ".mkv"
}

def extract_audio(input_file, output_dir="data"):

    input_file = Path(input_file)

    if not input_file.exists():
        raise FileNotFoundError(f"File not found: {input_file}")

    if input_file.suffix.lower() not in SUPPORTED_FORMATS:
        raise ValueError("Unsupported file format")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{input_file.stem}.wav"

    # Fetch the exact path to the bundled FFmpeg executable
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    command = [
        ffmpeg_exe,
        "-y",
        "-i", str(input_file),
        "-vn",
        "-ac", "1",
        "-ar", "16000",
        "-c:a", "pcm_s16le",
        str(output_file)
    ]

    subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True
    )

    return str(output_file)