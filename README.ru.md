<a id="readme-top"></a>

[![Форки][forks-shield]][forks-url]
[![Звёзды][stars-shield]][stars-url]
[![Задачи][issues-shield]][issues-url]
[![Лицензия MIT][license-shield]][license-url]



<!-- ЗАГОЛОВОК ПРОЕКТА -->
<br />
<div align="center">
  <h3 align="center">greenfish-webtools-mcp</h3>

  <p align="center">
    Лёгкий MCP-сервер, который даёт ИИ-ассистентам актуальный веб-поиск и чтение страниц — без API-ключей.
  </p>
</div>



<!-- ОГЛАВЛЕНИЕ -->
<details>
  <summary>Оглавление</summary>
  <ol>
    <li><a href="#о-проекте">О проекте</a></li>
    <li><a href="#стек">Стек</a></li>
    <li><a href="#начало-работы">Начало работы</a></li>
    <li><a href="#использование">Использование</a></li>
    <li><a href="#дорожная-карта">Дорожная карта</a></li>
    <li><a href="#участие-в-разработке">Участие в разработке</a></li>
    <li><a href="#лицензия">Лицензия</a></li>
    <li><a href="#контакты">Контакты</a></li>
    <li><a href="#благодарности">Благодарности</a></li>
  </ol>
</details>



<!-- О ПРОЕКТЕ -->
## О проекте

