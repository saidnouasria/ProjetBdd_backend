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
@api_view(['GET'])
def house_api(request,id=0) :


    if request.method =='GET' :
       houses = House.objects.raw("select * from homes_house")
       house_serializer = HouseSerializer(houses,many=True) 
       return Response(house_serializer.data)
         
@api_view(['POST'])
def add_house_api(request,id=0):
    
    if request.method == 'POST' :
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
        else :
         return Response(house_serializer.errors,status=400 )

@api_view(['GET'])
def my_houses_api(request) :

    id = 1
    if request.method =='GET' :
       my_houses_query=House.objects.raw("SELECT * FROM homes_house WHERE user_id_id = %s", [id])
       my_houses=[house for house in my_houses_query]

       house_serializer = HouseSerializer(my_houses,many=True) 
       return Response(house_serializer.data)



@api_view(['GET','PUT','DELETE'])
def house_details_api(request,house_id):
   try:
      i = House.objects.get(pk=house_id)
   except House.DoesNotExist : 
      return Response(status=404)

   if request.method =='GET' :
       house_query = House.objects.raw("select * from homes_house where house_id = %s ",[house_id])
       house_obj=[house for house in house_query]
       house_serializer = HouseSerializer(house_obj,many=True) 
       return Response(house_serializer.data)
   

   if request.method == 'PUT' :
      house_data=request.data
      house_serializer=HouseSerializer(data=house_data)
      if house_serializer.is_valid(): 
         sql = "UPDATE homes_house SET title=%s , price = %s ,address = %s,city= %s,description =%s, user_id =%s, property_type_id =%s, transaction_id =%s, WHERE house_id = %s ;"
         
         title = request.data.get('title')
         price=request.data.get( 'price')
         address=request.data.get( 'address')
         city=request.data.get('city')
         description=request.data.get('description')
         user_id=request.data.get('user_id')
         property_type_id=request.data.get('property_type_id')
         transaction_id=request.data.get('transaction_id')
         sql = "UPDATE homes_house SET title=%s , price = %s ,address = %s,city= %s,description =%s, user_id =%s, property_type_id =%s, transaction_id =%s, WHERE house_id = %s ;"
     
                 
         with connection.cursor() as cursor:
            cursor.execute(sql,
                           [title,price, address, city, description, user_id,property_type_id,transaction_id,house_id])
         return Response(house_serializer.data )
      else :
         return Response(house_serializer.errors,status=400 )
      

   if request.method == 'DELETE' :
      sql="DELETE FROM homes_house WHERE house_id=%s"
      with connection.cursor() as cursor:
            cursor.execute(sql,[house_id])
      
      return Response("DELETED SUCCESSFULY")