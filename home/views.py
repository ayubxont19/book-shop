from django.shortcuts import render, redirect, get_object_or_404
from . import models 
from .forms import referenceForm, StaffModelForm, Staff_Model, CostModelForm, Cost_Model, Output, OutputForm, Book_Model, BookModelForm, SotuvModelForm, Income_Model, Staff_payments, HodimModelForm, HodimIshForm, Staff_work, reference
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

@login_required(login_url='login')
def home(request):
    Kitoblar = models.Book_Model.objects.filter(IsDeleted=False)
    book_category = models.reference.objects.filter(name="Kitob turi")
    search = request.GET.get("search", None)
    category_filter = request.GET.get("category", None)

    if search:
        Kitoblar = Kitoblar.filter(name__icontains=search)

    if category_filter:
        Kitoblar = Kitoblar.filter(category__value=category_filter)

    context = {
        "Kitoblar":Kitoblar,
        "book_category":book_category
    }
    return render(request, 'index.html', context=context)

@login_required(login_url='login')
def reference_view(request):
    reference_models = models.reference.objects.all()
    names = set()
    reference_values = dict()
    for item in reference_models:
        names.add(item.name)
        for name in names:
            if name == item.name:
                if name not in reference_values:
                    reference_values[name]= [{'id':item.id, 'value':item.value}]
                else:
                    reference_values[name].append({'id':item.id, 'value':item.value})    
    context ={
        'reference_values':reference_values
    }
    return render(request , "reference.html" , context=context)

@login_required(login_url='login')
def reference_delete(request , pk):
    model = models.reference.objects.get(pk=pk)
    model.delete()
    return redirect(reference_view)

@login_required(login_url='login')
def reference_create(request):
    if request.method == "POST":
        form = referenceForm(request.POST)
        print("POST so‘rovi keldi!")  
        
        if form.is_valid():
            print("Forma valid!")  
            form.save()
            return redirect("reference")
        else:
            print("Xatolar:", form.errors)  

    form = referenceForm()
    form.fields['name'].choices = [(obj['name'], obj['name']) for obj in reference.objects.values('name').distinct()]
    
    context = {"form": form}
    return render(request, "reference_qoshish.html", context=context)

@login_required(login_url='login')
def reference_update(request, pk):
    reference = get_object_or_404(models.reference, pk=pk)  
    if request.method == "POST":
        forms = referenceForm(request.POST, instance=reference)
        if forms.is_valid():
            forms.save()
            return redirect(home)  
    else:
        forms = referenceForm(instance=reference)
    return render(request, 'reference_tahrirlash.html', {'forms': forms})

@login_required(login_url='login')
def staff_view(request):
    staff_models = models.Staff_Model.active_objects.all()
    staff_payment_list = models.Staff_payments.active_objects.all()
    staff_work_list = models.Staff_work.active_objects.all()

    staff_models2 = models.Staff_Model.objects.all()
    staff_payment_list2 = models.Staff_payments.objects.all()
    staff_work_list2 = models.Staff_work.objects.all()

    staff_balances = {}

    for staff in staff_models2:
        total_work_price = sum(
            work.time_work * work.price for work in models.Staff_work.objects.filter(staff=staff)
        )

        total_paid = sum(
            payment.price for payment in models.Staff_payments.objects.filter(staff=staff)
        )

        balance = abs(total_work_price - total_paid)
        staff_balances[staff.id] = balance

    full_name = request.GET.get("full_name",None)
    if full_name:
        staff_models = staff_models.filter(full_name__icontains=full_name)
    print(staff_models)

    phone_number = request.GET.get("phone_number",None)
    if phone_number:
        staff_models = staff_models.filter(phone_number__icontains=phone_number)
    print(staff_models)
    
    context = {
        'staff_values': staff_models,
        'staff_payment_list': staff_payment_list,
        'staff_work_list': staff_work_list,
        'staff_balances':staff_balances,
        
        'staff_models2': staff_models2,
        'staff_payment_list2': staff_payment_list2,
        'staff_work_list2': staff_work_list2
        }
    return render(request, "staff.html", context=context)

@login_required(login_url='login')
def staff_create(request):
    if request.method == "POST":
        forms = StaffModelForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect(staff_view)
        
    forms = StaffModelForm()
    context = {
        "forms":forms
    }
    return render(request, "staff_qoshish.html", context=context)

