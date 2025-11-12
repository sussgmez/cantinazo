import pandas as pd
import io
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, CreateView, DeleteView
from django.db.models import Sum
from .models import Student, Representative, Product, Order, OrderLine, ExchangeRate


class WelcomeView(TemplateView):
    template_name = "order_management/welcome.html"


class HomeView(TemplateView):
    template_name = "order_management/home.html"


class AdminView(TemplateView):
    template_name = "order_management/admin_cantinazo.html"


class AdminOrderListView(ListView):
    model = Order
    template_name = "order_management/admin_order_list.html"

    def get_queryset(self):
        orders = (
            Order.objects.filter(closed=True)
            .annotate(total=Sum("orderlines__product__price"))
            .order_by("payment_method", "checked")
        )
        return orders

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["exchange_rate"] = ExchangeRate.objects.get(pk=1)
        return context


class RepresentativeCreateView(CreateView):
    model = Representative
    template_name = "order_management/representative_create.html"
    fields = ["name", "phone_code", "phone_number"]

    def form_valid(self, form):
        representative = form.save(commit=False)
        representative.id = int(
            f"{representative.phone_code}{representative.phone_number}"
        )
        representative.save()

        context = {}
        context["representative"] = representative.id
        return render(self.request, "order_management/open_order.html", context=context)


class StudentCreateView(CreateView):
    model = Student
    template_name = "order_management/student_create.html"
    fields = ["representative", "name", "grade", "section"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["representative"] = self.request.GET["representative"]
        context["grades"] = Student.GRADE_CHOICES
        return context

    def form_valid(self, form):
        form.save()
        response = HttpResponse(status=204)
        response["HX-Trigger"] = "studentCreated"
        return response


class OrderView(TemplateView):
    template_name = "order_management/order.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["exchange_rate"] = ExchangeRate.objects.get(pk=1)
        representative = Representative.objects.get(
            id=self.request.GET["representative"]
        )
        context["students"] = representative.students.all()
        order = Order.objects.get_or_create(
            representative=representative, closed=False
        )[0]
        context["order"] = order
        context["total"] = (
            order.orderlines.all().aggregate(total=Sum("product__price"))["total"]
            if order.orderlines.all()
            else 0
        )
        context["closed_orders"] = Order.objects.filter(
            representative=representative, closed=True
        ).annotate(total=Sum("orderlines__product__price"))

        return context


class ProductListView(ListView):
    model = Product
    template_name = "order_management/product_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order"] = self.request.GET["order"]
        context["exchange_rate"] = ExchangeRate.objects.get(pk=1)
        context["student"] = self.request.GET["student"]
        return context


def student_delete(request, pk):
    student = Student.objects.get(pk=pk)
    if request.method == "GET":
        return render(
            request,
            template_name="order_management/student_delete.html",
            context={"student": student},
        )

    elif request.method == "POST":

        for orderline in student.orderlines.all():
            student.representative = None
            if orderline.order.closed == False:
                orderline.order.delete()
            student.save()

        response = HttpResponse(status=204)
        response["HX-Trigger"] = "studentDeleted"
        return response


def orderline_create(request):
    if request.method == "POST":

        OrderLine.objects.create(
            order_id=request.POST["order"],
            student_id=request.POST["student"],
            product_id=request.POST["product"],
        )

        response = HttpResponse(status=204)
        response["HX-Trigger"] = "orderCreated"
        return response


def orderline_remove(request, pk):
    OrderLine.objects.get(pk=pk).delete()
    response = HttpResponse(status=204)
    response["HX-Trigger"] = "orderLineRemoved"
    return response


def order_update(request, pk):
    if request.method == "POST":
        order = Order.objects.get(pk=pk)
        order.reference_number = (
            request.POST["reference_number"]
            if request.POST["reference_number"]
            else None
        )
        order.payment_method = request.POST["payment_method"]
        order.closed = True
        order.rejected = False
        order.save()

        response = HttpResponse(status=204)
        response["HX-Trigger"] = "orderClosed"
        return response


def order_update_status(request, pk):
    if request.method == "GET":
        if request.user.is_staff:
            order = Order.objects.get(pk=pk)

            status = request.GET["status"]
            if status == "0":
                order.rejected = False
                order.checked = True
            elif status == "1":
                order.checked = False
                order.rejected = True
            elif status == "2":
                order.checked = False
                order.rejected = False

            order.save()

            response = HttpResponse(status=204)
            response["HX-Trigger"] = "orderUpdated"
            return response


def export_excel(request):

    data = OrderLine.objects.filter(order__closed=True).values(
        "order__pk",
        "order__representative__name",
        "order__payment_method",
        "order__reference_number",
        "student__name",
        "product__name",
    )

    df = pd.DataFrame(list(data))

    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Sheet1", index=False)
    output.seek(0)
    excel_data = output.getvalue()
    response = HttpResponse(
        excel_data,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="exported_data.xlsx"'
    return response
