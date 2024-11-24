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
                tr.need_repairs, -- необходимость в обслуживании true/false
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
    context = {
        "departure_date": date_departure,
        "departure_time": {x: filter_raws[x][1] for x in range(count_rows)},
        "arrival_date": date_arrival,
        "arrival_time": {x: filter_raws[x][3] for x in range(count_rows)},
        "city_departure": city_departure,
        "station_departure": {x: filter_raws[x][5] for x in range(count_rows)},
        "city_arrival": city_arrival,
        "station_arrival": {x: filter_raws[x][7] for x in range(count_rows)},
        "need_repairs": {x: filter_raws[x][8] for x in range(count_rows)},
        "year_of_manufacture": {x: filter_raws[x][9] for x in range(count_rows)},
        "name_model": {x: filter_raws[x][10] for x in range(count_rows)},
        "capacity": {x: filter_raws[x][11] for x in range(count_rows)},
        "travel_speed": {x: filter_raws[x][12] for x in range(count_rows)},
        "service_life": {x: filter_raws[x][13] for x in range(count_rows)},
        "seat_type": {x: filter_raws[x][14] for x in range(count_rows)},
        "motor_used": {x: filter_raws[x][15] for x in range(count_rows)},
        "condition_system": {x: filter_raws[x][16] for x in range(count_rows)},
        "train_type": {x: filter_raws[x][17] for x in range(count_rows)},
    }
    return render(request, "routes/list_routes.html", context)


# Create your views here.
