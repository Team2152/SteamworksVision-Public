import tapeDetector
import cv2

def run(queue, status):
	camera = cv2.VideoCapture(0) 
	myTapeDetector = tapeDetector.tapeDetector("peg", queue)
	while not status.isStopped():
		grabbed, frame = camera.read()
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break
		result, mask = myTapeDetector.detectTape(frame)
		cv2.imshow("window1", result)
		cv2.imshow("window2", mask)
	camera.release
	cv2.destroyAllWindows


