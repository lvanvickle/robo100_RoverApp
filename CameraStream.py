import cv2

class CameraStream:
    def __init__(self):
        # Initialize video capture on the default camera
        self.cap = cv2.VideoCapture(0)
        # Check if the camera is successfully opened
        if not self.cap.isOpened():
            raise Exception("Could not open video device")
        
        # Load the Haar cascade file used for face detection
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        # Check if the cascade classifier has been successfully loaded
        if self.face_cascade.empty():
            raise Exception("Failed to load cascade classifier")
        
    def __del__(self):
        self.cap.release() # Release the camera when done
        
    def get_frame(self):
        # Capture a single frame from the camera
        success, image = self.cap.read()
        # If frame could not be captured successfully, log an error and return None
        if not success:
            return None
        else:
            # If successful, process the capture image for face detection
            return self.process_frame(image)
        
    def process_frame(self, image):
        # Convet the captured image to grayscale for better face detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Detect faces in the image using the preloaded Haar cascade
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        
        # Initialize a counter for the number of faces detected
        face_count = 0
        # Draw rectangles around faces and count them
        for(x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            face_count += 1
            
        # Print the number of detected faces
        if face_count > 0:
            print(f"Detected {face_count} face(s) in this frame.")
            
        # Encode the frame into JPEG format
        _, jpeg = cv2.imencode('.jpeg', image)
        return jpeg.tobytes()
    
    def frames(self):
        # Continuously generate frames to be used for streaming
        while True:
            frame = self.get_frame()
            # Only show frames that were successfully captured
            if frame is not None:
                yield(b'--frame\r\n'
                      b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')