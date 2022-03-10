from rest_framework import viewsets
from ..models import UserModel
from django.db.models import QuerySet
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..serializers import UserSerializer
from ..helper import customResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView





class UserViewSet(viewsets.ModelViewSet):
    queryset: QuerySet = UserModel.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer


    # Configures Permissions for Individual View Actions

    def get_permissions(self):
        print(self.action)
        if self.action == 'create' or self.action == 'exists':
            self.permission_classes = [AllowAny, ]
        else:
            self.permission_classes = [IsAuthenticated, ]

        return super().get_permissions()

    @action(detail=False, methods=['POST', 'GET'], )
    def exists(self, request: Request, pk=None):
        data = request.data
        print(str(data))
        email = data.get('email')
        print(email)
        try:
            user: UserModel = UserModel.objects.filter(email__exact=email).get()
            serializer = UserSerializer(user, many=False)
            resp = serializer.data
            resp.pop('password')
            token, created = Token.objects.get_or_create(user=serializer.data['id'])
            print(token.key)
            resp = {
                'token': token.key,
                'user': serializer.data,
            }
            return customResponse(True, resp)
        except Exception as e:
            print(e)
            return customResponse(False, {"error": str(e)})

    def retrieve(self, request, *args, **kwargs):
        instance: UserModel = self.get_object()
        serializer = self.get_serializer(instance)
        resp = serializer.data
        resp.pop('password')
        return customResponse(True, resp)


    def create(self, request, *args, **kwargs):
        # return customResponse(False, {"error": "Method Not Allowed"})
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            user = UserModel.objects.get_by_natural_key(serializer.validated_data.get('email'))
            token, created = Token.objects.get_or_create(user=user)
            data = serializer.data
            data.pop('password')
            resp = {
                'token': token.key,
                'user': data
            }
            return customResponse(True, resp)
        except:
            return customResponse(False,)

# custom auth token so that can return desired response

class ObtainAuthTokenViewSet(ObtainAuthToken):
    def get(self, request):
        return Response(
            {
                "hi": "hello"
            }
        )

    def post(self, request, *args, **kwargs):
        print(request)
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                {
                    "success": "false",
                    "error": "Invalid Credentials",
                },
                status=HTTP_401_UNAUTHORIZED
            )

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user = UserModel.objects.get(id=token.user_id)
        resp = UserSerializer(user).data
        resp.pop('password')
        data = {'auth_token': token.key, 'user': resp}
        return customResponse(True, data)



class CreateExistingToken(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        for user in UserModel.objects.all():
            Token.objects.get_or_create(user=user)

        return Response(
            {
                "success": "true"
            }
        )
