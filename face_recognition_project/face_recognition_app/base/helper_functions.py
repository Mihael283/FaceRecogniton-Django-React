import os
import tempfile
import datetime
from django.utils import timezone as tz
from .models import Detections

def create_temp(file):
    ### write the data to a temp file
    tup = tempfile.mkstemp() # make a tmp file
    f = os.fdopen(tup[0], 'wb') # open the tmp file for writing
    f.write(file.read()) # write the tmp file
    f.close()
    ### return the path of the file
    filepath = tup[1] # get the filepath
    return filepath

def delete_file(file):
    if os.path.isfile(file):
        os.remove(file)

def create_dir(static_path,name):
    path = os.path.join(static_path, name)
    path_exists = os.path.exists(path)
    if(path_exists is False):
        os.mkdir(path)

def check_for_valid_string(data):
    if(' ' in data['name']):
        data['name']=data['name'].replace(" ","")
        print("Removed whitespace from name!")
    
    if(' ' in data['surname']):
        data['surname']=data['surname'].replace(" ","")
        print("Removed whitespace from surname!")

    return data

def delete_all():
    Detections.objects.all().delete()

"""
Funkcija koja se koristi za dodavanje detekcija u bazu poodataka tocnije spremanje novih detekcija u bazu

Params: face_names -> array imena napravljenih u funkciji recognize_face, koristi se za dodavanje u bazu
    
Retruns: NON

"""

def mark_detection(face_names):
    if not face_names:
        return 0

    d = tz.now() - datetime.timedelta(seconds=15)
    detections = Detections.objects.filter(time__range = [d,tz.now()])
    if not detections:
        for name in face_names:
            if(name == "Unknown"):

                det = Detections.objects.create(
                    name = "Unknown",
                    surname = "Unknown",
                    time = tz.now(),
                    unknown = True,
                )
                det.save()
            else:
                det = Detections.objects.create(
                    name = name.split()[0],
                    surname = name.split()[1],
                    time = tz.now(),
                    unknown = False,
                )
                det.save()
    else:
        for name in face_names:
            if(name == "Unknown"):
                pass
            elif(detections.filter(name = name.split()[0], surname = name.split()[1]).exists()):
                pass
            else:
                det = Detections.objects.create(
                    name = name.split()[0],
                    surname = name.split()[1],
                    time = tz.now(),
                    unknown = False,
                )
                det.save()

       
        

       
        

