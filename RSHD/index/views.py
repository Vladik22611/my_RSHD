from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import psycopg2
from constants import yesterday, delta, min_day_value, max_day_value, tommorow


# from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


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
    cursor.execute("SELECT get_races_count();")
    count_races = cursor.fetchone()[0]
    context = {
        "today": yesterday.strftime("%Y-%m-%d"),
        "min_day_value": min_day_value,
        "max_day_value": max_day_value,
        "tommorow": tommorow,
        "popular_cites": popular_cites,
        "is_superuser": is_superuser,
        "count_races": count_races,
    }
    return render(request, "index/main.html", context)

