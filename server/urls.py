from django.urls import path
from .import views as server_views

urlpatterns = [
    path('account-list/', server_views.AccountView.as_view(), name='account_list'),
    path('account-create/', server_views.AccountView.as_view(), name='account_create'),
    path('account-update/<account_id>/<mode>/', server_views.AccountView.as_view(), name='account_update'),

    path('account-based-destination-list/<account_id>/', server_views.DestinationView.as_view(), name='account_based_destination_list'),
    path('destination-list/', server_views.DestinationView.as_view(), name='destination_list'),
    path('destination-create/', server_views.DestinationView.as_view(), name='destination_create'),
    path('destination-update/<destination_id>/<mode>/', server_views.DestinationView.as_view(), name='destination_update'),

    path('incoming-data/', server_views.IncomingDataView.as_view(), name='incoming_data'),

]
