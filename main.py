from youtube_transcript_api import YouTubeTranscriptApi
from google import genai
from google.genai import types
from rich.console import Console
from rich.panel import Panel
from rich.markup import escape
from rich.markdown import Markdown
from dotenv import load_dotenv
from markdown_pdf import MarkdownPdf, Section
from yt_dlp import YoutubeDL
from typing import Any
import datetime
import os

version = "1.1.3"
console = Console()
model = "gemini-2.5-flash"

config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(
                        include_thoughts=True,
                        thinking_budget=24576
                    ),
                    tools=[
                    types.Tool(
                        google_search=types.GoogleSearch()
                    )]
                )

load_dotenv()

yt_metadata = {'quiet': True, 'no_warnings': True}

# Feel free to edit your own prompt! 
PERSONA = """You are an expert assistant specializing in detailed and accurate summarization. Your task is to summarize the provided YouTube video transcript thoroughly, ensuring no key details, insights, or action items are omitted.
"""
PROMPT = """
Structure your summary as follows:
# YouTube Title
## YouTube Uploader
1. **Main Topics/Sections:** Identify and list the primary topics or sections covered in the video.
2. **Key Points:** For each topic, summarize the key points discussed. Be comprehensive—include definitions, explanations, examples, and any data or statistics mentioned.
3. **Important Decisions or Conclusions:** Document any significant decisions, conclusions, or takeaways presented in the video.
4. **Action Items or Steps:** List any recommended actions, steps, or instructions provided by the speaker(s). Include any sequence or priority mentioned.
5. **Challenges, Problems, or Solutions:** Note any challenges or problems described, along with any solutions or workarounds discussed. Since this is a bullet list, this is the format:
- Challenge: the challenge
- - Solution: the solution
6. **Notable Quotes or Insights [Grammatically Corrected]:** Include any memorable or significant quotes, statements, or unique insights from the speaker(s) transcript. 
7. **Speakers/Participants:** If multiple speakers are present or referenced, attribute key points, insights, or quotes to them where possible.
8. **Time Frames or Deadlines:** Document any specific time frames, deadlines, or schedules mentioned.
9. **Resources or References:** List any resources, tools, links, or references mentioned during the video.
10. **Next Steps or Follow-Up:** Summarize any next steps, follow-up actions, or future topics suggested at the end of the video.
11. **Sources:** Input the references, separated in new lines, that have been used in verifying factual and accurate information.

Conclude with a brief, high-level overview capturing the essence and purpose of the video.

Ensure the summary is clear, logically structured, and retains all critical information from the transcript. Do not omit any substantive content.

You must use Google Search to verify any information made available from the summary if it is factual and accurate.

You must add in-text citations according to the transcript's start time-stamp noted by "[hh:mm:ss]"

Example
Transcript
[00:06:09] now if you want to replicate this and [00:06:10] you're a
small business you only really [00:06:12] need to create four groups for your [00:06:13]

Summary
If you're a small business, you need to create four groups [00:06:09-00:06:13].

Interpretation
There will be a starting to ending time on the in-text citation.
---
Transcript:
"""
def load_transcript(yt_api: YouTubeTranscriptApi, video_id: str) -> str:
    """
    Loads the transcript using the youtube_transcript_api package with its video_id.
    
    Args:
        yt_api (YouTubeTranscriptApi): The YouTubeTranscriptApi instance.
        video_id (str): The video id.

    Returns:
        full_transcript (str): The full transcript with the start timestamp and transcription.
    """
    with console.status("Loading transcript...", spinner="dots"):
        transcript_data = yt_api.fetch(video_id).to_raw_data()

        full_transcript = " ".join(f"[{datetime.timedelta(seconds=round(segment['start']))}] {segment['text']}" for segment in transcript_data)

    return full_transcript

def save_transcript(transcript: str) -> None:
    """
    Saves the transcript on the default file location name.
    Args:
        transcript (str): The full transcript.
    """
    with console.status("Saving transcript...", spinner="dots"):
        with open("transcript.txt", "w", encoding="utf-8-sig") as f:
            f.write(transcript)
            f.close()

