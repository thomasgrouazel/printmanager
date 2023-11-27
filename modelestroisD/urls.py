from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("modele_list/", views.modele_list, name='modele_list'),
    path("add_modele/", views.add_modele, name='add_modele'),
    path("edit_modele/<uuid:uuid>/", views.edit_modele, name='edit_modele'),
    path("delete_modele/<uuid:modele_uuid>/", views.delete_modele, name='delete_modele'),
    path("modele/<uuid:modele_uuid>/", views.modele_detail, name='modele_detail'),
    path("variante/<uuid:variante_uuid>/", views.variante_detail, name='variante_detail'),
    path("variante/<uuid:variante_uuid>/delete/", views.delete_variante, name='delete_variante'),
    path("version/<uuid:version_uuid>/", views.version_detail, name='version_detail'),
    path("version/<uuid:version_uuid>/delete/", views.delete_version, name='delete_version'),
    path("modele/<uuid:modele_uuid>/add_variante/", views.add_variante, name='add_variante'),
    path("variante/<uuid:variante_uuid>/add_version/", views.add_version, name='add_version'),
    path("modele_tree/<uuid:modele_uuid>/", views.modele_tree, name='modele_tree'),
    path("version_data/<uuid:version_uuid>/", views.version_data, name='version_data'),
    path("variante/<uuid:variante_uuid>/edit_data/", views.edit_variante_data, name='edit_variante_data'),
    path('version/<uuid:version_uuid>/edit_data/', views.edit_version_data, name='edit_version_data'),
    path('toggle_favorite/<uuid:version_uuid>/', views.toggle_favorite, name='toggle_favorite'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
