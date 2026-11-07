from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    from .exporter import export_transcript
    from .extractor import extract_audio
    from .transcriber import transcribe_audio
except ImportError:
    from exporter import export_transcript
    from extractor import extract_audio
    from transcriber import transcribe_audio


def process_file(input_file: str | Path) -> dict[str, Any]:
    input_path = Path(input_file)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    print("Step 1/3: Extracting audio...")
    audio_path = extract_audio(
        input_path,
        output_dir=Path(__file__).parent / "data",
    )

    print("Step 2/3: Transcribing audio...")
    transcript = transcribe_audio(audio_path)

    print("Step 3/3: Creating transcript files...")
    output_files = export_transcript(
        transcript,
        output_name=input_path.stem,
        output_dir=Path(__file__).parent / "transcription",
    )
    print("Created:")
    for output_file in output_files:
        print(f"  {output_file}")

    return transcript


if __name__ == "__main__":
    process_file(Path(__file__).parent / "data" / "Lecture.mp4")
