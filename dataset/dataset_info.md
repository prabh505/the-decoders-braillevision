# Dataset Info

## Source
- **Primary:** Roboflow Universe — *Braille Detection* (`yapayzeka/braille-detection-vxtp1`), ~1,324 labelled-letter images.
  Link: https://universe.roboflow.com/yapayzeka/braille-detection-vxtp1
- **Own data:** `<N>` photos captured with our oblique-light rig (varied position / distance / lighting).
- Full/combined dataset download: `<DRIVE or ROBOFLOW LINK>`

## Annotation format
- **YOLO detection** — one `.txt` per image: `class x_center y_center width height` (normalized).
- A representative `data.yaml` is in `dataset/data.yaml`; samples in `dataset/sample_images/` + `dataset/sample_annotations/`.

## Classes (<N>)
`A B C D E F G H I J K L M N O P Q R S T U V W X Y Z`  (edit to match `data.yaml` exactly).

## Preprocessing
- Capture under oblique side-lighting (dots cast shadows).
- (Optional) CLAHE contrast enhancement; resize to 640.
- Roboflow auto-orient + resize on export.

## Split
| Split | Images |
|-------|--------|
| train | `<n>` |
| val   | `<n>` |
| test (held-out, our rig — never trained on) | `<n>` |

## YOLO folders (in the full dataset)
```
images/train  images/val   labels/train  labels/val   data.yaml
```

## Sample images
See `dataset/sample_images/` (a few representative inputs) and `sample_inputs/` (real test photos).
