#!/usr/bin/env python3
"""
BrailleVision -- live web app (Gradio). Deploy free on Hugging Face Spaces.

Reuses the SAME cell-classifier model + reading-order decode as app.py.
Webcam stream -> YOLO -> annotated view + decoded text + a Speak button.

Opening the Space URL on a PHONE uses the phone camera -> instant "mobile app"
experience, with the phone's better close-up camera for Braille.

Deploy on Hugging Face Spaces:
  1. New Space -> SDK = Gradio, hardware = CPU (free; fine for a nano model)
  2. Upload:  this file renamed to  app.py  ,  requirements.txt  ,  best.pt
  3. It builds and goes live at https://huggingface.co/spaces/<you>/<name>
Local quick test:  python app_web.py   (or demo.launch(share=True) for a temp public link)
"""

import os
import tempfile
from collections import deque, Counter

import cv2
import numpy as np
import gradio as gr
from ultralytics import YOLO
from gtts import gTTS

MODEL_PATH = os.environ.get("MODEL_PATH", "best.pt")
model = YOLO(MODEL_PATH)
names = model.names
_hist = deque(maxlen=5)          # simple temporal smoothing (single-user demo)


def reading_order(dets, line_tol_frac=0.6, space_mult=1.7):
    """dets: list of (cx, cy, label, box_height) -> text in reading order."""
    if not dets:
        return ""
    med_h = float(np.median([d[3] for d in dets]))
    dets = sorted(dets, key=lambda d: d[1])
    lines, cur = [], [dets[0]]
    for d in dets[1:]:
        if abs(d[1] - cur[-1][1]) <= med_h * line_tol_frac:
            cur.append(d)
        else:
            lines.append(cur)
            cur = [d]
    lines.append(cur)
    out = []
    for ln in lines:
        ln = sorted(ln, key=lambda d: d[0])
        text = ln[0][2]
        for prev, d in zip(ln, ln[1:]):
            if (d[0] - prev[0]) > med_h * space_mult:
                text += " "
            text += d[2]
        out.append(text)
    return "\n".join(out)


def process(frame_rgb, conf):
    """Runs on each streamed webcam frame. Returns annotated image + reading."""
    if frame_rgb is None:
        return None, ""
    bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)        # ultralytics expects BGR
    res = model.predict(bgr, conf=conf, verbose=False)[0]
    annotated = frame_rgb.copy()
    dets = []
    for b in res.boxes:
        x1, y1, x2, y2 = b.xyxy[0].tolist()
        label = names[int(b.cls[0])]
        dets.append(((x1 + x2) / 2, (y1 + y2) / 2, label, y2 - y1))
        cv2.rectangle(annotated, (int(x1), int(y1)), (int(x2), int(y2)), (0, 230, 0), 2)
        cv2.putText(annotated, label, (int(x1), int(y1) - 6),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 230, 0), 2)
    _hist.append(reading_order(dets))
    stable = Counter(_hist).most_common(1)[0][0] if _hist else ""
    return annotated, stable


def speak(text):
    """Turn the current reading into speech (gTTS) for the audio player."""
    if not text or not text.strip():
        return None
    f = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    gTTS(text.replace("\n", ". ")).save(f.name)
    return f.name


with gr.Blocks(title="BrailleVision", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        "# 👁️ BrailleVision\n"
        "Point your camera at embossed Braille under good side-lighting. "
        "The reading appears below — tap **Speak** to hear it."
    )
    with gr.Row():
        cam = gr.Image(sources=["webcam"], streaming=True, type="numpy", label="Camera")
        out_img = gr.Image(type="numpy", label="Detected cells")
    conf = gr.Slider(0.05, 0.9, value=0.35, step=0.05, label="Detection confidence")
    text = gr.Textbox(label="Reading", lines=2, show_copy_button=True)
    with gr.Row():
        speak_btn = gr.Button("🔊 Speak", variant="primary")
        clear_btn = gr.Button("Clear")
    audio = gr.Audio(label="Speech", autoplay=True)

    cam.stream(process, inputs=[cam, conf], outputs=[out_img, text],
               stream_every=0.2, time_limit=600)
    speak_btn.click(speak, inputs=text, outputs=audio)
    clear_btn.click(lambda: (_hist.clear(), "")[1], outputs=text)

if __name__ == "__main__":
    demo.launch()
