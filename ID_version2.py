from helpers import *
img_path = "C:\\Users\\USER\\Documents\\Grad_project\\Authentication\\Authentication_Grad_Project\\test-dataset\\test_chris.jpg"

img = get_img_from_path(img_path)
gray = img_to_gray(img)

# Get homography between Gomhoreyet Masr template and ID
M, match_boundingbox = findOrientation(gray)

# If matches found Apply Orientation
if M is not None:
    gray, img, M = applyOrientation(gray, img, M)

    # blur gray for smoothing the image for the edge detection
    gray = blur_img(gray)
    # Adaptive threshold
    bin = adaptive_threshold(gray,11, 2)
    # Edge detection
    edges = canny_edge_detector(bin, 200, 600)


    # Getting largest Contour
    contour_bbox, largest_contour = findLargestContour(edges)
    if contour_bbox is not None:

        cropped_img = output_img(img, largest_contour) 
        cropped_gray = img_to_gray(cropped_img)
        ##output_pth = 'C:\\Users\\USER\\Documents\\Grad_project\\Authentication\\Authentication_Grad_Project\\output\\'

        selections, bboxes = detect_text_regions(cropped_gray)
        for i in selections:
            x, y, x2, y2 = bboxes[i]
            text_img = cropped_img[y:y2, x:x2]
            text_bin = preproccess_OCR(text_img)
            id_str = OCR_pytesseract(text_bin).replace(" ","").replace("\n","").rstrip()
            if len(id_str) != 14:
                continue
            National_ID = int(id_str)
            print(National_ID)

            

            



                    
    else:
                print("No contours")
else:
            print("No ID Card Found / No contours")
        

