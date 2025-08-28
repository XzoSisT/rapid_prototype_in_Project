import io
import time
from pathlib import Path

import numpy as np
import cv2
import requests
from PIL import Image, ExifTags
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Image Processing Lab", layout="wide")

# ---------------- Utilities ----------------
def pil_to_rgb_array(pil_img: Image.Image) -> np.ndarray:
    """PIL.Image -> RGB numpy array"""
    return np.array(pil_img.convert("RGB"))

def bytes_to_rgb_array(raw: bytes) -> np.ndarray:
    """Bytes (e.g., from URL) -> RGB numpy array"""
    arr = np.frombuffer(raw, np.uint8)
    bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if bgr is None:
        raise ValueError("ไม่สามารถอ่านภาพจากข้อมูลที่ได้รับ")
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

def get_exif_dict(pil_img: Image.Image) -> dict:
    info = {}
    try:
        exif = pil_img.getexif()
        if exif:
            for k, v in exif.items():
                tag = ExifTags.TAGS.get(k, k)
                info[tag] = v
    except Exception:
        pass
    return info

def show_histogram(img_rgb: np.ndarray, title="Histogram (RGB)"):
    fig, ax = plt.subplots()
    if img_rgb.ndim == 2:  # grayscale
        ax.hist(img_rgb.ravel(), bins=256)
    else:
        for i, ch in enumerate(("R", "G", "B")):
            ax.hist(img_rgb[..., i].ravel(), bins=256, alpha=0.5, label=ch)
        ax.legend()
    ax.set_title(title)
    st.pyplot(fig)

def apply_processing(img_rgb: np.ndarray,
                     to_gray: bool,
                     blur_k: int,
                     do_canny: bool, c1: int, c2: int,
                     alpha: float, beta: int,
                     morph_op: str, morph_k: int) -> np.ndarray:
    """ประมวลผลภาพตามพารามิเตอร์จาก sidebar"""
    out = img_rgb.copy()

    # brightness/contrast ก่อน
    # alpha: contrast (1.0 = เดิม), beta: brightness (0 = เดิม)
    out = cv2.convertScaleAbs(out, alpha=alpha, beta=beta)

    if blur_k > 1 and blur_k % 2 == 1:
        out = cv2.GaussianBlur(out, (blur_k, blur_k), 0)

    if to_gray and out.ndim == 3:
        out = cv2.cvtColor(out, cv2.COLOR_RGB2GRAY)

    if do_canny:
        gray = out if out.ndim == 2 else cv2.cvtColor(out, cv2.COLOR_RGB2GRAY)
        out = cv2.Canny(gray, c1, c2)

    if morph_op != "None":
        k = np.ones((morph_k, morph_k), np.uint8)
        if morph_op == "Dilate":
            out = cv2.dilate(out, k, iterations=1)
        elif morph_op == "Erode":
            out = cv2.erode(out, k, iterations=1)
        elif morph_op == "Open":
            out = cv2.morphologyEx(out, cv2.MORPH_OPEN, k)
        elif morph_op == "Close":
            out = cv2.morphologyEx(out, cv2.MORPH_CLOSE, k)

    return out

def image_info(pil_img: Image.Image, raw_bytes: bytes | None = None):
    w, h = pil_img.size
    mode = pil_img.mode
    fmt  = pil_img.format
    size_kb = None if raw_bytes is None else round(len(raw_bytes)/1024, 2)
    st.subheader("📄 Image Info")
    col1, col2 = st.columns(2)
    with col1:
        st.write({"width": w, "height": h, "mode": mode, "format": fmt, "size_kB": size_kb})
    with col2:
        exif = get_exif_dict(pil_img)
        st.write("EXIF (ย่อ):", {k: exif[k] for i, k in enumerate(exif) if i < 12})
    show_histogram(pil_to_rgb_array(pil_img))

