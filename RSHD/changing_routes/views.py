from django.shortcuts import render, redirect
import psycopg2
from django.http import HttpResponse
from .forms import (
    AddItForm,
    AddModelForm,
    AddRouteForm,
    AddStationForm,
    ChangeItForm,
    ChangeModelForm,
    ChangeStationForm,
    ChangeTrainForm,
    DelItForm,
    DelModelForm,
    DelRouteForm,
    ChangeRouteForm,
    AddTrainForm,
    DelStationForm,
    DelTrainForm,
)


def add_route(request):
    try:
        # пытаемся подключиться к базе данных
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
    if request.method == "POST":
        form = AddRouteForm(request.POST)
        if form.is_valid():
            # Используем функцию INSERT из postgresql
            a = form.cleaned_data
            try:
                cursor.execute(
                    "CALL insert_race(%s, %s, %s, %s, %s, %s)",
                    (
                        a["id_route"],
                        a["departure_date"],
                        a["departure_time"],
                        a["arrival_date"],
                        a["arrival_time"],
                        a["id_train"],
                    ),
                )
                conn.commit()
                return render(
                    request,
                    "changing_routes/happy_add.html",
                    {
                        "title": "Добавление рейса",
                    },
                )  # Перенаправляем на страницу успеха или другую страницу
            except BaseException as e:
                # Проверяем сообщение об ошибке
                if "Запись с такими же значениями уже существует" in str(e):
                    error_message = (
                        "Ошибка: запись с такими же значениями уже существует!"
                    )
                else:
                    error_message = "Произошла ошибка при добавлении записи."
                return render(
                    request,
                    "changing_routes/sad_add.html",
                    {
                        "title": error_message,
                    },
                )
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
    else:
        form = AddRouteForm()

    return render(
        request,
        "changing_routes/changing_route.html",
        {
            "form": form,
            "our_url": "add_route",
            "title": "Добавление рейса",
            "button_title": "Добавить рейс",
        },
    )


def del_route(request):
    try:
        # пытаемся подключиться к базе данных
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
    if request.method == "POST":
        form = DelRouteForm(request.POST)
        if form.is_valid():
            # Используем функцию DELETE из postgresql
            try:
                cursor.execute(
                    "CALL delete_race(%s)",
                    (form.cleaned_data["id_race"],),
                )
                conn.commit()
                return render(
                    request,
                    "changing_routes/happy_add.html",
                    {
                        "title": "Удаление рейса",
                    },
                )  # Перенаправляем на страницу успеха или другую страницу
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
    else:
        form = DelRouteForm()

    return render(
        request,
        "changing_routes/changing_route.html",
        {
            "form": form,
            "our_url": "del_route",
            "title": "Удаление рейса",
            "button_title": "Удалить рейс",
        },
    )


def change_route(request):
    try:
        # пытаемся подключиться к базе данных
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
    if request.method == "POST":
        form = DelRouteForm(request.POST)
        if form.is_valid():
            try:
                return redirect(
                    "change_route_def", pk=form.cleaned_data["id_race"]
                )  # Перенаправляем на страницу успеха или другую страницу
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
    else:
        form = DelRouteForm()

    return render(
        request,
        "changing_routes/changing_route.html",
        {
            "form": form,
            "our_url": "change_route",
            "title": "Изменение рейса",
            "button_title": "Изменить рейс",
        },
    )


def change_route_def(request, pk):
    try:
        # пытаемся подключиться к базе данных
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
    if request.method == "POST":
        form = ChangeRouteForm(request.POST, pk=pk)
        if form.is_valid():
            # Используем функцию INSERT из postgresql
            a = form.cleaned_data
            try:
                cursor.execute(
                    "SELECT update_race(%s,%s, %s, %s, %s, %s, %s)",
                    (
                        pk,
                        a["id_train"],
                        a["id_route"],
                        a["departure_date"],
                        a["departure_time"],
                        a["arrival_date"],
                        a["arrival_time"],
                    ),
                )
                conn.commit()
                return render(
                    request,
                    "changing_routes/happy_add.html",
                    {
                        "title": "Изменение рейса",
                    },
                )  # Перенаправляем на страницу успеха или другую страницу
            except BaseException as e:
                # Проверяем сообщение об ошибке
                if "идентичная строка уже существует" in str(e):
                    error_message = (
                        "Ошибка: запись с такими же значениями уже существует!"
                    )
                else:
                    error_message = "Произошла ошибка при добавлении записи."
                return render(
                    request,
                    "changing_routes/sad_add.html",
                    {
                        "title": error_message,
                    },
                )
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
    else:
        form = ChangeRouteForm(pk=pk)

    return render(
        request,
        "changing_routes/changing_route_pk.html",
        {
            "form": form,
            "our_url": "change_route_def",
            "pk": pk,
            "title": "Изменение рейса",
            "button_title": "Изменить рейс",
        },
    )


