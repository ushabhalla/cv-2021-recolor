# cv-2021-recolor
Final project for Computer Vision Spring 2021 @ Brown University by Usha Bhalla, Sierra Rowley, Cam Wenzel, and Ally Zhu 

Read our paper here:
https://www.overleaf.com/read/pdgpftwjbytq

##Project Overview

###image_segmentation.py
Contains code for running k-means and recoloring, our main file

###recolor.py
Contains code for all the recolor functions

###kmeans.py
Contains code for our own implementation of k-means

###app.py
Contains code for connecting our program to the frontend gui

##How to Run the Program
To run locally, within the code directory run: python image_segmentation.py -d <path to data image> -k <value of k> -o <path to store output>
  
To run the GUI, run: flask run
