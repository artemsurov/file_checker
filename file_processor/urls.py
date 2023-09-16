from file_processor.routes import DetailPostRouter
from file_processor.views import FileProcessorViewSet

router = DetailPostRouter()
router.register('', FileProcessorViewSet)

urlpatterns = router.urls