def add_train(request):
    try:
        # пытаемся подключиться к базе данных
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
    if request.method == "POST":
        form = AddTrainForm(request.POST)
        if form.is_valid():
            # Используем функцию INSERT из postgresql
            a = form.cleaned_data
            try:
                print(a)
                cursor.execute(
                    "SELECT insert_train(%s, %s, %s)",
                    (
                        a["id_model"],
                        a["need_repairs"],
                        a["year_of_manufacture"],
                    ),
                )

                conn.commit()
                return render(
                    request,
                    "changing_routes/happy_add.html",
                    {
                        "title": "Добавление поезда",
                    },
                )  # Перенаправляем на страницу успеха или другую страницу

            except BaseException as e:
                # Проверяем сообщение об ошибке
                if "Запись с такими же значениями уже существует" in str(e):
                    error_message = (
                        "Ошибка: запись с такими же значениями уже существует!"
                    )
                else:
                    error_message = "Произошла ошибка при добавлении записи."
                return render(
                    request,
                    "changing_routes/sad_add.html",
                    {
                        "title": error_message,
                    },
                )
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

    else:
        form = AddTrainForm()

    return render(
        request,
        "changing_routes/changing_route.html",
        {
            "form": form,
            "our_url": "add_train",
            "title": "Добавление поезда",
            "button_title": "Добавить поезд",
        },
    )


def del_train(request):
    try:
        # пытаемся подключиться к базе данных
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
    if request.method == "POST":
        form = DelTrainForm(request.POST)
        if form.is_valid():
            # Используем функцию DELETE из postgresql
            try:
                cursor.execute(
                    "CALL delete_train(%s)",
                    (form.cleaned_data["id_train"],),
                )
                conn.commit()
                return render(
                    request,
                    "changing_routes/happy_add.html",
                    {
                        "title": "Удаление поезда",
                    },
                )  # Перенаправляем на страницу успеха или другую страницу
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
    else:
        form = DelTrainForm()

    return render(
        request,
        "changing_routes/changing_route.html",
        {
            "form": form,
            "our_url": "del_train",
            "title": "Удаление поезда",
            "button_title": "Удалить поезд",
        },
    )


def change_train(request):
    try:
        # пытаемся подключиться к базе данных
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
    if request.method == "POST":
        form = DelTrainForm(request.POST)
        if form.is_valid():
            try:
                return redirect(
                    "change_train_def", pk=form.cleaned_data["id_train"]
                )  # Перенаправляем на страницу успеха или другую страницу
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
    else:
        form = DelTrainForm()

    return render(
        request,
        "changing_routes/changing_route.html",
        {
            "form": form,
            "our_url": "change_train",
            "title": "Изменение поезда",
            "button_title": "Изменить поезд",
        },
    )


def change_train_def(request, pk):
    try:
        # пытаемся подключиться к базе данных
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
    if request.method == "POST":
        form = ChangeTrainForm(request.POST, pk=pk)
        if form.is_valid():
            # Используем функцию INSERT из postgresql
            a = form.cleaned_data
            try:
                cursor.execute(
                    "SELECT update_train1(%s,%s, %s, %s)",
                    (
                        pk,
                        a["id_model"],
                        a["need_repairs"],
                        a["year_of_manufacture"],
                    ),
                )
                conn.commit()
                return render(
                    request,
                    "changing_routes/happy_add.html",
                    {
                        "title": "Изменение поезда",
                    },
                )  # Перенаправляем на страницу успеха или другую страницу
            
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
    else:
        form = ChangeTrainForm(pk=pk)

    return render(
        request,
        "changing_routes/changing_route_pk.html",
        {
            "form": form,
            "our_url": "change_train_def",
            "pk": pk,
            "title": "Изменение поезда",
            "button_title": "Изменить поезд",
        },
    )


