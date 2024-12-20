# Лабораторная 3 * (со звездочкой)

## Задание
Сделать красиво работу с секретами. Например, поднять Hashicorp Vault (или другую секретохранилку) и сделать так, чтобы ci/cd пайплайн (или любой другой ваш сервис) ходил туда, брал секрет, использовал его не светя в логах. 
В Readme аргументировать почему ваш способ красивый, а также описать, почему хранение секретов в CI/CD переменных репозитория не является хорошей практикой.

## Выбор ПО для управления секретами

Выбор пал на `Doppler`, поскольку он прост в освоении и работает в РФ (только зарегаться надо с впн).

## Ход работы

Сначала создадим аккаунт в Doppler, создадим в нем проект (окружение `CI_CD` с конфигом `cd`), добавим в конфиг 2 секрета `DOCKER_HUB_NAME` и `DOCKER_HUB_TOKEN` (для контекста: в 3 лабе мой CI/CD пайплан заключался в том, что скрипт на питоне проходит пару тестов на раннере и при успешном прохождении с ним создается образ контейнера, который загружается в докер хаб).

![image](https://github.com/user-attachments/assets/7623ad84-126d-45f4-8926-c5e2ad14d872)
![image](https://github.com/user-attachments/assets/f72bff27-3e9f-4f76-a0ff-2b8c3f7d98ed)

Теперь, чтобы получить доступ в этим секретам нам нужен `service token` допплера, который даст нам доступ к конфигу `cd`, генерируем:

![image](https://github.com/user-attachments/assets/bea60469-101c-4ffe-bc5d-8936d6ee8358)

Создаем секрет с этим токеном в репозитории

![image](https://github.com/user-attachments/assets/869a9939-5b6e-4969-903d-59966ecf4ae2)

Осталось только немного изменить yaml файл пайплайна. (Здесть только 2-я джоба, т.к. 1-я без изменений)

```
  Build-deploy:
    needs: Test
    runs-on: ubuntu-22.04
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      - name: Install Doppler CLI
        uses: dopplerhq/cli-action@v3
      - name: Accessing Doppler secrets
        run: |
          echo ${{ secrets.DOPPLER_TOKEN }} | doppler configure set token --scope /
          echo "DOCKER_HUB_NAME=$(doppler secrets get DOCKER_HUB_NAME --plain)" >> $GITHUB_ENV
          echo "DOCKER_HUB_TOKEN=$(doppler secrets get DOCKER_HUB_TOKEN --plain)" >> $GITHUB_ENV
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ env.DOCKER_HUB_NAME }}
          password: ${{ env.DOCKER_HUB_TOKEN }}
      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          push: true
          tags: ${{ env.DOCKER_HUB_NAME }}/my_app:latest
```

Что изменили: здесь мы с помощью action ставим допплер на раннер, логинимся через токен допплера и секреты из допплера переносим в переменные окружения раннера, используем их чтобы запушить образ со скриптом.

![image](https://github.com/user-attachments/assets/546e7048-8ae6-4ff2-9f8c-7f43a8ad2ccf)

Как видим, пайплайн успешно отработал и образ успешно запушился

![image](https://github.com/user-attachments/assets/27a65dc9-3dd5-43ed-868f-c75fc30c7ba1)

## Аргументы
### Почему способ красивый?
Максимально понятный и простой интерфейс Doppler'a, понятная документация Doppler CLI. Создаем в допплере секреты и токен, в yaml файле дописываем несколько строчек и добавляем один секрет в репозиторий, ctrl+c -> ctrl+v несколько раз - всё.

### Почему хранения секретов в репозитории - плохая практика?
Малая гибкость, нельзя как-то разделить по ролям, окружениям, все в одной куче + если кто-то получить доступ к репозиторию, то сможет через workflow файл получить все чувствительные данные, а если мы используем секретохранилку, то это дополнительный слой безопасности. Если проект небольшой и безопасность не особо волнует, то может быть гитхаю секретов хватит, но если проект большой с кучей секретов, то какая бы то ни было секретохранилка предложит лучшее, централизованное решение.

## Итог

В результате выполнения лабы 3*, пайплайн из лабы 3 был модернизирован, чтобы принимать секреты из Doppler.
