from django.db.models.signals import post_delete, post_save, pre_delete
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

@receiver(pre_delete, sender=Book_Model)
def soft_delete_signal(sender, instance, **kwargs):
    if not instance.IsDeleted:
        instance.IsDeleted = True
        instance.save()

        # Asl delete ni bloklaymiz
        raise Exception("Bu mahsulot arxivga yuborildi. (Soft delete)")