def add_model(request):
    try:
        # пытаемся подключиться к базе данных
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
    if request.method == "POST":
        form = AddModelForm(request.POST)
        if form.is_valid():
            # Используем функцию INSERT из postgresql
            a = form.cleaned_data
            try:
                print(a)
                cursor.execute(
                    "SELECT insert_model(%s, %s, %s, %s, %s, %s, %s, %s)",
                    (
                        a["name_model"],
                        a["capacity"],
                        a["travel_speed"],
                        a["service_life"],
                        a["seat_type"],
                        a["motor_used"],
                        a["condition_system"],
                        a["train_type"],
                    ),
                )

                conn.commit()
                return render(
                    request,
                    "changing_routes/happy_add.html",
                    {
                        "title": "Добавление модели поезда",
                    },
                )  # Перенаправляем на страницу успеха или другую страницу

            except BaseException as e:
                # Проверяем сообщение об ошибке
                if "Запись с такими же значениями уже существует" in str(e):
                    error_message = (
                        "Ошибка: запись с такими же значениями уже существует!"
                    )
                else:
                    error_message = "Произошла ошибка при добавлении записи."
                return render(
                    request,
                    "changing_routes/sad_add.html",
                    {
                        "title": error_message,
                    },
                )
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

    else:
        form = AddModelForm()

    return render(
        request,
        "changing_routes/changing_route.html",
        {
            "form": form,
            "our_url": "add_model",
            "title": "Добавление модели поезда",
            "button_title": "Добавить модель поезда",
        },
    )


def del_model(request):
    try:
        # пытаемся подключиться к базе данных
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
    if request.method == "POST":
        form = DelModelForm(request.POST)
        if form.is_valid():
            # Используем функцию DELETE из postgresql
            try:
                cursor.execute(
                    "SELECT delete_model(%s)",
                    (form.cleaned_data["id_model"],),
                )
                conn.commit()
                return render(
                    request,
                    "changing_routes/happy_add.html",
                    {
                        "title": "Удаление модели поезда",
                    },
                )  # Перенаправляем на страницу успеха или другую страницу
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
    else:
        form = DelModelForm()

    return render(
        request,
        "changing_routes/changing_route.html",
        {
            "form": form,
            "our_url": "del_model",
            "title": "Удаление модели поезда",
            "button_title": "Удалить модель поезда",
        },
    )


def change_model(request):
    try:
        # пытаемся подключиться к базе данных
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
    if request.method == "POST":
        form = DelModelForm(request.POST)
        if form.is_valid():
            try:
                return redirect(
                    "change_model_def", pk=form.cleaned_data["id_model"]
                )  # Перенаправляем на страницу успеха или другую страницу
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
    else:
        form = DelModelForm()

    return render(
        request,
        "changing_routes/changing_route.html",
        {
            "form": form,
            "our_url": "change_model",
            "title": "Изменение модели поезда",
            "button_title": "Изменить модель поезда",
        },
    )


def change_model_def(request, pk):
    try:
        # пытаемся подключиться к базе данных
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
    if request.method == "POST":
        form = ChangeModelForm(request.POST, pk=pk)
        if form.is_valid():
            # Используем функцию INSERT из postgresql
            a = form.cleaned_data
            try:
                cursor.execute(
                    "SELECT public.update_model1(%s,%s, %s, %s, %s, %s, %s, %s, %s)",
                    (
                        pk,
                        a["name_model"],
                        a["capacity"],
                        a["travel_speed"],
                        a["service_life"],
                        a["seat_type"],
                        a["motor_used"],
                        a["condition_system"],
                        a["train_type"],
                    ),
                )
                conn.commit()
                return render(
                    request,
                    "changing_routes/happy_add.html",
                    {
                        "title": "Изменение модели поезда",
                    },
                )  # Перенаправляем на страницу успеха или другую страницу

            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
    else:
        form = ChangeModelForm(pk=pk)

    return render(
        request,
        "changing_routes/changing_route_pk.html",
        {
            "form": form,
            "our_url": "change_model_def",
            "pk": pk,
            "title": "Изменение модели поезда",
            "button_title": "Изменить модель",
        },
    )


