from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from order_management import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "staff/event/<int:event>/",
        login_required(views.StaffEventView.as_view()),
        name="staff-event",
    ),
    path("staff/login/", LoginView.as_view(), name="login"),
    path("staff/logout/", LogoutView.as_view(), name="logout"),
    path("", views.WelcomeView.as_view(), name="welcome"),
    path("evento/<int:event>/pedido/", views.HomeView.as_view(), name="home"),
    path(
        "representative/create/",
        views.RepresentativeCreateView.as_view(),
        name="representative-create",
    ),
    path("student/list/", views.StudentListView.as_view(), name="student-list"),
    path("student/create/", views.StudentCreateView.as_view(), name="student-create"),
    path("student/delete/<int:pk>", views.student_remove, name="student-delete"),
    path(
        "order/student/",
        views.OrderStudentView.as_view(),
        name="order-student",
    ),
    path("order/list/", views.OrderListView.as_view(), name="order-list"),
    path(
        "staff/order/list/",
        login_required(views.StaffOderList.as_view()),
        name="staff-order-list",
    ),
    path(
        "staff/product/list/<int:event>/",
        login_required(views.StaffProductListView.as_view()),
        name="staff-product-list",
    ),
    path(
        "staff/product/create/",
        login_required(views.StaffProductCreateView.as_view()),
        name="staff-product-create",
    ),
    path("product/list/", views.ProductListView.as_view(), name="product-list"),
    path(
        "orderline/create/",
        views.OrderLineCreateView.as_view(),
        name="orderline-create",
    ),
    path("orderline/delete/", views.orderline_delete, name="orderline-delete"),
    path("order/close/<int:pk>/", views.order_close, name="order-close"),
    path(
        "order/update/status/<int:pk>/",
        views.order_update_status,
        name="order-update-status",
    ),
    path("order/export/", views.export_orders, name="export-orders"),
    path("product/export/", views.export_products, name="export-products"),
]
"""
path(
    "cantinazo_admin/",
    login_required(views.AdminView.as_view()),
    name="admin-cantinazo",
),
path("", views.WelcomeView.as_view(), name="welcome"),
path("event/<int:pk>/", views.EventView.as_view(), name="event"),
path("pedido/", views.HomeView.as_view(), name="home"),
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
path(
    "export_product_excel/", views.export_product_excel, name="export-product-excel"
),
path(
    "export_representative_excel/",
    views.export_representative_excel,
    name="export-representative-excel",
),
"""