def get_metadata(url: str) -> dict:
    """
    Gets the metadata of the provided complete url of the YouTube video.
    Args:
        url (str): URL of the YouTube video.

    Returns:
        metadata (dict): The metadata of the YouTube video including the title and uploader.
    """
    with YoutubeDL(yt_metadata) as ydl:
        info: dict[str, Any] | None = ydl.extract_info(url, download=False)
        
        if info is None:
            raise Exception
        
        metadata: dict[str, str] = {"title": info.get("title", "Unknown Title"), "uploader": info.get("uploader", "Unknown Uploader")}
        return metadata

def fetch_and_print_transcript() -> None:
    """
    Prompts the user for a YouTube video ID, fetches its transcript,
    and console.prints the transcript as a single, continuous block of text.
    
    Args:
        None
    
    Returns:
        None
    """
    console.clear(home=True)
    
    header = f"""
    This script will fetch the full transcript of a [bold][black on white]You[/black on white][white on red]Tube[/white on red][/bold] video.
    
    To get the Video ID, look at the [lightblue]URL[/lightblue] of the video:
    For example, in '[gray][underline]https://www.youtube.com/watch?v=dQw4w9WgXcQ[/gray][/underline]',
    The Video ID is the part after '[gray]v=[/gray]': [yellow]dQw4w9WgXcQ[/yellow]
    
    Version: {version}
    """
    
    console.print(Panel.fit(header, title="YouTube Transcript Summarizer (YTS)", subtitle="Christian Klein C. Ramos"))    
    video_id = console.input("Please enter the YouTube Video ID: ").strip()

    if not video_id:
        console.print("\n[ERROR] No Video ID was entered. The script will now exit.")
        return

    console.print(f"\nAttempting to fetch the transcript for Video ID: '{video_id}'...")

    try:
        tt = YouTubeTranscriptApi()
        
        # Load the transcript
        full_transcript: str = load_transcript(yt_api=tt, video_id=video_id)
        console.print("\nSuccess! Transcript extracted.\n")
        console.print(Panel(full_transcript, title="Transcript",expand=False))
        
        # Save the transcript
        save_transcript(full_transcript)
        console.print("[green]Transcript saved.[/green]")
        
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        
        response = ""

        with console.status("Getting YouTube metadata...", spinner="dots"):
            metadata = get_metadata(f"https://youtube.com/watch?v={video_id}")
            meta_prompt = f"""YouTube Title: {metadata.get("title")}
            YouTube Uploader: {metadata.get("uploader")}
            """
        # We enable thinking to include thoughts to display on our status. Do note that this requires you using a Gemini model supporting Chain-of-Thought (CoT).
        with console.status("Summarization request sent. Waiting for AI...", spinner="dots") as status:
            response_stream = client.models.generate_content_stream(
                model=model, contents=f"{PERSONA}{meta_prompt}{PROMPT}{full_transcript}",
                config=config
            )
            for chunk in response_stream:
                if chunk.candidates:
                    candidate = chunk.candidates[0]
                    if candidate.content and candidate.content.parts:
                        for part in candidate.content.parts:
                            if part.thought:
                                status.update(Markdown(escape(str(part.text))))
                            elif part.text: 
                                response += part.text

        console.print(Panel(Markdown(escape(response)), title="Summarized Transcript"))

        # Save to current working directory as markdown  and PDF of the summarized transcript.
        with console.status("Saving summarized transcript...", spinner="dots"):
            with open("summarized.md", "w", encoding="utf-8-sig") as f:
                f.write(response)
                f.close()
                console.print("[green]Summarized transcript saved.[/green]")
            pdf = MarkdownPdf(toc_level=4)
            pdf.add_section(Section(response))
            pdf.meta["title"] = "Transcribed PDF"
            pdf.meta["author"] = "YouTube Transcript Summarizer by Lolfaceftw"
            pdf.save(f"{metadata.get('title')}.pdf")

    except Exception as e:
        console.print(f"\n[ERROR] An unexpected error occurred.")
        console.print(f"Details: {escape(str(e))}")

if __name__ == "__main__":
    while True:
        fetch_and_print_transcript()
        do_loop = console.input("Transcribe [yellow]another video[/yellow]? (Y/n) ")
        if do_loop == "Y" or do_loop == "" or do_loop == " ":
            continue
        else:
            exit()
