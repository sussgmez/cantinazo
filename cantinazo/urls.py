from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from order_management import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", LoginView.as_view(), name="login"),
    path(
        "cantinazo_admin/",
        login_required(views.AdminView.as_view()),
        name="admin-cantinazo",
    ),
    path("welcome/", views.WelcomeView.as_view(), name="welcome"),
    path("", views.HomeView.as_view(), name="home"),
    # Representative
    path(
        "representative/create/",
        views.RepresentativeCreateView.as_view(),
        name="representative-create",
    ),
    # Student
    path(
        "student/create/",
        views.StudentCreateView.as_view(),
        name="student-create",
    ),
    path(
        "student/delete/<int:pk>/",
        views.student_delete,
        name="student-delete",
    ),
    # Order
    path(
        "cantinazo_admin/order/list/",
        login_required(views.AdminOrderListView.as_view()),
        name="admin-order-list",
    ),
    path(
        "order/",
        views.OrderView.as_view(),
        name="order",
    ),
    path(
        "order/update/<int:pk>/",
        views.order_update,
        name="order-update",
    ),
    path(
        "order/status/<int:pk>/",
        views.order_update_status,
        name="order-update-status",
    ),
    path("order/orderline/create/", views.orderline_create, name="orderline-create"),
    path(
        "order/orderline/remove/<int:pk>/",
        views.orderline_remove,
        name="orderline-remove",
    ),
    path("export_excel", views.export_excel, name="export-excel"),
    # Product
    path(
        "product/list/",
        views.ProductListView.as_view(),
        name="product-list",
    ),
]
