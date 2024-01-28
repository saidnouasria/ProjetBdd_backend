from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.response import Response
from django.db import connection
from django.contrib.auth import authenticate, login
from rest_framework import status
from django.db.models import Q
from .serializers import HouseSerializer,UserSerializer,TransactionSerializer,PropertySerializer,loginSerializer
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

         sql="insert into homes_house (title , price , address , city , description , user_id_id , property_type_id_id , transaction_id_id  )values (%s,%s,%s,%s,%s,%s,%s,%s)"
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
         
         
         title = request.data.get('title')
         price=request.data.get( 'price')
         address=request.data.get( 'address')
         city=request.data.get('city')
         description=request.data.get('description')
         user_id=request.data.get('user_id')
         property_type_id=request.data.get('property_type_id')
         transaction_id=request.data.get('transaction_id')
         sql = "UPDATE homes_house SET title=%s , price = %s ,address = %s,city= %s,description =%s, user_id_id =%s, property_type_id_id =%s, transaction_id_id =%s WHERE house_id = %s ;"
     
                 
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

   else:
      return Response(status=400)
@api_view(['POST'])
def signup_api(request):
      if request.method == 'POST':
         user_data=request.data
         user_serializer=UserSerializer(data=user_data)
         if user_serializer.is_valid():
            sql="insert into homes_user (first_name, last_name, email, phone, gender, password )values (%s,%s,%s,%s,%s,%s)"
            values =(
                     user_serializer.data ['first_name'],
                     user_serializer.data ['last_name'],
                     user_serializer.data ['email'],
                     user_serializer.data ['phone'],
                     user_serializer.data ['gender'],
                     user_serializer.data ['password']

                  )
            with connection.cursor() as cursor:
               cursor.execute(sql,values)

               
         
            return Response(user_serializer.data,status=201)
         else:
            return Response(user_serializer.errors,status=400)

from django.contrib.auth.hashers import check_password

@api_view(['POST'])
def login_api(request):
    if request.method == 'POST':
        user_data = request.data
        login_serializer = loginSerializer(data=user_data)
        if login_serializer.is_valid():
            email = login_serializer.data.get('email')
            password = login_serializer.data.get('password')
            print(f"Attempting login with email: {email}, password: {password}")
            authnig = User.objects.raw(f"select password from homes_user where email = {email}")
            print(f"Authentication result: {authnig}")
            if authnig == password:
                return Response({'message': 'Login successful'})
            

      #       if user is not None and check_password(password, user.password):
      #           login(request, user)
      #           return Response({'message': 'Login successful'})
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
      #   else:
      #       return Response(login_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            


@api_view(['GET'])
def search_api(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        print(f"Searching for {query}")
        houses = House.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        print(f"Found {len(houses)} results")
        house_serializer = HouseSerializer(houses, many=True)
        return Response(house_serializer.data)


