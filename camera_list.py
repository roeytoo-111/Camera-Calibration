"""
List the cameras connected to this PC.

Run on the WINDOWS side:
    python list_cameras.py

It does two things:
  1. Asks Windows (via DirectShow) for the real device NAMES, if pygrabber
     is installed (`pip install pygrabber`).
  2. Probes OpenCV indices 0-9 and reports which ones actually open,
     along with the resolution they report.

The index that works here is the number you pass to capture_checkerboard.py
with --camera.
"""

import cv2


def device_names_via_dshow():
    """Return a list of camera names from Windows DirectShow, or None."""
    try:
        from pygrabber.dshow_graph import FilterGraph
    except ImportError:
        return None
    return FilterGraph().get_input_devices()


def probe_opencv(max_index=10):
    """Try to open each index and read one frame. Returns list of working ones."""
    working = []
    for i in range(max_index):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)  # DirectShow = reliable on Windows
        if cap.isOpened():
            ok, _ = cap.read()
            w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            working.append((i, ok, w, h))
        cap.release()
    return working


def main():
    print("=" * 55)
    print("Camera device NAMES (Windows DirectShow):")
    names = device_names_via_dshow()
    if names is None:
        print("  pygrabber not installed - run 'pip install pygrabber'")
        print("  for human-readable device names (optional).")
    elif not names:
        print("  No devices reported by Windows.")
    else:
        for idx, name in enumerate(names):
            print(f"  [{idx}] {name}")

    print("=" * 55)
    print("Probing OpenCV indices 0-9 (a few seconds)...")
    cams = probe_opencv(10)
    if not cams:
        print("  No camera index could be opened.")
    else:
        for i, ok, w, h in cams:
            status = "OK, frame read" if ok else "opened but NO frame"
            print(f"  index {i}: {status}  ({w}x{h})")
    print("=" * 55)


if __name__ == "__main__":
    main()
