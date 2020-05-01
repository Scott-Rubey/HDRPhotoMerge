#credit to https://www.learnopencv.com/high-dynamic-range-hdr-imaging-using-opencv-cpp-python/
#and https://docs.opencv.org/3.4/d3/db7/tutorial_hdr_imaging.html for their helpful
#opencv tutorials

import cv2
import numpy
import argparse
import os

savePath = "/Users/srubey/Desktop/School/CS510 Computational Photography/Project/Rainier/Result"

def main():
    parser = argparse.ArgumentParser(description='CS510 Computational Photography - Final Project - Scott Rubey.')
    parser.add_argument('--input', type=str, help='Path to the directory that contains images and exposure times.')
    args = parser.parse_args()

    if not args.input:
      parser.print_help()
      exit(0)

    images, times = loadImages(args.input)
    align(images)
    rc = getRespCurve(images, times)
    hdr = mergeSrcImages(images, times, rc)
    ldr = tonemap(hdr)
    result = adjustParams(ldr)

    #cv2.imshow('Edited Image', result)
    #cv2.waitKey(0)
    cv2.destroyAllWindows()

def loadImages(path):
    images = []
    times = []

    print("Loading Source Images...")

    with open(os.path.join(path, 'Rainier.txt')) as f:
        content = f.readlines()

    for line in content:
        tokens = line.split()
        images.append(cv2.imread(os.path.join(path, tokens[0])))
        times.append(1 / float(tokens[1]))

    return images, numpy.asarray(times, dtype=numpy.float32)

def align(images):
    print("Aligning Source Images...")
    align = cv2.createAlignMTB()
    align.process(images, images)

def getRespCurve(images, times):
    calDev = cv2.createCalibrateDebevec()
    response = calDev.process(images, times)

    return response

def mergeSrcImages(images, times, response):
    print("Creating HDR Image...")
    merge = cv2.createMergeMertens()
    hdr = merge.process(images, times, response)

    # Save HDR image.
    hdrCompleteName = os.path.join(savePath, "HDR.hdr")
    cv2.imwrite(hdrCompleteName, hdr)

    return hdr

def tonemap(hdr):
    def tmCallback(val):
        pass

    #create user interface w/ tone mapping controls
    cv2.namedWindow("Tone Map", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Tone Map", 750, 750)
    cv2.imshow("Tone Map", hdr)

    cv2.createTrackbar("Gamma         ", "Tone Map", 0, 4, tmCallback)
    cv2.createTrackbar("Compression", "Tone Map", 0, 4, tmCallback)
    cv2.waitKey(0)

    #capture trackbar values
    gamma = cv2.getTrackbarPos("Gamma         ", "Tone Map")
    comp = cv2.getTrackbarPos("Compression", "Tone Map")

    cv2.destroyAllWindows()
    print("Tone Mapping...")

    # Tonemap using Reinhard's method to obtain 24-bit color image
    tonemap = cv2.createTonemapReinhard(gamma/4.0, 0, comp/4.0, 0)
    ldr = tonemap.process(hdr)
    completeName = os.path.join(savePath, "Result.jpg")
    cv2.imwrite(completeName, ldr * 255)

    return ldr

def adjustParams(ldr):
    result = ldr

    #create preview window
    cv2.namedWindow("Preview", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Preview", 750, 750)
    renderResult(result)

    #create trackbars
    cv2.createTrackbar("Brightness", "Preview", 50, 100,
                       lambda x: callback(x, cv2.getTrackbarPos("Saturation ", "Preview"),
                                          cv2.getTrackbarPos("Whites      ", "Preview"),
                                          cv2.getTrackbarPos("Blacks      ", "Preview"), result))
    cv2.createTrackbar("Saturation ", "Preview", 50, 100,
                       lambda x: callback(cv2.getTrackbarPos("Brightness", "Preview"), x,
                                          cv2.getTrackbarPos("Whites      ", "Preview"),
                                          cv2.getTrackbarPos("Blacks      ", "Preview"), result))
    cv2.createTrackbar("Whites      ", "Preview", 50, 100,
                       lambda x: callback(cv2.getTrackbarPos("Brightness", "Preview"),
                                          cv2.getTrackbarPos("Saturation ", "Preview"), x,
                                          cv2.getTrackbarPos("Blacks      ", "Preview"), result))
    cv2.createTrackbar("Blacks      ", "Preview", 50, 100,
                       lambda x: callback(cv2.getTrackbarPos("Brightness", "Preview"),
                                          cv2.getTrackbarPos("Saturation ", "Preview"),
                                          cv2.getTrackbarPos("Whites      ", "Preview"), x, result))

    cv2.waitKey(0)

def callback(br, sat, wht, blk, result):
    result = saturation(sat, result)
    result = calcBlacks(blk, result)
    result = calcWhites(wht, result)
    result = brightness(br, result)
    renderResult(result)

#interfering with blacks slider
def brightness(br, result):
    result = cv2.convertScaleAbs(result, -1, alpha=br*5)
    return result

def saturation(sat, result):
    hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
    hsv[:,:,1] += (sat - 50)/500
    result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return result

def calcWhites(whts, img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)
    L,a,b = cv2.split(lab)

    Lmin = L.min()

    for i in range(len(L)):
        for j in range(len(L[i])):
            if(whts > 50):
                temp = whts - 50
                L[i][j] += temp / 2.5
            else:
                temp = 50 - whts
                L[i][j] -= temp / 2.5

    Lnorm = cv2.normalize(L, None, Lmin, L.max(), cv2.NORM_MINMAX)
    merged = cv2.merge((Lnorm,a,b))
    result = cv2.cvtColor(merged, cv2.COLOR_Lab2BGR)

    return result

def calcBlacks(blks, img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)
    L,a,b = cv2.split(lab)

    Lmax = L.max()

    for i in range(len(L)):
        for j in range(len(L[i])):
            if(blks < 50):
                temp = 50 - blks
                L[i][j] -= temp / 1.5
            else:
                temp = blks - 50
                L[i][j] += temp / 1.5

    Lnorm = cv2.normalize(L, None, L.min(), Lmax, cv2.NORM_MINMAX)
    merged = cv2.merge((Lnorm,a,b))
    result = cv2.cvtColor(merged, cv2.COLOR_Lab2BGR)

    return result

def renderResult(result):
    cv2.imshow("Preview", result)

main()