@login_required(login_url='login')
def staff_update(request, id):
    staff = get_object_or_404(Staff_Model, id=id)
    if request.method == "POST":
        forms = StaffModelForm(request.POST, instance=staff) 
        if forms.is_valid():
            forms.save()
            return redirect('staff_name') 
    else:
        forms = StaffModelForm(instance=staff)

    return render(request, 'staff_update.html', {'forms': forms})

@login_required(login_url='login')
def staff_delete(request, id):
    staff = get_object_or_404(Staff_Model, id=id)
    staff.delete()
    return redirect('staff_name')

@login_required(login_url='login')
def cost_view(request):
    cost_list = models.Cost_Model.active_objects.all()

    name = request.GET.get("name",None)
    if name:
        cost_list = cost_list.filter(name__name__icontains=name)

    category = request.GET.get("category",None)
    if category:
        cost_list = cost_list.filter(name__category__value__icontains=category)

    context = {
        "cost_list":cost_list
    }
    return render(request, 'cost.html', context=context)

@login_required(login_url='login')
def cost_create(request):
    if request.method == "POST":
        forms = CostModelForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect("cost_name")
        else:
            print(forms.errors)
    forms = CostModelForm()
    context = {
        "forms":forms
    }
    return render(request, "cost_create.html", context=context)

@login_required(login_url='login')
def cost_delete(request, pk):
    cost = get_object_or_404(Cost_Model, pk=pk)
    cost.delete() 
    return redirect('cost_name')

@login_required(login_url='login')
def cost_update(request, pk):
    cost = get_object_or_404(Cost_Model, pk=pk)
    if request.method == "POST":
        forms = CostModelForm(request.POST, instance=cost) 
        if forms.is_valid():
            forms.save()
            return redirect('cost_name') 
    else:
        forms = CostModelForm(instance=cost)
    return render(request, 'cost_update.html', {'forms': forms})

@login_required(login_url='login')
def output_view(request):
    output_list = models.Output.active_objects.all()

    name = request.GET.get("name", None)
    if name:
        output_list = output_list.filter(name__value__icontains=name)
    print(output_list)

    context = {
        "output_list": output_list
    }
    return render(request, 'output.html', context=context)    

@login_required(login_url='login')
def output_create(request):
    if request.method == "POST":
        forms = OutputForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect("output_name")
        else:
            print(forms.errors)
    forms = OutputForm()
    context = {
        "forms":forms
    }
    return render(request, "output_create.html", context=context)

@login_required(login_url='login')
def output_delete(request, pk):
    output = get_object_or_404(Output, pk=pk)
    output.delete()
    return redirect('output_name')

@login_required(login_url='login')
def output_update(request, pk):
    output = get_object_or_404(Output, pk=pk)
    if request.method == "POST":
        forms = OutputForm(request.POST, instance=output) 
        if forms.is_valid():
            forms.save()
            return redirect('output_name') 
    else:
        forms = OutputForm(instance=output)
    return render(request, 'output_update.html', {'forms': forms})

@login_required(login_url='login')
def book_create(request):
    if request.method == "POST":
        forms = BookModelForm(request.POST, request.FILES)  
        if forms.is_valid():
            book = forms.save(commit=False) 
            book.save() 
            return redirect("home")
        else:
            print("❌ Xatolik:", forms.errors) 
    else:
        forms = BookModelForm()

    context = {"forms": forms}
    return render(request, "bookcreate.html", context=context)

@login_required(login_url='login')
def book_delete(request, pk):
    book = get_object_or_404(Book_Model, pk=pk)
    book.IsDeleted = True
    book.save()
    return redirect('home')

@login_required(login_url='login')
def book_update(request, pk):
    book = get_object_or_404(Book_Model, pk=pk)
    if request.method == "POST":
        forms = BookModelForm(request.POST, request.FILES, instance=book) 
        if forms.is_valid():
            forms.save()
            return redirect('home') 
    else:
        forms = BookModelForm(instance=book)
    return render(request, 'book_update.html', {'forms': forms})

def book_detail(request, book_id):
    book = get_object_or_404(Book_Model, id=book_id)
    return render(request, 'book_detail.html', {'book': book})

@login_required(login_url='login')
def income_view(request):
    income_list = models.Income_Model.active_objects.all()

    name = request.GET.get("name", None)
    if name:
        income_list = income_list.filter(sold_book__name__icontains=name)

    context = {
        "income_list":income_list
    }
    return render(request, 'income.html', context=context)    

