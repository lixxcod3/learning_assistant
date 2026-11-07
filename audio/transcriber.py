from faster_whisper import WhisperModel

model = WhisperModel (
    "base",
    device="cpu",
    compute_type="int8"
)

def transcribe_audio(audio_file):
    
    segments, info=model.transcribe(
        audio_file,
        beam_size=5,
        vad_filter=True
    )
    
    result = []
    
    for segment in segments:
        results.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text.strip()
        })

    return {
        "language": info.language,
        "duration": info.duration,
        "segments": results
    }