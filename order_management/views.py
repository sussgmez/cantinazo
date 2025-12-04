import pandas as pd
import io
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.db.models import Sum, Case, When, Value, CharField, Count
from django.contrib import messages
from .models import (
    Student,
    Representative,
    Product,
    Order,
    OrderLine,
    ExchangeRate,
    Event,
)
from .utils import send_whatsapp_message


class WelcomeView(TemplateView):
    template_name = "order_management/welcome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next_event"] = Event.objects.filter(active=True).first()
        return context


class HomeView(TemplateView):
    template_name = "order_management/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class RepresentativeCreateView(CreateView):
    model = Representative
    template_name = "order_management/representative/create.html"
    fields = ["phone_code", "phone_number", "first_name"]

    def form_valid(self, form):
        representative = form.save(commit=False)
        representative.id = int(
            f"{representative.phone_code}{representative.phone_number}"
        )
        representative.save()
        context = {}
        context["representative"] = representative.id
        context["event"] = self.request.POST.get("event")

        return render(self.request, "order_management/order_view.html", context=context)


class StudentListView(ListView):
    model = Student
    template_name = "order_management/student/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        representative = self.request.GET.get("representative")
        context["representative"] = representative
        event = self.request.GET.get("event")
        context["event"] = event

        order = Order.objects.get_or_create(
            representative_id=representative, closed=False, event_id=event
        )[0]
        context["order"] = order
        return context

    def get_queryset(self):
        return Student.objects.filter(
            representative__id=self.request.GET.get("representative")
        )


class StudentCreateView(CreateView):
    model = Student
    template_name = "order_management/student/create.html"
    fields = ["representative", "name", "section", "grade"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["grades"] = Student.GRADE_CHOICES
        context["representative"] = self.request.GET.get("representative")
        context["sections"] = Student.SECTION_CHOICES
        return context

    def form_valid(self, form):
        form.save()
        response = HttpResponse(status=204)
        response["HX-Trigger"] = "studentCreated"
        return response


class OrderStudentView(TemplateView):
    template_name = "order_management/order/order_student.html"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response["HX-Trigger"] = "studentChanged"

        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = Event.objects.get(pk=self.request.GET.get("event"))
        try:
            student = Student.objects.get(pk=self.request.GET.get("student"))
            order = Order.objects.get_or_create(
                representative=student.representative, closed=False, event=event
            )[0]
            context["student"] = student
            context["order"] = order

            context["exchange_rate"] = (
                ExchangeRate.objects.all().order_by("-created_at").first()
            )
        except:
            pass

        context["event"] = event
        return context


class OrderListView(ListView):
    model = Order
    template_name = "order_management/order/list.html"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                representative_id=self.request.GET.get("representative"),
                event_id=self.request.GET.get("event"),
                closed=True,
            )
            .annotate(total=Sum("orderlines__product__price"))
        )


class ProductListView(ListView):
    model = Product
    template_name = "order_management/product/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order"] = self.request.GET.get("order")
        context["student"] = self.request.GET.get("student")
        context["exchange_rate"] = (
            ExchangeRate.objects.all().order_by("-created_at").first()
        )
        return context

    def get_queryset(self):
        return super().get_queryset().filter(event_id=self.request.GET.get("event"))


class OrderLineCreateView(CreateView):
    model = OrderLine
    template_name = "order_management/orderline/create.html"
    fields = ["student", "order", "product"]

    def form_valid(self, form):
        form.save()
        response = HttpResponse(status=204)
        response["HX-Trigger"] = "orderlineCreated"
        return response


class StaffView(TemplateView):
    template_name = "order_management/staff/staff.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = Event.objects.all()
        return context


class StaffEventView(TemplateView):
    template_name = "order_management/staff/staff_event.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["grades"] = Student.GRADE_CHOICES
        context["event"] = Event.objects.get(pk=kwargs["event"])
        return context


class StaffOderList(ListView):
    model = Order
    template_name = "order_management/staff/order/list.html"

    def get_queryset(self):
        queryset = (
            Order.objects.filter(closed=True, event_id=self.request.GET.get("event"))
            .annotate(total=Sum("orderlines__product__price"))
            .order_by("-pk")
        )
        return queryset


class StaffProductListView(ListView):
    model = Product
    template_name = "order_management/staff/product/list.html"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(event=self.kwargs.get("event"), hidden=False)
            .annotate(sold=Count("orderlines"))
        )