@login_required(login_url='login')
def income_create(request):
    if request.method == "POST":
        forms = SotuvModelForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect("income_name")
        else:
            print(forms.errors)
    forms = SotuvModelForm()
    context = {
        "forms":forms
    }
    return render(request, "income_create.html", context=context)

@login_required(login_url='login')
def income_delete(request, pk):
    income = get_object_or_404(Income_Model, pk=pk)
    income.delete()
    return redirect('income_name')

@login_required(login_url='login')
def income_update(request, pk):
    income = get_object_or_404(Income_Model, pk=pk)
    if request.method == "POST":
        forms = SotuvModelForm(request.POST, instance=income)
        if forms.is_valid():
            forms.save()
            return redirect(income_view)
    else:
        forms = SotuvModelForm(instance=income)
    return render(request, "income_update.html", {'forms':forms})

@login_required(login_url='login')

def daromad(request):
    # GET requestdan sanalarni olish
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Sanalarni `datetime.date` ga o‘tkazish
    start_date = parse_date(start_date) if start_date else None
    end_date = parse_date(end_date) if end_date else None

    # Filtirlar qo‘shish
    filters = {}
    if start_date and end_date:
        filters["created_at__range"] = (start_date, end_date)

    # Filterlangan ma’lumotlarni olish
    cost_list = models.Cost_Model.objects.filter(**filters)
    output_list = models.Output.objects.filter(**filters)
    staff_list = models.Staff_payments.objects.filter(**filters)
    income_list = models.Income_Model.objects.filter(**filters)

    # Hisoblash
    cost_total_sum = sum(i.price * i.quantity for i in cost_list)
    output_total_sum = sum(i.price for i in output_list)
    staff_total_sum = sum(i.price for i in staff_list)
    income_total_sum = sum(i.price * i.quantity for i in income_list)

    # Foyda hisoblash
    profit = income_total_sum - (output_total_sum + cost_total_sum + staff_total_sum)

    context = {
        "cost_total_sum": cost_total_sum,
        "output_total_sum": output_total_sum,
        "staff_total_sum": staff_total_sum,
        "income_total_sum": income_total_sum,
        "profit": profit
    }

    return render(request, "daromad.html", context=context)
@login_required(login_url='login')
def staff_payment_create(request):
    if request.method == "POST":
        forms = HodimModelForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect(staff_view)
    else:
        forms = HodimModelForm()
    print(forms)
    context = {
        "forms":forms
    }
    return render(request , "staff_payment_create.html", context=context)

@login_required(login_url='login')
def staff_payment_delete(request, pk):
    staff_payment = get_object_or_404(Staff_payments, pk=pk)
    staff_payment.delete()
    return redirect(staff_view)

@login_required(login_url='login')
def staff_payment_update(request, pk):
    staff_payment = get_object_or_404(Staff_payments, pk=pk)
    if request.method == "POST":
        forms = HodimModelForm(request.POST, instance=staff_payment)
        if forms.is_valid():
            forms.save()
            return redirect('staff_name')
    else:
        forms = HodimModelForm(instance=staff_payment)
    return render(request, "staff_payment_update.html", {'forms':forms})

@login_required(login_url='login')
def staff_work_create(request):
    if request.method == "POST":
        forms = HodimIshForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect(staff_view)
    else:
        forms = HodimIshForm()
    print(forms)
    context = {
        "forms":forms
    }
    return render(request , "staff_work_create.html", context=context)

@login_required(login_url='login')
def staff_work_delete(request, pk):
    staff_work = get_object_or_404(Staff_work, pk=pk)
    staff_work.delete()
    return redirect(staff_view)

@login_required(login_url='login')
def staff_work_update(request, pk):
    staff_work = get_object_or_404(Staff_work, pk=pk)
    if request.method == "POST":
        forms = HodimIshForm(request.POST, instance=staff_work)
        if forms.is_valid():
            forms.save()
            return redirect('staff_name')
    else:
        forms = HodimIshForm(instance=staff_work)
    return render(request, "staff_work_update.html", {'forms':forms})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Tizimga muvaffaqiyatli kirdingiz.")
            return redirect("home")
        else:
            messages.error(request, "Login yoki parol noto'g'ri.")
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    messages.info(request, "Tizimdan chiqdingiz.")
    return redirect('home')