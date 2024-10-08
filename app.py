import streamlit as st
import numpy as np
from ultralytics import YOLO
import cv2
import os
import pandas as pd
from collections import defaultdict
import pickle
from pycaret.classification import load_model

# Load YOLOv8 model
yolo_model = YOLO("yolov8m-pose.pt") 

# Prepare the keypoints' names and indices
KEYPOINT_DICT = {
'nose': 0,
'left_eye': 1,
'right_eye': 2,
'left_ear': 3,
'right_ear': 4,
'left_shoulder': 5,
'right_shoulder': 6,
'left_elbow': 7,
'right_elbow': 8,
'left_wrist': 9,
'right_wrist': 10,
'left_hip': 11,
'right_hip': 12,
'left_knee': 13,
'right_knee': 14,
'left_ankle': 15,
'right_ankle': 16
}

# Function for processing video and returning keypoints in a Pandas DataFrame
def create_df_coords(video_file):
    # Initialise list to store keypoints of all frames
    rows_list = []

    # Set frame index for tracking frame number
    frame_index = 1

    # Create a VideoCapture object to open the video file
    cap = cv2.VideoCapture(video_file)

    # Loop through the video frames
    while cap.isOpened():
        success, frame = cap.read()

        if success:
            # Extract the landmarks for every 60 frames i.e. 2 seconds
            if frame_index % 60 == 0 and frame_index <= 1800:
                results = yolo_model.track(frame, conf=0.5, stream=True)

                # Store the track history
                track_history = defaultdict(lambda: [])

                # process through results generator
                for r in results:
                    boxes = r[0].boxes.xywh.cpu()
                    track_ids = r[0].boxes.id.int().cpu().tolist()

                    for box, track_id in zip(boxes, track_ids):
                        x, y, w, h = box
                        track = track_history[track_id]
                        track.append((float(x), float(y)))
                        if len(track) > 30:
                            track.pop(0)

                    # retrieve keypoints, add keypoints to df
                    row = r.keypoints.xyn.cpu().numpy()[0].flatten().tolist()
                    row.insert(0, track_id)

                    # append row to rows_list
                    rows_list.append(row)
        else:
            break

        frame_index += 1
      
    
    
    
    
    # Create column names for data frame used for prediction
    columns = []
    for i in range(1, 31):
        columns.append(str(i) + '_' + "person")
    
        for key, value in KEYPOINT_DICT.items():
            columns.extend([str(i) + '_' + key + '_x', str(i) + '_' + key + '_y']) 
                       
    # Flatten rows_list
    flattened_rows_list = [item for sublist in rows_list for item in sublist]
    
    # Convert to DataFrame with a single row
    keypoints_df = pd.DataFrame([flattened_rows_list], columns=columns)

    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()

    return keypoints_df



# Streamlit app
st.title("Yoga Form Detector")

# Video upload
video_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])

# Process video if uploaded
if video_file:
    # Create the temp_video directory if it doesn't exist
    #if not os.path.exists("temp_video"):
    #    os.makedirs("temp_video")

    # Save uploaded file temporarily
    temp_file_path = os.path.join("", video_file.name)
    with open(temp_file_path, "wb") as f:
        f.write(video_file.getbuffer())

    #st.write(f"Video saved to {temp_file_path}")

    # Process the video and get keypoints in DataFrame
    keypoints_df = create_df_coords(temp_file_path)

    #st.success("Keypoints extracted and saved to DataFrame")
    
    # Delete the temporary video file after predictions are made
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)
        #st.write(f"Temporary file {video_file.name} deleted.")

    # Dropping columns containing 'person', 'nose', 'eye', or 'ear' in their names
    columns_to_drop = keypoints_df.filter(regex='person|nose|eye|ear').columns
    keypoints_df = keypoints_df.drop(columns=columns_to_drop)

    # Fill the missing keypoints with 0 due to lack of frames in some videos
    keypoints_df.fillna(0, inplace=True)

    # Display the updated DataFrame
    #st.write("Processed Keypoints Data:")
    #st.dataframe(keypoints_df.head())

    # Make predictions using the PyCaret model
    #st.write("Making predictions...")
    # Load the PyCaret model
    model = load_model('model')
    predictions = model.predict(keypoints_df)

    # Display the predictions
    st.write("Yoga form is ", predictions[0])
