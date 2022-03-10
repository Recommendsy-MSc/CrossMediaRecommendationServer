from rest_framework import serializers
from ..models import UserModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'

    def create(self, validated_data):
        return UserModel.objects.create_user(**validated_data)

        # # if create user by post data, remove this or else passowrd wont be saved
        # exclude = ['password', ]