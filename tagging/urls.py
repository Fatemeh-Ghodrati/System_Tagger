from rest_framework.routers import DefaultRouter
from .views import DatasetViewSet, TagViewSet, TextViewSet, CSVUploadViewset


router = DefaultRouter()
router.register(r'dataset', DatasetViewSet)
router.register(r'tag', TagViewSet)
router.register(r'text', TextViewSet)
router.register(r'csv-upload', CSVUploadViewset, basename='csv-upload')

urlpatterns = router.urls