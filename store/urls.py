from . import views
from django.urls import path, include


urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('album/', views.album_base_view, name='album_base'),
    path('album/<int:album_id>/<int:page_number>/', views.album_view, name='album_page'),
    path('collect/<int:item_id>/', views.collect_item_view, name='collect_item'),  # Add this line
    path('buy/<int:item_id>/', views.buy_item, name='buy_item'), 
    path('register/', views.register_user, name="register"),
    path('sticker/<int:pk>', views.sticker, name="sticker"),
    path('category/<str:foo>', views.category, name="category"),
]