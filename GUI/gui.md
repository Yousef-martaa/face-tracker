# GUI MODULE – PRACTICAL EXPLANATION

## What the Gui class does

The Gui class is responsible for:

- displaying the interface
- showing the camera feed
- handling user interaction (start/stop)

It does NOT:

- handle camera logic
- process frames
- manage system state

It only controls presentation.

---

## Core idea

Gui = interface layer

It sits between:

User ↔ System

---

## How the GUI runs

Tkinter uses an event loop:

self.root.mainloop()

This loop:

- listens for user actions
- updates the UI
- runs scheduled tasks

---

## Important: No while loop

You do NOT use:

while True:

Because:

- it blocks the UI
- freezes the program

---

## Correct approach: after()

self.root.after(delay, function)

This means:

- run function after X milliseconds
- return control to GUI immediately

---

## Video update loop

\_update_video_frame()

Flow:

1. get frame from Cam
2. convert to RGB
3. resize
4. display in GUI
5. schedule next update

---

## Why after() is correct

after():

- keeps UI responsive
- avoids threading issues
- works with Tkinter event system

---

## Why NOT threads here

Threads would:

- complicate synchronization
- risk crashes
- require locks

Your solution:

- simpler
- safer
- correct

---

## Frame conversion

OpenCV uses:

BGR

Tkinter/PIL uses:

RGB

So you must convert:

cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

---

## Image pipeline

frame (OpenCV)
→ convert to RGB
→ PIL Image
→ ImageTk.PhotoImage
→ Tkinter Label

---

## Why ImageTk is needed

Tkinter cannot display raw arrays.

It needs:

PhotoImage

So:

ImageTk.PhotoImage(image)

---

## Resizing logic

scale = min(width_ratio, height_ratio)

This ensures:

- aspect ratio is preserved
- no stretching

---

## Why resize every frame

Window size can change.

Without resize:

- image may overflow
- layout breaks

---

## UI layout

Main parts:

- title
- camera dropdown
- start button
- stop button
- video display area

---

## Button logic

Start:

- start camera
- disable start button
- enable stop button

Stop:

- stop camera
- enable start button
- disable stop button

---

## Why disable buttons

Prevents:

- double start
- invalid states
- user errors

---

## Camera selection

Combobox:

self.combo.current()

Returns index of selected camera.

---

## Why dependency injection is used

Gui(cam=self.cam)

Instead of:

self.cam = Cam()

Reason:

- GUI does not create dependencies
- Manager controls everything
- better architecture

---

## Stopping video loop

self.root.after_cancel(self.video_job)

Important:

- prevents orphan loops
- avoids crashes
- stops updates cleanly

---

## Closing the app

\_on_close()

Steps:

1. stop camera
2. destroy window

Without this:

- camera may stay locked
- app may hang

---

## Performance

Target:

30 FPS

delay = 1000 / FPS

Example:

after(33)

---

## Common mistakes

Using while loop:
→ freezes UI

Not converting BGR:
→ wrong colors

Not resizing:
→ broken layout

Not stopping after():
→ ghost updates

---

## Role in system

Gui is:

- display layer
- user control layer

It is NOT:

- data processor
- system controller

---

## System position

Manager
↓
Gui
↓
Cam

---

## Key takeaway

Gui does NOT do the work.

It:

- shows results
- sends commands

---

## Final understanding

Gui is:

"A controlled window into the system"

Nothing more.
Nothing less.
