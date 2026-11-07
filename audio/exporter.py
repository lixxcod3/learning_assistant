from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _format_srt_time(seconds: float) -> str:
    milliseconds = round(seconds * 1000)
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds, milliseconds = divmod(remainder, 1_000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


def export_transcript(
    data: dict[str, Any],
    output_name: str = "transcript",
    output_dir: str | Path | None = None,
) -> tuple[Path, Path, Path]:
    """Write one transcript as JSON, plain text, and SRT files."""
    segments = data.get("segments")
    if not isinstance(segments, list):
        raise ValueError("Transcript data must contain a 'segments' list")

    destination = (
        Path(output_dir)
        if output_dir is not None
        else Path(__file__).parent / "transcription"
    )
    destination.mkdir(parents=True, exist_ok=True)

    json_file = destination / f"{output_name}.json"
    text_file = destination / f"{output_name}.txt"
    srt_file = destination / f"{output_name}.srt"

    json_file.write_text(
        json.dumps(data, ensure_ascii=False, indent=4),
        encoding="utf-8",
    )
    text_file.write_text(
        "".join(
            f"[{segment['start']:.2f} - {segment['end']:.2f}]\n"
            f"{segment['text']}\n\n"
            for segment in segments
        ),
        encoding="utf-8",
    )

    with srt_file.open("w", encoding="utf-8") as file:
        for index, segment in enumerate(segments, start=1):
            file.write(
                f"{index}\n"
                f"{_format_srt_time(segment['start'])} --> "
                f"{_format_srt_time(segment['end'])}\n"
                f"{segment['text']}\n\n"
            )

    return json_file, text_file, srt_file