# ---------------- Sidebar (Parameters) ----------------
st.sidebar.title("⚙️ Processing Parameters")
to_gray = st.sidebar.checkbox("Grayscale", value=False)
blur_k  = st.sidebar.slider("Gaussian Blur kernel (odd)", 1, 31, 1, step=2)
do_canny = st.sidebar.checkbox("Canny Edge", value=False)
c1 = st.sidebar.slider("Canny T1", 0, 255, 50)
c2 = st.sidebar.slider("Canny T2", 0, 255, 150)
alpha = st.sidebar.slider("Contrast (alpha)", 0.1, 3.0, 1.0, 0.1)
beta  = st.sidebar.slider("Brightness (beta)", -100, 100, 0, 1)
morph_op = st.sidebar.selectbox("Morphology", ["None", "Dilate", "Erode", "Open", "Close"])
morph_k  = st.sidebar.slider("Morph kernel", 1, 25, 3)

st.title("🖼️ Image Processing Lab (Streamlit)")

# ---------------- Source Tabs ----------------
tab1, tab2, tab3, tab4 = st.tabs(["📷 Webcam", "🌐 Image URL", "📤 Upload", "🖼️ Gallery"])

current_img_rgb = None
raw_bytes = None
pil_img = None

# --- 1) Webcam (ถ่ายภาพนิ่งด้วย st.camera_input) ---
with tab1:
    st.caption("ใช้ปุ่มด้านล่างเพื่อถ่ายภาพจากกล้องเว็บแคม (ภาพนิ่ง)")
    cam = st.camera_input("Take a photo")
    if cam is not None:
        raw_bytes = cam.getvalue()
        pil_img = Image.open(io.BytesIO(raw_bytes)).convert("RGB")
        current_img_rgb = pil_to_rgb_array(pil_img)

# --- 2) Image URL ---
with tab2:
    url = st.text_input("วาง URL ของรูปภาพ (เช่น https://.../image.jpg)")
    if st.button("Load from URL") and url:
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            raw_bytes = resp.content
            current_img_rgb = bytes_to_rgb_array(raw_bytes)
            pil_img = Image.open(io.BytesIO(raw_bytes)).convert("RGB")
            st.success("โหลดสำเร็จ")
        except Exception as e:
            st.error(f"โหลดรูปไม่สำเร็จ: {e}")

# --- 3) Upload จากไฟล์ ---
with tab3:
    up = st.file_uploader("อัปโหลดภาพ (JPG/PNG)", type=["jpg", "jpeg", "png"])
    if up:
        raw_bytes = up.getvalue()
        pil_img = Image.open(io.BytesIO(raw_bytes)).convert("RGB")
        current_img_rgb = pil_to_rgb_array(pil_img)

# --- 4) Gallery ภาพตัวอย่าง ---
with tab4:
    gallery_dir = Path("gallery")
    images = sorted(list(gallery_dir.glob("*.*")))
    if not images:
        st.info("วางไฟล์ตัวอย่างในโฟลเดอร์ 'gallery/' ก่อน")
    else:
        choice = st.selectbox("เลือกภาพจากแกลเลอรี", images, format_func=lambda p: p.name)
        if choice:
            raw_bytes = choice.read_bytes()
            pil_img = Image.open(choice).convert("RGB")
            current_img_rgb = pil_to_rgb_array(pil_img)
            st.success(f"โหลด {choice.name} สำเร็จ")

# ---------------- Processing & Display ----------------
if current_img_rgb is not None:
    colA, colB = st.columns(2)
    with colA:
        st.subheader("Original")
        st.image(current_img_rgb, channels="RGB", use_column_width=True)
        if pil_img is not None:
            image_info(pil_img, raw_bytes)

    processed = apply_processing(current_img_rgb, to_gray, blur_k, do_canny, c1, c2, alpha, beta, morph_op, morph_k)

    with colB:
        st.subheader("Processed")
        st.image(processed, use_column_width=True)

        # ปุ่มดาวน์โหลด
        if processed.ndim == 2:
            rgb_to_save = cv2.cvtColor(processed, cv2.COLOR_GRAY2RGB)
        else:
            rgb_to_save = processed
        bgr = cv2.cvtColor(rgb_to_save, cv2.COLOR_RGB2BGR)
        ok, buf = cv2.imencode(".png", bgr)
        if ok:
            st.download_button("⬇️ Download Processed PNG", data=buf.tobytes(), file_name="processed.png", mime="image/png")

else:
    st.info("เลือกรูปจากแหล่งใดแหล่งหนึ่งด้านบนก่อน")
