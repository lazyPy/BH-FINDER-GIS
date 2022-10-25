from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.models import Group

from .decorators import unauthenticated_user, admin_only, user_only


# Create your views here.

@unauthenticated_user
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('admin-home-page')
        else:
            messages.error(request, 'INCORRECT Username or Password')

    return render(request, 'login.html')


@unauthenticated_user
def registerUser(request):
    form = UserForm()

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='user')
            user.groups.add(group)
            messages.info(request, 'Account Created!')
            return redirect('login-page')
        else:
            messages.error(request, 'Invalid Credentials. Try again!')

    context = {
        'form': form,
    }
    return render(request, 'register.html', context)


@login_required(login_url='login-page')
def logoutUser(request):
    logout(request)
    return redirect('login-page')


@login_required(login_url='login-page')
@admin_only
def adminPage(request):
    boarding_houses = BoardingHouse.objects.all()

    context = {
        'boarding_houses': boarding_houses,
    }
    return render(request, 'home-admin.html', context)


@login_required(login_url='login-page')
@user_only
def homePage(request):
    boarding_houses = BoardingHouse.objects.all()

    context = {
        'boarding_houses': boarding_houses,
    }
    return render(request, 'home-user.html', context)


@login_required(login_url='login-page')
@user_only
def myBh(request, pk):
    boarding_houses = BoardingHouse.objects.all()

    context = {
        'boarding_houses': boarding_houses,
    }
    return render(request, 'my-bh.html', context)


@login_required(login_url='login-page')
@user_only
def bhDetail(request, pk):
    bh = BoardingHouse.objects.get(id=pk)

    context = {
        'bh': bh,
    }
    return render(request, 'bh-detail.html', context)


@login_required(login_url='login-page')
@user_only
def addBH(request):
    if request.method == 'POST':
        form = BoardingHouseFullForm(request.POST or None, request.FILES or None)
        pictures = request.FILES.getlist('picture')
        if form.is_valid():
            owner = request.user
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            phone = form.cleaned_data['phone']
            location = form.cleaned_data['location']
            latitude = form.cleaned_data['latitude']
            longitude = form.cleaned_data['longitude']
            bh_obj = BoardingHouse.objects.create(owner=owner, name=name, description=description, price=price,
                                                  phone=phone, location=location, latitude=latitude,
                                                  longitude=longitude)

            if pictures:  # check if user has uploaded some files
                for f in pictures:
                    Picture.objects.create(bh=bh_obj, picture=f)

            messages.success(request, 'Boarding house created!')
            return redirect('my-bh', request.user.id)
    return render(request, 'add-bh.html')


@login_required(login_url='login-page')
@user_only
def editBH(request, pk):
    bh = BoardingHouse.objects.get(id=pk)

    context = {
        'bh': bh,
    }
    return render(request, 'edit-bh.html', context)


@login_required(login_url='login')
@user_only
def updateBH(request, pk):
    bh = BoardingHouse.objects.get(id=pk)
    bh.owner = request.user
    bh.name = request.POST['name']
    bh.description = request.POST['description']
    bh.price = request.POST['price']
    bh.phone = request.POST['phone']
    bh.location = request.POST['location']
    bh.latitude = request.POST['latitude']
    bh.longitude = request.POST['longitude']
    bh.admin_approval = False

    pictures = request.FILES.getlist('picture')
    if pictures:  # check if user has uploaded some files
        for bh_pictures in bh.picture_set.all():
            bh_pictures.delete()
        for f in pictures:
            Picture.objects.create(bh=bh, picture=f)
    bh.save()
    messages.success(request, 'Updated Successfully!')

    return redirect('bh-detail', pk)


@login_required(login_url='login-page')
@user_only
def deleteBH(request, pk):
    bh = BoardingHouse.objects.get(id=pk)
    bh.delete()
    messages.success(request, 'Deleted Successfully!')
    return redirect('my-bh', pk)


def adminBHDetail(request, pk):
    bh = BoardingHouse.objects.get(id=pk)

    if bh.admin_approval:
        bh.admin_approval = 'APPROVED'
    else:
        bh.admin_approval = 'DENIED'

    if request.method == 'POST':
        bh.admin_approval = request.POST['admin_approval']
        if bh.admin_approval == 'APPROVED':
            bh.admin_approval = True
            bh.save(update_fields=['admin_approval'])
            messages.success(request, 'Updated Successfully!')
            bh.admin_approval = 'APPROVED'
        else:
            bh.admin_approval = False
            bh.save(update_fields=['admin_approval'])
            messages.success(request, 'Updated Successfully!')
            bh.admin_approval = 'DENIED'

    context = {
        'bh': bh,
        'status': bh.admin_approval
    }

    return render(request, 'bh-detail.html', context)
