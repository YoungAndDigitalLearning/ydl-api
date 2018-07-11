from rest_framework import permissions
from django.urls import path
from quiz import views as v

# Viewset mapping function
# Seperate from url pattern
# User

test_list = v.TestViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
test_detail = v.TestViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

answer_detail = v.AnswerViewSet.as_view({
    'put': 'update',
})


"""Urlpatterns to define reachable urls
"""
urlpatterns = [
    path('tests/', test_list, name="test-list"),
    path('tests/<int:pk>', test_detail, name="test-detail"),
    path('answers/<int:pk>', answer_detail, name="answer-detail")
    ]