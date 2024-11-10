from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PijjaHistorySerializer, UserCreationSerializer, BuyPizzaSerializer, LogPijjaSerializer, UserIDSerializer, UserSerializer, PijjaSerializer
from .models import DumDumUser, Pijja
from collections import defaultdict
from drf_yasg.utils import swagger_auto_schema
# Create your views here.


def generate_rank(src_di):
    sortable = []
    print(src_di)
    for key, val in src_di.items():
        timestamps = [x[1] for x in val]
        user_name = val[0][0]
        sortable.append((
            len(timestamps),
            max(timestamps),
            key,
            user_name,
        ))
    print(sortable)
    sortable.sort(key = lambda x: (-x[0], -x[1] or float('inf')))
    user_rank = {}
    counter = 1
    for item in sortable:
        user_id = item[2]
        name = item[3]
        user_rank[user_id] = {
            "name": name,
            "rank": counter
        }
        counter += 1
    return user_rank



class UserRequestView(APIView):

    @swagger_auto_schema(request_body=UserCreationSerializer)
    def post(self, request):
        user_creation_serializer = UserCreationSerializer(data = request.data)
        if user_creation_serializer.is_valid():
            user_creation_serializer.save()
            return Response(user_creation_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_creation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        try:
            users = DumDumUser.objects.all()
            serializer = UserSerializer(users, many = True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserDetailView(APIView):
    

    def get(self, request, user_id):
        try:
            users = DumDumUser.objects.filter(user_id = user_id)
            if len(users) == 0 or len(users) > 1:
                if len(users) == 0:
                    raise Exception("User not found")
                else:
                    raise Exception("Multiple users found")
            serializer = UserSerializer(users[0])
            return Response({
                "message": "Data fetched for " + user_id,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({
                "message": "Something went wrong"
            }, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, user_id):
        try:
            users = DumDumUser.objects.filter(user_id = user_id)
            if len(users) == 0 or len(users) > 1:
                if len(users) == 0:
                    raise Exception("User not found")
                else:
                    raise Exception("Multiple users found")
            user = users[0]
            user.delete()
            return Response({
                "message": "User " + user_id + " data deleted successfully",
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({
                "message": "Something went wrong"
            }, status=status.HTTP_400_BAD_REQUEST)

class LeaderboardView(APIView):

    def get(self, request):
        userToPijjaDict = defaultdict(list)
        pizzas = Pijja.objects.filter(state = 'LOGGED')

        for pizza in pizzas:
            userToPijjaDict[pizza.purchased_by.user_id].append([pizza.purchased_by.user_name, pizza.purchased_at.timestamp() * 1000])
        leaderboard_di = generate_rank(userToPijjaDict)

        return Response(leaderboard_di, status=status.HTTP_200_OK)

def bulkCreatePizzas(num):
    return [Pijja.objects.create() for _ in range(num)]

class BuyPizzaView(APIView):

    serializer_class = BuyPizzaSerializer
    @swagger_auto_schema(request_body=BuyPizzaSerializer)
    def post(self, request):
        try:
            serializer = self.serializer_class(data = request.data)
            if serializer.is_valid():
                userId = serializer.data["user_id"]
                pijjaId = serializer.data["pijja_id"]
                users = DumDumUser.objects.filter(user_id = userId)
                if len(users) == 0 or len(users) > 1:
                    if len(users) == 0:
                        raise Exception("User not found")
                    else:
                        raise Exception("Multiple users found")
                valid_user = users[0]
                pijjas = Pijja.objects.filter(pijja_id = pijjaId, state = 'CREATED')
                if len(pijjas) == 0 or len(pijjas) > 1:
                    if len(pijjas) == 0:
                        raise Exception("Pijja not found")
                    else:
                        raise Exception("Multiple pijjas found")
                pijja = pijjas[0]
                if pijja.price > valid_user.wallet_amount:
                    raise Exception("Amount insufficient in wallet")
                valid_user.bought_pizza(pijja)
                return Response({
                    "message": "Pijja Purchased succesfully"
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({
                "message": "Something went wrong"
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        try:
            pizzas = Pijja.objects.filter(purchased_by = None, state='CREATED')
            if pizzas.count() < 10:
                bulkCreatePizzas(10 - pizzas.count())
            qs = Pijja.objects.filter(purchased_by = None, state='CREATED').all()
            serializer = PijjaSerializer(qs, many = True)
            return Response({
                "pizzas": serializer.data,
                "message": "Fetched pizzas"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({
                "message": "Something went wrong"
            }, status=status.HTTP_400_BAD_REQUEST)


class LogPizzaView(APIView):

    serializer_class = LogPijjaSerializer
    @swagger_auto_schema(request_body=LogPijjaSerializer)
    def post(self, request):
        try:
            serializer = self.serializer_class(data = request.data)
            if serializer.is_valid():
                pijja_id = serializer.data["pijja_id"]
                user_id = serializer.data["user_id"]
                pijjas = Pijja.objects.filter(pijja_id = pijja_id, purchased_by = user_id, state = 'PURCHASED')
                if len(pijjas) == 0 or len(pijjas) > 1:
                    if len(pijjas) == 0:
                        raise Exception("Pijja not found")
                    else:
                        raise Exception("Multiple pijjas found")
                pijja = pijjas[0]
                pijja.mark_pijja_logged()
                return Response({
                    "message": "Pijja Logged succesfully"
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({
                "message": "Something went wrong"
            }, status=status.HTTP_400_BAD_REQUEST)
    

class GetPizzasToLogView(APIView):

    serializer_class = UserIDSerializer
    @swagger_auto_schema(request_body=UserIDSerializer)
    def post(self, request):
        try:
            serializer = self.serializer_class(data = request.data)
            if serializer.is_valid():
                user_id = serializer.data['user_id']
                pijjas = Pijja.objects.filter(purchased_by = user_id, state = 'PURCHASED')
                response_serializer = PijjaSerializer(pijjas, many = True)
                return Response({
                    "message": "Pijjas available to LOG",
                    "pijjas": response_serializer.data
                })
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({
                "message": "Something went wrong"
            }, status=status.HTTP_400_BAD_REQUEST)

class UserPizzaHistoryView(APIView):

    def get(self, request, user_id):
        qs = Pijja.objects.filter(purchased_by = user_id, state = 'LOGGED')
        serializer = PijjaHistorySerializer(qs, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)