from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Advisor, Main

class RegistrationSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}
## if password is not hashing 
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class AdvisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advisor
        fields=['khiladi','advisor_image','advisor_name','booking_time']
class MainSerializer(serializers.ModelSerializer):
    aadmi = AdvisorSerializer(many=True)

    class Meta:
        model = Main
        fields = ['user','aadmi']

        
