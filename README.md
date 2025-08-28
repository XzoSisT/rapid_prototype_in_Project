# the rapid prototype in AI Project (Streamlit)

## ✨ Features

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

# (Recommend) สร้างและเปิดใช้งาน virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Demo
<img width="1919" height="885" alt="image" src="https://github.com/user-attachments/assets/a4071fc7-2789-4ce3-8d53-68bdcda71c2c" />
<img width="1120" height="848" alt="image" src="https://github.com/user-attachments/assets/a4dbf324-ed0b-4a99-a62b-54f12b7544db" />


