# Face Tracker

Face Tracker is a desktop camera app built with Python, Tkinter, and OpenCV.
It provides a GUI to list available webcams, start and stop capture safely,
and display live video directly inside the app window.

## Current Status

The project now includes:

- Single app entry point through `main.py`
- Embedded live camera view in Tkinter (no external OpenCV popup window)
- Responsive video area that scales with window size while keeping aspect ratio
- Safer camera stop/cleanup flow to avoid crashes when stopping capture
- Faster camera probing on Windows
- Camera list showing friendly/full camera names when available
- Package-ready folders with `__init__.py`

## Requirements

- Windows (tested on Windows with Git Bash + Python)
- Python 3.13
- Webcam

Python packages are listed in `requirements.txt`:

- `opencv-python>=4.12`
- `pillow>=11.0`

## Install Dependencies (No venv)

Install globally using your Python interpreter:

```bash
"C:/Program Files/Python313/python.exe" -m pip install -r requirements.txt
```

## Run the App

From the project root (`face-tracker/`):

```bash
"C:/Program Files/Python313/python.exe" main.py
```

Alternative launcher:

```bash
py -3.13 main.py
```

## Project Structure

```text
face-tracker/
	BUFFER/
	CAM/
	FACE/
	GUI/
	MANAGER/
	main.py
	requirements.txt
	README.md
```

Core components:

- `main.py`: Application entry point
- `MANAGER/manager.py`: Orchestrates system setup and runtime
- `CAM/cam.py`: Camera detection/start/stop/frame reading
- `GUI/gui.py`: Tkinter interface and embedded live video rendering

## Troubleshooting

### `Import "cv2" could not be resolved`

VS Code is likely using a different interpreter than the one where OpenCV is installed.
Select the same Python interpreter used for running the app.

### `.venv/Scripts/python.exe: No such file or directory`

This project is configured to run without venv.
Use the global Python command shown above.

### Camera list is empty or camera fails to start

- Verify the camera is not in use by another app
- Try reconnecting the webcam
- Restart the app

## Git Ignore

The project includes `.gitignore` rules for:

- Python cache files (`__pycache__`, `*.pyc`)
- Temporary files and logs
- OS/editor artifact files
