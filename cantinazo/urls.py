from django.conf import settings
from django.contrib import admin
from django.urls import path
from order_management import views


urlpatterns = [
    path("admin/", admin.site.urls),
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
    # Order
    path(
        "order/",
        views.OrderView.as_view(),
        name="order",
    ),
    path("order/orderline/create/", views.orderline_create, name="orderline-create"),
    path(
        "order/orderline/remove/<int:pk>/",
        views.orderline_remove,
        name="orderline-remove",
    ),
    # Product
    path(
        "product/list/",
        views.ProductListView.as_view(),
        name="product-list",
    ),
]
"""
path("student/list/", views.StudentListView.as_view(), name="student-list"),
path(
    "representative/create/",
    views.RepresentativeCreateView.as_view(),
    name="representative-create",
),
path("student/create/", views.StudentCreateView.as_view(), name="student-create"),
path("product/list/", views.ProductListView.as_view(), name="product-list"),
path("product/add/", views.add_product, name="add-product"),
path("order/", views.OrderView.as_view(), name="order"),
path("order/list/", views.OrderListView.as_view(), name="order-list"),
path("order/remove/<int:pk>/", views.remove_order_line, name="order-line-remove"),
path(
    "order/reference/<int:pk>/", views.set_order_reference, name="order-reference"
),
""",
