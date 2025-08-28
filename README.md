# the rapid prototype in AI Project (Streamlit)

## ✨ คุณสมบัติ (Features)

- 📷 Webcam: ถ่ายภาพนิ่งผ่านเบราว์เซอร์ (st.camera_input)
- 🌐 Image URL: โหลดภาพจากลิงก์สาธารณะ
- 📤 Upload: อัปโหลดไฟล์ JPG/PNG
- 🖼️ Gallery: เลือกภาพตัวอย่างจากโฟลเดอร์ gallery/
- 🧪 Processing Parameters (GUI):
  -  Grayscale
  -  Gaussian Blur (odd kernel)
  -  Canny Edge (T1/T2)
  -  Brightness/Contrast (alpha/beta)
  -  Morphology: Dilate / Erode / Open / Close (+ kernel size)
- 👀 แสดง Original vs Processed แบบเรียลไทม์
- ℹ️ Image Info: ขนาด/โหมด/ฟอร์แมต/ขนาดไฟล์, EXIF (ย่อ), และ Histogram (RGB)
- ⬇️ ดาวน์โหลดผลลัพธ์เป็น processed.png

## Quick Start
```
git clone https://github.com/XzoSisT/rapid_prototype_in_Project.git
cd rapid_prototype_in_Project

# (แนะนำ) สร้างและเปิดใช้งาน virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```
