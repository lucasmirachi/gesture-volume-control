# Gesture Volume Control with MediaPipe and OpenCV
 
![Gesture Volume Control Gif](/images/gesturevolumecontrol.gif)

## Introduction

This is a study project I developed to implement my former [Hand Tracking Project](https://github.com/lucasmirachi/hand-tracking) in a more useful application. That's why I, with the guidance of this [informative video](https://www.youtube.com/watch?v=01sAkU_NvOY) created by [Murtaza Hassan](https://www.youtube.com/channel/UCYUjYU5FveRAscQ8V21w81A), implemented it in a program where it is possible to adjust the system's internal volume by varying the distances between the index finger's tip and thumb's tip.

## Development 

For this code, it was utilized the [MediaPipe](https://google.github.io/mediapipe/) framework. MediaPipe is a framework developed by Google that contains some amazing models that allows us to quickly get started with some fundamental AI problems such as Face Detection, Object Detection, Hair Segmentation and much more!

Having said that, the model I'll be working with for this project is going to be the [Hand Tracking](https://google.github.io/mediapipe/solutions/hands). Basically, it combines two main modules: the Palm Detection Model and the Hand Landmark Model.

As the name suggests, the **Palm Detection Model** will detect the user's hands and provides a cropped image of the hand. From there, the **Hand Landmark Model** can find up to 21 different landmarks on this cropped image of the hand (like the image bellow):

![Hand Landmarks](https://mediapipe.dev/images/mobile/hand_landmarks.png)
[Source](https://google.github.io/mediapipe/solutions/hands)

For this project, the landmarks ID numbers chosen to be utilized will be **4. THUMB_TIP** and **8. INDEX_FINGER_TIP**.

Because this project was developed to work in a <mark>Linux Pop!OS</mark> distribution, in order to effectively tweak the system's volume with Python, I decided to utilize the **subprocess** library. It is important to notice that this code works on any Debian Linux Distribution. For Windows it is needed to use the **pycaw** library. *Obs: Still need to verify how to implement it on MACOS and on Arch Linux based distros.*

To do so, the following chunk of code was utilized:

```
from subprocess import call
call(["amixer", "-D", "pulse", "sset", "Master", str(volume) + "%"])
```
In short, the only value I had to work with was the "volume" parameter, which turned to be relative to the distance between my index finger and my thump.

```
lenght = math.hypot((thumb_x-index_x), (thumb_y-index_y))
volume = np.interp(lenght,[50,300],[0,100]) 
```

---

## Files

<mark>HandTrackingModule.py</mark> contains the code that is required to run the Hand Tracking program.

<mark>GestureVolumeControl.py</mark> contains the code to effectively change the systems volume.