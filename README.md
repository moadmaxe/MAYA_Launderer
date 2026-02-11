# MAYA_Launderer
A python tool to make OBJ imports look like native Maya geometry

# 🛁 Maya Asset Launderer

**Stop manual cleanup. Make imported assets look native instantly.**

This is a Python tool for Autodesk Maya that takes messy imported geometry (OBJ/FBX from Blender, ZBrush, etc.) and "launders" it to look like it was modeled natively in Maya.

## 🚀 Features
* **Automatic Cleanup:** Unlocks normals, softens edges (30°), centers pivots, and deletes history.
* **Hierarchy Fixer:** Explodes "one object" meshes into separate parts and ungroups them to world.
* **Metadata Stripper:** Removes annoying "Blender_Custom_Props" and extra attributes.
* **Geometry Audit:** Fixes Lamina faces, non-manifold geometry, and zero-length edges.
* **The Disguise Kit:** Renames objects to native Maya conventions (`pCube1`, `curve1`, `locator1`) with **Simulated Deletions** (random numbering like `pCube4`, `pCube23`) to mimic a human workflow.

## 📦 Installation
1.  Download `MayaLaunderer.py`.
2.  Open **Maya**.
3.  Open the **Script Editor** (Windows > General Editors > Script Editor).
4.  Go to a **Python** tab.
5.  Drag and drop `MayaLaunderer.py` into the window (or copy/paste the code).
6.  Press **Play** (Ctrl+Enter).

## 🎮 How to Use
1.  **Ingest:** Import your OBJ. Select the mesh. Click "Separate Selected" to break it apart.
2.  **Clean:** Go to Tab 2 and run "Basic Clean" to fix pivots and normals.
3.  **Disguise:** Go to Tab 3. Select your boxy objects and click the **Cube Icon**. Select your pipes and click the **Cylinder Icon**. The tool will rename them to `pCube#` and `pCylinder#`.
4.  **Polish:** Go to Tab 4 and click "Apply Polish" to randomize wireframe colors and convert materials to Arnold.

## 📄 License
MIT License - Free to use for personal and commercial projects.
