import decimal

from django.contrib import admin
from django.db import models
from .models import Topic, Course, Student, Order




# 1.	In admin.py create a class TopicAdmin(admin.ModelAdmin), register this with the admin site and show the name and category fields, for each Topic, in the admin interface page that lists all Topics. Create a TabularInline class called CourseInline based on Course model and include this under the TopicAdmin, so Courses for a particular Topic may be edited on the Topic page itself.
class CourseInline(admin.TabularInline):
    model = Course

class TopicAdmin(admin.ModelAdmin):
    list_display = ('name','category')
    inlines = [CourseInline,]

# 2.	In admin.py write an action for CourseAdmin class that will reduce the price of the course by 10% for the selected courses and save the updated price in the database.
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    actions = ['reduce_price_by_10_percent']

    def reduce_price_by_10_percent(self, request, queryset):
        discount = 10

        for course in queryset:
            multiplier = discount / 100.  # discount / 100 in python 3
            old_price = course.price
            new_price = old_price - (decimal.Decimal(old_price) * decimal.Decimal(multiplier))
            course.price = new_price
            course.save(update_fields=['price'])

# 11.	In admin.py create a class StudentAdmin(admin.ModelAdmin), register this with the admin site and show the first_name, last_name fields and address
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','address')


# Register your models here.
admin.site.register(Topic,TopicAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(Order)