def add_it(request):
    try:
        # пытаемся подключиться к базе данных
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
    if request.method == "POST":
        form = AddItForm(request.POST)
        if form.is_valid():
            # Используем функцию INSERT из postgresql
            a = form.cleaned_data
            try:
                cursor.execute(
                    "SELECT insert_route1(%s, %s)",
                    (
                        a["id_dep"],
                        a["id_arr"],
                    ),
                )
                conn.commit()
                return render(
                    request,
                    "changing_routes/happy_add.html",
                    {
                        "title": "Добавление маршрута",
                    },
                )  # Перенаправляем на страницу успеха или другую страницу
            except BaseException as e:
                # Проверяем сообщение об ошибке
                if "повторяющееся значение" in str(e):
                    error_message = (
                        "Ошибка: запись с такими же значениями уже существует!"
                    )
                elif "не может быть равен" in str(e):
                    error_message = "Ошибка: ID станции отправления не может быть равен ID станции прибытия!"
                else:
                    error_message = "Произошла ошибка при добавлении записи."
                return render(
                    request,
                    "changing_routes/sad_add.html",
                    {
                        "title": error_message,
                    },
                )
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
    else:
        form = AddItForm()

    return render(
        request,
        "changing_routes/changing_route.html",
        {
            "form": form,
            "our_url": "add_it",
            "title": "Добавление маршрута",
            "button_title": "Добавить маршрут",
        },
    )


def del_it(request):
    try:
        # пытаемся подключиться к базе данных
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
    if request.method == "POST":
        form = DelItForm(request.POST)
        if form.is_valid():
            # Используем функцию DELETE из postgresql
            try:
                cursor.execute(
                    "SELECT delete_route(%s)",
                    (form.cleaned_data["id_route"],),
                )
                conn.commit()
                return render(
                    request,
                    "changing_routes/happy_add.html",
                    {
                        "title": "Удаление маршрута",
                    },
                )  # Перенаправляем на страницу успеха или другую страницу
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
    else:
        form = DelItForm()

    return render(
        request,
        "changing_routes/changing_route.html",
        {
            "form": form,
            "our_url": "del_it",
            "title": "Удаление мрашрута",
            "button_title": "Удалить маршрут",
        },
    )


def change_it(request):
    try:
        # пытаемся подключиться к базе данных
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
    if request.method == "POST":
        form = DelItForm(request.POST)
        if form.is_valid():
            try:
                return redirect(
                    "change_it_def", pk=form.cleaned_data["id_route"]
                )  # Перенаправляем на страницу успеха или другую страницу
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
    else:
        form = DelItForm()

    return render(
        request,
        "changing_routes/changing_route.html",
        {
            "form": form,
            "our_url": "change_it",
            "title": "Изменение маршрута",
            "button_title": "Изменить маршрут",
        },
    )


def change_it_def(request, pk):
    try:
        # пытаемся подключиться к базе данных
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
    if request.method == "POST":
        form = ChangeItForm(request.POST, pk=pk)
        if form.is_valid():
            # Используем функцию INSERT из postgresql
            a = form.cleaned_data
            try:
                cursor.execute(
                    "SELECT update_route(%s,%s, %s)",
                    (
                        pk,
                        a["id_dep"],
                        a["id_arr"],
                    ),
                )
                conn.commit()
                return render(
                    request,
                    "changing_routes/happy_add.html",
                    {
                        "title": "Изменение маршрута",
                    },
                )  # Перенаправляем на страницу успеха или другую страницу
            except BaseException as e:
                # Проверяем сообщение об ошибке
                if "не может быть равен" in str(e):
                    error_message = "Ошибка: ID станции отправления не может быть равен ID станции прибытия!"
                else:
                    error_message = (
                        "Ошибка: запись с такими же значениями уже существует!"
                    )
                return render(
                    request,
                    "changing_routes/sad_add.html",
                    {
                        "title": error_message,
                    },
                )
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
    else:
        form = ChangeItForm(pk=pk)

    return render(
        request,
        "changing_routes/changing_route_pk.html",
        {
            "form": form,
            "our_url": "change_it_def",
            "pk": pk,
            "title": "Изменение маршрута",
            "button_title": "Изменить маршрут",
        },
    )


