Yoga form detector using YOLOv8m

This project is a Computer Vision Project using YOLOv8m model for posture analysis, 
to detect if the yoga pose taken by a person is correct or not. 

Problem Statement: 
With the increasing popularity of yoga, many people want to learn and practice it on their own. However there are many versions taught as 'Sun Salutation Type A', 'Sun Salutation Type B', etc which do not do justice to the age old reputation of Surya Namaskar as a complete body workout. We are focusing on the version taught for generations. 

Solution:
Here is an attempt to develop a tool that can help learners identify their pose. 

Impact:


We have created a Streamlit App with the link: [
](https://yoga-pose-detector.streamlit.app/)

This Streamlit App takes video inputs with a Limit 200MB, mp4,avi,mov,mpeg. 
For live trials, please ensure your right profile faces the camera, with a distance of approximately 10ft and appropriate lighting. 

Data Source:
As we are focusing on an authentic version not practised by many, we went ahead and recorded our own
one minute videos for 'Good' and 'Bad' which were used to train the model as to how the correct 'Surya Namaskar' is to be performed. The practitioners of this authentic version, do not perform it non-stop more than 16-18 times as it can be very strenuous.
We encounteredmore difficulties here as some of the videos didn't have the correct lighting and some did not capture the required body joints called 'key point' to digitise the human body movements. We tried using Media Pipe, then tried using YOLOv8m for this purpose.

Key Components:
- Model: YOLOv8m for pose detection
- Keypoints: Defined in KEYPOINT_DICT, covering essential joints and body parts,
  for different classes "Good" or "Bad"
- CSV Structure: The script creates columns for tracking
  pose data(x,y coordinates of keypoints for each detected person)
- Video Processing: Processes video frames, extracts keypoints, and stores them in a CSV file

Process: 

We had the task of converting the 'Surya Namaskar' Yoga pose' into a digtal sequence for the computer model to analyse if its ok or not. In other words we had to convert a one minute video into a digital frame the computer could analyse.



<img width="233" alt="Screenshot 2024-09-11 at 6 43 29 AM" src="https://github.com/user-attachments/assets/4d01d460-6654-4ae5-be73-7465a5df59e2">



<img width="450" alt="Screenshot 2024-09-11 at 6 44 15 AM" src="https://github.com/user-attachments/assets/ccc7931a-224c-4f9a-ab5e-fae0df09399f">

Our videos were 1 minute long with a frame rate of 30 fps(frames per second), so we decided to capture the videos as follows:
We will set a counter to track the number of frames processed by the code, as it loops through the video,  frame_index is incremented after each frame is read in the video. It’s used to determine, which frames to process, based on our conditions, e.g. every 60th frame.

This way we extracted 30 frames from each video.


















