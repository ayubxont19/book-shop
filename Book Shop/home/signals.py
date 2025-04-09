from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import Cost_Model, Book_Model, Income_Model

#@receiver([post_save , post_delete], sender=Cost_Model)
def signal_quantity(sender, instance, **kwargs):
    Cost_list = Cost_Model.objects.filter(name__value=instance.name)
    
    book = Book_Model.objects.get(name__value=instance.name)

    cost_quantity = 0

    for i in Cost_list:
        cost_quantity += i.quantity

    book.quantity = cost_quantity
    book.save()