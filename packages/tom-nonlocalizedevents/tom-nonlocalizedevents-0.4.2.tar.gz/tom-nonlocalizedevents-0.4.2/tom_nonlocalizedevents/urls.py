from django.urls import path

from tom_common.api_router import SharedAPIRootRouter  # a singleton DRF Router

from . import views

# this mechanism allows ViewSets to be registered with the tom_common Router
# for any of the INSTALLED_APPS (i.e. the routes are added because the APP is
# INSTALLED -- nothing else is required))
router = SharedAPIRootRouter()
router.register(r'nonlocalizedevents', views.NonlocalizedEventViewSet)
router.register(r'eventlocalizations', views.EventLocalizationViewSet)
router.register(r'eventcandidates', views.EventCandidateViewSet)

# app_name provides namespace in {% url %} template tag
# (i.e. {% url 'nonlocalizedevents:detail' <pk> %}
app_name = 'nonlocalizedevents'

urlpatterns = [
    path('', views.NonlocalizedEventListView.as_view(), name='index'),
    path('<int:pk>/', views.NonlocalizedEventDetailView.as_view(), name='detail'),
]
