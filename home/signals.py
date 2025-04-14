from django.db.models.signals import post_delete, post_save, pre_delete
from django.dispatch import receiver
from .models import Cost_Model, Book_Model, Income_Model

@receiver([post_save, post_delete], sender=Cost_Model)
@receiver([post_save, post_delete], sender=Income_Model)
def signal_quantity(sender, instance, **kwargs):
    if sender == Cost_Model:
        book = instance.name  # ForeignKey(Book_Model)
    elif sender == Income_Model:
        book = instance.sold_book  # ForeignKey(Book_Model)
    else:
        return

    # Umumiy hisoblash
    cost_list = Cost_Model.objects.filter(name=book, is_deleted=False)
    income_list = Income_Model.objects.filter(sold_book=book,  is_deleted=False)

    cost_quantity = sum(item.quantity for item in cost_list)
    sold_quantity = sum(item.quantity for item in income_list)

    book.quantity = cost_quantity - sold_quantity
    book.save()
