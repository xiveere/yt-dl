import yt_dlp
import os
from typing import Optional, Tuple
import re
import tempfile
import glob

def sanitize_filename(filename: str) -> str:
    """
    Sanitizes a string to be used as a filename.
    Removes or replaces invalid characters.
    """
    # Replace invalid characters with spaces
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, ' ', filename)
    # Replace multiple spaces with a single space
    sanitized = re.sub(r'\s+', ' ', sanitized)
    # Remove leading/trailing spaces
    return sanitized.strip()

def get_artist_from_info(info: dict) -> str:
    """
    Extracts artist information from the video/track info.
    """
    # Try different possible artist fields
    artist_fields = ['artist', 'uploader', 'channel', 'creator']
    for field in artist_fields:
        if field in info and info[field]:
            return info[field]
    return "Unknown Artist"

def find_downloaded_file(directory: str, base_name: str) -> Optional[str]:
    """
    Finds the downloaded file in the directory, handling different possible extensions.
    """
    # Look for files that start with the base name
    pattern = os.path.join(directory, f"{base_name}*")
    files = glob.glob(pattern)
    if files:
        # Return the first matching file
        return files[0]
    return None

def download_audio_flac(url: str, output_path: str = "downloads") -> Optional[str]:
    """
    Downloads audio from either YouTube or SoundCloud in FLAC format using yt-dlp.
    
    Args:
        url (str): URL of the audio (YouTube or SoundCloud)
        output_path (str): Directory to save the downloaded files (default: 'downloads')
    
    Returns:
        str: Path to the downloaded FLAC file
    """
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        # First, get the video/track info without downloading
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Unknown Title')
            artist = get_artist_from_info(info)
            
            # Sanitize the title and artist
            title = sanitize_filename(title)
            artist = sanitize_filename(artist)
            
            # Create the final filename format
            final_filename = f"{title} - {artist}.flac"
            final_filename = sanitize_filename(final_filename)
            final_path = os.path.join(output_path, final_filename)
            
            # Create a temporary filename for the download
            temp_base = f"temp_{os.urandom(8).hex()}"
            temp_path = os.path.join(output_path, temp_base)
            
            # Configure yt-dlp options with the temporary filename
            ydl_opts = {
                'format': 'bestaudio/best',  # Select best audio quality
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'flac',
                    'preferredquality': '0',  # 0 is the highest quality
                }],
                'outtmpl': temp_path,
                'verbose': True,
            }
        
        # Download and extract audio
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading and converting to FLAC: {url}")
            info = ydl.extract_info(url, download=True)
            
            # Find the downloaded file
            downloaded_file = find_downloaded_file(output_path, temp_base)
            if downloaded_file:
                if os.path.exists(final_path):
                    os.remove(final_path)  # Remove existing file if it exists
                os.rename(downloaded_file, final_path)
                print(f"Successfully downloaded and converted to FLAC: {final_path}")
                return final_path
            else:
                print("Download failed - could not find downloaded file")
                return None
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        # Clean up any temporary files
        if 'temp_base' in locals():
            temp_files = glob.glob(os.path.join(output_path, f"{temp_base}*"))
            for temp_file in temp_files:
                try:
                    os.remove(temp_file)
                except:
                    pass
        return None

# Example usage
if __name__ == "__main__":
    # Example URLs
    youtube_url = "https://www.youtube.com/watch?v=example"
    soundcloud_url = "https://soundcloud.com/example"
    download_audio_flac(youtube_url)
    download_audio_flac(soundcloud_url) 