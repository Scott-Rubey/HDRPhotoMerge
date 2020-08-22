This is a program that combines multiple low-dynamic-range (LDR) source images and combines them into a single high-dynamic-range (HDR) composite.  All that is required in order to run the program is a directory that includes source images and a .txt file reflecting exposure times.  See the included sample images and .txt files for guidance.  You may also view the included slide show for information regarding HDR photography and program controls.

Gamma and Vibrance are subjective, dependent upon image.  Gamma should be set to a value greater than 0, as 0 represents pure black.  

Once the program has created the HDR composite, the user will be given the option to make some basic post-processing adjustments, including brightness, saturation, whites and blacks (i.e. contrast).

Little attention was paid to the user interface with this program, as the intent was to create a simple program that performed the above referenced functionality with no bells or whistles.  Sample images have been provided for the user's convenience; the program may be altered to accommodate the user's source images.  (All sample images are copyrighted by the author, Scott Rubey; more of my photography may be viewed at www.scottrubey.com.)  

To run program from the command line:

1) python3 hdr.py --input <source image folder name>*
2) comment/uncomment lines 10 - 13 to select appropriate save path
3) comment/uncomment lines 43 - 46 to select source images

When adjustments to images have been completed in each preview window, the 'a' key will save results and advance the program.

*Test images included for this project are included in the following folders, thus should be entered in place of <source image folder name>:

BlueHoleCave
Bryce
Rainier
