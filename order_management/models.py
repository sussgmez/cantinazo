from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class Event(models.Model):
    name = models.CharField(_("Nombre"), max_length=100)
    scheduled_for = models.DateField(_("Fecha"))
    active = models.BooleanField(_("Activo"), default=False)

    def __str__(self):
        return self.name


class ExchangeRate(models.Model):
    rate = models.FloatField(_("Tasa de cambio"))
    created_at = models.DateTimeField(_("Fecha de creación"), auto_now_add=True)

    def __str__(self):
        return f"{str(self.rate)} Bs. | {self.created_at.strftime("%d/%m/%Y")}"


class Representative(models.Model):
    id = models.IntegerField(_("ID"), unique=True, primary_key=True)
    first_name = models.CharField(_("Nombre"), max_length=100, blank=True, null=True)
    last_name = models.CharField(_("Apellido"), max_length=100, blank=True, null=True)
    phone_code = models.CharField(_("Código telefónico"), max_length=3)
    phone_number = models.CharField(_("Nro. de teléfono"), max_length=10)

    def __str__(self):
        return self.first_name


class Student(models.Model):
    GRADE_CHOICES = [
        ("1er. grado", "1er. grado"),
        ("2do. grado", "2do. grado"),
        ("3er. grado", "3er. grado"),
        ("4to. grado", "4to. grado"),
        ("5to. grado", "5to. grado"),
        ("6to. grado", "6to. grado"),
        ("1er. año", "1er. año"),
        ("2do. año", "2do. año"),
        ("3er. año", "3er. año"),
        ("4to. año", "4to. año"),
        ("5to. año", "5to. año"),
    ]
    SECTION_CHOICES = [
        ("U", "U"),
        ("A", "A"),
        ("B", "B"),
    ]
    name = models.CharField(_("Estudiante"), max_length=100)
    grade = models.CharField(_("Grado"), max_length=15, choices=GRADE_CHOICES)
    section = models.CharField(_("Sección"), max_length=1, choices=SECTION_CHOICES)

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
    event = models.ForeignKey(Event, verbose_name=_("Evento"), on_delete=models.CASCADE)

    rejected = models.BooleanField(_("Orden rechazada"), default=False)
    closed = models.BooleanField(_("Orden cerrada"), default=False)
    checked = models.BooleanField(_("Orden confirmada"), default=False)
    created_at = models.DateTimeField(_("Fecha de creación"), auto_now_add=True)

    def __str__(self):
        return f'ORDEN #{self.pk} - {self.representative.first_name} - {"Cerrada" if self.closed else "Abierta"}'


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
        Product,
        verbose_name=_("Producto"),
        on_delete=models.CASCADE,
        related_name="orderlines",
    )
    exchange_rate = models.ForeignKey(
        ExchangeRate,
        verbose_name=_("Tasa de cambio"),
        on_delete=models.CASCADE,
        default=1,
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
