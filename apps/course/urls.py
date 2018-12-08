from django.urls import path
from .views import (
        course_index, course_detail, course_token, course_order,
        course_order_key, notify_view)

app_name = 'course'
urlpatterns = [
    path('', course_index, name='course_index'),
    path('course_token/', course_token, name='course_token'),
    path('<int:course_id>/', course_detail, name='course_detail'),
    path('course_order/<int:course_pk>/', course_order, name='course_order'),
    path('course_order_key/', course_order_key, name='course_order_key'),
    path('notify_view/', notify_view, name='notify_view'),
]
