from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class ExchangeRate(models.Model):
    rate = models.DecimalField(_("Tasa de cambio"), max_digits=10, decimal_places=2)


class Representative(models.Model):
    id = models.IntegerField(_("ID"), unique=True, primary_key=True)
    name = models.CharField(_("Nombre"), max_length=100, blank=True, null=True)
    phone_code = models.CharField(_("Código telefónico"), max_length=3)
    phone_number = models.CharField(_("Nro. de teléfono"), max_length=10)


class Student(models.Model):
    GRADE_CHOICES = [
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
    ]
    SECTION_CHOICES = [
        ("A", "A"),
        ("B", "B"),
    ]
    name = models.CharField(_("Estudiante"), max_length=100)
    grade = models.CharField(_("Grado"), max_length=20, choices=GRADE_CHOICES)
    section = models.CharField(_("Sección"), max_length=20, choices=SECTION_CHOICES)
    representative = models.ForeignKey(
        Representative,
        verbose_name=_("Representante"),
        related_name="students",
        on_delete=models.CASCADE,
    )


class Product(models.Model):
    name = models.CharField(_("Producto"), max_length=100)
    price = models.FloatField(_("Precio"))
    stock = models.IntegerField(_("Disponible"))


class Order(models.Model):
    representative = models.ForeignKey(
        Representative,
        verbose_name=_("Representante"),
        on_delete=models.CASCADE,
        related_name="orders",
    )
    reference_number = models.IntegerField(
        _("Nro. de referencia"), blank=True, null=True
    )
    closed = models.BooleanField(_("Orden cerrada"), default=False)
    checked = models.BooleanField(_("Orden confirmada"), default=False)


class OrderLine(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name=_("Orden"),
        on_delete=models.CASCADE,
        related_name="orderlines",
    )
    student = models.ForeignKey(
        Student, verbose_name=_("Estudiante"), on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, verbose_name=_("Producto"), on_delete=models.CASCADE
    )
