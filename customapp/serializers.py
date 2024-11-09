from rest_framework.serializers import ModelSerializer, Serializer, ListSerializer
from rest_framework import serializers
from .models import DumDumUser, Pijja

class UserCreationSerializer(ModelSerializer):
    class Meta:
        model = DumDumUser
        fields = ['user_name', 'age', 'gender']

class UserSerializer(ModelSerializer):
    class Meta:
        model = DumDumUser
        fields = '__all__'

class UserIDSerializer(Serializer):
    user_id = serializers.CharField(max_length=20)

class BuyPizzaSerializer(Serializer):
    user_id = serializers.CharField(max_length=20)
    pijja_id = serializers.CharField(max_length=20)

class LogPijjaSerializer(Serializer):
    pijja_id = serializers.CharField(max_length=20)
    user_id = serializers.CharField(max_length=20)


class PijjaSerializer(ModelSerializer):
    class Meta:
        model = Pijja
        fields = ['pijja_id', 'price']