from django.urls import path, include
from playground import views

urlpatterns = [
    path("__debug__/", include('debug_toolbar.urls')),
    path("query-sets/", views.query_sets, name="query_sets"),
    path("send-email/", views.send_email, name="send_email"),
    path("send-email-admins/", views.send_email_admins, name="send_email_admins"),
    path("send-email-with-attachments/", views.send_email_with_attachments, name="send_email_with_attachments"),
    path("send-templated-email/", views.send_templated_email, name="send_templated_email"),
    path("delay-response/", views.delay_response, name="delay_response"),
]
