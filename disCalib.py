import cv2
import numpy as np
import pyrealsense2 as rs
# from realsense_depth import *
pipeline = rs.pipeline()
config = rs.config()
# Get device product line for setting a supporting resolution
# pipeline_wrapper = rs.pipeline_wrapper(pipeline)
# pipeline_profile = config.resolve(pipeline_wrapper)
# device = pipeline_profile.get_device()
# device_product_line = str(device.get_info(rs.camera_info.product_line))

config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
#config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 15)



# Start streaming
pipeline.start(config)

point = [1100, 300]
def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

def get_frame():
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    #color_frame = frames.get_color_frame()


    depth_image = np.asanyarray(depth_frame.get_data())
    #color_image = np.asanyarray(color_frame.get_data())
    # if not depth_frame or not color_frame:
    #     return False, None, None
    return True, depth_image,depth_frame

# Initialize Camera Intel Realsense

# Create mouse event
cv2.namedWindow("Real Sense")
while True:
    ret, depth_frame, depth_real_frame = get_frame()
    # Show distance for a specific point
    distance = depth_real_frame.get_distance(1100,300)
    # for i in range(220,420):
    xs, ys = 1000, 100
    xe, ye = 1200, 500
    cnt = 0
    for i in range(xs,xe):
        for j in range(ys,ye):
            current_distance = depth_real_frame.get_distance(i,j)
            if(current_distance < 0.8 and current_distance < distance and current_distance != 0):
                distance = depth_real_frame.get_distance(i,j)
                point= [i,j]
                cnt = cnt + 1
            if cnt == 5:
                break
        if cnt == 5:
            break

    # cv2.circle(color_frame, point, 4, (0, 0, 255))
    # cv2.rectangle(color_frame,(xs,ys),(xe,ye), (255,0,0),thickness=3)
    # cv2.putText(color_frame, "{}cm at {},{}".format("{:.1f}".format(distance*100),point[1],point[0]), (point[0], point[1] - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
    print("Closest point = ", point, " with distance = {}".format("{:.1f}".format(distance*100)))

    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_frame, alpha=0.03), cv2.COLORMAP_JET)
    cv2.rectangle(depth_colormap,(xs,ys),(xe,ye), (0,255,255),thickness=3)
    cv2.circle(depth_colormap, point, 4, (0, 255, 255))
    cv2.putText(depth_colormap, "{}cm at {},{}".format("{:.1f}".format(distance*100),point[1],point[0]), (point[0], point[1] - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)


    # color_frame = image_resize(color_frame, 720)
    depth_colormap = image_resize(depth_colormap, 720)
    # big_screen = np.hstack((color_frame,depth_colormap))
    #cv2.imshow("Real Sense", big_screen)
    cv2.imshow("Real Sense", depth_colormap)
    # cv2.imshow("Color frame", color_frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

pipeline.stop()



