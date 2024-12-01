from django import forms
import psycopg2
from django.core.validators import MinValueValidator

try:
    conn = psycopg2.connect(
        dbname="RZHD",
        user="django_admin",
        password="123",
        host="127.0.0.1",
        port="5433",
        # пытаемся подключиться к базе данных
    )
except:
    print("База данных: ошибка подключения!")

cursor = conn.cursor()


class AddRouteForm(forms.Form):
    query1 = """
    SELECT id FROM routes;
    """
    cursor.execute(query1)
    id_route_mas = cursor.fetchall()
    query2 = """
    SELECT id FROM trains;
    """
    cursor.execute(query2)
    id_train_mas = cursor.fetchall()
    # Поля для информации о рейсе
    id_route = forms.ChoiceField(
        label="ID маршрута",
        choices=[],  # Замените пустой список на выбор из базы данных
        widget=forms.Select(
            attrs={
                "class": "wide",
                "class": "single-input",
            }
        ),
    )
    departure_date = forms.DateField(
        label="Дата отправления",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "single-input",
            }
        ),
    )
    departure_time = forms.TimeField(
        label="Время отправления",
        widget=forms.TimeInput(
            attrs={
                "type": "time",
                "class": "single-input",
            }
        ),
    )
    arrival_date = forms.DateField(
        label="Дата прибытия",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "single-input",
            }
        ),
    )
    arrival_time = forms.TimeField(
        label="Время прибытия",
        widget=forms.TimeInput(
            attrs={
                "type": "time",
                "class": "single-input",
            }
        ),
    )

    # Поля для информации о поезде
    id_train = forms.ChoiceField(
        label="ID Поезда",
        choices=[],  # Замените пустой список на выбор из базы данных
        widget=forms.Select(
            attrs={
                "class": "wide",
                "class": "single-input",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Заполнение choices для id_route
        self.fields["id_route"].choices = [(x[0], x[0]) for x in self.id_route_mas]
        # Заполнение choices для id_train
        self.fields["id_train"].choices = [(x[0], x[0]) for x in self.id_train_mas]


class DelRouteForm(forms.Form):
    query1 = """
    SELECT id FROM races;
    """
    cursor.execute(query1)
    id_races_mas = cursor.fetchall()
    id_race = forms.ChoiceField(
        label="ID рейса",
        choices=[],  # Замените пустой список на выбор из базы данных
        widget=forms.Select(
            attrs={
                "class": "wide",
                "class": "single-input",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Заполнение choices для id_race
        self.fields["id_race"].choices = [(x[0], x[0]) for x in self.id_races_mas]


class ChangeRouteForm(AddRouteForm):
    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop("pk", None)  # Извлекаем pk из аргументов
        super().__init__(*args, **kwargs)

        # Открытие соединения с базой данных и выполнение запросов
        with conn.cursor() as cursor:
            cursor.execute(self.query1)
            self.id_route_mas = cursor.fetchall()
            cursor.execute(self.query2)
            self.id_train_mas = cursor.fetchall()

            cursor.execute("SELECT * from get_race_by_id(%s);", (self.pk,))
            self.def_value = cursor.fetchall()
            print(self.pk, self.def_value)

        # Заполнение choices для id_route
        self.fields["id_route"].choices = [(x[0], x[0]) for x in self.id_route_mas]
        # Заполнение choices для id_train
        self.fields["id_train"].choices = [(x[0], x[0]) for x in self.id_train_mas]

        # Установка значений по умолчанию
        if self.fields["id_route"].choices:
            self.initial["id_route"] = self.def_value[0][1]
        if self.fields["id_train"].choices:
            self.initial["id_train"] = self.def_value[0][0]

        # Установка значений по умолчанию для даты и времени
        self.initial["departure_date"] = forms.DateField().widget.format_value(
            self.def_value[0][2]
        )
        self.initial["departure_time"] = forms.TimeField().widget.format_value(
            self.def_value[0][3]
        )
        self.initial["arrival_date"] = forms.DateField().widget.format_value(
            self.def_value[0][4]
        )
        self.initial["arrival_time"] = forms.TimeField().widget.format_value(
            self.def_value[0][5]
        )


class AddTrainForm(forms.Form):
    query1 = """
    SELECT id FROM model_train;
    """
    cursor = conn.cursor()
    cursor.execute(query1)
    id_model_mas = cursor.fetchall()

    # Поля для информации о поезде
    id_model = forms.ChoiceField(
        label="ID модели",
        choices=[],  # Замените пустой список на выбор из базы данных
        widget=forms.Select(
            attrs={
                "class": "wide",
                "class": "single-input",
            }
        ),
    )

    need_repairs = forms.BooleanField(
        label="Нужен ли ремонт?",
        required=False,  # Поле не обязательно заполнять
        widget=forms.CheckboxInput(
            attrs={
                "class": "checkbox",
            }
        ),
    )

    year_of_manufacture = forms.DateField(
        label="Дата выпуска",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "single-input",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Заполнение choices для id_model
        self.fields["id_model"].choices = [(x[0], x[0]) for x in self.id_model_mas]


class DelTrainForm(forms.Form):
    # SQL-запрос для выборки id поездов из таблицы trains
    query1 = """
    SELECT id FROM trains;
    """

    # Выполнение запроса к базе данных
    with conn.cursor() as cursor:
        cursor.execute(query1)
        id_trains_mas = cursor.fetchall()  # Получаем все id поездов

    id_train = forms.ChoiceField(
        label="ID поезда",
        choices=[],  # пустой список, который будет заполнен позже
        widget=forms.Select(
            attrs={
                "class": "wide",
                "class": "single-input",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Заполнение choices для id_train
        self.fields["id_train"].choices = [(x[0], x[0]) for x in self.id_trains_mas]


class ChangeTrainForm(
    AddTrainForm
):  # Предполагая, что вы уже создали форму AddTrainForm
    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop("pk", None)  # Извлекаем pk из аргументов
        super().__init__(*args, **kwargs)

        # Открытие соединения с базой данных и выполнение запросов
        with conn.cursor() as cursor:
            # Запрос для получения всех доступных ID поездов
            cursor.execute(self.query1)
            self.id_model_mas = (
                cursor.fetchall()
            )  # Предполагается, что это ваш запрос к trains

            # Запрос для получения информации о конкретном поезде по pk
            cursor.execute("SELECT * FROM get_train_by_id3(%s);", (self.pk,))
            self.def_value = cursor.fetchall()

        # Заполнение choices для id_train
        self.fields["id_model"].choices = [(x[0], x[0]) for x in self.id_model_mas]

        # Установка значений по умолчанию
        if self.fields["id_model"].choices:
            self.initial["id_model"] = self.def_value[0][
                0
            ]  # Замените индекс в зависимости от структуры ваших данных
        print(self.def_value)
        self.initial["year_of_manufacture"] = forms.DateField().widget.format_value(
            self.def_value[0][1]
        )
        self.initial["need_repairs"] = self.def_value[0][2]

        # Если вы хотите устанавливать значения для других полей, добавьте их здесь


class AddModelForm(forms.Form):
    name_model = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "wide",
                "class": "single-input",
                "placeholder": "Название модели",
            }
        ),
    )

    capacity = forms.IntegerField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "wide",
                "class": "single-input",
                "placeholder": "Вместимость",
            }
        ),
    )

    travel_speed = forms.IntegerField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "wide",
                "class": "single-input",
                "placeholder": "Скорость поезда",
            }
        ),
    )

    service_life = forms.IntegerField(
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "wide",
                "class": "single-input",
                "placeholder": "Срок эксплуатации",
            }
        ),
    )

    seat_type = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "wide",
                "class": "single-input",
                "placeholder": "Тип сидений",
            }
        ),
    )

    motor_used = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "wide",
                "class": "single-input",
                "placeholder": "Используемый мотор",
            }
        ),
    )

    condition_system = forms.BooleanField(
        label="Система кондиционирования?",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "checkbox",
            }
        ),
    )

    train_type = forms.ChoiceField(
        label="Тип поезда",
        choices=[
            ("Пассажирский", "Пассажирский"),
            ("Грузовой", "Грузовой"),
        ],
        widget=forms.Select(
            attrs={
                "class": "wide",
                "class": "single-input",
            }
        ),
    )


