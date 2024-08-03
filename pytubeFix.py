### Author: Sahand Namvar

# pytubefix docs: https://pytubefix.readthedocs.io/en/latest/index.html
# pytubefix github: https://github.com/JuanBindez/pytubefix/blob/main/docs/user/streams.rst#working-with-streams-and-streamquery

from pytubefix import YouTube
import re

def seconds_to_min_sec(seconds):
    """
    Convert seconds to a tuple of minutes and seconds.

    Args:
        seconds (float): The time in seconds to be converted.

    Returns:
        tuple: A tuple containing minutes and seconds.
    """
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return minutes, seconds

def is_valid_youtube_url(url):
    """
    Validate if the provided URL is a valid YouTube URL.

    Args:
        url (str): The URL to be validated.

    Returns:
        bool: True if valid, False otherwise.
    """
    youtube_regex = (
        r'(https?://)?(www\.)?'
        'youtube(\.com/watch\?v=|\.be/|\.com/embed/|\.com/v/)?'
        '([a-zA-Z0-9_-]{11})'
    )
    return re.match(youtube_regex, url) is not None

def format_file_size(size_in_bytes):
    """
    Convert bytes to megabytes (MB).

    Args:
        size_in_bytes (int): The size in bytes.

    Returns:
        float: The size in MB.
    """
    return size_in_bytes / (1024 * 1024)

def print_divider():
    """
    Print a divider line.
    """
    print("\n" + "#" * 50 + "\n")

def main():
    # Prompt user for YouTube video URL
    url = input("\nEnter YouTube Video URL: ").strip()

    if not is_valid_youtube_url(url):
        print("Error: Invalid YouTube URL. Please provide a valid URL.")
        return

    try:
        # Create YouTube object
        yt = YouTube(url)
    except Exception as e:
        print(f"Error: Could not retrieve YouTube video. {e}")
        return

    # Print video details
    print_divider()
    print(f"Title: {yt.title}")
    print_divider()
    print(f"Views: {yt.views}")
    print_divider()
    print(f"Thumbnail URL: {yt.thumbnail_url}")
    print_divider()
    print(f"Keywords:\n{', '.join(yt.keywords)}")
    print_divider()
    print(f"Metadata:\n{', '.join(yt.metadata)}")
    print_divider()

    try:
        # Get the highest resolution video stream (no audio - DASH stream)
        video_stream = yt.streams.get_highest_resolution(progressive=False)
        print(f"Highest Resolution Video Stream:")
        print(f"itag: {video_stream.itag}")
        print(f"mime_type: {video_stream.mime_type}")
        print(f"resolution: {video_stream.resolution}")
        print(f"fps: {video_stream.fps}")
        print(f"progressive: {video_stream.is_progressive}")
        print(f"type: {video_stream.type}")

        # Get the size of the video stream in MB
        video_size_mb = format_file_size(video_stream.filesize)
        print(f"Video Size: {video_size_mb:.2f} MB")
    except Exception as e:
        print(f"Error: Could not retrieve video stream. {e}")
    
    print_divider()

    try:
        # Get all audio streams
        audio_streams = yt.streams.filter(only_audio=True)

        # Find the audio stream with the highest bitrate
        highest_bitrate_stream = max(audio_streams, key=lambda stream: int(stream.abr.replace('kbps', '')))
        print(f"Highest Bitrate Audio Stream:")
        print(f"itag: {highest_bitrate_stream.itag}")
        print(f"mime_type: {highest_bitrate_stream.mime_type}")
        print(f"abr: {highest_bitrate_stream.abr}")
        print(f"progressive: {highest_bitrate_stream.is_progressive}")
        print(f"type: {highest_bitrate_stream.type}")

        # Get the size of the highest bitrate audio stream in MB
        audio_size_mb = format_file_size(highest_bitrate_stream.filesize)
        print(f"Audio Size: {audio_size_mb:.2f} MB")
    except Exception as e:
        print(f"Error: Could not retrieve audio streams. {e}")

    print_divider()

    try:
        # Get replay heatmap data
        replayed_heatmap = yt.replayed_heatmap

        # Initialize variables to track the segment with the highest intensity
        highest_intensity = 0
        most_replayed_segment = {}

        # Iterate through the heatmap data to find the segment with the highest intensity
        for segment in replayed_heatmap:
            if segment['norm_intensity'] > highest_intensity:
                highest_intensity = segment['norm_intensity']
                most_replayed_segment = segment

        # Convert the start time and duration to minutes and seconds
        start_seconds = most_replayed_segment.get('start_seconds', 0)
        duration = most_replayed_segment.get('duration', 0)
        start_minutes, start_seconds = seconds_to_min_sec(start_seconds)
        duration_minutes, duration_seconds = seconds_to_min_sec(duration)
        norm_intensity = most_replayed_segment.get('norm_intensity', 'N/A')

        # Print the most replayed part of the video with times in minutes and seconds
        print(f"Most replayed segment starts at {start_minutes}m {start_seconds}s, "
              f"lasts for {duration_minutes}m {duration_seconds}s, "
              f"with a normalized intensity of {norm_intensity}.")
    except Exception as e:
        print(f"Error: Could not retrieve replay heatmap data. {e}")

    print_divider()

    # Ask the user if they want to download the streams
    download_choice = input("\nDo you want to download the highest resolution video and the highest bitrate audio stream? (yes/no): ").strip().lower()

    if download_choice in ['yes', 'y']:
        try:
            # Download the highest resolution video stream
            v_stream = yt.streams.get_by_itag(int(video_stream.itag))
            v_stream.download(filename='video.mp4')
            print("Video downloaded successfully.")

            # Download the highest bitrate audio stream
            a_stream = yt.streams.get_by_itag(int(highest_bitrate_stream.itag))
            a_stream.download(filename='audio.mp3')
            print("Audio downloaded successfully.")
        except Exception as e:
            print(f"Error: Could not download streams. {e}")
    else:
        print("Download canceled.")

if __name__ == "__main__":
    main()


'''
some streams listed have both a video codec and audio codec, while others have just video or just audio, this is a result of YouTube supporting a streaming technique called Dynamic Adaptive Streaming over HTTP (DASH).

In the context of pytubefix, the implications are for the highest quality streams; you now need to download both the audio and video tracks and then post-process them with software like FFmpeg to merge them.

The legacy streams that contain the audio and video in a single file (referred to as "progressive download") are still available, but only for resolutions 720p and below.
'''