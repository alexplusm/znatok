from django.shortcuts import render, redirect
from .forms import RegistrationForm, ProfileForm, UserUpdateForm, PasswordUpdateForm
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from .models import Result, Rank
from exam.models import Question
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            questions = Question.objects.all()
            results = (Result(user=user, question=question) for question in questions)
            Result.objects.bulk_create(results)
            domain = get_current_site(request).domain
            protocol = 'https' if request.is_secure() else 'http'

            message = render_to_string('active_email.html', {
                'domain': domain,
                'protocol': protocol,
                'user': user,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            subject = 'Активация аккаунта'
            to_email = form.cleaned_data.get('email')
            send_mail(subject, message, None, [to_email], fail_silently=False)

            return redirect('confirm')
    else:
        form = RegistrationForm()

    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('confirm_done')
    else:
        return redirect('confirm_fail')


def profile(request):
    if request.method == 'POST':
        print(request.POST)
        if 'first_name' in request.POST:
            user_form = UserUpdateForm(request.POST, instance=request.user)
            profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                return redirect('profile')
            password_form = PasswordUpdateForm(request.user)

        if 'old_password' in request.POST:
            password_form = PasswordUpdateForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return redirect('profile')
            user_form = UserUpdateForm(instance=request.user)
            profile_form = ProfileForm(instance=request.user.profile)

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        password_form = PasswordUpdateForm(request.user)
        ranks = list(Rank.objects.all().values())
    return render(request, 'profile.html', {'forms': [user_form, profile_form], 'password_form':[password_form], 'ranks': ranks})


def take_point(request):
    if request.method == 'POST' and request.is_ajax():
        points = request.user.profile.rank.rank_reward_point

        request.user.profile.points += points
        if request.user.profile.rank_id != 8:
            request.user.profile.rank_id += 1
        request.user.profile.rank_progress = 0
        request.user.save()

        ranks = Rank.objects.all()

        return render(request, 'achievement.html', {'ranks': ranks})


def get_block_achievement(request):
    if request.method == 'POST' and request.is_ajax():
        ranks = Rank.objects.all()
        return render(request, 'achievement.html', {'ranks': ranks})


def get_block_information(request):
    if request.method == 'POST' and request.is_ajax():
        return render(request, 'information.html')