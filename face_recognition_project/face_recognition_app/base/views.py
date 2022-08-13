
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from .serializer import ProfileSerializer
from .helper_functions import check_for_valid_string, create_temp, delete_file
from .face_recog_functions import encode_face, extract_face, generate_feed
from .exceptions import NoFaceFound
from .models import Profile
from rest_framework import status
from django.http import StreamingHttpResponse


@api_view(['POST'])
def registerProfile(request):
    data = request.data
  
    data = check_for_valid_string(data)
    id_image = request.FILES.get('id_image')
    selfie_image = request.FILES.get('selfie_image')
    filepath_id = create_temp(id_image)
    filepath_selfie = create_temp(selfie_image)
    
    
    try:
        id_image_path = extract_face(filepath_id,data,"ID")
        if(id_image_path == 0 ):
            print("Dir for given name already exists, please contact the admin!")

        delete_file(filepath_id)
    except NoFaceFound: 
        message = {'details': 'No face found on id card!'}
        return Response(message,status=status.HTTP_404_NOT_FOUND)

    try:
        selfie_image_path = extract_face(filepath_selfie,data,"SELFIE")
        delete_file(filepath_selfie)
    except NoFaceFound: 
        message = {'details': 'No face found on selife image!'}
        return Response(message,status=status.HTTP_404_NOT_FOUND)

    profile = Profile.objects.create(
        name = data['name'],
        surname = data['surname'],
        id_image = id_image_path,
        selfie_image = selfie_image_path,
    )
    encode_face('static/images/'+data['name']+ "_" + data['surname']+"/",data['name'],profile.profile_id)
    serializer = ProfileSerializer(profile,many= False)
    return Response(serializer.data)


def camerafeed(request): 
    return StreamingHttpResponse(generate_feed(1),content_type="multipart/x-mixed-replace;boundary=frame")
    
@api_view(['GET'])
def test(request,pk):
    person = Profile.objects.get(profile_id = pk)
    print(person.encodings)
    serializer = ProfileSerializer(person,many=False)
    return Response(serializer.data)
