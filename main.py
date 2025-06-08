import os
import tempfile
import subprocess
import openai

from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def download_audio(youtube_url):
    temp_dir = tempfile.gettempdir()
    output_path = os.path.join(temp_dir, "audio.mp3")
    subprocess.run([
        "yt-dlp",
        "-x", "--audio-format", "mp3",
        "-o", output_path,
        youtube_url
    ], check=True)
    return output_path

def transcribe_audio_with_openai(audio_file_path):
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")
    try:
        with open(audio_file_path, "rb") as f:
            transcript = openai.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                timeout=120  # Optional: set a timeout in seconds
            )
        return transcript.text
    except Exception as e:
        print(f"Transcription error: {e}")
        return ""

def generate_notes_with_openai(transcript):
    system_prompt = ("""
You are an expert note-taker and content summarizer.

Your task is to convert the following English transcript of a spoken Hindi video into beautifully structured notes.

Focus on clarity, structure, and completeness.

### Guidelines:
1. Organize the content into **clear sections with meaningful headings**.
2. Use **bullet points** under each heading to summarize key ideas concisely.
3. If a section has deeper points, use **nested bullet points**.
4. Where applicable, convert content into **tables** (e.g., comparisons, stats).
5. Remove filler words, repetitions, or off-topic content.
6. Maintain the original **tone and intent** of the speaker.
7. Format the final output in **Markdown**.

---
TRANSCRIPT:
{transcript}
---

Now, write the notes below:
""")

    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": transcript}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content

def pipeline(youtube_url):
    audio_file = download_audio(youtube_url)
    print("Audio downloaded")
    transcript = transcribe_audio_with_openai(audio_file)
    print("Transcription done")
    notes = generate_notes_with_openai(transcript)
    print("Notes generated")
    os.remove(audio_file)
    return notes
