from rest_framework import serializers
from news.models import *


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class PageENSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageEN
        fields = '__all__'

class PageCNSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageCN
        fields = '__all__'