# Bricklayers (Patched Fork)
Interlocking Layers Post-Processing Script for PrusaSlicer, OrcaSlicer, and BambuStudio

This fork adds fixes and features on top of [GeekDetour/BrickLayers](https://github.com/GeekDetour/BrickLayers).

## Added Features

### G2/G3 Arc Support
Arc fitting can now be left **enabled** in your slicer. This fork properly handles G2/G3 arc commands:
- **Bounding box:** Computes true arc bounding box via cardinal angle crossing detection (not just endpoints)
- **Wipe path:** Arc-aware distance calculation and endpoint interpolation for correct wipe retracing

### Feature Branches for Upstream PRs

| Branch | Feature |
|---|---|
| [`arc-support`](../../tree/arc-support) | G2/G3 arc bounding box and wipe path |

---

## Original README

## Video about this script:
[![Brick Layers for everybody](https://img.youtube.com/vi/qqJOa46OTTs/maxresdefault.jpg)](https://www.youtube.com/watch?v=qqJOa46OTTs)

---
# We are back: v0.2.1

I made major changes on travel, retraction, and wiping. It is printing much better. 

But just like a 0.6mm nozzle, it seems Brick Layers is prone to stringing - time to start playing with settings and share our findings!

!['CaliCat' printed with Brick Layers on the Elegoo Centauri Carbon](docs/img/v0.2.1.jpg)

---

## Install Python or Pypy
To use the script, you need **Python 3** installed in your machine:
- [Download Python 3](https://www.python.org/downloads/) CPython, or
- [Download PyPy 3](https://pypy.org/download.html) PYPY (faster)

---

## Setup in your Slicer
Edit the **"Post processing scripts"** section in your slicer.

!['Post-processing Scripts' example, in Orca Slicer](docs/img/postprocessingscripts_orca.png)

**Make sure to update the path** to match:
- Your **Python installation** folder.
- The folder where **you saved `bricklayers.py`**.

### **Windows Examples 🖥️**
- Normal Python (CPython):<br>
```"%USERPROFILE%\AppData\Local\Programs\Python\Python313\python.exe" "C:\3DPrinting\Scripts\bricklayers.py" -startAtLayer 3 -extrusionMultiplier 1.05 -enabled 1;```
- PYPY3:<br>
```"C:\3DPrinting\pypy3.11-v7.3.19-win64\pypy3.exe" "C:\3DPrinting\Scripts\bricklayers.py" -startAtLayer 3 -extrusionMultiplier 1.05 -enabled 1;```

### **Mac/Linux Examples 🍏 🐧**
- CPython (installed globally):<br>
```/usr/local/bin/python3 /Volumes/3DPrinting/Scripts/bricklayers.py -startAtLayer 3 -extrusionMultiplier 1.05 -enabled 1;```
- CPython (installed locally):<br>
```/Users/YourName/.pyenv/shims/python3 /Volumes/3DPrinting/Scripts/bricklayers.py -startAtLayer 3 -extrusionMultiplier 1.05 -enabled 1;```
- PyPy3 (installed globally):<br>
```/usr/local/bin/pypy3 /Volumes/3DPrinting/Scripts/bricklayers.py -startAtLayer 3 -extrusionMultiplier 1.05 -enabled 1;```
- PyPy3 (installed locally):<br>
```/Users/YourName/.pyenv/versions/pypy3/bin/pypy3 /Volumes/3DPrinting/Scripts/bricklayers.py -startAtLayer 3 -extrusionMultiplier 1.05 -enabled 1;```

### **Wall Generator** and **Walls printing order**:
In "Quality", "Walls printing order" be sure you select **"Inner/Outer"** - this is very important for the right detection of the Loops 'Depth':

!['Wall generator' to 'Classic' and 'Inner/Outer', in Orca Slicer](docs/img/wallorder_orca.png)

In **Prusa Slicer** you can choose **Classic** or **Arachne**, both work equaly fine. 
But on **Orca Slicer** and **Bambu Studio** forks, Arachne sometimes creates orphaned loops that will turn into minor glitches in Brick Layers (I cannot fix, so far) - so I recommend **'Classic'**.

### **Arc fitting** (now supported in this fork)
This fork adds full G2/G3 arc support — you can leave arc fitting **enabled** in your slicer settings.

### **Binary G-code** on Prusa Slicer:
You must **disable** `"Supports binary G-code"` in **Printers → General → Firmware** (Expert Mode)

The Binary G-code format is **incompatible with post-processing scripts**.

---

# How to see the Preview?

Saddly, none of the slicers show the changes automatically - which is weird since we can see they are running the Post-processing Script every time we slice.

We need to **drag the exported gcode file back to the Slicer** to see the results of any Post-Processing Script.

I wish this was different. Post-processing scripts would be more appealing if previewing was automatic.

More details: https://github.com/GeekDetour/BrickLayers/issues/20

---

## Command Line Interface
You can use the script to modify GCode files outside of the slicer.
First, I recommend you to check 2 examples in this file:
https://github.com/GeekDetour/BrickLayers/blob/main/sample_tests/simpletest.sh

Try running it once, as provided.

If you downloaded or cloned the repository, in your Terminal, go to the repository and:
```sh
cd sample_tests
chmod +x simpletest.sh
./simpletest.sh
```

You should see something like this:
![running the simpletest.sh on your machine](docs/img/cli_simpletest.png)



