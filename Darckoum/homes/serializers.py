from rest_framework import serializers 
from homes.models import House,User,Transaction,Property

class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model=House
        fields='__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'
        
class loginSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['user_id','password']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=  Transaction
        fields='__all__'


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model=Property
        fields='__all__'