greenfish-webtools-mcp — это сервер [Model Context Protocol](https://modelcontextprotocol.io), который открывает ИИ-ассистентам доступ к живому интернету. Он предоставляет два инструмента: **веб-поиск** и **извлечение содержимого страницы**.

Ключевое архитектурное решение: сервер не обращается ни к каким проприетарным поисковым API. Вместо этого он делегирует всю работу вашему собственному экземпляру [SearXNG](https://github.com/searxng/searxng) — самохостируемому, активно развивающемуся мета-поисковику, который агрегирует результаты из нескольких поисковых систем и предоставляет стабильный JSON API, который не исчезнет в один день и не сменит условия использования. Вы запускаете SearXNG, этот сервер подключается к нему и передаёт результаты модели.

`greenfish_websearch` отправляет запрос в SearXNG и возвращает ранжированный, дедуплицированный список результатов. `greenfish_fetch_url` скачивает конкретную страницу и возвращает её основной читаемый текст, очищенный от навигации, рекламы и шаблонного мусора с помощью [trafilatura](https://github.com/adbar/trafilatura).

<p align="right">(<a href="#readme-top">наверх</a>)</p>



<!-- СТЕК -->
## Стек

[![Python][Python-shield]][Python-url]
[![SearXNG][SearXNG-shield]][SearXNG-url]
[![uv][uv-shield]][uv-url]

<p align="right">(<a href="#readme-top">наверх</a>)</p>



<!-- НАЧАЛО РАБОТЫ -->
## Начало работы

Прежде всего убедитесь, что на вашей машине установлены **Python 3.10+** и **[uv](https://github.com/astral-sh/uv)**. Также потребуется работающий экземпляр SearXNG с включённым JSON-выводом. Самый быстрый способ его поднять — через Docker:

```sh
docker run -d --name searxng -p 1818:8080 searxng/searxng
```

После этого откройте интерфейс SearXNG, перейдите в **Настройки → Общие** и включите `json` как формат вывода. Либо найдите `settings.yml` внутри контейнера, добавьте `json` в список `search.formats` и перезапустите контейнер.

Теперь клонируйте этот репозиторий и установите зависимости:

```sh
git clone https://github.com/DumbGreenFish/GreenFishWebtoolsMCP.git
cd greenfish-webtools-mcp
uv sync
```

На этом всё. Никаких API-ключей и регистраций.

<p align="right">(<a href="#readme-top">наверх</a>)</p>



<!-- ИСПОЛЬЗОВАНИЕ -->
## Использование

Зарегистрируйте сервер в конфигурационном файле вашего MCP-клиента. Пример ниже подходит для Claude Desktop и большинства других клиентов, принимающих стандартный JSON-формат:

```json
{
  "mcpServers": {
    "greenfish-webtools": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/greenfish-webtools-mcp",
        "run",
        "app.py"
      ],
      "env": {
        "SEARXNG_URL": "http://127.0.0.1:1818/search"
      }
    }
  }
}
```

Замените `/path/to/greenfish-webtools-mcp` на реальный путь к склонированному репозиторию на вашей машине, а `SEARXNG_URL` скорректируйте под адрес, по которому работает ваш SearXNG. После запуска MCP-сервера ИИ-ассистент автоматически получит доступ к инструментам `greenfish_websearch` и `greenfish_fetch_url`.

<p align="right">(<a href="#readme-top">наверх</a>)</p>



<!-- ДОРОЖНАЯ КАРТА -->
## Дорожная карта

- [ ] Поддержка дополнительных параметров SearXNG (временной диапазон, категории поиска)
- [ ] Настраиваемая стратегия ранжирования и дедупликации результатов
- [ ] Документация на нескольких языках

Полный список предложенных функций и известных проблем — в [открытых задачах](DumbGreenFish/GreenFishWebtoolsMCP/issues).

<p align="right">(<a href="#readme-top">наверх</a>)</p>



<!-- УЧАСТИЕ В РАЗРАБОТКЕ -->
## Участие в разработке

Вклад сообщества делает open source таким вдохновляющим местом для обучения и творчества. Любой ваш вклад **очень ценится**.

Если у вас есть идея по улучшению — сделайте форк репозитория и откройте pull request. Можно также просто открыть задачу с тегом "enhancement". И не забудьте поставить звезду проекту — спасибо!

<p align="right">(<a href="#readme-top">наверх</a>)</p>



<!-- ЛИЦЕНЗИЯ -->
## Лицензия

Распространяется под лицензией GNU GPLv3. Подробнее — в файле `LICENSE`.

<p align="right">(<a href="#readme-top">наверх</a>)</p>



<!-- КОНТАКТЫ -->
## Контакты

Ссылка на проект: [https://github.com/DumbGreenFish/GreenFishWebtoolsMCP](DumbGreenFish/GreenFishWebtoolsMCP)

<p align="right">(<a href="#readme-top">наверх</a>)</p>



<!-- БЛАГОДАРНОСТИ -->
## Благодарности

Этот проект не существовал бы без [SearXNG](https://github.com/searxng/searxng), который выполняет всю реальную поисковую работу. Отдельная благодарность авторам [FastMCP](https://github.com/jlowin/fastmcp), [trafilatura](https://github.com/adbar/trafilatura) и [httpx](https://github.com/encode/httpx).

<p align="right">(<a href="#readme-top">наверх</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
[forks-shield]: https://img.shields.io/github/forks/DumbGreenFish/GreenFishWebtoolsMCP.svg?style=for-the-badge
[forks-url]: DumbGreenFish/GreenFishWebtoolsMCP/network/members
[stars-shield]: https://img.shields.io/github/stars/DumbGreenFish/GreenFishWebtoolsMCP.svg?style=for-the-badge
[stars-url]: DumbGreenFish/GreenFishWebtoolsMCP/stargazers
[issues-shield]: https://img.shields.io/github/issues/DumbGreenFish/GreenFishWebtoolsMCP.svg?style=for-the-badge
[issues-url]: DumbGreenFish/GreenFishWebtoolsMCP/issues
[license-shield]: https://img.shields.io/github/license/DumbGreenFish/GreenFishWebtoolsMCP.svg?style=for-the-badge
[license-url]: DumbGreenFish/GreenFishWebtoolsMCP/blob/master/LICENSE
[Python-shield]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[SearXNG-shield]: https://img.shields.io/badge/SearXNG-3050B0?style=for-the-badge
[SearXNG-url]: https://github.com/searxng/searxng
[uv-shield]: https://img.shields.io/badge/uv-DE5FE9?style=for-the-badge
[uv-url]: https://github.com/astral-sh/uv
