from django.contrib import admin
from .models import ExchangeRate, Order, OrderLine, Student, Representative, Product


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(Representative)
class RepresentativeAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


class OrderLineInline(admin.TabularInline):
    model = OrderLine


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderLineInline]
