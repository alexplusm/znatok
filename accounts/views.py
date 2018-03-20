from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from .models import Profile, Result
from exam.models import Question


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
            profile = Profile(user=user)
            profile.save()
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
            send_mail(subject, message, 'znatokPDD', [to_email], fail_silently=False)
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
