# Define the dimensions of the image
width = 640
height = 480

# Define the number of rows and columns
rows = 3
cols = 3

# Compute the width and height of each box
box_width = width // cols
box_height = height // rows

# Define the labels of the boxes
labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

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
        box = {
            'label': labels[i * cols + j],
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
            'mid_x': mid_x,
            'mid_y': mid_y
        }
        boxes.append(box)

# Return the list of boxes
print(boxes)