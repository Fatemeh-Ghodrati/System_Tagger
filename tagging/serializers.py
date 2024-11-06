from rest_framework import serializers
from .models import Dataset, Tag, Text

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ['id', 'name', 'description']

class TagSerializer(serializers.ModelSerializer):
    tagged_text_count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ['id', 'name', 'is_active', 'dataset', 'tagged_text_count']

    def get_tagged_text_count(self, obj):
        return obj.tagged_text_count()

class TextSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Text
        fields = ['id', 'content', 'dataset', 'tags']
