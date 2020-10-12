# testtasks

Админка: http://{host}/admin/  
  
Авторизация (POST): http://{host}/api/token/  
Обновление токена (POST): http://{host}/api/token/refresh/  
Инструкция по авторазации: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html#usage
  
Получение списка (GET)/Создание (POST) задач: http://{host}/api/task/  
Обновление задачи (Patch): http://{host}/api/task/{task_id}/  

Формат задачи:  
{  
    "id": 1,  
    "title": "First task",  
    "description": "First task",  
    "executor": 2,  
    "observers": [
        1,
        3
    ],  
    "status": 0,  
    "start_timestamp": null,  
    "completion_timestamp": null
    "planned_completion_timestamp": "2020-10-12T23:00:00Z",  
    "items": [  
        {
            "id": 1,
            "order": 0,
            "name": "Сделать одно",
            "is_completed": false
        },  
        {
            "id": 2,
            "order": 1,
            "name": "Сделать другое",
            "is_completed": false
        }  
    ]  
}

Где:  
  "id" - ID задачи  
  "title" - Заголовок задачи  
  "description" - Описание задачи  
  "executor" - ID исполнителя  
  "observers" - Список ID наблюдателей  
  "status" - Статус задачи  
  "start_timestamp" - Время начала    
  "completion_timestamp" - Время завершения  
  "planned_completion_timestamp" - Планируемое время завершения  
  "items" - Чек-лист  
  
