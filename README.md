# Дополнительная информация которую вы захотите указать
1. Так как поля *from* и *to* в django сделать нельзя
(`from` - ключевое слово), то мне пришлось сменить их на *timeFrom* и *timeTo*
2. Так как django нормально мигрировать не умеет, я заставляю
его делать это при запуске, так что микросервис аккаунтов
запускается по 20-40сек
3. Если вы видите `[{"name": str}, ...]` для ролей или названий комнат в больнице,
знайте, что на самом деле надо указывать данные в формате `["name1", "name2", 
"name3", ...]` и сериализатор swagger просто нагло врёт (чтобы сделать, как в
задании, пришлось извернуться)
4. Если мы ищем объекты по ForeignKey (например, Timetable по больнице) и 
родительской сущности (больницы) в БД нет, 
# Основное задание:
1. Account URL: http://localhost:8081/ui-swagger
2. Hospital URL: http://localhost:8082/ui-swagger
3. Timetable URL: http://localhost:8083/ui-swagger
4. Document URL: http://localhost:8084/ui-swagger
# Дополнительное задание:
1. ElasticSearch URL: http://elasticsearch-service/  # TODO: elastic
2. Kibana URL: http://kibana-service/  # TODO: kibana
# Запуск
`docker-compose up -d --build`