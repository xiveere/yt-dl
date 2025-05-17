import streamlit as st
from youtube_downloader import download_audio_flac
import os
import time
from typing import List

st.set_page_config(
    page_title="Audio FLAC Downloader",
    page_icon="🎵",
    layout="centered"
)

st.title("Audio FLAC Downloader 🎵")
st.markdown("Download audio from YouTube and SoundCloud in high-quality FLAC format")

# Initialize session state for queue if it doesn't exist
if 'download_queue' not in st.session_state:
    st.session_state.download_queue = []
if 'completed_downloads' not in st.session_state:
    st.session_state.completed_downloads = []

# Input method selection
input_method = st.radio(
    "Choose input method:",
    ["Single URL", "Multiple URLs"],
    horizontal=True
)

# URL input based on selection
if input_method == "Single URL":
    url = st.text_input("Enter URL:", placeholder="https://www.youtube.com/watch?v=... or https://soundcloud.com/...")
    if url and st.button("Add to Queue", type="primary"):
        if url not in st.session_state.download_queue:
            st.session_state.download_queue.append(url)
            st.success(f"Added to queue: {url}")
else:
    urls_text = st.text_area(
        "Enter URLs (one per line):",
        placeholder="https://www.youtube.com/watch?v=...\nhttps://soundcloud.com/...",
        height=150
    )
    if urls_text and st.button("Add to Queue", type="primary"):
        new_urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
        for url in new_urls:
            if url not in st.session_state.download_queue:
                st.session_state.download_queue.append(url)
        st.success(f"Added {len(new_urls)} URLs to queue")

# Optional output directory selection
output_dir = st.text_input("Output Directory (optional):", value="downloads")

# Show current queue
if st.session_state.download_queue:
    st.markdown("### Current Queue")
    for i, url in enumerate(st.session_state.download_queue):
        col1, col2 = st.columns([4, 1])
        with col1:
            platform = "YouTube" if "youtube.com" in url or "youtu.be" in url else "SoundCloud"
            st.text(f"{i+1}. [{platform}] {url}")
        with col2:
            if st.button("Remove", key=f"remove_{i}"):
                st.session_state.download_queue.pop(i)
                st.rerun()

# Download button for queue
if st.session_state.download_queue and st.button("Download Queue", type="primary"):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, url in enumerate(st.session_state.download_queue):
        platform = "YouTube" if "youtube.com" in url or "youtu.be" in url else "SoundCloud"
        status_text.text(f"Downloading {i+1}/{len(st.session_state.download_queue)}: [{platform}] {url}")
        try:
            flac_path = download_audio_flac(url, output_dir)
            if flac_path and os.path.exists(flac_path):
                st.session_state.completed_downloads.append({
                    'url': url,
                    'path': flac_path,
                    'platform': platform,
                    'status': 'success'
                })
            else:
                st.session_state.completed_downloads.append({
                    'url': url,
                    'path': None,
                    'platform': platform,
                    'status': 'failed'
                })
        except Exception as e:
            st.session_state.completed_downloads.append({
                'url': url,
                'path': None,
                'platform': platform,
                'status': 'error',
                'error': str(e)
            })
        
        progress = (i + 1) / len(st.session_state.download_queue)
        progress_bar.progress(progress)
    
    # Clear queue after download
    st.session_state.download_queue = []
    st.rerun()

# Show completed downloads
if st.session_state.completed_downloads:
    st.markdown("### Completed Downloads")
    for download in st.session_state.completed_downloads:
        if download['status'] == 'success':
            st.success(f"✅ [{download['platform']}] {os.path.basename(download['path'])}")
            st.info(f"Saved to: {download['path']}")
        else:
            st.error(f"❌ [{download['platform']}] Failed to download: {download['url']}")
            if 'error' in download:
                st.error(f"Error: {download['error']}")

# Clear completed downloads button
if st.session_state.completed_downloads and st.button("Clear History"):
    st.session_state.completed_downloads = []
    st.rerun()

# Add some helpful information
st.markdown("---")
st.markdown("""
### How to use:
1. Choose input method (Single URL or Multiple URLs)
2. Enter YouTube or SoundCloud URL(s)
3. Add to queue
4. (Optional) Choose an output directory
5. Click 'Download Queue' to process all downloads
6. Wait for the downloads to complete

The files will be saved in FLAC format with the highest possible quality.

### Supported Platforms:
- YouTube (youtube.com, youtu.be)
- SoundCloud (soundcloud.com)
""") 