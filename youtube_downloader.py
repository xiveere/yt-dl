import yt_dlp
import os

def download_youtube_flac(url, output_path="downloads"):
    """
    Downloads a YouTube video and extracts the audio in FLAC format using yt-dlp.
    
    Args:
        url (str): YouTube video URL
        output_path (str): Directory to save the downloaded files (default: 'downloads')
    
    Returns:
        str: Path to the downloaded FLAC file
    """
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        # Configure yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',  # Select best audio quality
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'flac',
                'preferredquality': '0',  # 0 is the highest quality
            }],
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'verbose': True,
        }
        
        # Download and extract audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading and converting to FLAC: {url}")
            info = ydl.extract_info(url, download=True)
            flac_path = os.path.join(output_path, f"{info['title']}.flac")
            print(f"Successfully downloaded and converted to FLAC: {flac_path}")
            return flac_path
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # Example YouTube URL
    youtube_url = "https://www.youtube.com/watch?v=example"
    download_youtube_flac(youtube_url) 