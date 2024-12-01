from django.shortcuts import render
import psycopg2
from django.http import HttpResponse


def table(request, name_table):
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

    query1 = f"""SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = '{name_table}';
    """

    cursor.execute(query1)
    column_name = cursor.fetchall()
    mas_column_name = []
    for i in column_name:
        mas_column_name.append(i[0])

    query2 = f"""SELECT * 
            FROM {name_table};
    """
    cursor.execute(query2)
    data = cursor.fetchall()

    return render(
        request,
        "show_table/show_table.html",
        {"title": f"Таблица {name_table}", "columns": mas_column_name, "data": data},
    )


# Create your views here.
