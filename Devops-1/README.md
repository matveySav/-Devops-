# 1 Лаба по DevOps 
Для начала устанавливаем nginx по [инструкции](http://nginx.org/en/linux_packages.html#Ubuntu) (я сижу на Ubuntu). После установки при необходимости запускаем nginx командой 
```
sudo systemctl nginx start
```

В качестве проектов, между которыми будет настраиваться навигация возьму 2 стандартных html странички `index1.html` и `index2.html`, я расположил их по адресу `/var/lab1_devops` у себя на локальной машине. Чтобы они были доступны по https нам понадобиться протокол ssl, можно самому сгенерировать с помщью команды (надо установить openssl при необходимости)
```
openssl req -newkey rsa:4096 \
            -x509 \
            -sha256 \
            -days 3650 \
            -nodes \
            -out example.crt \
            -keyout example.key
```
В результате выполнения команды в текущей директории появятся файлы `example.crt` и `example.key` - сертификат и приватный ключ соответсвенно. В команде мы также указываем, что <br />
`-newkey rsa:4096` - создает новый ключ с RSA шифрованием длиной 4096 бит<br />
`-x509` - стандарт сертификата<br />
`-sha256` - алгоритм хэширования<br />
`-days 3650 ` - срок действия сертификата<br />
`-out example.crt` - указание имени созданного сертификата<br /> 
`-keyout example.key`- указание имени созданного приватного ключа<br /> 

Теперь мы должны создать конфигурационные файлы для наших сайтов(хорошая практика под каждый сайт писать свой конфиг). Для этого по адресу `/etc/nginx/conf.d/` создадим `test1.conf` и `test2.conf`. В них добавим ![image](https://github.com/user-attachments/assets/0876b219-7556-4364-9693-60f675b307b6) ![image](https://github.com/user-attachments/assets/b3bdac42-0c32-4a8c-ba98-dce405f16a18) <br/>
В них мы указываем, что слушаем порт 443, расположение ssl созданного сертификата и ключа, название сервера(понадобиться при создании виртуальный хостов, чтобы можно были иметь несколько доменных имен на лок. машине), и, конечно же, директорию html'ками. index указывает на файл, который будет открываться если конкретный путь до файла не указан. <br/>
Настроим виртуальные хосты на локальной машине. Поскольку в моей конфигурации nginx виртуальные хосты активируются без `sites-enabled`, а берутся из папки `/etc/nginx/conf.d/`, то остается только добавить названия хостов в `/etc/hosts`, чтобы протестить локально
```
127.0.0.1 example1
127.0.0.1 example2
```
Осталось настроить перенаправление HTTP запросов на HTTPS, для этого в блок http файла `/etc/nginx/nginx.conf` добавим 
```
server {
		listen 80 default_server;
		server_name _;
		return 301 https://$host$request_uri;
	}

```

Который означает, что весь трафик HTTP (порт 80), с любым именем хоста (`server_name _`), (301 - означает постоянное перенаправление),`https://$host$request_uri` - означает тот же адрес, но уже с `https://`.<br/>
Кстати, не забываем, что после каждого изменения конфигов нужно ввести `sudo nginx -s reload`, чтобы nginx перезагрузил конфиги.
Теперь введя в браузере `example1/` и `example2/` получим соответсвенно![image](https://github.com/user-attachments/assets/9071f365-6388-4440-aea8-90cb3c1dd86c) <br/> и <br/> ![image](https://github.com/user-attachments/assets/4547744e-22ed-4750-a96d-7dde978522a1). <br/>
Победа, у нас есть два виртуальных хоста доступных по HTTPS с автоматическим перенаправлением с HTTP. Добавим например картинку `1.jpg` по пути `/etc/lab1_devops_images/`, т.к. эта папка находится на том же уровне, что и root для наших сайтов, то используем `alias`, чтобы картинка была доступна с сайта `example2`. Для этого переходим в его конфиг и добавляем 
```
location /images/ {
		alias /var/lab1_devops_images/;
	}
```
Делаем `sudo nginx -s reload`. Теперь мы можем увидеть его в браузере по адресу `https://example2/images/1.jpg` ![image](https://github.com/user-attachments/assets/8161eb4c-23d7-435b-ad57-76662a158f7c)

В качестве еще одной интересной штуки мы можем запустить локально простецкое приложение на flask (`app1.py`) на 5000 порту и настроить перенаправление на него, например, с адреса `https://example1/app1/`,  для этого добавим в конфиг первого сайта 
```
	location /app1/ {
		proxy_pass http://127.0.0.1:5000/;
	}
```
Делаем `sudo nginx -s reload`. И проверяем, предварительно запусти flask приложение на нужном порту ![image](https://github.com/user-attachments/assets/aada2f91-72d6-4491-9a59-09a598662f03)

# ИТОГО
Были выполнены все пунктики первой лабораторной, в качестве проектов были использованы обычные html странички с картинкой и простейшее web-приложение на flask. Все упомянутые,или измененные мной файлы в данной директории.