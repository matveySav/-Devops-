# Облачная теория 
## Рубежка 1, вариант 1
### Вопрос 

Зачем в облаке предусмотрено столько регионов? Зачем там кроме регионов еще и зоны?

### Ответ

Облако разделено на географически отделенные друг от друга зоны, называемые регионами, которые в свою очередь разделены на зоны доступности, состоящие из 1 и более датацентров, каждый со своей внутренней сетью и источником питания. Количество и расположение регионов обусловлено тем, чтобы минимизировать время на ожидание выполнения запросов как можно большему числу клиентов. Зоны доступности в свою очередь предлагают приложениям и сервисам, которые хостятся в облаке клиентами облачного провайдера, ряд преимуществ:

#### **Устойчивость к ошибкам и высокая доступность** 

Сами по себе датацентры в 1-й зоне доступности не зависят друг от друга, в то же время они являются довольно надежными, гарантируя, что около % близкого к 100% от всего рабочего времени будут функционировать, и в случае маловероятного сбоя в одном датацентре другой из той же зоны доступности может взять на себя его сервисы, таким образом приложение клиентов останется доступным для пользователей даже при отказе 1 датацентра, а вероятность того, что их приложение будет не доступно равно вероятности отказа всех датацентров в зоне доступности, то есть это (Близкий к 0%)^n, где n - число датацентров в зоне доступности, поскольку они функционируют независимо друг от друга. Таким образом, клиентам облачного провайдера гарантируется, что время, когда их приложение или сервисы будут доступны, будет составлять 99,99...% и много девяток, что по определению высокая доступность.

#### **Масштабируемость** 

Из-за того, что датацентры связаны между собой сетью с высокой проводимостью и низкой задержкой, то при масштабируемости сервиса, который изначально хостился в одном датацентре, могут быть задействованы ресурсы других датацентров из зоны доступа. Это обеспечивает возможности к масштабируемости, которые 1 датацентр физически не мог бы себе позволить.

**Итак**, облако разделено на регионы и зоны доступности внутри них для максимизации скорости передачи данных и минимизации времени ожидания и сбоев для клиентов облачных провайдеров и пользователей продуктов этих клиентов.

---

## Рубежка 2, вариант 1
### Вопрос 

Апрель 2020 года, ваша команда выиграла дорогостоящий тендер на разработку системы пропусков во время карантина. Предложите сервисы в облаке, которые могло бы использовать такое приложение. Можно на конкретных примерах провайдеров (AWS, Azure, Google, Yandex, Mail.RU).

### Ответ

Для наглядности возьмем Azure в качестве облачного провайдера.

#### Azure SQL Database
Для системы пропусков во время карантина нам, очевидно, понадобиться база данных для хранения информации о людях, которые сделали привику, чтобы присвоить им какой-то уникальный пропуск. Допустим, мы выбрали в качестве СУБД Microsoft SQL server, тогда нам подойдет сервис **Azure SQL Database**, который предоставляет PaaS Microsoft SQL server, с высокой доступностью, устойчивостью и масштабируемостью.

#### Azure App Service
Также, нам надо, чтобы пользователи могли самостоятельно получить свой пропуск, для этого нам понадобиться веб-приложение, откуда пользователи смогут доставать свой пропуск. Для этого подойдет **Azure App Service**, сервис для хостинга веб-приложений, который предлагает множество языков / фреймворков для разработки, возможность работы с контейнерами внутри App Service, безопасность и масштабируемость.

#### Azure Blob Storage
Нам может понадобиться хранилище картинок, видео, другой неструктурированных данных для нашего веб-приложения / сайта. Для этого подойдет **Azure Blob Storage** - объектное хранилище в облаке в исполнении Microsoft.

#### Azure Application Gateway
Поскольку мы разрабатываем систему на целое государство, ожидается, что трафик нашего сайта будет большим, поэтому будем пользоваться балансировщиком нагрузки, сервисом **Azure Applicaton Gateway**, таким образом будем пытаться не перегружать нашу систему, оптимально распределяя нагрузку.

#### Azure Content Delivery Network
Ввиду того фактора, что Россия большая страна (И то, что датацентры Azure не находятся в России), имеет смысл использовать **Azure CDN**, для ускорения передачи данных до пользователей, через промежуточные датацентры.

#### Azure API Management
Опять же, поскольку наша система охватывает целое гос-во, было бы удобно если бы она была интегрирована в, скажем, госуслуги, тогда люди смогут получать свои пропуска без нашего веб-приложения. Для этого разработаем API, который будет хоститься на специально для этого спроектированном сервере сервиса **Azure API Management**.

**Итак**, у нас получится разработать систему пропусков во время карантина, облачные сервисы которой взяты у Azure.
