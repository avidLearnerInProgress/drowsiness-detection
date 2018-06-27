import numpy as np 
import cv2
import _thread, winsound

def detect(face_haar_cascade, eye_haar_cascade):
	stream = 'http://192.168.0.2:8080/video'
	cam = cv2.VideoCapture(stream)
	cnt, i = 0, 0

	while(True):
		ret, current = cam.read()
		gray = cv2.cvtColor(current, cv2.COLOR_BGR2GRAY)
		faces = face_haar_cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors = 1, minSize = (10, 10))
		for (x, y, width, height) in faces:
			roi_gray = gray[y : y+height, x : x+width]
			roi_color = current[y : y+height, x : x+width]
			eyes = eye_haar_cascade.detectMultiScale(roi_gray)

			if len(eyes) == 0:
				print("Eyes closed")
			else:
				print("Eyes open")

			cnt += len(eyes)
			i += 1

			if i == 2:
				i = 0
				if cnt == 0:
					print("You are feeling sleepy!")
					_thread.start_new_thread(beep, ())
				cnt = 0
			
			for (ex, ey, ew, eh) in eyes:
				cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
		cv2.imshow('current_frame', current)

		if cv2.waitKey(1) & OxFF == ord('q'):
			cv2.destroyAllWindows()
			break

def main():
	face_haar_cascade = cv2.CascadeClassifier('../haarcascade_frontalface_default.xml')
	eye_haar_cascade = cv2.CascadeClassifier('../haarcascade_eye.xml')
	detect(face_haar_cascade, eye_haar_cascade)

if __name__ == '__main__':
	main()