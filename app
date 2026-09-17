import os
import hashlib
import cv2

def calculate_file_hash(file_path):
    """
    Generates a SHA-256 hash of a file.
    This hash serves as the unique digital fingerprint for the Blockchain registry.
    """
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            # Read file in small chunks to handle large video files without crashing memory
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return None

def extract_video_frames(video_path, output_folder, frame_interval=10):
    """
    Extracts frames from a video file at a given interval.
    These frames will later be passed into your Deep Learning model for fake detection.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    video_capture = cv2.VideoCapture(video_path)
    if not video_capture.isOpened():
        print(f"❌ Error: Could not open video file {video_path}")
        return False

    frame_count = 0
    saved_count = 0

    print(f"🎬 Processing video: {video_path}...")
    
    while True:
        success, frame = video_capture.read()
        if not success:
            break  # End of video stream

        # Extract every 'Nth' frame to save storage and speed up AI inference
        if frame_count % frame_interval == 0:
            frame_name = f"frame_{saved_count:04d}.jpg"
            frame_path = os.path.join(output_folder, frame_name)
            
            # Save the frame as an image file
            cv2.imwrite(frame_path, frame)
            saved_count += 1

        frame_count += 1

    video_capture.release()
    print(f"✅ Successfully extracted {saved_count} frames to folder: '{output_folder}'")
    return True

# 🚀 Execution Block
if __name__ == "__main__":
    # Define your paths (Replace 'sample_video.mp4' with an actual video filename)
    VIDEO_FILE = "sample_video.mp4" 
    OUTPUT_DIR = "extracted_frames"

    print("--- Phase 1: File Processing Startup ---")

    # 1. Generate Blockchain Hash
    file_hash = calculate_file_hash(VIDEO_FILE)
    if file_hash:
        print(f"🔒 File SHA-256 Hash: {file_hash}")
        print("   (Save this string! This is what you will write to your Smart Contract later.)\n")
    else:
        print(f"⚠️ Please place a valid video file named '{VIDEO_FILE}' in this directory to test.\n")

    # 2. Extract Frames for AI Processing
    if os.path.exists(VIDEO_FILE):
        # frame_interval=10 means it saves every 10th frame of the video
        extract_video_frames(VIDEO_FILE, OUTPUT_DIR, frame_interval=10)
