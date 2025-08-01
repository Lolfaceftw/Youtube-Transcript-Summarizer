from youtube_transcript_api import YouTubeTranscriptApi
from google import genai
from google.genai import types
from rich.console import Console
from rich.panel import Panel
from rich.markup import escape
from rich.markdown import Markdown
from dotenv import load_dotenv
import os

console = Console()
<<<<<<< HEAD
model = "gemini-2.5-flash"
=======
model = "gemini-2.5-pro"
config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(
                        include_thoughts=True
                    ),
                    tools=[types.Tool(
                        google_search=types.GoogleSearch()
                    )]
                )
>>>>>>> 361f6e5 (time stamp)

load_dotenv()

# Feel free to edit your own prompt! 
PROMPT = """
You are an expert assistant specializing in detailed and accurate summarization. Your task is to summarize the provided YouTube video transcript thoroughly, ensuring no key details, insights, or action items are omitted.

Structure your summary as follows:

1. **Main Topics/Sections:** Identify and list the primary topics or sections covered in the video.
2. **Key Points:** For each topic, summarize the key points discussed. Be comprehensive—include definitions, explanations, examples, and any data or statistics mentioned.
3. **Important Decisions or Conclusions:** Document any significant decisions, conclusions, or takeaways presented in the video.
4. **Action Items or Steps:** List any recommended actions, steps, or instructions provided by the speaker(s). Include any sequence or priority mentioned.
5. **Challenges, Problems, or Solutions:** Note any challenges or problems described, along with any solutions or workarounds discussed.
6. **Notable Quotes or Insights:** Include any memorable or significant quotes, statements, or unique insights from the speaker(s).
7. **Speakers/Participants:** If multiple speakers are present or referenced, attribute key points, insights, or quotes to them where possible.
8. **Time Frames or Deadlines:** Document any specific time frames, deadlines, or schedules mentioned.
9. **Resources or References:** List any resources, tools, links, or references mentioned during the video.
10. **Next Steps or Follow-Up:** Summarize any next steps, follow-up actions, or future topics suggested at the end of the video.

Conclude with a brief, high-level overview capturing the essence and purpose of the video.

Ensure the summary is clear, logically structured, and retains all critical information from the transcript. Do not omit any substantive content.

<<<<<<< HEAD
=======
You must use Google Search to verify any information made available from the summary if it is factual and accurate.

You must add in-text citations according to the transcript's time-stamp noted by "(seconds.ms)"

Example
Transcript
(369.18) now if you want to replicate this and (371.52) you're a
small business you only really (373.259) need to create four groups for your

Summary
If you're a small business, you need to create four groups [00:06:09-00:06:13].

How to Calculate:
Round off the start and end, 369 and 373. Convert the seconds to hh:mm:ss.

How? 369/3600 = 0.1025
00 for hours (before the dot).

after the dot, .1205 * 60 minutes = 6.15 minutes
06 for minutes.

0.15 * 60 seconds = 09 seconds

so, 00:06:09 for the start.

<u>When you will add the in-text citation, strictly re-read the sentence again, check their timestamps on the transcript, and cross-verify. Accuracy of time-stamps are paramount and ensure we only have a 1-2 second error!</u>
>>>>>>> 361f6e5 (time stamp)
---
Transcript:
"""

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
    
    header ="""This script will fetch the full transcript of a [bold][black on white]You[/black on white][white on red]Tube[/white on red][/bold] video.
    \nTo get the Video ID, look at the [lightblue]URL[/lightblue] of the video:
    For example, in '[gray][underline]https://www.youtube.com/watch?v=dQw4w9WgXcQ[/gray][/underline]',
    The Video ID is the part after '[gray]v=[/gray]': [yellow]dQw4w9WgXcQ[/yellow]
    """
    
    console.print(Panel.fit(header, title="YouTube Transcript Extractor (YTE)", subtitle="Christian Klein C. Ramos"))
    video_id = console.input("Please enter the YouTube Video ID: ").strip()

    if not video_id:
        console.print("\n[ERROR] No Video ID was entered. The script will now exit.")
        return

    console.print(f"\nAttempting to fetch the transcript for Video ID: '{video_id}'...")

    try:
        tt = YouTubeTranscriptApi()
        with console.status("Loading transcript...", spinner="dots"):
            transcript_data = tt.fetch(video_id).to_raw_data()

            full_transcript = " ".join(f"({segment['start']}) {segment['text']}" for segment in transcript_data)

        console.print("\nSuccess! Transcript extracted.\n")
        console.print(Panel(full_transcript, title="Transcript",expand=False))

        with console.status("Saving transcript...", spinner="dots"):
            with open("transcript.txt", "w", encoding="utf-8-sig") as f:
                f.write(full_transcript)
                f.close()
                console.print("[green]Transcript saved.[/green]")
        
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        
        response = ""

        # We enable thinking to include thoughts to display on our status. Do note that this requires you using a Gemini model supporting Chain-of-Thought (CoT).
        with console.status("Summarization request sent. Waiting for AI...", spinner="dots") as status:
            response_stream = client.models.generate_content_stream(
                model=model, contents=f"{PROMPT}{full_transcript}",
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(
                        include_thoughts=True
                    )
                )
            )
            for chunk in response_stream:
                for part in chunk.candidates[0].content.parts:
                    if part.thought:
                        thought_text = part.text.strip()
                        status.update(Markdown(escape(thought_text)))
                    elif part.text:
                        response += part.text

        console.print(Panel(Markdown(escape(response)), title="Summarized Transcript"))

        # Save to current working directory as markdown of the summarized transcript.
        with console.status("Saving summarized transcript...", spinner="dots"):
            with open("summarized.md", "w", encoding="utf-8-sig") as f:
                f.write(response)
                f.close()
                console.print("[green]Summarized transcript saved.[/green]")

    except Exception as e:
        console.print(f"\n[ERROR] An unexpected error occurred.")
        console.print(f"Details: {escape(str(e))}")

if __name__ == "__main__":
    fetch_and_print_transcript()
