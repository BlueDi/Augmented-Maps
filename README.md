# Augmented Maps
The objective of this work is to develop a set of programs that can be used to "augment" geographic map images by associating one or more images of the point of interest closest to the center of the image and marking the location of the point of interest on the map.

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
