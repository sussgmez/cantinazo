from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, CreateView
from django.db.models import Sum
from .models import Student, Representative, Product, Order, OrderLine, ExchangeRate


class WelcomeView(TemplateView):
    template_name = "order_management/welcome.html"


class HomeView(TemplateView):
    template_name = "order_management/home.html"


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
