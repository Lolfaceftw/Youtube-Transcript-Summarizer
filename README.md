# YouTube Transcript Summarizer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Description/Overview

The YouTube Transcript Summarizer is a Python script that fetches the transcript of a YouTube video and uses Google's Gemini AI to generate a comprehensive summary. This tool is designed for developers, researchers, and content creators who need to quickly understand the content of a video without watching it in its entirety. In short, this project provides a quick, AI-powered summary of any YouTube video with a transcript.

## Features

*   **Fetch Transcripts:** Extracts the full transcript from any YouTube video using its video ID.
*   **AI-Powered Summarization:** Utilizes the Gemini AI model to create detailed and structured summaries of the video content.
*   **Structured Summaries:** The AI is prompted to provide summaries that include main topics, key points, action items, and more.
*   **Save Locally:** Saves both the full transcript and the summarized version as local files (`transcript.txt` and `summarized.md`).
*   **Interactive CLI:** A user-friendly command-line interface guides the user through the process.
*   **Rich Console Output:** Uses the `rich` library to present information in a clear and visually appealing format.

## Requirements/Prerequisites

Before you begin, ensure you have the following installed:

*   Python 3.6+
*   pip (Python package installer)

You will also need the following Python libraries:

*   `youtube_transcript_api`
*   `google-genai`
*   `rich`
*   `python-dotenv`

A Google Gemini API key is also required.

## Installation/Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Lolfaceftw/Youtube-Transcript-Summarizer.git
    cd Youtube-Transcript-Summarizer
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    Create a file named `.env` in the root directory of the project and add your Google Gemini API key:
    ```
    GEMINI_API_KEY="<YOUR_API_KEY>"
    ```

## Usage

To run the script, execute the following command in your terminal:

```bash
python main.py
```

The script will then prompt you to enter the YouTube Video ID. To find the Video ID, look at the URL of the video. For example, in `https://www.youtube.com/watch?v=dQw4w9WgXcQ`, the Video ID is `dQw4w9WgXcQ`.

After you provide the ID, the script will:
1.  Fetch the video's transcript.
2.  Display the full transcript.
3.  Save the transcript to `transcript.txt`.
4.  Send the transcript to the Gemini AI for summarization.
5.  Display the summarized transcript.
6.  Save the summary to `summarized.md`.

## Configuration

The primary configuration required is your Google Gemini API key, which must be stored in a `.env` file in the project's root directory.

*   **`GEMINI_API_KEY`**: Your API key for accessing the Google Gemini model.

You can also modify the `PROMPT` constant within `main.py` to customize the instructions given to the AI for summarization.

## API/Function Reference

### `fetch_and_print_transcript()`

This is the main function of the script.

*   **Description:** Prompts the user for a YouTube video ID, fetches the transcript, prints it, generates a summary using Gemini AI, prints the summary, and saves both the transcript and the summary to local files.
*   **Parameters:** None.
*   **Returns:** None.

## Testing

Currently, the project does not have a dedicated test suite. To test the functionality, you can run the `main.py` script with a valid YouTube video ID that is known to have a transcript.

## Contributing Guidelines

Contributions are welcome! If you have suggestions for improvements, please open an issue or submit a pull request.

1.  **Fork the repository.**
2.  **Create a new branch:** `git checkout -b feature-or-fix-name`
3.  **Make your changes.**
4.  **Commit your changes:** `git commit -m 'Add some feature'`
5.  **Push to the branch:** `git push origin feature-or-fix-name`
6.  **Open a pull request.**

Please make sure to update tests as appropriate.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.

## Changelog/Version History

All notable changes to this project will be documented in the `CHANGELOG.md` file.

## Acknowledgments/Credits

*   **[youtube_transcript_api](https://pypi.org/project/youtube-transcript-api/):** For providing an easy way to fetch YouTube video transcripts.
*   **[Google Gemini](https://ai.google.dev/):** For the powerful summarization capabilities.
*   **[Rich](https://github.com/Textualize/rich):** For beautiful and informative console output.

## Contact/Support

If you encounter any issues or have questions, please file an issue on the [GitHub issues page](https://github.com/Lolfaceftw/Youtube-Transcript-Summarizer/issues).