def add_station(request):
    try:
        # пытаемся подключиться к базе данных
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
    if request.method == "POST":
        form = AddStationForm(request.POST)
        if form.is_valid():
            # Используем функцию INSERT из postgresql
            a = form.cleaned_data
            try:
                cursor.execute(
                    "SELECT insert_station(%s, %s)",
                    (
                        a["railway_station_name"],
                        a["city_name"],
                    ),
                )
                conn.commit()
                return render(
                    request,
                    "changing_routes/happy_add.html",
                    {
                        "title": "Добавление станции",
                    },
                )  # Перенаправляем на страницу успеха или другую страницу
            except BaseException as e:
                # Проверяем сообщение об ошибке
                if "Станция с таким именем" in str(e):
                    error_message = (
                        "Ошибка: Станция с таким именем уже существует в данном городе."
                    )

                else:
                    error_message = "Произошла ошибка при добавлении записи."
                return render(
                    request,
                    "changing_routes/sad_add.html",
                    {
                        "title": error_message,
                    },
                )
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
    else:
        form = AddStationForm()

    return render(
        request,
        "changing_routes/changing_route.html",
        {
            "form": form,
            "our_url": "add_station",
            "title": "Добавление станции",
            "button_title": "Добавить станцию",
        },
    )


def del_station(request):
    try:
        # пытаемся подключиться к базе данных
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
    if request.method == "POST":
        form = DelStationForm(request.POST)
        if form.is_valid():
            # Используем функцию DELETE из postgresql
            try:
                cursor.execute(
                    "SELECT delete_station(%s)",
                    (form.cleaned_data["id_station"],),
                )
                conn.commit()
                return render(
                    request,
                    "changing_routes/happy_add.html",
                    {
                        "title": "Удаление станции",
                    },
                )  # Перенаправляем на страницу успеха или другую страницу
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
    else:
        form = DelStationForm()

    return render(
        request,
        "changing_routes/changing_route.html",
        {
            "form": form,
            "our_url": "del_station",
            "title": "Удаление станции",
            "button_title": "Удалить станцию",
        },
    )


def change_station(request):
    try:
        # пытаемся подключиться к базе данных
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
    if request.method == "POST":
        form = DelStationForm(request.POST)
        if form.is_valid():
            try:
                return redirect(
                    "change_station_def", pk=form.cleaned_data["id_station"]
                )  # Перенаправляем на страницу успеха или другую страницу
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
    else:
        form = DelStationForm()

    return render(
        request,
        "changing_routes/changing_route.html",
        {
            "form": form,
            "our_url": "change_station",
            "title": "Изменение станции",
            "button_title": "Изменить станцию",
        },
    )



def change_station_def(request, pk):
    try:
        # пытаемся подключиться к базе данных
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
    if request.method == "POST":
        form = ChangeStationForm(request.POST, pk=pk)
        if form.is_valid():
            # Используем функцию INSERT из postgresql
            a = form.cleaned_data
            try:
                cursor.execute(
                    "SELECT update_station(%s,%s, %s)",
                    (
                        pk,
                        a["railway_station_name"],
                        a["city_name"],
                    ),
                )
                conn.commit()
                return render(
                    request,
                    "changing_routes/happy_add.html",
                    {
                        "title": "Изменение станции",
                    },
                )  # Перенаправляем на страницу успеха или другую страницу
            except BaseException as e:
                # Проверяем сообщение об ошибке
                if "Запись с названиями станции" in str(e):
                    error_message = f"Ошибка: Запись с названиями станции {a['railway_station_name']} и города {a['city_name']} уже существует."
                else:
                    error_message = (
                        "Ошибка: при изменении записи"
                    )
                return render(
                    request,
                    "changing_routes/sad_add.html",
                    {
                        "title": error_message,
                    },
                )
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
    else:
        form = ChangeStationForm(pk=pk)

    return render(
        request,
        "changing_routes/changing_route_pk.html",
        {
            "form": form,
            "our_url": "change_station_def",
            "pk": pk,
            "title": "Изменение станции",
            "button_title": "Изменить станцию",
        },
    )
