from helpers import *
def OCR_pipeline(img_path=''):
    """from ID img to ID number through applying contours and wrap prespective , cropping the image , thresholding and finally applying OCR

    Args:
        img_path(string): contains image path , defaults to ''
        
    Raises:
        Exception: if ID_number are not  14 digit

    Returns:
        int: ID number
        """
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
                return(National_ID)
        else:
                    print("No contours")
    else:
                print("No ID Card Found / No contours")

            


#******************************************************

# TODO: make pipeline input: img path, output: ID number, Bool:is_same_person
# Testing
img_path = "C:\\Users\\USER\\Documents\\Grad_project\\Authentication\\Authentication_Grad_Project\\test-dataset\\test_chris.jpg"
test_person_path = "C:\\Users\\USER\\Documents\\Grad_project\\Authentication\\Authentication_Grad_Project\\test-dataset\\test_chris_person.jpg"
is_same_persone = match_user_id_pic(img_path,test_person_path)
print(f"is_same_persone: {is_same_persone}")
print(f'National ID: {OCR_pipeline(img_path)}')

        

