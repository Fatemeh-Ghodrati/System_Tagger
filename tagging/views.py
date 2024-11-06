from rest_framework import viewsets, permissions, filters
from .models import Dataset, Tag, Text
from .serializers import DatasetSerializer, TagSerializer, TextSerializer
import csv
from rest_framework.response import Response

# Create your views here.
class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        user = self.request.user
        return Dataset.objects.filter(operatoraccess__user=user)
    

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        dataset_id = self.request.query_params.get('dataset_id')
        return Tag.objects.filter(dataset_id=dataset_id)


class TextViewSet(viewsets.ModelViewSet):
    queryset = Text.objects.all()
    serializer_class = TextSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]  
    search_fields = ['content'] 

    def get_queryset(self):
        return Text.objects.all()
    
    def perform_create(self, serializer):
        tags = self.request.data.get('tags', [])
        text_instance = serializer.save()

        if tags:
            for tag_id in tags:
                try:
                    tag = Tag.objects.get(id=tag_id)
                    text_instance.tags.add(tag)
                except Tag.DoesNotExist:
                    continue  
                
        return text_instance
    
    
class CSVUploadViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        dataset_id = request.data.get('dataset_id')
        csv_file = request.FILES.get('file')

        if not csv_file:
            return Response({"error": "No file provided"}, status=400)

        reader = csv.reader(csv_file.read().decode('utf-8').splitlines())
        for row in reader:
            Text.objects.create(dataset_id=dataset_id, content=row[0])

        return Response({"status": "CSV data added to dataset"})

