from .models import User
from .serializers import *
from django.contrib.auth import authenticate
from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view,action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,GenericViewSet,ReadOnlyModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

#when sending token in header we nedd to specify Toekn or Bearer
# use [BearerTokenAuthentication] insted of [TokenAuthentication]
class BearerTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'

#login for Employee and Pilot. returns a token
class login(APIView):
    def post(self, request, format=None):
        try:
            username = request.data['username']
            password = request.data['password']
        except:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)    
        
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        token,_ = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user) # or use payload = model_to_dict(user) 
        # refresh = RefreshToken.for_user(user)
        return Response({"payload":serializer.data,"access":str(token.key)})
    
class view_details(APIView):
    # authentication_classes = [JWTAuthentication]
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        auth_token = request.auth
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)
 
class UserdetailViewset(ListModelMixin,GenericViewSet):
    serializer_class = UserSerializer
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)
    
    @action(detail=False,methods=['GET'])
    def me(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data) 
    # def get_queryset(self):
    #     return User.objects.filter(username=self.request.user.username)
    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
       
#Station viewset
class StationViewSet(ReadOnlyModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer 
    