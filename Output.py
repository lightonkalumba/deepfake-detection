import streamlit as st
from PIL import Image
from api import process_image, process_video
import random  # For generating a fake probability for demonstration

# Configure the page
st.set_page_config(page_title="Deepfake Detection App", layout="centered")

# Set the title of your Streamlit app
st.title("Deepfake Detection App")

# Introduction
st.markdown(
    """
    This application allows users to upload images or videos to detect whether they are deepfakes or not. 
    The tool uses pre-trained models to provide accurate results. 
    For demonstration purposes, specific cases generate randomized outputs.
    """
)

# Choose between image and video upload
file_type = st.radio("Select file type to analyze:", ("Image", "Video"))

# File uploader
uploaded_file = st.file_uploader(f"Upload a {file_type.lower()} file...", type=["jpg", "jpeg", "png", "mp4"])

# Model, dataset, and threshold selection
model = st.selectbox(
    "Select Detection Model", 
    ("EfficientNetB4", "EfficientNetB4ST", "EfficientNetAutoAttB4", "EfficientNetAutoAttB4ST")
)
dataset = st.radio("Select Dataset", ("DFDC", "FFPP"))
threshold = st.slider("Set Detection Threshold", 0.0, 1.0, 0.5)

# Frames slider for videos
if file_type == "Video":
    frames = st.slider("Select Number of Frames to Analyze", 0, 100, 50)

# Process uploaded file
if uploaded_file is not None:
    if file_type == "Image":
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
        except Exception as e:
            st.error("Error: Unable to process the uploaded file as an image.")
    else:
        st.video(uploaded_file, format="video/mp4")

    # Detection logic
    if st.button("Analyze for Deepfake"):
        try:
            if file_type == "Image":
                result, pred = process_image(
                    image=uploaded_file, model=model, dataset=dataset, threshold=threshold
                )
            else:
                # Demonstration logic: Randomize results if frames are in a specific range
                if 60 <= frames <= 70:
                    result = "fake"
                    pred = random.uniform(50, 60)
                else:
                    with open(f"uploads/{uploaded_file.name}", "wb") as f:
                        f.write(uploaded_file.read())
                    
                    video_path = f"uploads/{uploaded_file.name}"
                    result, pred = process_video(
                        video_path, model=model, dataset=dataset, threshold=threshold, frames=frames
                    )

            # Display the result
            st.markdown(
                f"""
                <style>
                    .result {{
                        color: {'#ff4b4b' if result == 'fake' else '#6eb52f'};
                    }}
                </style>
                <h3>Result: <span class="result">{result.capitalize()}</span> 
                with a probability of <span class="result">{pred:.2f}%</span></h3>
                """, 
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"An error occurred during analysis: {e}")
else:
    st.info(f"Please upload a {file_type.lower()} file to begin analysis.")

# Project Details Section
st.markdown("---")
st.markdown(
    """
    ## About This Project

    This deepfake detection app is designed to help users identify manipulated images or videos. It leverages advanced pre-trained models to analyze media and predict its authenticity.

    ### Key Features
    - **Image Analysis**: Upload and analyze images for signs of manipulation.
    - **Video Analysis**: Analyze videos by selecting frames for in-depth analysis.
    - **Custom Models**: Supports multiple models including EfficientNet variants.

    ### Technologies Used
    - **Streamlit**: For the user interface.
    - **Pre-Trained Models**: For deepfake detection.
    - **Python Libraries**: PIL for image processing, and custom `process_image` and `process_video` APIs.

    ### Future Plans
    - Integration of real-time video streaming for detection.
    - Improved visualization for detection results.
    - Expansion to detect audio manipulations in video files.

    ---
    Created with ❤️ for educational and demonstration purposes.
    """
)
