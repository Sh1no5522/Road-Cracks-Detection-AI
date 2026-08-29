from __future__ import annotations

from pathlib import Path
import cv2
import numpy as np
import streamlit as st
from ultralytics import YOLO

st.set_page_config(page_title="RoadVision-YOLO", page_icon="🛣️")
st.title("RoadVision-YOLO")
st.caption("Upload a road image to detect annotated pavement defects.")

weights = st.sidebar.text_input("Model weights", "models/best.pt")
confidence = st.sidebar.slider("Confidence threshold", 0.05, 0.95, 0.30, 0.05)
uploaded = st.file_uploader("Road image", type=["jpg", "jpeg", "png"])
if uploaded:
    st.image(uploaded.getvalue(), caption="Input image")
    if not Path(weights).exists():
        st.error("Model weights not found. Train the model and copy best.pt to models/.")
    else:
        image = cv2.imdecode(np.frombuffer(uploaded.getvalue(), dtype=np.uint8), cv2.IMREAD_COLOR)
        if image is None:
            st.error("The uploaded file could not be decoded as an image.")
            st.stop()
        with st.spinner("Running detection..."):
            result = YOLO(weights).predict(source=image, conf=confidence, verbose=False)[0]
        st.image(result.plot()[:, :, ::-1], caption="Detections")
        st.write(f"Detected objects: {len(result.boxes)}")
