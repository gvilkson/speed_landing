from django.shortcuts import render, redirect
from django.contrib.auth import logout
from accounts.models import UserProfile
import pytz
import datetime
from django.contrib.auth import login
from accounts.forms import CustomUserCreateForm

# Variáveis globais --------------------------------------
avatar_url = None
current_datetime = None
email = None
# End Variáveis globais ----------------------------------

def register(request):
    if request.method == "POST":
        form = CustomUserCreateForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = CustomUserCreateForm()
    return render(request, "accounts/register.html", {"form": form})



def profile(request):
    if request.user.is_authenticated:

        profile = UserProfile.objects.get(user=request.user)
        avatar = profile.avatar_url()
        
        context = {
            'avatar':avatar
        }
        return render(request, 'accounts/profile.html', context)
    else:
        # Usuário não autenticado
        user_profile = None
        return redirect("login")

def logout_view(request):
    global avatar_url
    global current_datetime
    global email

    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        email = user_profile.user.email
        avatar_url = user_profile.avatar_url()  # Obtém a URL da imagem do avatar

        try:
            user_country = user_profile.country
            country_timezone = pytz.timezone(user_country.timezone)
            current_datetime = datetime.datetime.now(country_timezone)
        except (AttributeError, pytz.UnknownTimeZoneError):
            current_datetime = datetime.datetime.now()
    else:
        current_datetime = datetime.datetime.now()


    logout(request)  # Realiza o logout do usuário
    return redirect('accounts:lock-screen')

def lock_screen(request):
    global avatar_url
    global current_datetime
    global email

    # Separar a data, hora, minuto e segundo
    date = current_datetime.date()
    time = current_datetime.time()
    hour = current_datetime.hour
    minute = current_datetime.minute
    second = current_datetime.second

    # Determinar se é manhã (AM), tarde (PM), noite, meia-noite ou meio-dia
    if hour == 0 and minute == 0 and second == 0:
        period = 'MN'  # Meia-noite
    elif hour == 12 and minute == 0 and second == 0:
        period = 'NO'  # Meio-dia
    elif hour < 12:
        period = 'AM'  # Manhã
    elif hour < 18:
        period = 'PM'  # Tarde
    else:
        period = 'NI'  # Noite

    context = {
        'email': email,
        'avatar_url': avatar_url,
        'date': date,
        'time': time,
        'hour': hour,
        'minute': minute,
        'second': second,
        'period': period,
    }

    return render(request, 'accounts/lock-screen.html', context)
