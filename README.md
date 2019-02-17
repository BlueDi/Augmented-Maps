# Augmented Maps
The objective of this work is to develop a set of programs that can be used to "augment" geographic map images by associating one or more images of the point of interest closest to the center of the image and marking the location of the point of interest on the map.

For more information, visit the [wiki](https://github.com/BlueDi/Augmented-Maps/wiki) page of this project.

<img src="https://user-images.githubusercontent.com/9451036/52912893-d4101480-32af-11e9-85a3-457b480d5cb2.png" alt="Preparation interface" width="400" /> <img src="https://user-images.githubusercontent.com/9451036/52912958-c60ec380-32b0-11e9-9c31-60fbb3954bfa.png" alt="Augment interface" width="440" />
(Note: the images were taken in different runnings of the program, the closest interest point in the first image would be _cristal_)

## Instructions
### Preparation
To run the preparation project: at the root of the project, switch to the `src` directory and run `python preparation.py`. 
You can add the `-d` flag if you want to run in debug mode, displaying intermediate process windows or displaying logs in the program console. 
You can also add the `-c` flag to calibrate the camera.

<img src="https://user-images.githubusercontent.com/9451036/52912937-5567a700-32b0-11e9-973c-c25bfc09b5b9.png" alt="Preparation console with debug active" width="300" />

### Augment
To run the augment project: at the root of the project, switch to the `src` directory and run `python augment.py`. 
You can add the `-d` flag if you want to run in debug mode, displaying intermediate process windows or displaying logs in the program console.

<img src="https://user-images.githubusercontent.com/9451036/52913084-48e44e00-32b2-11e9-9cc3-c6ec3c88b21b.png" alt="Augment console with debug active" width="300" />

### Flags
In both projects, it is possible to run the `-h` or `--help` flag for information on the available flags.

If you want to change the front image of the map, the path to the image can be passed as an argument of the `-ib` flag in both projects, or for a permanent solution, the path in the _IMAGE_BASE variable_ (line 13) of the `./src/preparation.py` file and the path in the _IMAGE_BASE variable_ (line 17) of the `./src/augment.py` file will have to be changed.

If you want to change the image to be augmented, the path in the _IMAGE_TEST variable_ (line 18) of the `./src/augment.py` file can be passed as an argument to the `-it` flag, or to a permanent solution.

It is still possible in the augmentation program to choose whether to draw a green circle instead of the enlarged pyramid through the `-cir` or `--circle` flag.

## References
1. S. A. K. Tareen e Z. Saleem, «A comparative analysis of SIFT, SURF, KAZE, AKAZE, ORB, and BRISK», em 2018 International Conference on Computing, Mathematics and Engineering Technologies (iCoMET), 2018, pp. 1–10.
2. P. F. Alcantarilla, A. Bartoli, e A. J. Davison, «KAZE Features», em Computer Vision – ECCV 2012, 2012, pp. 214–227.
3. «Blob detection», Wikipedia. 13-Out-2018.
4. X. Li, «Chapter 8 - Image Processing at Your Fingertips: The New Horizon of Mobile Imaging», em Academic Press Library in Signal Processing, vol. 4, J. Trussell, A. Srivastava, A. K. Roy-Chowdhury, A. Srivastava, P. A. Naylor, R. Chellappa, e S. Theodoridis, Eds. Elsevier, 2014, pp. 249–264.
5. M. A. Fischler e R. C. Bolles, «Random Sample Consensus: A Paradigm for Model Fitting with Applications to Image Analysis and Automated Cartography», Commun. ACM, vol. 24, n. 6, pp. 381–395, Jun. 1981.
6. "Feature Matching",  https://docs.opencv.org/3.0‐beta/doc/py_tutorials/py_feature2d/py_matcher/py_matcher.html, 2018‐12‐06  
7. "Feature Matching + Homography to find Objects", https://docs.opencv.org/3.0‐beta/doc/py_tutorials/py_feature2d/py_feature_homography/py_feature_homography.html, 2018‐12‐06  
8. "Pose estimation", https://docs.opencv.org/3.4/d7/d53/tutorial_py_pose.html, 2018‐12‐06 
9. "Camera calibration", https://docs.opencv.org/3.1.0/dc/dbb/tutorial_py_calibration.html, 2018‐12‐06



