from django.db.models.signals import post_delete, post_save, pre_delete
from django.dispatch import receiver
from .models import Cost_Model, Book_Model, Income_Model

@receiver([post_save , post_delete], sender=Cost_Model)
@receiver([post_save , post_delete], sender=Income_Model)
def signal_quantity(sender, instance, **kwargs):

    try:
        Cost_list = Cost_Model.objects.filter(name__name=instance.name)
        book = Book_Model.objects.get(id=instance.name.id)
        Income_list = Income_Model.objects.filter(sold_book__name=instance.name)
    except:
        Cost_list = Cost_Model.objects.filter(name__name=instance.sold_book)
        book = Book_Model.objects.get(name=instance.sold_book)
        Income_list = Income_Model.objects.filter(sold_book__name=instance.sold_book)

        cost_quantity = 0
        sold_book_quantity = 0 

        for i in Cost_list:
            cost_quantity += i.quantity

        for i in Income_list:
            sold_book_quantity += i.quantity

        book.quantity = cost_quantity - sold_book_quantity
        book.save()