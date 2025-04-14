from django import forms
from home.models import STATUS_CHOICES
from .models import reference, Staff_Model, Cost_Model, Output, Book_Model, Income_Model, Staff_payments, Staff_work

class referenceForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('Name', 'Name'),
        ('Category', 'Category'),
        ('Jinsi', 'Jinsi'),
        ('Output', 'Output')
    ]

    class Meta:
        model = reference
        fields = ['name', 'value']
        widgets = {
            'name': forms.Select(attrs={"class": "form-control"}, choices=STATUS_CHOICES),
            'value': forms.TextInput(attrs={"class": "form-control"})
        }

    def __init__(self, *args, **kwargs):
        super(referenceForm, self).__init__(*args, **kwargs)
        self.fields['name'].choices = [(obj.name, obj.name) for obj in reference.objects.all()]

class StaffModelForm(forms.ModelForm):

    class Meta:
        model = Staff_Model
        fields = ['full_name', 'birthday', 'gender', 'phone_number', 'added_at', 'experience']

        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Full Name"}),
            "birthday": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "gender": forms.Select(attrs={"class": "form-control"}), 
            "phone_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number"}),
            "added_at": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "experience": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Experience in years"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  

        self.fields['gender'].queryset = reference.objects.filter(name="Jinsi", IsDeleted=False)  

class CostModelForm(forms.ModelForm):

    class Meta:
        model = Cost_Model
        fields = ['name', 'price', 'quantity',  'description', 'created_at']

        widgets = {
            'name': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Enter name here',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price',
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter quantity',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Enter description',
            }),
            'created_at': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  

        self.fields['name'].queryset = Book_Model.objects.filter(IsDeleted=False)

class OutputForm(forms.ModelForm):
     
    class Meta:
        model = Output
        fields = ['name', 'price', 'description', 'created_at']

        widgets = {
            'name': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Enter name here',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Enter description',
            }),
            'created_at': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  

        self.fields['name'].queryset = reference.objects.filter(name="Output", IsDeleted=False)  

class BookModelForm(forms.ModelForm):

    class Meta:
        model = Book_Model
        fields = ['name', 'author', 'price', 'quantity', 'description', 'category', 'image']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description', 'rows': 4}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  

        self.fields['author'].queryset = reference.objects.filter(name="author")
        self.fields['category'].queryset = reference.objects.filter(name="Kitob turi", IsDeleted=False)

class SotuvModelForm(forms.ModelForm):

    class Meta:
        model = Income_Model
        fields = ['sold_book', 'price', 'quantity', 'description', 'created_at']

        widgets = {
            'sold_book': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Sold book name',
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price',
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter quantity',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add a description...',
            }),
            'created_at': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  

        self.fields['sold_book'].queryset = Book_Model.objects.filter(IsDeleted=False)

class HodimModelForm(forms.ModelForm):

    class Meta:
        model = Staff_payments
        fields = ['staff', 'price']

        widgets = {
            'staff': forms.Select(attrs={
                'class': 'form-control',
                
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  

        self.fields['staff'].queryset = Book_Model.objects.filter(IsDeleted=False)
        

class HodimIshForm(forms.ModelForm):

    class Meta:
        model = Staff_work
        fields = ['staff', 'time_work', 'price']

        widgets = {
            'staff': forms.Select(attrs={
                'class': 'form-control',
                
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price',
            }),
            'time_work': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  

        self.fields['staff'].queryset = Book_Model.objects.filter(IsDeleted=False)