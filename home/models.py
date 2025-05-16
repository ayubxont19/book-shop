from django.db import models

STATUS_CHOICES = [
        ('Kitob turi', 'Kitob turi'),
        ('author', 'author'),
        ('Jinsi', 'Jinsi'),
        ('Output', 'Output')
    ]

class reference(models.Model):
    name = models.CharField(max_length=255, verbose_name="reference nomi")
    value = models.CharField(max_length=255, verbose_name="reference qiymati")
    IsDeleted = models.BooleanField(default=False)

    def __str__(self):
        return self.value

class Book_Model(models.Model):
    name = models.CharField(verbose_name="Kitob nomi", max_length=255)
    category = models.ForeignKey(reference, on_delete=models.CASCADE, related_name="book_category_references")
    author = models.ForeignKey(reference, on_delete=models.CASCADE, related_name="book_author_references")
    price = models.FloatField(verbose_name="Kitob narxi")
    quantity = models.IntegerField(verbose_name="Kitob soni", default=0)
    description = models.TextField(verbose_name="Kitob haqida")
    image = models.ImageField(upload_to="media/", verbose_name="Kitob rasmi")  
    IsDeleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class CostModelManager(models.Manager):
    """Faol (o‘chirilmagan) obyektlarni qaytarish"""
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Cost_Model(models.Model):
    name = models.ForeignKey(Book_Model, on_delete=models.CASCADE, verbose_name="Cost nomi", related_name="cost_name_references")
    price = models.FloatField(verbose_name="Xarid narxi")
    quantity = models.IntegerField(verbose_name="Xarid soni")
    description = models.TextField(verbose_name="Xarid haqida")
    created_at = models.DateField(verbose_name="Xarid sanasi")
    is_deleted = models.BooleanField(default=False) 

    objects = models.Manager() 
    active_objects = CostModelManager() 

    def delete(self):
        """Yumshoq o‘chirish funksiyasi"""
        self.is_deleted = True
        self.save()

    def restore(self):
        """O‘chirilgan obyektni tiklash"""
        self.is_deleted = False
        self.save()

    def __str__(self):
        return f"{self.name} - {self.price}"

class Income_Model(models.Model):
    sold_book = models.ForeignKey(Book_Model, on_delete=models.CASCADE, related_name="income_sold_book_references")
    price = models.FloatField(verbose_name="Narxi")
    quantity = models.IntegerField(verbose_name="Soni")
    description = models.TextField(verbose_name="haqida")
    created_at = models.DateField(verbose_name="sanasi")
    is_deleted = models.BooleanField(default=False)

    objects = models.Manager() 
    active_objects = CostModelManager()

    def delete(self):
        """Yumshoq o‘chirish funksiyasi"""
        self.is_deleted = True
        self.save()

    def restore(self):
        """O‘chirilgan obyektni tiklash"""
        self.is_deleted = False
        self.save()

    def __str__(self):
        return f"{self.sold_book} - {self.price}"

class Output(models.Model):
    name = models.ForeignKey(reference, on_delete=models.CASCADE)
    price = models.BigIntegerField(verbose_name="Chiqim narxi")
    description = models.TextField(verbose_name="Chiqim haqida")
    created_at = models.DateField(verbose_name="Chiqim sanasi")
    is_deleted = models.BooleanField(default=False)

    objects = models.Manager() 
    active_objects = CostModelManager()

    def delete(self):
        """Yumshoq o‘chirish funksiyasi"""
        self.is_deleted = True
        self.save()

    def restore(self):
        """O‘chirilgan obyektni tiklash"""
        self.is_deleted = False
        self.save()

    def __str__(self):
        return f"{self.name} - {self.price}"

class Staff_Model(models.Model):
    full_name = models.CharField(max_length=255 , verbose_name="Xodimning ism familiyasi")
    birthday = models.DateField(verbose_name="Xodimning tug'ilgan sanasi")
    gender = models.ForeignKey(reference, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=255 , verbose_name="Xodimning telefon raqami")
    added_at = models.DateField()
    experience = models.FloatField(verbose_name="Xodimning tajribasi")
    is_deleted = models.BooleanField(default=False)

    objects = models.Manager() 
    active_objects = CostModelManager()

    def delete(self):
        """Yumshoq o‘chirish funksiyasi"""
        self.is_deleted = True
        self.save()

    def restore(self):
        """O‘chirilgan obyektni tiklash"""
        self.is_deleted = False
        self.save()

    def __str__(self):
        return f"{self.full_name} - {self.price}"


    def __str__(self):
        return self.full_name

class Staff_work(models.Model):
    staff = models.ForeignKey(Staff_Model, on_delete=models.CASCADE, verbose_name="Xodim")
    time_work = models.IntegerField("Xodimning ishlagan vaqti")
    price = models.FloatField(verbose_name="Xodimning xaqqi")
    is_deleted = models.BooleanField(default=False)

    objects = models.Manager() 
    active_objects = CostModelManager()

    def delete(self):
        """Yumshoq o‘chirish funksiyasi"""
        self.is_deleted = True
        self.save()

    def restore(self):
        """O‘chirilgan obyektni tiklash"""
        self.is_deleted = False
        self.save()

    def __str__(self):
        return f"{self.staff} - {self.price}"


class Staff_payments(models.Model):
    staff = models.ForeignKey(Staff_Model, on_delete=models.CASCADE, verbose_name="Xodim")
    price =  models.FloatField(verbose_name="Xodim xaqqi")
    created_at = models.DateField(verbose_name="Xodim Sanasi", auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    objects = models.Manager() 
    active_objects = CostModelManager()

    def delete(self):
        """Yumshoq o‘chirish funksiyasi"""
        self.is_deleted = True
        self.save()

    def restore(self):
        """O‘chirilgan obyektni tiklash"""
        self.is_deleted = False
        self.save()

    def __str__(self):
        return f"{self.staff} - {self.price}"