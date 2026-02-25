from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from order_management import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "staff/",
        login_required(views.StaffView.as_view()),
        name="staff",
    ),
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
    path(
        "staff/product/update/<int:pk>/",
        login_required(views.StaffProductUpdateView.as_view()),
        name="staff-product-update",
    ),
    path(
        "staff/product/delete/<int:pk>/",
        login_required(views.StaffProductHideView.as_view()),
        name="staff-product-hide",
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
    path("info/", views.info_view, name="info"),
    path("movement/create/", views.movement_create, name="movement-create"),
    path("movement/delete/<int:pk>/", views.movement_delete, name="movement-delete"),
    path("movement/list/", views.movement_list, name="movement-list"),
    path("info/progress_bar/", views.progress_bar, name="progress-bar"),
]
