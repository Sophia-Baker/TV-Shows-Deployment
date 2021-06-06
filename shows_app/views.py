from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html')

def user(request):
    User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        password=request.POST['password']
    )
    return redirect('/')

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        return redirect('/dashboard')

def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id = request.session['user_id'])
    context = {
        'shows': Show.objects.all(),
        'user': user,
        'user_shows': Show.objects.filter(owner=user),
    }
    return render(request, 'shows.html', context)

def summary(request, show_id):
    if 'user_id' not in request.session:
        return redirect('/')
    one_show = Show.objects.get(id=show_id)
    user = User.objects.get(id = request.session['user_id'])
    context = {
        'show': one_show,
        'user': user,
    }
    return render(request, 'show.html', context)

def shows(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id = request.session['user_id'])
    context = {
        'shows': Show.objects.all(),
        'user': user,
    }
    return render(request, 'shows.html', context)

def new(request):
    if 'user_id' not in request.session:
        return redirect('/')
    return render(request,'new.html')

def create(request):
    if 'user_id' not in request.session:
        return redirect('/')
    errors = Show.objects.basic_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/new')
    Show.objects.create(
        title = request.POST['title'],
        network = request.POST['network'],
        release_date = request.POST['release_date'],
        description = request.POST['description'],
        owner=User.objects.get(id=request.session['user_id'])
    )
    return redirect('/dashboard')

def edit(request, show_id):
    if 'user_id' not in request.session:
        return redirect('/')
    one_show = Show.objects.get(id=show_id)
    context = {
        'show': one_show
    }
    return render(request, 'edit.html', context)

def delete(request, show_id):
    if 'user_id' not in request.session:
        return redirect('/')
    to_delete = Show.objects.get(id=show_id)
    to_delete.delete()
    return redirect('/dashboard')

def update(request, show_id):
    errors = Show.objects.basic_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/{show_id}/edit')
    else:
        to_update = Show.objects.get(id=show_id)
        to_update.title = request.POST['title']
        to_update.network = request.POST['network']
        to_update.release_date = request.POST['release_date']
        to_update.description = request.POST['description']
        to_update.save()
        return redirect('/dashboard')