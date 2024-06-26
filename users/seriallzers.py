from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
           'id',  
           'email',
           'first_name',
           'last_name', 
           'phone', 
           'telegram_id', 
           'password' 
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        new_user = User(**validated_data)
        new_user.set_password(password)
        new_user.is_staff = False
        new_user.save()
        return  new_user
