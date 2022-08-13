import os
import pickle
import mediapipe as mp
import cv2

from .helper_functions import create_dir, delete_all, mark_detection
from .exceptions import NoFaceFound, TypeUnknown
import face_recognition
from .models import Profile
from mediapipe.python.solutions.drawing_utils import _normalized_to_pixel_coordinates
import numpy as np

static_path = 'static/images/'

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.7,model_selection=1)

def extract_face(filepath,data,type):
    with mp_face_detection.FaceDetection(
        model_selection=1, min_detection_confidence=0.5) as face_detection:
        img = cv2.imread(filepath)
    
        results = face_detection.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        # Draw face detections of each face.
        if results.detections is None:
            raise NoFaceFound
        else:
            if type == 'ID':
                desc = data['name']+"_"+data['surname'] + "/" +data['name'] + "_id.jpg"
                img_name = os.path.join(static_path,desc)
            elif type == 'SELFIE':
                desc = data['name']+ "_"+data['surname'] + "/" +data['name'] + "_selfie.jpg"
                img_name = os.path.join(static_path,desc)
            else:
                raise TypeUnknown

            
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
            
                xmin = int(bbox.xmin * img.shape[1])
                ymin = int(bbox.ymin * img.shape[0])
                width = int(bbox.width * img.shape[1])
                height = int(bbox.height * img.shape[0])
                roi=img[ymin-10:ymin+height+10,xmin-10:xmin+width+10]

            create_dir(static_path,data['name']+"_"+data['surname'])
            cv2.imwrite(img_name, roi)
            return img_name

def encode_face(path,name,profile_id):
    faces = list()
    person = dict()

    for img in os.listdir(path):
        image = face_recognition.load_image_file(path + img)
        face_encodings = face_recognition.face_encodings(image)
        print(face_encodings)
        if len(face_encodings) > 0: #it would be possible that no faces are found in a photo
            faces.append(face_encodings[0])
    person[name] = faces
    profile = Profile.objects.get(profile_id = profile_id)
    profile.encodings = person[name]
    profile.save()
    

def generate_feed(camera):
    cap = cv2.VideoCapture(1)
    font = cv2.FONT_HERSHEY_DUPLEX
    known_face_encodings,known_face_names = load_profiles()

    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break


        image_cols  = int(cap.get(3)) 
        image_rows = int(cap.get(4))

        results = face_detection.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        
        """
        if results.detections:
        for detection in results.detections:
            mp_drawing.draw_detection(img, detection)
        """

        if results.detections:
            for detection in results.detections:
                try:
                    #cv2.waitKey(1000)
                    bbox = detection.location_data.relative_bounding_box
                    rect_start_point = _normalized_to_pixel_coordinates(bbox.xmin, bbox.ymin, image_cols,image_rows)
                    rect_end_point = _normalized_to_pixel_coordinates(bbox.xmin + bbox.width,bbox.ymin + bbox.height, image_cols,image_rows)
                    color = (255, 0, 0)
                    thickness = 2
                    xleft,ytop=rect_start_point
                    xright,ybot=rect_end_point
                    face_locations = [(ytop,xright,ybot,xleft)]
                    cv2.rectangle(img, (xleft,ytop),(xright,ybot) ,color, thickness)
                    face_names = recognize_face(face_locations,img,known_face_encodings,known_face_names)
                    mark_detection(face_names)
                except TypeError:
                    cv2.putText(img, "No face detected", (50,50),font, 1.0, (255, 255, 255), 1)
                except Exception as e:
                    print("Debug later")
                    print(e)
        else:
            cv2.putText(img, "No face detected", (50,50),font, 1.0, (255, 255, 255), 1)

        

        ret,buffer = cv2.imencode('.jpg', img)
        img = buffer.tobytes()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')            


"""
Funkcija koja se koristi za loadanje profila iz baze podataka u arrayeve koje koristi face_recognition libarary

NOTE: 100% postoji efikasniji nacin za ovo napraviti ali trenutacno ga se ne mogu sjetiti
TODO: pokusaj optimizirati load times u slucaju velikog broja objekata iz baze

Params: None
Retruns: 2 lists

"""
def load_profiles():
    profiles = Profile.objects.all()
    known_face_encodings = []
    known_face_names = []
    for profile in profiles:
        for i in range(len(profile.encodings)):
            known_face_encodings.append(profile.encodings[i])
        for i in range(len(profile.encodings)):
            person = profile.name + " " + profile.surname
            known_face_names.append(person)

    return known_face_encodings,known_face_names
    

"""
Funkcija koja se koristi za prepozavanja lica u trenutnom frame-u koristeći face_recognition library

NOTE: trenutacno runna okej ali ima prostora za dodatnu optimizaciju
TODO: dodaj provjere za svaki od ulaznih parametara 

Params: face_locations -> array opisan koordinatama lica unutar slike (ytop,xright,ybot,xleft)
        img -> trenutni open cv frame
        known_face_encodings -> lista koja se dobiva iz funkcije load_profiles te sadrži encodinge svakog lica(profila) koji je u bazi
        known_face_names -> lista koja se dobiva iz funkcije load_profiles te sadrži imena svakog profila koji je u bazi

Retruns: listu sa imenima prepoznatih/ne prepoznatih lica

"""
def recognize_face(face_locations,img,known_face_encodings,known_face_names):
    face_encodings = face_recognition.face_encodings(img, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        try:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)
        except Exception as e:
            print(e)
            
    return face_names
    