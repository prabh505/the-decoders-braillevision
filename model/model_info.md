# Model Info

## Architecture
- **Family:** Ultralytics YOLO (object detection).
- **Variant:** `yolo26n` (Account A, fine-tuned) / `yolo26s` (Account B). Shipped model: `<A or B>`.
- **Task:** detect each Braille cell and classify it as a letter.
- **Input size:** 640 × 640.
- **Classes (<N>):** A–Z  `<list exactly as in dataset/data.yaml>`.

## Files
| File | Format | Use |
|------|--------|-----|
| `model/best.pt`     | PyTorch | local inference / evaluation (inference.py, evaluate.py) |
| `model/best.tflite` | TFLite (int8) | on-device Android app |

## Training summary
- **Base / warm-start:** `<yolo26n.pt / existing prototype weights>`
- **Dataset:** Roboflow `yapayzeka/braille-detection-vxtp1` + own captures (see `dataset/dataset_info.md`)
- **Command:** `training/train_kaggle.py` on Kaggle GPU (P100 / T4)
- **Hyperparameters:** imgsz=640, epochs=`<80/120>`, batch=16, optimizer=auto, patience=25
- **Augmentation (B):** degrees=8, translate=0.1, scale=0.5, shear=2, perspective=0.0005, hsv_v=0.5, mosaic=1.0, mixup=0.1
- **Hardware:** Kaggle GPU; **Trained during the hackathon window** (see commit history + `training/training_logs/`)

## Metrics (held-out test set)
| Metric | Value |
|--------|-------|
| mAP50      | `<0.XX>` |
| mAP50-95   | `<0.XX>` |
| exact-match (string) | `<XX%>` |
| mean CER   | `<0.XX>` |

Training curves and confusion matrix: `training/results/results.png`, `training/results/confusion_matrix.png`.

## Load & run
```python
from ultralytics import YOLO
m = YOLO("model/best.pt")
print(m.names)                 # class names
m.predict("sample_inputs/test_braille.jpg", conf=0.35)
```
