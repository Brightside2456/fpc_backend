from djoser import serializers
from rest_framework import  serializers as s
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUserModel, AddressModel, TokenModel

class CustomUserModelSerializer(serializers.UserCreateSerializer):
    def create(self, validated_data):
        password = validated_data.get('password')
        if password:
            c_user = CustomUserModel(**validated_data)
            c_user.set_password(password)
        else:
            c_user = CustomUserModel(**validated_data)
        c_user.save()
        return c_user


    class Meta(serializers.UserCreateSerializer.Meta):
        model = CustomUserModel
        fields = '__all__'

class AddressSerializer(s.ModelSerializer):
    model = AddressModel
    fields = '__all__'

class TokenModelSerializer(s.ModelSerializer):
    model = TokenModel
    fields = '__all__'

class CustomTokenObtainViewSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['referral_code'] = user.referral_code
        token['address'] = user.address
        token['email'] = user.email
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['phone'] = user.phone
        return token
    def validate(self, attrs):
        attrs['email'] = attrs.get('email')
        return super().validate(attrs)
    pass