import os
import subprocess
import yt_dlp
import re
import glob

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def download_youtube_audio(url, output_folder):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = sanitize_filename(info['title'])
        return find_audio_file(output_folder, title)

def find_audio_file(folder, title):
    pattern = os.path.join(folder, f"{title}.*")
    files = glob.glob(pattern)
    return files[0] if files else None

def transcribe_audio(audio_file):
    command = [
        "insanely-fast-whisper",
        "--file-name", audio_file,
        "--device-id", "mps",
        "--model-name", "openai/whisper-large-v3",
        "--batch-size", "24",
        "--timestamp", "word"
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout

def main():
    choice = input("Enter '1' for YouTube URL or '2' for local audio file path: ")
    
    if choice == '1':
        youtube_url = input("Enter the YouTube URL: ")
        audio_folder = "youtube_audio"
        os.makedirs(audio_folder, exist_ok=True)
        print("Downloading and converting YouTube video...")
        audio_file = download_youtube_audio(youtube_url, audio_folder)
    elif choice == '2':
        audio_file = input("Enter the path to the local audio file: ")
    else:
        print("Invalid choice. Exiting.")
        return

    if audio_file is None:
        print("Error: Could not find the audio file.")
        return

    transcript_folder = "youtube_transcript"
    os.makedirs(transcript_folder, exist_ok=True)
    
    print(f"Audio file to be transcribed: {os.path.abspath(audio_file)}")
    
    if not os.path.exists(audio_file):
        print(f"Error: The audio file '{audio_file}' does not exist.")
        return
    
    print("Transcribing audio...")
    transcription = transcribe_audio(audio_file)
    
    print("Transcription complete. Results:")
    print(transcription)
    
    video_name = os.path.splitext(os.path.basename(audio_file))[0]
    transcript_file = os.path.join(transcript_folder, f"{video_name}.txt")
    with open(transcript_file, "w", encoding="utf-8") as f:
        f.write(transcription)
    print(f"Transcription saved to {transcript_file}")

if __name__ == "__main__":
    main()