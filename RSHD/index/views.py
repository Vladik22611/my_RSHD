from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import psycopg2
from .forms import NameForm, DateForm
from constants import yesterday, delta, min_day_value, max_day_value, tommorow
from django.contrib.auth.views import LoginView
from .forms import UserRegistrationForm, LoginForm

# from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


@login_required
def index(request):
    # View code here...

    try:
        conn = psycopg2.connect(
            dbname="RZHD",
            user="django_admin",
            password="123",
            host="127.0.0.1",
            port="5433",
        )
    except:
        # в случае сбоя подключения будет выведено сообщение в STDOUT
        return HttpResponse("<h1>Потеряно подключение к базе данных!</h1>")

    cursor = conn.cursor()
    query1 = """ 
            SELECT DISTINCT(city_name), id
            FROM railway_stations 
            LIMIT 14
    """
    cursor.execute(query1)  # создаем представление
    conn.commit()
    cites = cursor.fetchall()
    popular_cites = []
    for x in range(len(cites)):
        popular_cites.append({"id": cites[x][1], "city_name": cites[x][0]})

    # is_client = request.user.groups.filter(name="Clients").exists()
    is_superuser = request.user.is_superuser
    context = {
        "today": yesterday.strftime("%Y-%m-%d"),
        "min_day_value": min_day_value,
        "max_day_value": max_day_value,
        "tommorow": tommorow,
        "popular_cites": popular_cites,
        "is_superuser": is_superuser,
    }
    return render(request, "index/main.html", context)


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data["password"])
            # Save the User object
            new_user.save()
            return render(request, "index/register_done.html", {"new_user": new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, "index/register.html", {"user_form": user_form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            # Аутентификация пользователя
            user = authenticate(username=username, password=password)
            if user is not None:
                # Логиним пользователя
                login(request, user=user)
                return redirect("index")  # Направляем на главную страницу или другую э
            else:
                form.add_error(None, "Неверный логин или пароль.")
    else:
        form = LoginForm()

    return render(request, "index/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("index")  # Замените на нужный URL или имя представления
