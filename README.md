# BrailleVision 👁️ — Real-Time Physical Braille → Text & Speech

Reads **real embossed Braille** from a camera and converts it to English **text and speech**, fully **on-device / offline**. Built with a fine-tuned **YOLO** cell detector + a deterministic reading-order decoder. Ships as an **Android APK** (on-device) and a **Python CLI / web app** for local verification.

- 🎥 **Demo video:** `<YOUR VIDEO LINK>`
- 📱 **Android APK:** `<YOUR GITHUB RELEASE LINK>`
- 🌐 **Live web demo (optional):** `<YOUR HF SPACE LINK>`

---

## ✅ Verify locally in 3 commands (for judges)

```bash
git clone <YOUR REPO URL> && cd <repo>
pip install -r requirements.txt
python inference.py --source sample_inputs/test_braille.jpg --weights model/best.pt
```

This prints the decoded Braille text and writes an annotated image + `.txt` to `sample_outputs/`. Run on a folder with `--source sample_inputs/`. The trained weights (`model/best.pt`) are committed in this repo, so **no extra access is needed** to verify the model.

---

## What it does / approach

1. **Capture** under oblique side-lighting so the colorless dots cast shadows.
2. **Detect** each Braille cell with a YOLO model that classifies it as a letter.
3. **Decode** detections into text (sort left→right, group lines by row, gaps→spaces).
4. **Speak** the result (offline TTS).

Decode is deterministic (no contractions / Grade-1), keeping the system robust and debuggable.

## Tech stack
- **Model:** Ultralytics YOLO (YOLO26-n / -s), trained on Roboflow + own captures, exported to **`.pt`** and **`.tflite`**.
- **Inference:** Python (`ultralytics`, OpenCV, NumPy); Flutter `ultralytics_yolo` on Android.
- **Speech:** `flutter_tts` (mobile), macOS `say` / `pyttsx3` (desktop), `gTTS` (web).
- **Model type:** YOLO (object detection) + rule-based decoder = **Hybrid**.

---

## Repository structure
```
<team-name>-braillevision/
├── README.md                 ← this file
├── requirements.txt
├── setup_instructions.md
├── inference.py              ← local verification entry point
├── evaluate.py               ← held-out metrics (exact-match, CER)
├── app.py                    ← desktop live webcam demo
├── app_web.py                ← web-app fallback (Gradio)
├── model/
│   ├── best.pt               ← trained weights (committed; ~6–12 MB)
│   ├── best.tflite           ← mobile export
│   └── model_info.md
├── training/
│   ├── train_kaggle.py       ← training + TFLite export (Kaggle)
│   ├── training_logs/        ← screenshots / logs
│   └── results/              ← results.png, confusion_matrix.png
├── dataset/
│   ├── data.yaml
│   ├── sample_images/
│   ├── sample_annotations/
│   └── dataset_info.md
├── sample_inputs/            ← real Braille photos for testing
├── sample_outputs/           ← inference.py writes here
├── flutter_app/              ← Android app (see FLUTTER_APK_SETUP.md)
├── demo/
│   ├── demo_video_link.txt
│   └── screenshots/
├── ai_tools_disclosure.md
└── LICENSE                   ← AGPL-3.0
```

---

## Dataset
- **Source:** Roboflow Universe "Braille Detection" (`yapayzeka/braille-detection-vxtp1`) + our own captured photos.
- **Format:** YOLO (`images/` + `labels/` txt boxes), classes = A–Z.
- Full details, counts, splits, preprocessing, and samples: **[`dataset/dataset_info.md`](dataset/dataset_info.md)**.
- `dataset/data.yaml` is included; full dataset link: `<DATASET DOWNLOAD LINK>`.

## Model & weights
- `model/best.pt` (committed) and `model/best.tflite` (mobile).
- Architecture, input size, classes, and metrics: **[`model/model_info.md`](model/model_info.md)**.

## Training (reproducible)
- Script: `training/train_kaggle.py` (run on Kaggle GPU). Command, hyperparameters, epochs, and logs are documented in `model/model_info.md` and `training/`.
- Re-validate any weights: `python evaluate.py model/best.pt` (expects `test/labels.csv`).

## Evaluation (held-out, our capture rig)
| Model | exact-match | mean CER | mAP50 | FPS (device) |
|------|------|------|------|------|
| A (fine-tuned) | `<XX%>` | `<0.XX>` | `<0.XX>` | `<XX>` |
| B (yolo26s)    | `<XX%>` | `<0.XX>` | `<0.XX>` | `<XX>` |

Reproduce with `evaluate.py`. Training curves / confusion matrix in `training/results/`.

---

## 📱 Android APK
Install the prebuilt APK from the release above, or build it: see **`FLUTTER_APK_SETUP.md`**. Runs the `.tflite` model on-device with the phone camera, fully offline.

## 🌐 Web app (optional fallback)
```bash
python app_web.py      # local; or deploy app_web.py to a Hugging Face Space
```

## 🖥️ Desktop live demo
```bash
python app.py --weights model/best.pt        # q quit · s speak · space pause
```

---

## Model verification access
The trained model is **committed directly** (`model/best.pt`, `model/best.tflite`) — judges can load and run it immediately with `inference.py`. No private access required. Contact for live verification: `<PHONE / EMAIL>`.

## AI tools used
Disclosed in **[`ai_tools_disclosure.md`](ai_tools_disclosure.md)**.

## Hackathon timeline
Developed during BrailleVision Hackathon 2026. The git commit history reflects incremental progress across the official window.

## Limitations
Grade-1 (uncontracted) Braille; single-sided pages; best under even oblique lighting (tuned to our capture rig).

## License
AGPL-3.0 (Ultralytics YOLO + the Flutter plugin are AGPL-3.0). See `LICENSE`.
