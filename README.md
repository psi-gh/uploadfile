Скрипты для реализации возможности загрузки файлов на сервер и генерации превью изображений

#I. Файлы:
getpreview.wsgi - скрипт вызывается, чтобы сгенерировать превью. само превью генерирует previewclass
sendfile.wsgi - скрипт вызывается для загрузки файла на сервер в папку Storage
clear.py - очищает Storage и Previews. Вызывается через crontab
previewclass.py - генератор превью. создает превью с указанными размерами в папке Previews. Для каждой картинки каждого размера своё уникальное имя (хэш md5). МД5 вместо простого именования файла-превью по URI этого файла был выбран, чтобы не заморачиваться с экранированием символов, ну и чтобы избавиться от слишком длинных имен.

#II. Установка:
1. Установить Apache и mod_wsgi. 
sudo apt-get install apache2 libapache2-mod-wsgi
2. Создать в папке с сайтами папку uploadfile, а в ней wsgi.  (например, скрипты будут располагаться в /var/www/uploadfile/wsgi/)
3. В sites-available должно быть прописано следующее
WSGIScriptAlias /sendfile /var/www/uploadfile/wsgi/sendfile.wsgi
WSGIScriptAlias /getpreview /var/www/uploadfile/wsgi/getpreview.wsgi
Тогда обращение будет к примеру таким: %%sever_name%%/sendfile 
4. В папке с данными wsgi-скриптами создать папки Storage и Previews, а затем разрешить их изменение, например:
sudo chmod 777 Previews/
sudo chmod 777 Storage/
5. Cоздать лог-файл для previewclass по пути '/var/log/preview.log' и также выдать на него разрешения на запись.
6. Установить: python-httplib2 python-imaging python-imaging-tk

#III. Использование:
Загрузка файла:
Стандартный POST запрос с файлом на http://%%server_name%%/sendfile?to=JID_TO_SEND
вместо JID_TO_SEND должен передаваться jid контакта, которому кидается файл. Нужен, чтобы возвратить правильный javascript-код, который выполнится как callback в Neiron Talk. Аргументами функции в этом JS коде будет адрес файла и JID.
Работает только через PhoneGap! Чтобы тестировать через браузер, надо добавить теги &lt;script>, обрамляющие возвращаемый JS код (переменная output в sendfile.wsgi), но тогда не будет работать через PhoneGap.

# Получение превью:
Сделать запрос на 
http://webgranula.dyndns.org:82/getpreview?x=SIZE_X&y=SIZE_Y&addr=LINK
возвратится изображение. LINK - ссылка на изображение, на которое должно быть сделано превью. Должно быть url-закодировано. Ссылку поместить прямо в тег <img src="LINK_TO_PREVIEW">
Предпологается, что LINK является валидной ссылкой на изображение.
Пример:
<img src="http://webgranula.dyndns.org:82/getpreview?x=200&y=100&addr=http%3A%2F%2Fwebgranula.dyndns.org%3A82%2Fuploadfile%2Fwsgi%2FStorage%2FQgBmmQxG%2F1323298110728.jpg">

# Запуск очистки по расписанию:
$ sudo crontab -u root -e
Добавить строку с нужными настройками, например
1 * * * * python /var/www/uploadfile/wsgi/clear.py
Будет вызываться каждый час. Удаляет файлы и превью старше 1 дня.


Чтобы не забыть:
Если убирать парс по расширению со стороны talk, то в случае файла без расшринения в previewclass может произойти ошибка при сохранении im.save
