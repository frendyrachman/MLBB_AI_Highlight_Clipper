import os
import zipfile
import shutil
from ultralytics import YOLO
import cv2
from moviepy.video.io.VideoFileClip import VideoFileClip
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from io import BytesIO
import tempfile

# Directories for uploaded videos and output clips
UPLOAD_FOLDER = 'uploaded_videos'
OUTPUT_FOLDER = 'output_clips'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load YOLO model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'train_size_n', 'weights', 'best.pt')
model = YOLO(MODEL_PATH)

# Create FastAPI instance
app = FastAPI()

# Mount a static directory to serve the output clips
app.mount("/static", StaticFiles(directory=OUTPUT_FOLDER), name="static")

def process_video(video_path):
    """Process the video to generate highlights"""
    clip_output_folder = os.path.join(OUTPUT_FOLDER, 'clips')
    os.makedirs(clip_output_folder, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise HTTPException(status_code=400, detail="Cannot open video file")

    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    frame_skip = int(frame_rate * 1.5)  # Process every 1.5 seconds

    events = []
    highlight_moments = []

    while cap.isOpened():
        current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(source=frame, save=False, conf=0.5)
        if results[0].boxes is None:
            continue

        timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0

        for box in results[0].boxes:
            class_id = int(box.cls)
            class_name = model.names[class_id]
            event = {
                'class_name': class_name,
                'timestamp': timestamp
            }
            events.append(event)

        cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame + frame_skip)

    cap.release()

    # Group highlights
    current_highlight = None
    buffer_start, buffer_end = 7, 10

    for event in events:
        if current_highlight is None:
            current_highlight = {
                'start': max(event['timestamp'] - buffer_start, 0),
                'end': event['timestamp'] + buffer_end
            }
        else:
            if event['timestamp'] <= current_highlight['end'] + 10:
                current_highlight['end'] = event['timestamp'] + buffer_end
            else:
                if current_highlight['end'] - current_highlight['start'] >= 10:
                    highlight_moments.append(current_highlight)
                current_highlight = {
                    'start': max(event['timestamp'] - buffer_start, 0),
                    'end': event['timestamp'] + buffer_end
                }

    if current_highlight and current_highlight['end'] - current_highlight['start'] >= 10:
        highlight_moments.append(current_highlight)

    # Save highlights as video
    zip_path = os.path.join(OUTPUT_FOLDER, 'highlights.zip')
    clip_count = 0

    try:
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for moment in highlight_moments:
                start_time = max(moment['start'], 0)
                end_time = min(moment['end'], VideoFileClip(video_path).duration)

                # Create a new VideoFileClip for the segment
                with VideoFileClip(video_path) as video_segment:
                    clip = video_segment.subclip(start_time, end_time)
                    clip_filename = os.path.join(clip_output_folder, f"highlight_{clip_count}.mp4")
                    clip.write_videofile(clip_filename, codec="libx264", audio_codec="aac")
                    zipf.write(clip_filename, arcname=f"highlight_{clip_count}.mp4")
                    clip_count += 1
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during video processing: {str(e)}")

    return f"Rendering complete. {clip_count} highlights were generated.", zip_path

@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    """Endpoint to upload a video and generate highlights"""
    try:
        # Save uploaded file
        video_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(video_path, "wb") as f:
            f.write(await file.read())

        # Process video and generate highlights
        result_message, result_path = process_video(video_path)

        # Return the generated highlights zip file as a response
        if result_path.endswith(".zip"):
            return FileResponse(result_path, media_type='application/zip', filename="highlights.zip")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/")
async def read_root():
    """Root endpoint"""
    return {"message": "Welcome to the Mobile Legends AI Highlights Generator API"}

# Running the app with FastAPI's Uvicorn server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
