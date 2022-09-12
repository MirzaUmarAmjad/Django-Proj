import decimal

from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.
from django.utils.timezone import now



def validate_price(value):
    if value < 50 or value > 500:
        raise ValidationError(
            _('Price should be between $50 and $500'),
            params={'value': value},
        )

# Topic model
class Topic(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.name


# course model
class Course(models.Model):
    topic = models.ForeignKey(Topic, related_name='courses',on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2,validators=[validate_price])
    hours = models.PositiveIntegerField(null=True, blank=True)
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(max_length=300, null=True, blank=True)
    interested = models.PositiveIntegerField(default=0)
    stages = models.PositiveIntegerField(default=3)

    def __str__(self):
        return self.name
# function to apply 10 percent discount on price
    def discount(self):
        self.price = self.price - (self.price * decimal.Decimal(0.1))
        self.save()

# student model extend from user
class Student(User):
    CITY_CHOICES = [('WS', 'Windsor'),('CG', 'Calgery'), ('MR', 'Montreal'), ('VC', 'Vancouver')]
    school = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='WS')
    address = models.CharField(max_length=200, null=True, blank=True)
    interested_in = models.ManyToManyField(Topic)
    profile_photo = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.first_name

    class Meta:
        db_table = "Students"

# order model
class Order(models.Model):
    ORDER_STATUS_CHOICES = [(0,'Cancelled'), (1, 'Order Confirmed')]
    course = models.ForeignKey(Course, related_name='courses',on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='students', on_delete=models.CASCADE)
    levels = models.PositiveIntegerField(null=True, blank=True)
    order_status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=1)
    order_date = models.DateField(default=now, blank=True)

    def __str__(self):
        return self.course.name

    def total_cost(self):
        total = Order.objects.aggregate(total=Sum('price'))
        return total

