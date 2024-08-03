# YouTube Video and Audio Stream Analyzer (& Downloader)

This project is a Python script that uses the `pytubefix` library to analyze YouTube videos. It provides functionalities to extract various details about the video, such as metadata, highest resolution streams, highest bitrate audio, and more. Additionally, it includes features to download the highest resolution video and highest bitrate audio stream, if desired.

## Introduction

This script was created out of curiosity and a desire to learn more about working with YouTube data and media streams. It leverages the `pytubefix` library to fetch and analyze various aspects of a YouTube video, including the ability to download streams if needed.

## Features

- Retrieve and display video metadata (title, views, thumbnail URL, keywords, and more).
- Identify and display the highest resolution video stream available.
- Find and display the audio stream with the highest bitrate.
- Calculate and display the size of both video and audio streams.
- Show the most replayed segment of the video based on heatmap data.
- Optionally download the highest resolution video and highest bitrate audio stream.

## Requirements

- Python 3.6 or higher
- `pytubefix` library (installation instructions below)
- FFmpeg (for merging audio and video streams if necessary)

## Installation
1. **Clone repo:** it clone https://github.com/sahandnamvar/youtube-analyzer-downloader.git
2. **Install packages:** pip install pytubefix
3. **Run the script:** python youtube_stream_analyzer.py

## Key Concepts for working with PytubeFix

### Dynamic Adaptive Streaming over HTTP (DASH)

YouTube uses a streaming technique called **Dynamic Adaptive Streaming over HTTP (DASH)**. This allows YouTube to provide different video and audio qualities dynamically based on the viewer's network conditions. Consequently, the highest quality streams are split into separate video and audio tracks, which means you often need to download and merge them using tools like FFmpeg or Canva. Legacy streams with both video and audio (also known as **Progressive**) in a single file are available for resolutions up to 720p.