# Insanely Fast Transcription

This tool provides an easy-to-use interface for transcribing audio from YouTube videos or local audio files using the Insanely Fast Whisper model. It leverages the power of GPU acceleration to provide quick and accurate transcriptions.

## Features

- Download audio from YouTube videos
- Transcribe local audio files
- Utilize GPU acceleration for faster processing
- Support for both Mac (MPS) and NVIDIA (CUDA) GPUs

## Requirements

- Python 3.7+
- pipx (for installing Insanely Fast Whisper)
- FFmpeg (for audio processing)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/doriandarko/insanely-fast-whisper-tool.git
   cd insanely-fast-whisper-tool
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Install Insanely Fast Whisper:
   ```
   pipx install insanely-fast-whisper==0.0.15 --force --pip-args="--ignore-requires-python"
   ```

## Usage

Run the script using Python:
```
python3 transcription.py
```
Follow the prompts to either download a YouTube video or specify a local audio file for transcription.

## Mac vs. NVIDIA GPU Usage

### Mac with Apple Silicon (M1/M2)

The script is configured to use the MPS (Metal Performance Shaders) backend on Mac. It uses the following settings:

- `--device-id mps`
- `--batch-size 4`

These settings are optimized for Mac devices to avoid out-of-memory issues.

### NVIDIA GPUs

For systems with NVIDIA GPUs, you should modify the `transcribe_audio` function in `nemain.py`:

1. Change `--device-id mps` to `--device-id 0` (or the appropriate GPU index)
2. You can increase `--batch-size` to 24 or higher, depending on your GPU's memory

## Notes

- The Insanely Fast Whisper model used is "openai/whisper-large-v3"
- Transcriptions are saved in the "youtube_transcript" folder
- Downloaded audio files are saved in the "youtube_audio" folder

## Troubleshooting

If you encounter any issues, please ensure that:
- FFmpeg is installed and accessible in your system PATH
- You have the latest version of Insanely Fast Whisper installed
- Your GPU drivers are up to date

For Mac users, if you face memory issues, try reducing the batch size further.

## Acknowledgements

This tool uses the Insanely Fast Whisper project, which is powered by 🤗 Transformers, Optimum & flash-attn. Special thanks to the OpenAI Whisper team and the Hugging Face Transformers team.