class StaffProductCreateView(CreateView):
    model = Product
    template_name = "order_management/staff/product/create.html"
    fields = ["name", "price", "stock", "event"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event"] = self.request.GET.get("event")
        return context

    def form_valid(self, form):
        form.save()
        response = HttpResponse(status=204)
        response["HX-Trigger"] = "productCreated"
        return response


class StaffProductUpdateView(UpdateView):
    model = Product
    template_name = "order_management/staff/product/update.html"
    fields = ["name", "price", "stock"]

    def form_valid(self, form):
        form.save()
        response = HttpResponse(status=204)
        response["HX-Trigger"] = "productUpdated"
        return response


class StaffProductHideView(UpdateView):
    model = Product
    template_name = "order_management/staff/product/hide.html"
    fields = ["hidden"]

    def form_valid(self, form):
        form.save()
        response = HttpResponse(status=204)
        response["HX-Trigger"] = "productUpdated"
        return response


def order_close(request, pk):

    if request.method == "POST":
        order = Order.objects.get(pk=pk)
        order.reference_number = (
            request.POST.get("reference_number")
            if request.POST.get("reference_number") != ""
            else None
        )
        order.payment_method = request.POST.get("payment_method")
        order.exchange_rate = ExchangeRate.objects.get(
            pk=request.POST.get("exchange_rate")
        )
        order.closed = True
        order.save()

        message = f"+{order.representative.phone_code} {order.representative.phone_number}: {order.representative.first_name} ha realizado una nueva orden, nro. de referencia #{order.reference_number}. Por favor confirmar pago."

        try:
            send_whatsapp_message("+584123517748", message)
            send_whatsapp_message("+584248377782", message)
            send_whatsapp_message("+584121665210", message)
        except:
            print("Twilio error")

        messages.success(request, "Pedido realizado con éxito")

        return redirect("home", order.event.pk)

    elif request.method == "GET":
        context = {}
        order = Order.objects.get(pk=pk)
        context["order"] = order

        context["exchange_rate"] = (
            ExchangeRate.objects.all().order_by("-created_at").first()
        )

        context["total"] = (
            order.orderlines.all().aggregate(total=Sum("product__price"))["total"]
            if order.orderlines.all()
            else 0
        )

        return render(
            request, "order_management/order/order_close.html", context=context
        )


def order_update_status(request, pk):
    if request.method == "GET":
        if request.user.is_staff:
            order = Order.objects.get(pk=pk)

            status = request.GET["status"]
            if status == "0":
                order.rejected = False
                order.checked = True
            elif status == "1":
                order.rejected = True
                order.checked = False
            elif status == "2":
                order.checked = False
                order.rejected = False

            order.save()

            response = HttpResponse(status=204)
            response["HX-Trigger"] = "orderStatusUpdated"
            return response


def orderline_delete(request):
    if request.method == "POST":
        orderline = OrderLine.objects.get(pk=request.POST.get("orderline"))
        orderline.delete()

        response = HttpResponse(status=204)
        response["HX-Trigger"] = "orderlineRemoved"
        return response


def student_remove(request, pk):
    if request.method == "GET":
        context = {}
        context["student"] = Student.objects.get(pk=pk)
        return render(request, "order_management/student/delete.html", context=context)

    elif request.method == "POST":
        student = Student.objects.get(pk=pk)
        student.representative = None
        for orderline in OrderLine.objects.filter(student=student, order__closed=False):
            orderline.delete()

        student.save()

        response = HttpResponse(status=204)
        response["HX-Trigger"] = "studentRemoved"
        return response


def export_orders(request):
    grade_choices = Student.GRADE_CHOICES
    student_grade_display_case = Case(
        *[
            When(student__grade=valor_db, then=Value(label))
            for valor_db, label in grade_choices
        ],
        default=Value("Desconocido"),
        output_field=CharField(),
    )

    payment_method_choices = Order.PAYMENT_METHOD_CHOICES
    order_payment_method_display_case = Case(
        *[
            When(order__payment_method=valor_db, then=Value(label))
            for valor_db, label in payment_method_choices
        ],
        default=Value("Desconocido"),
        output_field=CharField(),
    )

    grade = request.GET.get("grade")
    event = request.GET.get("event")

    if grade:
        orderlines = OrderLine.objects.filter(
            order__event=event, order__closed=True, student__grade=grade
        )
    else:
        orderlines = OrderLine.objects.filter(order__event=event, order__closed=True)

    data = (
        orderlines.exclude(order__rejected=True)
        .annotate(total=Sum("order__orderlines__product__price"))
        .annotate(student__grade_display=student_grade_display_case)
        .annotate(order__payment_method_display=order_payment_method_display_case)
        .values(
            "order__pk",
            "order__representative__first_name",
            "order__payment_method_display",
            "order__reference_number",
            "total",
            "student__name",
            "student__grade_display",
            "student__section",
            "product__name",
            "product__price",
        )
    )

    df = pd.DataFrame(list(data))

    if not df.empty:
        df.columns = [
            "ID",
            "Nombre del representante",
            "Método de pago",
            "# de referencia",
            "Total del pago",
            "Nombre del estudiante",
            "Grado",
            "Sección",
            "Producto",
            "Precio del producto",
        ]

    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Sheet1", index=False)
    output.seek(0)
    excel_data = output.getvalue()
    response = HttpResponse(
        excel_data,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="pedidos.xlsx"'
    return response


def export_products(request):
    event = request.GET.get("event", "")
    data = (
        Product.objects.filter(event_id=event, hidden=False)
        .annotate(sold=Count("orderlines"))
        .values("name", "price", "stock", "sold")
    )

    df = pd.DataFrame(list(data))

    if not df.empty:
        df.columns = [
            "Nombre",
            "Precio",
            "Disponibles",
            "Vendidos",
        ]

    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Sheet1", index=False)
    output.seek(0)
    excel_data = output.getvalue()
    response = HttpResponse(
        excel_data,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="productos.xlsx"'
    return response
