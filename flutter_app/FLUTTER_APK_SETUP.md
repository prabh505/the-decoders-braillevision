# BrailleVision — Flutter → APK Setup

How to turn the trained model + the Dart files (`braille_screen.dart`, `main.dart`) into a downloadable APK. Work **inside the official example app** — it already has the Gradle config, manifest, and camera permission set up, which removes most of the risk.

---

## 0. Prerequisites
```bash
flutter doctor        # all green for "Android toolchain" + a connected device/emulator
```
Enable **USB debugging** on an Android phone and plug it in (or start an emulator). The phone's rear camera is better for close-up Braille than a webcam.

---

## 1. Get the example app + add dependencies
```bash
git clone https://github.com/ultralytics/yolo-flutter-app
cd yolo-flutter-app/example
flutter pub add ultralytics_yolo flutter_tts
flutter pub get
```
Resulting `pubspec.yaml` deps (versions resolve to latest compatible):
```yaml
dependencies:
  flutter:
    sdk: flutter
  ultralytics_yolo: ^0.3.1     # latest from pub.dev
  flutter_tts: ^4.2.0          # latest from pub.dev
```

---

## 2. ⚠️ CRITICAL GATE — validate on the phone with a STOCK model first
Before touching your own model, run the example app as-is (it downloads an official model like `yolo11n`) and confirm **live detection works on your phone**:
```bash
flutter run --release
```
- **Works (you see boxes on objects)** → the whole on-device pipeline is good; continue.
- **Fails (toolchain/build/camera errors you can't fix in ~30 min)** → **switch to the web-app fallback** (`app_web.py` on a Hugging Face Space). Don't sink hours here. The web app is your guaranteed demo.

---

## 3. Drop in your files + model
1. Copy `braille_screen.dart` and `main.dart` into `example/lib/`. (Both import each other by filename, so they must sit together in `lib/`.)
2. Put your trained model at **`example/android/app/src/main/assets/best.tflite`** — this is the **native** assets folder (create `assets/` if missing), **not** Flutter's `assets/` in pubspec. The code references it by filename without extension: `modelPath: 'best'`.

That's it — `main.dart` already sets `BrailleScreen` as the home screen.

---

## 4. Android config (the example already covers these — verify only)
- `android/app/src/main/AndroidManifest.xml` contains:
  ```xml
  <uses-permission android:name="android.permission.CAMERA" />
  ```
- `minSdkVersion` ≥ 24 (the example sets a suitable value; the plugin needs API 21+, but 24+ is safest for TFLite).
- `flutter_tts` needs no extra permission on Android.

---

## 5. Run on the phone
```bash
flutter run --release
```
Point it at embossed Braille under good **side-lighting** (the rig). You should see letter boxes, the decoded text at the bottom, and hear speech as the reading settles. Tune by editing `braille_screen.dart`: voting window (`_history` length), the space gap (`spaceMult`), TTS rate.

---

## 6. Build + distribute the APK
```bash
flutter build apk --release
```
Output: `build/app/outputs/flutter-apk/app-release.apk`.

- **Distribute:** create a **GitHub Release** in your repo and upload the `.apk` as a release asset. Link it in the README. No Play Store needed for a hackathon.
- **Signing:** if `--release` complains about signing, either set up a keystore (Flutter docs → "Build and release an Android app"), or use `flutter build apk --debug` / the APK from `flutter run` — both **sideload fine** for a demo.

---

## 7. Model export reminder (from `train_kaggle.py`)
The model must be exported to TFLite with metadata:
```bash
yolo export model=best.pt format=tflite int8=True data=data.yaml imgsz=640
```
- The Ultralytics plugin is **strict about export params** — if detection misbehaves, follow the exact export command in the plugin's README (`github.com/ultralytics/yolo-flutter-app`).
- If `int8` hurts accuracy on the subtle Braille dots, re-export with `half=True` (fp16) or full precision instead.

---

## 8. Troubleshooting
- **Labels show as numbers (0,1,2…) instead of letters** → class-name metadata wasn't embedded in the export. Re-export and confirm the model's `names` are present; the plugin reads metadata from the model.
- **`r.boundingBox` doesn't compile / wrong field** → your plugin version may expose the box under a different name (e.g. `normalizedBox`). Open the example app's detection-result class in `lib/` and match the field; the decode only needs each box's center-x, center-y, and height.
- **Laggy** → it's already nano + int8; if needed, lower the camera/inference rate via the plugin's `streamingConfig` (e.g. `inferenceFrequency: 10`), or reduce preview resolution.
- **No detections** → confirm `best.tflite` is in `android/app/src/main/assets/`, `modelPath: 'best'` matches the filename, and the page is well-lit (oblique light).
- **App crashes on close** → make sure you're on a current plugin version (recent releases fixed a TFLite-dispose crash).

---

## 9. What ships in the repo
- `flutter_app/` — the example app with your `best.tflite`, `braille_screen.dart`, `main.dart`.
- The **APK** on a GitHub Release (linked in README).
- Python side: `train_kaggle.py`, `evaluate.py`, `app_web.py` (fallback).
- Docs: README (APK install + results table + video), `TOOLS.md`, `data/README.md`, `LICENSE` (AGPL-3.0).
