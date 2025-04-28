# Mobile Legends AI Highlights Generator

Welcome to the **Mobile Legends AI Highlights Generator**!  
This application automatically detects exciting moments from your Mobile Legends gameplay videos and generates highlight clips using a YOLOv8-based AI model.

✨ **Hosted on Hugging Face Space:** [Hugging Face Link](https://huggingface.co/spaces/frendyrachman/mlbb-ai-clipper)

---

## 🚀 Features

- **Automatic Highlights Detection**  
  Detects key events in gameplay videos using a YOLOv8 object detection model.

- **Custom Model**  
  Uses a fine-tuned YOLOv8 model hosted on Hugging Face Hub.

- **Highlight Clipping**  
  Clips interesting moments and packages them into a downloadable `.zip` file.

- **User-friendly Interface**  
  Simple upload, process, and download workflow powered by Gradio.

---

## 🧰 Tech Stack

- **Python**  
- **YOLOv8** (via Ultralytics)
- **OpenCV** (for video frame capture)
- **MoviePy** (for video cutting and saving)
- **Gradio** (for the web interface)
- **Hugging Face Hub** (for model storage and download)

---

## 📦 Installation and Usage (Local Development)

1. **Clone this repository**
   ```bash
   git clone https://github.com/your-username/mlbb-ai-clipper.git
   cd mlbb-ai-clipper
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   python app.py
   ```

4. **Access the app**
   Open your browser at `http://localhost:7860/`

---

## 📹 How It Works

1. **Upload a video** (supported formats: MP4, AVI, MOV, MKV).
2. **AI model analyzes** the video and identifies key events every ~1.5 seconds.
3. **Clips** are generated around detected events (+7 seconds before and +10 seconds after).
4. **Download** a `.zip` file containing all highlights.

---

## 📁 Project Structure

```
├── uploaded_videos/    # Folder to store uploaded videos
├── output_clips/       # Folder to store generated highlight clips
├── app.py              # Main application file
└── README.md           # Project documentation
```

---

## ⚠️ Important Notes

- The app currently processes video every **1.5 seconds** for efficiency.
- It groups close-together events into one clip if events occur within **10 seconds** of each other.
- Minimum clip length is **10 seconds** to ensure meaningful highlights.
- Running this app locally or on limited resources (like free HF Spaces) may be slower for long videos.

---

## 🤝 Acknowledgements

- YOLOv8 by [Ultralytics](https://ultralytics.com/)
- Hugging Face for model and app hosting
- Gradio for building simple ML web apps

---

## 📢 Future Improvements

- Allow users to adjust event detection thresholds dynamically.
- Add support for other games and more flexible model selection.
- Improve event grouping logic with smarter timeline algorithms.

---

## 📬 Contact

Feel free to connect or report issues:

- **Author:** [Frendy Rachman](https://huggingface.co/spaces/frendyrachman/mlbb-ai-auto-clipper)
- **Email:** frendyrachman@gmail.com"# MLBB_AI_Highlight_Clipper" 
