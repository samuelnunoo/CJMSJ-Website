from django.contrib import admin
from django.urls import path, include
from .views import simple_upload, form_upload,page_view,blog_view,review,review_article, preview_article, preview, edit, approve,rejected
from submissions.views import submission_form

app_name='blogs'

urlpatterns = [
    path('create/',submission_form, name='create'),
    path('',blog_view,name='show'),
    path('<int:id>',page_view,name='page'),
    path('review/',review,name='review'),
    path('review/<int:id>',review_article,name='review_article'),
    path('preview/<int:id>', preview_article, name='preview_article'),
    path('ajax/preview', preview, name = 'preview'),
    path('ajax/edit', edit, name = 'edit'),
    path('ajax/approve',approve, name = 'approve'),
    path('ajax/reject',rejected, name = 'rejected'),

]
