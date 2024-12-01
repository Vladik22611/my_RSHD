from django.shortcuts import render
from constants import yesterday, tommorow
import psycopg2
from django.http import HttpResponse


def list_routes(request):
    context = {}
    return render(request, "routes/list_routes.html", context)


def route(request):
    city_departure = request.POST.get("departure", "Москва")
    city_arrival = request.POST.get("arrival", "Ессентуки")
    date_departure = request.POST.get("date_start", yesterday.strftime("%Y-%m-%d"))
    date_arrival = request.POST.get("date_stop", tommorow)
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
    query1 = """
            CREATE OR REPLACE VIEW data_station AS 
            SELECT 
                r.departure_date, -- дата отправления  
                r.departure_time, -- время отправления
                r.arrival_date, -- дата прибытия
                r.arrival_time, -- время прибытия
                rs.city_name as city_departure, -- город отправления
                rs.railway_station_name as station_departure, -- вокзал отправления
                rs1.city_name as city_arrival, -- город прибытия
                rs1.railway_station_name as station_arrival, -- вокзал прибытия
                tr.need_repairs, -- необходимость в обслуживании true/false +
                tr.year_of_manufacture, -- год выпуска
                mt.name_model, -- название модели поезда
                mt.capacity, -- вместимость поезда
                mt.travel_speed, -- скорость поезда
                mt.service_life, -- срок эксплуатации
                mt.seat_type, -- тип сидений
                mt.motor_used, -- мотор
                mt.condition_system, -- система кондиционирования true/false
                mt.train_type -- тип поезда/рейса
            FROM races r
            JOIN routes ro ON r.id_route = ro.id 
            JOIN railway_stations rs ON ro.id_departure_station = rs.id
            JOIN railway_stations rs1 ON ro.id_arrival_station = rs1.id
            JOIN trains tr ON r.id_train = tr.id 
            JOIN model_train mt ON tr.id_model = mt.id;
            """
    cursor.execute(query1)  # создаем представление
    conn.commit()
    query2 = f"""
            SELECT * 
            FROM data_station  
            WHERE city_departure = '{city_departure}' 
            AND city_arrival = '{city_arrival}'
            AND departure_date = '{date_departure}'
            AND arrival_date = '{date_arrival}' 
    """
    cursor.execute(query2)
    conn.commit()
    filter_raws = cursor.fetchall()
    print(filter_raws)
    cursor.close()  # закрываем курсор
    conn.close()  # закрываем соединени
    count_rows = len(filter_raws)
    a = []
    for x in range(count_rows):
        a.append(
            {
                "id": x,
                "departure_date": date_departure,
                "departure_time": filter_raws[x][1].strftime("%H:%M"),
                "arrival_date": date_arrival,
                "arrival_time": (filter_raws[x][3]).strftime("%H:%M"),
                "city_departure": city_departure,
                "station_departure": filter_raws[x][5],
                "city_arrival": city_arrival,
                "station_arrival": filter_raws[x][7],
                "need_repairs": filter_raws[x][8],
                "year_of_manufacture": (filter_raws[x][9]).strftime("%Y"),
                "name_model": filter_raws[x][10],
                "capacity": filter_raws[x][11],
                "travel_speed": filter_raws[x][12],
                "service_life": filter_raws[x][13],
                "seat_type": filter_raws[x][14],
                "motor_used": filter_raws[x][15],
                "condition_system": filter_raws[x][16],
                "train_type": filter_raws[x][17],
                "r_service_life": int((filter_raws[x][9]).strftime("%Y"))
                + filter_raws[x][13]
                - int(yesterday.strftime("%Y")),
            }
        )
    context = {
        'mas': a
    }
    return render(request, "routes/list_routes.html", context)


def popular_city(request, pk):
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
    query1 = f"""
    SELECT city_name
    FROM railway_stations
    WHERE id = {pk};
    """
    cursor.execute(query1)
    city_name = cursor.fetchall()[0][0]
    query2 = f"""
            SELECT * 
            FROM data_station  
            WHERE city_arrival = '{city_name}'
    """
    cursor.execute(query2)
    conn.commit()
    filter_raws = cursor.fetchall()
    count_rows = len(filter_raws)
    a = []
    for x in range(count_rows):
        a.append(
            {
                "id": x,
                "departure_date": filter_raws[x][0],
                "departure_time": filter_raws[x][1].strftime("%H:%M"),
                "arrival_date": filter_raws[x][2],
                "arrival_time": (filter_raws[x][3]).strftime("%H:%M"),
                "city_departure": filter_raws[x][4],
                "station_departure": filter_raws[x][5],
                "city_arrival": city_name,
                "station_arrival": filter_raws[x][7],
                "need_repairs": filter_raws[x][8],
                "year_of_manufacture": (filter_raws[x][9]).strftime("%Y"),
                "name_model": filter_raws[x][10],
                "capacity": filter_raws[x][11],
                "travel_speed": filter_raws[x][12],
                "service_life": filter_raws[x][13],
                "seat_type": filter_raws[x][14],
                "motor_used": filter_raws[x][15],
                "condition_system": filter_raws[x][16],
                "train_type": filter_raws[x][17],
                "r_service_life": int((filter_raws[x][9]).strftime("%Y"))
                + filter_raws[x][13]
                - int(yesterday.strftime("%Y")),
            }
        )
    context = {
        'mas': a
    }
    return render(request, "routes/list_routes.html", context)



# Create your views here.
