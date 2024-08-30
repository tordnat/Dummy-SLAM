
import pyzed.sl as sl
import math
import numpy as np
import sys

def main():
    # Create a Camera object
    zed = sl.Camera()

    init_params = sl.InitParameters()
    init_params.depth_mode = sl.DEPTH_MODE.ULTRA  # Use ULTRA depth mode
    init_params.coordinate_units = sl.UNIT.MILLIMETER  # Use meter units (for depth measurements)


    # Open the camera
    err = zed.open(init_params)
    if (err!=sl.ERROR_CODE.SUCCESS):
        exit(-1)
    img_num = 0
    img_to_capture = 1000
    image = sl.Mat()
    depth = sl.Mat()
    point_cloud = sl.Mat()
    while (img_num < img_to_capture):
        if(zed.grab() == sl.ERROR_CODE.SUCCESS):
            zed.retrieve_image(image, sl.VIEW.LEFT)
            zed.retrieve_measure(depth, sl.MEASURE.DEPTH)
            zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA)
            img_num += 1
            x = round(image.get_width() / 2)
            y = round(image.get_height() / 2)
            err, point_cloud_value = point_cloud.get_value(x,y)
            if math.isfinite(point_cloud_value[2]):
                distance = math.sqrt(point_cloud_value[0] * point_cloud_value[0] +
                                    point_cloud_value[1] * point_cloud_value[1] +
                                    point_cloud_value[2] * point_cloud_value[2])
                print(f"Distance to Camera at {{{x};{y}}}: {distance}")
            else : 
                print(f"The distance can not be computed at {{{x};{y}}}")
    zed.close()
    

if __name__ == "__main__":
    main()