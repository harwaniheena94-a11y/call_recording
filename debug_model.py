import os
from faster_whisper import download_model
from faster_whisper import WhisperModel

print("Downloading model...")

model_path = download_model("tiny")

print("Downloaded to:", model_path)

print("Loading model from local path...")

model = WhisperModel(
    model_path,
    device="cpu",
    compute_type="int8"
)

print("SUCCESS!")