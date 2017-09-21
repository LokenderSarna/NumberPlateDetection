from PIL import Image
import subprocess
import util
import cv2
import numpy as np
tesseract_exe_name = 'tesseract' 
scratch_image_name = "temp.bmp" 
scratch_text_name_root = "temp" 
cleanup_scratch_flag = True
def call_tesseract(input_filename, output_filename):
	args = [tesseract_exe_name, input_filename, output_filename]
	proc = subprocess.Popen(args)
	retcode = proc.wait()
	if retcode!=0:
		errors.check_for_errors()

def image_to_string(im, cleanup = cleanup_scratch_flag):
	try:
		util.image_to_scratch(im, scratch_image_name)
		call_tesseract(scratch_image_name, scratch_text_name_root)
		text = util.retrieve_text(scratch_text_name_root)
	finally:
		if cleanup:
			util.perform_cleanup(scratch_image_name, scratch_text_name_root)
	return text


if __name__=='__main__':
    cap = cv2.VideoCapture(0)

    while(True):
        # Capture frame-by-frame
        ret,img = cap.read()
        img1=img
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret,img = cv2.threshold(img,100,255,cv2.THRESH_BINARY)
        img = cv2.GaussianBlur(img,(5,5),0)
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
        img = cv2.erode(img,kernel)
        img = cv2.dilate(img,kernel)
        cv2.imshow('PRESS C TO CAPTURE',img1)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            break
    cv2.imwrite('t.jpg',img)
    im = Image.open('t.jpg')
    text = image_to_string(im)
    text = text.translate(None, '!@#$%^&*(){[-=}]:;_":><?/.~`')
    print text
    cv2.destroyAllWindows()

