import cv2

# Function to update variable based on slider position
def update_value(value):
    global variable
    variable = value

# Initialize variable
variable = 0

# Create OpenCV window
cv2.namedWindow("Slider Demo")

# Create trackbar and attach it to the window
cv2.createTrackbar("Value", "Slider Demo", variable, 100, update_value)

# Loop to update window and variable
while True:
    # Do some processing with the variable
    processed_image = cv2.imread("image.jpg")
    processed_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2BGRA)
    processed_image = cv2.threshold(processed_image, variable, 255, cv2.THRESH_BINARY)[1]

    # Display the processed image in the window
    cv2.imshow("Slider Demo", processed_image)

    # Check for user input to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up