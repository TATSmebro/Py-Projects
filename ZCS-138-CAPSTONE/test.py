import cv2 
import matplotlib.pyplot as plt
  
image = cv2.imread("ZCS-138-CAPSTONE/dataset/a" + str(11) + ".jpg") 
cv2.waitKey(0) 
  
# Grayscale 
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
  
# Find Canny edges 
edged = cv2.Canny(gray, 30, 200) 
cv2.waitKey(0) 
  
# Finding Contours
contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 

# Plot edge
plt.imshow(edged, cmap = "gray")
plt.title('Canny edge detection result')
  
print("Number of Contours found = " + str(len(contours))) 
  
# Draw contours 
cv2.drawContours(image, contours, -1, (0, 255, 0), 3) 

# Plot original image with contour
plt.figure(figsize=(8, 8))
plt.imshow(image, cmap = "gray")
plt.title('Image with contour')
plt.legend()
plt.show()