class DelModelForm(forms.Form):
    # SQL-запрос для выборки id поездов из таблицы trains
    query1 = """
    SELECT id FROM model_train;
    """

    # Выполнение запроса к базе данных
    with conn.cursor() as cursor:
        cursor.execute(query1)
        id_models_mas = cursor.fetchall()  # Получаем все id

    id_model = forms.ChoiceField(
        label="ID модели",
        choices=[],  # пустой список, который будет заполнен позже
        widget=forms.Select(
            attrs={
                "class": "wide",
                "class": "single-input",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Заполнение choices для id_train
        self.fields["id_model"].choices = [(x[0], x[0]) for x in self.id_models_mas]


class ChangeModelForm(AddModelForm):
    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop("pk", None)  # Извлекаем pk из аргументов
        super().__init__(*args, **kwargs)

        # Открытие соединения с базой данных и выполнение запросов
        with conn.cursor() as cursor:
            # Запрос для получения информации о конкретном поезде по pk
            cursor.execute("SELECT * FROM get_model_by_id2(%s);", (self.pk,))
            self.def_value = cursor.fetchall()

        self.initial["name_model"] = self.def_value[0][0]
        self.initial["capacity"] = self.def_value[0][1]
        self.initial["travel_speed"] = self.def_value[0][2]
        self.initial["service_life"] = self.def_value[0][3]
        self.initial["seat_type"] = self.def_value[0][4]
        self.initial["motor_used"] = self.def_value[0][5]
        self.initial["condition_system"] = self.def_value[0][6]
        self.initial["train_type"] = self.def_value[0][7]


class AddItForm(forms.Form):
    query1 = """
    SELECT id FROM railway_stations;
    """
    cursor.execute(query1)
    id_dep_mas = cursor.fetchall()
    query2 = """
    SELECT id FROM railway_stations;
    """
    cursor.execute(query2)
    id_arr_mas = cursor.fetchall()
    # Поля для информации о рейсе
    id_dep = forms.ChoiceField(
        label="ID станции отправления",
        choices=[],  # Замените пустой список на выбор из базы данных
        widget=forms.Select(
            attrs={
                "class": "wide",
                "class": "single-input",
            }
        ),
    )
   
    # Поля для информации о поезде
    id_arr = forms.ChoiceField(
        label="ID стацнии прибытия",
        choices=[],  # Замените пустой список на выбор из базы данных
        widget=forms.Select(
            attrs={
                "class": "wide",
                "class": "single-input",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Заполнение choices для id_route
        self.fields["id_dep"].choices = [(x[0], x[0]) for x in self.id_dep_mas]
        # Заполнение choices для id_train
        self.fields["id_arr"].choices = [(x[0], x[0]) for x in self.id_arr_mas]



class DelItForm(forms.Form):

    query1 = """
    SELECT id FROM routes;
    """
    cursor.execute(query1)
    id_routes_mas = cursor.fetchall()
    id_route = forms.ChoiceField(
        label="ID маршрута",
        choices=[],  # Замените пустой список на выбор из базы данных
        widget=forms.Select(
            attrs={
                "class": "wide",
                "class": "single-input",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Заполнение choices для id_race
        self.fields["id_route"].choices = [(x[0], x[0]) for x in self.id_routes_mas]


class ChangeItForm(AddItForm):
    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop("pk", None)  # Извлекаем pk из аргументов
        super().__init__(*args, **kwargs)

        # Открытие соединения с базой данных и выполнение запросов
        with conn.cursor() as cursor:
            cursor.execute(self.query1)
            self.id_station = cursor.fetchall()

            cursor.execute("SELECT id_departure_station, id_arrival_station from routes WHERE id = %s;", (self.pk,))
            self.def_value = cursor.fetchall()

        # Заполнение choices для id_route
        self.fields["id_dep"].choices = [(x[0], x[0]) for x in self.id_station]
        self.fields["id_arr"].choices = [(x[0], x[0]) for x in self.id_station]


        # Установка значений по умолчанию
        if self.fields["id_dep"].choices:
            self.initial["id_dep"] = self.def_value[0][0]
        if self.fields["id_arr"].choices:
            self.initial["id_arr"] = self.def_value[0][1]


class AddStationForm(forms.Form):
    railway_station_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "wide",
                "class": "single-input",
                "placeholder": "Ж/Д станция",
            }
        ),
    )

    city_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "wide",
                "class": "single-input",
                "placeholder": "Город",
            }
        ),
    )


class DelStationForm(forms.Form):
    # SQL-запрос для выборки id поездов из таблицы trains
    query1 = """
    SELECT id FROM railway_stations;
    """

    # Выполнение запроса к базе данных
    with conn.cursor() as cursor:
        cursor.execute(query1)
        id_stations_mas = cursor.fetchall()  # Получаем все id

    id_station = forms.ChoiceField(
        label="ID станции",
        choices=[],  # пустой список, который будет заполнен позже
        widget=forms.Select(
            attrs={
                "class": "wide",
                "class": "single-input",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Заполнение choices для id_train
        self.fields["id_station"].choices = [(x[0], x[0]) for x in self.id_stations_mas]


class ChangeStationForm(AddStationForm):
    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop("pk", None)  # Извлекаем pk из аргументов
        super().__init__(*args, **kwargs)

        # Открытие соединения с базой данных и выполнение запросов
        with conn.cursor() as cursor:
            # Запрос для получения информации о конкретном поезде по pk
            cursor.execute("SELECT railway_station_name, city_name FROM railway_stations WHERE id = %s;", (self.pk,))
            self.def_value = cursor.fetchall()

        self.initial["railway_station_name"] = self.def_value[0][0]
        self.initial["city_name"] = self.def_value[0][1]
