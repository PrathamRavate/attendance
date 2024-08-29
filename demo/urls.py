from django.urls import path
from .views import print_data, cdataView, get_profile, getreqView

urlpatterns = [
    path('print/', print_data, name='print_data'),
    path('iclock/cdata.aspx', cdataView, name='cdataView'),
    path('get-profile/', get_profile, name='get-profile'),
    path('iclock/getrequest.aspx', getreqView, name='getreqView')
]
