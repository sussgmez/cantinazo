from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class ExchangeRate(models.Model):
    rate = models.DecimalField(_("Tasa de cambio"), max_digits=10, decimal_places=2)


class Representative(models.Model):
    id = models.IntegerField(_("ID"), unique=True, primary_key=True)
    name = models.CharField(_("Nombre"), max_length=100, blank=True, null=True)
    phone_code = models.CharField(_("Código telefónico"), max_length=3)
    phone_number = models.CharField(_("Nro. de teléfono"), max_length=10)

    def __str__(self):
        return self.name


class Student(models.Model):
    GRADE_CHOICES = [
        ("1", "1er. grado"),
        ("2", "2do. grado"),
        ("3", "3er. grado"),
        ("4", "4to. grado"),
        ("5", "5to. grado"),
        ("6", "6to. grado"),
        ("7", "1er. año"),
        ("8", "2do. año"),
        ("9", "3er. año"),
        ("10", "4to. año"),
        ("11", "5to. año"),
    ]
    SECTION_CHOICES = [
        ("U", "U"),
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
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(_("Producto"), max_length=100)
    price = models.FloatField(_("Precio"))
    stock = models.IntegerField(_("Disponible"))

    def __str__(self):
        return self.name


class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        (0, "Pago móvil"),
        (1, "Efectivo"),
    ]
    payment_method = models.SmallIntegerField(_("Método de pago"), default=0)
    representative = models.ForeignKey(
        Representative,
        verbose_name=_("Representante"),
        on_delete=models.CASCADE,
        related_name="orders",
    )
    reference_number = models.IntegerField(
        _("Nro. de referencia"), blank=True, null=True
    )
    rejected = models.BooleanField(_("Orden rechazada"), default=False)
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
        Student,
        verbose_name=_("Estudiante"),
        on_delete=models.CASCADE,
        related_name="orderlines",
    )
    product = models.ForeignKey(
        Product, verbose_name=_("Producto"), on_delete=models.CASCADE
    )


@receiver(post_save, sender=OrderLine)
def orderline_post_save_receiver(sender, instance, created, **kwargs):
    if created:
        instance.product.stock -= 1
        instance.product.save()


@receiver(pre_delete, sender=OrderLine)
def orderline_pre_delete_receiver(sender, instance, **kwargs):
    instance.product.stock += 1
    instance.product.save()
