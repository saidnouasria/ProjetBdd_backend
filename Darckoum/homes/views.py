from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.response import Response
from django.db import connection

from .serializers import HouseSerializer,UserSerializer,TransactionSerializer,PropertySerializer
from homes.models import House,User,Transaction,Property


# Create your views here.

@csrf_exempt
@api_view(['GET','POST'])
def house_api(request,id=0) :


    if request.method =='GET' :
       houses = House.objects.raw("select * from homes_house")
       house_serializer = HouseSerializer(houses,many=True) 

       print(house_serializer.data)
       print (connection.queries)

       return Response(house_serializer.data)
    
     # if request.method == 'POST' :
     #     house_data=JSONParser().parse(request)
     #     house_serializer=HouseSerializer(data=house_data)
     #     if serializer.is_valid(): 
     #         House.objects.raw("INSERT INTO homes_house values ")
     #         serializer.save()
     #         return JsonResponse(serializer.data , status= status.HTTP_201_CREATED)
    elif request.method == 'POST' :
        house_data=request.data
        house_serializer=HouseSerializer(data=house_data)
        if house_serializer.is_valid(): 

         sql="insert into homes_house (title , price , address , city , description , property_type_id_id , transaction_id_id , user_id_id )values (%s,%s,%s,%s,%s,%s,%s,%s)"
         values =(
                  house_serializer.data ['title'],
                 house_serializer.data ['price'],
                 house_serializer.data ['address'],
                 house_serializer.data ['city'],
                 house_serializer.data ['description'],
                 house_serializer.data ['user_id'],
                 house_serializer.data ['property_type_id'],
                 house_serializer.data ['transaction_id']
                 )
         with connection.cursor() as cursor:
            cursor.execute(sql,values)

            
        
         return Response(house_serializer.data )