from django.contrib import admin
from .models import reference, Book_Model, Cost_Model, Staff_Model, Staff_work, Output, Income_Model,Staff_payments

admin.site.register(reference)
admin.site.register(Book_Model)
admin.site.register(Cost_Model)
admin.site.register(Staff_Model)
admin.site.register(Staff_work)
admin.site.register(Income_Model)
admin.site.register(Output)
admin.site.register(Staff_payments)