from rest_framework import serializers
from rest_framework.throttling import UserRateThrottle

from .models import Project


class SearchThrottle(UserRateThrottle):
    rate = '200/min'


class ProjectSerializer(serializers.ModelSerializer):

    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Project
        exclude = ('user', 'datetime')

    def get_is_owner(self, obj):

        return self.context['request'].user == obj.user