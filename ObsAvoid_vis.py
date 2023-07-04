import pyrealsense2 as rs
import numpy as np
import cv2
import datetime
class Box:
    def __init__(self, x1, y1, x2, y2, mid_x, mid_y):
        # self.label = label
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.mid_x = mid_x
        self.mid_y = mid_y
def box_cal(width,height):
    # Define the dimensions of the image

    # Define the number of rows and columns
    rows = 15
    cols = 15

    # Compute the width and height of each box
    box_width = width // cols
    box_height = height // rows

    # Define the labels of the boxes
    # labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

    # Compute the coordinates and midpoints of each box
    boxes = []
    for i in range(rows):
        for j in range(cols):
            # Compute the top-left and bottom-right coordinates of the box
            x1 = j * box_width
            y1 = i * box_height
            x2 = x1 + box_width
            y2 = y1 + box_height
            
            # Compute the midpoint of the box
            mid_x = (x1 + x2) // 2
            mid_y = (y1 + y2) // 2
            
            # Add the box coordinates and midpoint to the list
            new_box = Box(
                # label= labels[i * cols + j],
                x1= x1,
                y1= y1,
                x2= x2,
                y2= y2,
                mid_x= mid_x,
                mid_y= mid_y
            )
            boxes.append(new_box)
    return boxes
def draw_box(boxes):
       for i in range(len(boxes)):
            cv2.circle(depth_colormap, (frame_box[i].mid_x,frame_box[i].mid_y), 4, (0, 255, 255),-1)
       pass

max_distance = 2.0 # Declare number of pixels to stop
pipeline = rs.pipeline()
config = rs.config()
# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)
pipeline.start(config)
count = 0
frame_box = box_cal(848, 480)
cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)

while (True):
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    depth_image = np.asanyarray(depth_frame.get_data())
    # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
    draw_box(frame_box)
    # cv2.imshow('RealSense', depth_colormap)
    # distances = depth_data.flatten().tolist()
    counter = 0
    obj_max_distance = 100000.0
    # test_distance = 0.0
    goOrStop = True

    # start_time = datetime.datetime.now()
    for k in range((15*3),len(frame_box)-(15*1)):
        if frame_box[k].mid_x <=2:
            continue
        current_distance = depth_frame.get_distance(frame_box[k].mid_x,frame_box[k].mid_y)
        # if depth_frame.get_distance(frame_box[k].mid_x,frame_box[k].mid_y) < max_distance:
            # print("Object Found in region ", k)
            # for i in range(frame_box[k].x1,frame_box[k].x2):
            #     for j in range(frame_box[k].y1,frame_box[k].y2):
                    # current_distance = depth_frame.get_distance(i, j)
                    # test_distance = distances[i * 1280 + j]
        if 770<frame_box[k].mid_x<848 and current_distance <= 0.62 and current_distance != 0: 
                        obj_max_distance = current_distance
                        cv2.circle(depth_colormap, (frame_box[k].mid_x,frame_box[k].mid_y), 4, (0, 0, 255),-1)
                        print("Object at A")
                        goOrStop = False
                        break
        if 660<frame_box[k].mid_x<769 and current_distance <= 0.71 and current_distance != 0: 
                        obj_max_distance = current_distance
                        cv2.circle(depth_colormap, (frame_box[k].mid_x,frame_box[k].mid_y), 4, (0, 0, 255),-1)
                        goOrStop = False
                        print("Object at B")
                        break
        if 460<frame_box[k].mid_x<659 and current_distance <= 0.82 and current_distance != 0: 
                        obj_max_distance = current_distance
                        cv2.circle(depth_colormap, (frame_box[k].mid_x,frame_box[k].mid_y), 4, (0, 0, 255),-1)
                        goOrStop = False
                        print("Object at C")
                        break
        if 110<frame_box[k].mid_x<459 and current_distance <= 1.18 and current_distance != 0: 
                        obj_max_distance = current_distance
                        cv2.circle(depth_colormap, (frame_box[k].mid_x,frame_box[k].mid_y), 4, (0, 0, 255),-1)
                        goOrStop = False
                        print("Object at D")
                        break
                    # if counter == 50000:
                    #     goOrStop = False
                    #     break
                
                # if counter == 50000:
                #     break
        # if counter == 50000:
        #             break
    cv2.imshow('RealSense', depth_colormap)
    # end_time = datetime.datetime.now()
    # time_diff = end_time- start_time
    # print("Time after ini is ", time_diff.total_seconds())



    if goOrStop == True:
        print("Go")
    else:
        print("STOP: Detect object at {}cm.".format(obj_max_distance * 100))
        # print("TEST: Detect object at {}cm.".format(test_distance * 100))
    key = cv2.waitKey(1)
    if key ==  27:
        break
   
pipeline.stop()
