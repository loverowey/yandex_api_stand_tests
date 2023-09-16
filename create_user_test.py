import sender_stand_request
import data

def get_user_body(first_name):
    # копирование словаря с телом запроса из файла data, чтобы не потерять данные в исходном словаре
    current_body = data.user_body.copy()
    # изменение значения в поле firstName
    current_body["firstName"] = first_name
    # возвращается новый словарь с нужным значением firstName
    return current_body

def test_create_user_2_letter_in_first_name_get_success_response():
    # В переменную user_body сохраняется обновленное тело запроса с именем “Аа”
    user_body = get_user_body("Аа")
    # В переменную user_response сохраняется результат запроса на создание пользователя
    user_response = sender_stand_request.post_new_user(user_body)

    # Проверяется, что код ответа равен 201
    assert user_response.status_code == 201
    # Проверяется, что в ответе есть поле authToken, и оно не пустое
    assert user_response.json()["authToken"] != ""

    # В переменную users_table_response сохраняется результат запрос на получение данных из таблицы user_model
    users_table_response = sender_stand_request.get_users_table()
    # Строка, которая должна быть в ответе запроса на получение данных из таблицы users
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    # Проверка, что такой пользователь есть, и он единственный
    assert users_table_response.text.count(str_user) == 1

def test_create_user_15_letter_in_first_name_get_success_response():
    # В переменную user_body сохраняется обновленное тело запроса с именем “Ааааааааааааааа”
    user_body = get_user_body("Ааааааааааааааа")
    # В переменную user_response сохраняется результат запроса на создание пользователя
    user_response = sender_stand_request.post_new_user(user_body)

    # Проверяется, что код ответа равен 201
    assert user_response.status_code == 201
    # Проверяется, что в ответе есть поле authToken, и оно не пустое
    assert user_response.json()["authToken"] != ""

    # В переменную users_table_response сохраняется результат запрос на получение данных из таблицы user_model
    users_table_response = sender_stand_request.get_users_table()
    # Строка, которая должна быть в ответе запроса на получение данных из таблицы users
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
                   + user_body["address"] + ",,," + user_response.json()["authToken"]

    # Проверка, что такой пользователь есть, и он единственный
    assert users_table_response.text.count(str_user) == 1

def test_negative_assert_symbol_1_letter():
    user_body = get_user_body("А")
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400
    assert user_response.json()["message"] == "Имя пользователя введено некорректно. " \
                                         "Имя может содержать только русские или латинские буквы, " \
                                         "длина должна быть не менее 2 и не более 15 символов"

def test_negative_assert_symbol_16_letter():
    user_body = get_user_body("Аааааааааааааааа")
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400
    assert user_response.json()["message"] == "Имя пользователя введено некорректно. " \
                                         "Имя может содержать только русские или латинские буквы, " \
                                         "длина должна быть не менее 2 и не более 15 символов"

def test_create_user_eng_letter_in_first_name_get_success_response():
    user_body = get_user_body("QWErty")
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""
    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]
    assert users_table_response.text.count(str_user) == 1

def test_create_user_rus_letter_in_first_name_get_success_response():
    user_body = get_user_body("Мария")
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""
    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]
    assert users_table_response.text.count(str_user) == 1

def test_negative_assert_symbol_space_letter():
    user_body = get_user_body("Человек и Ко")
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400
    assert user_response.json()["message"] == "Имя пользователя введено некорректно. " \
                                         "Имя может содержать только русские или латинские буквы, " \
                                         "длина должна быть не менее 2 и не более 15 символов"

def test_negative_assert_symbol_special_letter():
    user_body = get_user_body("№%@")
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400
    assert user_response.json()["message"] == "Имя пользователя введено некорректно. " \
                                         "Имя может содержать только русские или латинские буквы, " \
                                         "длина должна быть не менее 2 и не более 15 символов"

def test_negative_assert_symbol_numb_letter():
    user_body = get_user_body("123")
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400
    assert user_response.json()["message"] == "Имя пользователя введено некорректно. " \
                                         "Имя может содержать только русские или латинские буквы, " \
                                         "длина должна быть не менее 2 и не более 15 символов"

def test_negative_assert_symbol_no_first_name_letter():
    user_body = data.user_body.copy()
    user_body.pop("firstName")
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400
    assert user_response.json()["message"] == "Не все необходимые параметры были переданы"

def test_negative_assert_symbol_not_letter():
    user_body = get_user_body("")
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400
    assert user_response.json()["message"] == "Не все необходимые параметры были переданы"

def test_negative_assert_symbol_wrongParam_letter():
    user_body = get_user_body(12)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400