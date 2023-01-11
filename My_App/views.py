import uuid
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import *
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from django.core.mail import EmailMessage


# Create your views here.

def registerUser(request):
    form = UserForm()

    if request.method == 'POST':
        form = UserForm(request.POST)

        if get_user_model().objects.filter(email=request.POST['email'], is_active=False).exists():
            messages.info(request, 'This email is registered. Please verify your account!')

        elif form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Confirm your email verification'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

            messages.info(request, 'Please confirm your email address to complete the registration')

        else:
            messages.info(request, 'Invalid Credentials. Try again!')

    context = {
        'form': form,
    }
    return render(request, 'register.html', context)


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'You can now login your account!')
        return redirect('login-page')
    else:
        messages.info(request, 'Activation link is invalid or expired!')
        return redirect('register-page')


def loginAdmin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if not user.is_superuser:
            messages.info(request, 'This page is for administrator login!')
        elif user is not None:
            login(request, user)
            return redirect('admin-page')
        else:
            messages.info(request, 'INCORRECT Credential!')

    return render(request, 'login-admin.html')


def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user.is_superuser:
            messages.info(request, 'This page is NOT for administrator login!')
        elif user is not None:
            request.session.flush()
            login(request, user)
            return redirect('bh-owner')
        else:
            messages.info(request, 'UNVERIFIED Account or INCORRECT Credential!')

    return render(request, 'login.html')


def logoutUser(request):
    logout(request)
    return redirect('user-page')


def userPage(request):
    boarding_houses = BoardingHouse.objects.all()

    context = {
        'boarding_houses': boarding_houses,
    }
    return render(request, 'home-user.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='login-admin-page')
def adminPage(request):
    boarding_houses = BoardingHouse.objects.all()

    context = {
        'boarding_houses': boarding_houses,
    }
    return render(request, 'home-admin.html', context)


@login_required(login_url='login-page')
@user_passes_test(lambda u: not u.is_superuser, login_url='login-page')
def ownerPage(request):
    boarding_houses = BoardingHouse.objects.all()

    context = {
        'boarding_houses': boarding_houses,
    }
    return render(request, 'home-bh-owner.html', context)


@user_passes_test(lambda u: u.is_superuser, login_url='login-admin-page')
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


def bhDetail(request, pk):
    get_bh = BoardingHouse.objects.get(id=pk)
    bh_messages = get_bh.message_set.all()
    user_messages = get_bh.message_set.all().order_by().values('session').distinct()


    try:
        session = Session.objects.get(session_id=request.session['nonuser'])
    except:
        request.session['nonuser'] = str(uuid.uuid4())
        session = Session.objects.create(session_id=request.session['nonuser'])

    if request.user.is_authenticated:
        session.delete()

    if request.method == 'POST':
        if request.user.is_authenticated:
            Message.objects.create(
                user=request.user,
                bh=get_bh,
                body=request.POST.get('body')
            )
        else:
            Message.objects.create(
                bh=get_bh,
                body=request.POST.get('body'),
                session=session
            )

    context = {
        'bh': get_bh,
        'bh_messages': bh_messages,
        'user_messages': user_messages,
        'session': session
    }
    return render(request, 'bh-detail.html', context)


@login_required(login_url='login-page')
@user_passes_test(lambda u: not u.is_superuser, login_url='login-page')
def addBH(request):
    if request.method == 'POST':
        form = BoardingHouseFullForm(request.POST or None, request.FILES or None)
        pictures = request.FILES.getlist('picture')
        if form.is_valid():
            owner = request.user
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            avail_room = form.cleaned_data['avail_room']
            phone = form.cleaned_data['phone']
            location = form.cleaned_data['location']
            latitude = form.cleaned_data['latitude']
            longitude = form.cleaned_data['longitude']
            bh_obj = BoardingHouse.objects.create(owner=owner, name=name, description=description, price=price,
                                                  avail_room=avail_room, phone=phone, location=location,
                                                  latitude=latitude, longitude=longitude)

            if pictures:  # check if user has uploaded some files
                for f in pictures:
                    Picture.objects.create(bh=bh_obj, picture=f)

            messages.success(request, 'Boarding house created!')
            return redirect('bh-owner', request.user.id)
    return render(request, 'add-bh.html')


@login_required(login_url='login-page')
@user_passes_test(lambda u: not u.is_superuser, login_url='login-page')
def editBH(request, pk):
    bh = BoardingHouse.objects.get(id=pk)

    context = {
        'bh': bh,
    }
    return render(request, 'edit-bh.html', context)


@login_required(login_url='login')
@user_passes_test(lambda u: not u.is_superuser, login_url='login-page')
def updateBH(request, pk):
    bh = BoardingHouse.objects.get(id=pk)
    bh.owner = request.user
    bh.name = request.POST['name']
    bh.description = request.POST['description']
    bh.price = request.POST['price']
    bh.avail_room = request.POST['avail_room']
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
@user_passes_test(lambda u: not u.is_superuser, login_url='login-page')
def deleteBH(request, pk):
    bh = BoardingHouse.objects.get(id=pk)
    bh.delete()
    messages.success(request, 'Deleted Successfully!')
    return redirect('bh-owner', pk)
