from django.shortcuts import render
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from .serializers import   AdvisorSerializer,MainSerializer,RegistrationSerializers
from rest_framework.response import Response
from .models import Advisor,Main
from rest_framework.authentication import TokenAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,AllowAny
from rest_framework import status

#---------------------------------------------------------token based auth --------------------------------------------#######
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@api_view(['POST'],)
def registration_view(request):
    if request.method == "POST":
        serializer = RegistrationSerializers(data = request.data)
        data={}
        if serializer.is_valid():

            account = serializer.save()
            data['username'] = account.username
            data['email'] = account.email
            token = Token.objects.get(user=account).key
            data['token'] = token
            data['Response'] = "Registration success "
            return Response(data)
    else:
        msg={'msg':"post request bhej bhai "}
        return Response(msg)

@api_view(['POST'],)
@authentication_classes([TokenAuthentication,BasicAuthentication])
@permission_classes([AllowAny])
def logout(request):
    if request.method == "POST":
        print('-------------------------------------------------------------------------------------------------------')
        # print(request.user)
        request.user.auth_token.delete()
        return Response(
            {
                "msg":"you are logout "
            }
        )

#-------------------------------------------------------token based auth end------------------------------------------######



@api_view(['GET','POST','PATCH','DELETE','PUT'])
@authentication_classes([TokenAuthentication,BasicAuthentication])
@permission_classes([IsAuthenticated])
def book_api(request):
    if request.method == "GET":
        stu=Main.objects.all()
        print((stu))
        serializer  = MainSerializer(stu,many=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response(serializer.data)

@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication,BasicAuthentication])
@permission_classes([IsAuthenticated])
def fav_api(request):
    if request.method == "GET":
            stu=Advisor.objects.all()
            print((stu))
            serializer  = AdvisorSerializer(stu,many=True)
            msg={'msg':" apka favourite abhi koi  nhi hai phle kuch add kro phir dekho"}
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)


    if request.method == "POST":
        # print(request.data)

        # print(request.user)
        # print(request.user.id)
        stu=Main.objects.get(user_id=request.user)
        myd = stu
        print(type(myd))
        print(stu)
        print(type(stu))
        iscorrectuser = request.data['khiladi'] 
        print(type(iscorrectuser))
        if str(myd.id) == iscorrectuser:
            print("yes")
        print(type(str(myd.id)))

        # print("-------------------------------------------------")
        if iscorrectuser == str(myd.id):
            serializer = AdvisorSerializer(data=request.data)
            print(serializer)
            if serializer.is_valid(): 
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors)
        else:
            msg= {'msg':'Not permitted '}
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)

        



        
