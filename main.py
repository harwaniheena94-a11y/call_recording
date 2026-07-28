import os
import time
import pandas as pd

from tqdm import tqdm
from faster_whisper import WhisperModel

# ==========================
# CONFIGURATION
# ==========================

INPUT_FOLDER = "recordings"
TRANSCRIPT_FOLDER = "transcripts"
OUTPUT_FOLDER = "output"

MODEL_SIZE = "medium"     # tiny, base, small, medium, large-v3

# ==========================
# Create folders
# ==========================

os.makedirs(TRANSCRIPT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ==========================
# Load Whisper Model
# ==========================

print("Loading Whisper model...")

model = WhisperModel(
    MODEL_SIZE,
    device="cpu",
    compute_type="int8"
)

print("✅ Model loaded successfully.")

# ==========================
# Supported Formats
# ==========================

SUPPORTED_FORMATS = (
    ".mp3",
    ".wav",
    ".m4a",
    ".flac",
    ".aac",
    ".ogg"
)

files = [
    f for f in os.listdir(INPUT_FOLDER)
    if f.lower().endswith(SUPPORTED_FORMATS)
]

print(f"Found {len(files)} audio files.\n")

results = []

# ==========================
# Process Each Recording
# ==========================

for file in tqdm(files):

    audio_path = os.path.join(INPUT_FOLDER, file)

    start = time.time()

    segments, info = model.transcribe(
        audio_path,
        beam_size=5,
        vad_filter=False
    )

    transcript = ""

    print("Starting transcription...")

    for i, segment in enumerate(segments, 1):
        print(
            f"[{i}] {segment.start:.1f}s --> {segment.end:.1f}s : {segment.text}"
        )
        transcript += segment.text.strip() + " "

    print("Finished transcription.")

    transcript = transcript.strip()

    duration = round(info.duration, 2)

    elapsed = round(time.time() - start, 2)

    # Save Transcript

    txt_name = os.path.splitext(file)[0] + ".txt"

    txt_path = os.path.join(
        TRANSCRIPT_FOLDER,
        txt_name
    )

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(transcript)

    results.append({
        "Recording": file,
        "Duration (sec)": duration,
        "Processing Time (sec)": elapsed,
        "Transcript": transcript
    })

# ==========================
# Save Excel Report
# ==========================

df = pd.DataFrame(results)

excel_path = os.path.join(
    OUTPUT_FOLDER,
    "Call_Transcripts.xlsx"
)

df.to_excel(
    excel_path,
    index=False
)

print("\nDone!")
print(f"Excel saved at : {excel_path}")
print(f"Text files saved in : {TRANSCRIPT_FOLDER}")