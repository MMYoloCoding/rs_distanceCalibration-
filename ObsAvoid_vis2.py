import pyrealsense2 as rs
import numpy as np
import cv2
import datetime
box_dim = 15
level = 0 #     0 = 90cm, 1 = 120cm
zone_max_height = [0.62,0.71,0.82,1.18]
class Box:
    def __init__(self, x1, y1, x2, y2, mid_x, mid_y):
        # self.label = label
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.mid_x = mid_x
        self.mid_y = mid_y
def box_cal(width,height,box_dim):
    # Define the dimensions of the image

    # Define the number of rows and columns
    rows = box_dim
    cols = box_dim

    # Compute the width and height of each box
    box_width = width // cols
    box_height = height // rows

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
def draw_box(boxes,xs,ys,ye,box_dim):
       for i in range((box_dim*ys),len(boxes)-(box_dim*ye)):
            if i%box_dim < xs:
                continue
            cv2.circle(depth_colormap, (frame_box[i].mid_x,frame_box[i].mid_y), 4, (0, 255, 255),-1)

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
frame_box = box_cal(848, 480,box_dim)
cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)

while (True):
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    depth_image = np.asanyarray(depth_frame.get_data())
    # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
    xs,ys = 2,3
    xe,ye = 15,1
    draw_box(frame_box,xs,ys,ye,box_dim)
    counter = 0
    obj_max_distance = 100000.0
    goOrStop = True

    # start_time = datetime.datetime.now()
    for k in range((15*3),len(frame_box)-(15*1)):
        if frame_box[k].mid_x <=2:
            continue
        current_distance = depth_frame.get_distance(frame_box[k].mid_x,frame_box[k].mid_y)
        if 770<frame_box[k].mid_x<848 and current_distance <= (zone_max_height[0] +level*0.15) and current_distance != 0: 
                        obj_max_distance = current_distance
                        cv2.circle(depth_colormap, (frame_box[k].mid_x,frame_box[k].mid_y), 4, (0, 0, 255),-1)
                        print("Object at A")
                        goOrStop = False
                        break
        if 660<frame_box[k].mid_x<769 and current_distance <= (zone_max_height[1] + level*0.15) and current_distance != 0: 
                        obj_max_distance = current_distance
                        cv2.circle(depth_colormap, (frame_box[k].mid_x,frame_box[k].mid_y), 4, (0, 0, 255),-1)
                        goOrStop = False
                        print("Object at B")
                        break
        if 460<frame_box[k].mid_x<659 and current_distance <= (zone_max_height[2] + level*0.2) and current_distance != 0: 
                        obj_max_distance = current_distance
                        cv2.circle(depth_colormap, (frame_box[k].mid_x,frame_box[k].mid_y), 4, (0, 0, 255),-1)
                        goOrStop = False
                        print("Object at C")
                        break
        if 110<frame_box[k].mid_x<459 and current_distance <= (zone_max_height[3] +level*0.17) and current_distance != 0: 
                        obj_max_distance = current_distance
                        cv2.circle(depth_colormap, (frame_box[k].mid_x,frame_box[k].mid_y), 4, (0, 0, 255),-1)
                        goOrStop = False
                        print("Object at D")
                        break
    cv2.imshow('RealSense', depth_colormap)
    # end_time = datetime.datetime.now()
    # time_diff = end_time- start_time
    # print("Time after ini is ", time_diff.total_seconds())
    if goOrStop == True:
        print("Go")
    else:
        print("STOP: Detect object at {}cm.".format(obj_max_distance * 100))
    key = cv2.waitKey(1)
    if key ==  27:
        break
   
pipeline.stop()
