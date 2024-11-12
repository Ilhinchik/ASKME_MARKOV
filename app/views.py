from django.http import HttpResponse
from django.shortcuts import render
import copy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

questions = [
    {'id': 0, 
     'title': 'Какой язык программирования самый популярный?',
     'text': 'Привет! Я хочу начать изучать программирование и не могу выбрать язык. Очень часто слышу о Python, особенно в контексте анализа данных и искусственного интеллекта. Но при этом многие говорят, что для разработки веб-приложений лучше использовать JavaScript. Есть ли смысл учить оба этих языка сразу или все-таки выбрать один? Может, стоит обратить внимание на другие языки, такие как Java или C++, если я хочу работать в крупных компаниях или заниматься разработкой ПО с высокой производительностью? Что скажете, какой язык будет лучшим выбором на 2024 год?',
     'tags': ['Python', 'JavaScript', 'Programming'],
     'image': '/static/images/0.webp',
     'answers': [
         "На мой взгляд, Python действительно отличный выбор для начала, особенно если ты хочешь заниматься анализом данных и искусственным интеллектом. Я начал с него и не пожалел. Однако для веб-разработки JavaScript незаменим. Лучше учить их параллельно, потому что оба языка имеют очень разные области применения, и это расширяет твои возможности.",
         "Если ты хочешь работать в крупных компаниях, возможно, стоит также обратить внимание на Java или C++. Эти языки по-прежнему очень востребованы, особенно в разработке ПО с высокой производительностью. Но если тебе интересна разработка на стартапах или с использованием ИИ, Python — отличный старт.",
         "Я бы порекомендовал начать с Python, а потом уже осваивать JavaScript, если хочешь развиваться в веб-разработке. Эти языки прекрасно дополняют друг друга, и ты сможешь применять их в разных областях."
     ]
    }, 

    {'id': 1, 
     'title': 'Как стать веб-разработчиком?', 
     'text': 'Привет, друзья! Я решил стать веб-разработчиком, но с чего начать — не знаю. Задумываюсь, стоит ли начинать с самого основного, типа HTML и CSS, или сразу переходить к изучению JavaScript? И как понять, что именно выбрать — фронтенд или бэкенд? Например, хочется работать с React или Angular, но не знаю, насколько это будет полезно в будущем. Есть ли смысл изучать Python для бэкенда или лучше сразу осваивать что-то вроде Node.js? В общем, как стать хорошим веб-разработчиком и какие технологии наиболее востребованы?',
     'tags': ['Career', 'Web Development', 'Frontend', 'Backend'],
     'image': '/static/images/1.webp',
     'answers': [
         "Лучше начать с HTML и CSS, они — основа веб-разработки. Без этого ты не сможешь нормально работать с JavaScript. После этого смело переходи к JS и фреймворкам вроде React. По поводу бэкенда — на начальном этапе можно попробовать Node.js, он идеально подходит для новичков.",
         "Я бы порекомендовал сначала осваивать фронтенд, особенно JavaScript, и только потом переходить к бэкенду. Для бэкенда можно выбрать Python, если тебе интересен более легкий старт, или же Node.js для тесной интеграции с фронтендом.",
         "Для начала изучи HTML, CSS и основы JavaScript. Затем выбери, хочешь ли ты развиваться в фронтенде или бэкенде. Фреймворки React и Vue очень популярны, но сначала нужно хорошо освоить базовые концепции."
     ]
    },  

    {'id': 2, 
     'title': 'Что такое искусственный интеллект?',
     'text': 'Ребята, мне интересно, что же на самом деле такое искусственный интеллект? Сейчас я много слышу про ИИ, от голосовых помощников типа Siri и Alexa до систем, которые помогают в медицине и финансах. Как же устроены такие системы? Например, есть ли реальная польза от ИИ в повседневной жизни, или это пока что больше теория? Также интересно узнать, как ИИ влияет на рабочие места и экономику, стоит ли бояться его появления в других отраслях? К тому же, насколько сложно освоить технологии машинного обучения и искусственного интеллекта?',
     'tags': ['AI', 'Machine Learning', 'Technology'],
     'image': '/static/images/2.webp',
     'answers': [
         "Искусственный интеллект — это не просто голосовые помощники. Он применяется в медицине, финансах, даже в маркетинге. Реально заметить пользу ИИ в повседневной жизни, особенно в таких вещах, как диагностика заболеваний или помощь в управлении финансами. Но пока что он не заменит людей во всех аспектах.",
         "Искусственный интеллект — это системы, которые способны самостоятельно учиться и принимать решения. В повседневной жизни мы уже сталкиваемся с ИИ в различных формах, например, в системах рекомендаций на платформах как Netflix или Amazon. Да, технологии машинного обучения становятся все доступнее, но они требуют много практики и времени, чтобы освоить."
     ]
    }, 

    {'id': 3, 
     'title': 'Как выбрать лучший хостинг для сайта?',
     'text': 'Друзья, мне нужно выбрать хостинг для своего сайта, и я немного запутался. Существуют разные виды хостинга, но что именно мне нужно? Стоит ли выбирать дешевый общий хостинг, или лучше сразу взять VPS, чтобы потом не было проблем с производительностью? Как понять, какой хостинг подойдет для небольшого сайта, который я собираюсь развивать, и что важно учитывать, чтобы не столкнуться с проблемами в будущем? Например, как выбрать подходящего провайдера с точки зрения безопасности и скорости работы? Буду благодарен за советы!',
     'tags': ['Hosting', 'Web Development', 'Tech'],
     'image': '/static/images/3.webp',
     'answers': [
         "Для начала реши, какой тип хостинга тебе нужен. Если сайт небольшой, можно начать с общего хостинга. Но если у тебя планируется высокая посещаемость или сложные веб-приложения, лучше перейти на VPS. Он дает больше возможностей для настройки и управления сервером.",
         "Для безопасности и скорости лучше выбирать провайдера с хорошей репутацией. Поищи отзывы о них, обязательно убедись, что у них есть SSL-сертификаты и защита от DDoS-атак. Для сайта с хорошей нагрузкой VPS — это минимум, с ним будет проще масштабироваться."
     ]
    }, 

    {'id': 4, 
     'title': 'Что такое блокчейн?',
     'text': 'Привет всем! Все вокруг говорят о блокчейне и криптовалютах, но я до сих пор не понимаю, как работает сама эта технология. Что такое блокчейн? Как он помогает не только в криптовалютах, но и в других сферах, например, в логистике или в управлении данными? Почему блокчейн так привлекателен для стартапов и крупных компаний? И есть ли у него будущее в мире технологий? Стоит ли изучать блокчейн, если я хочу стать специалистом в области технологий? Заранее благодарен за разъяснения!',
     'tags': ['Blockchain', 'Cryptocurrency', 'Technology'],
     'image': '/static/images/4.webp',
     'answers': [
         "Блокчейн — это технология распределенного хранения данных, которая обеспечивает безопасность, прозрачность и неизменность данных. Она используется не только для криптовалют, но и в таких сферах, как логистика, управление данными и даже в голосовании. Стоит изучать, если интересуетесь новыми технологиями.",
         "Если ты хочешь работать в стартапах или в крупных технологических компаниях, изучение блокчейна будет большим плюсом. Это крайне востребованная технология, которая уже находит применение в банковской сфере, здравоохранении и других областях."
     ]
    }, 

    {'id': 5, 
     'title': 'Как работает квантовый компьютер?',
     'text': 'Привет! Недавно я прочитал статью о квантовых компьютерах, и теперь мне стало интересно, как они работают. Чем квантовые компьютеры отличаются от обычных? Как они могут обрабатывать данные быстрее, чем классические компьютеры? И вообще, в каких областях квантовые технологии могут быть полезными? Слышал, что они могут помочь в таких сферах, как криптография и моделирование молекул для медицины. Это реально или пока что всё в стадии теории? Стоит ли в будущем изучать квантовые вычисления, если я хочу работать в передовых технологиях?',
     'tags': ['Quantum Computing', 'Technology', 'Science'],
     'image': '/static/images/5.webp',
     'answers': [
         "Квантовый компьютер работает на основе принципов квантовой механики, что позволяет ему решать задачи, которые невозможно решить на классических компьютерах. Это открывает новые горизонты в таких областях, как криптография и моделирование молекул, что важно для медицины.",
         "Квантовые технологии действительно перспективны, но они пока что в стадии разработки. В будущем они могут значительно ускорить вычисления в науке и бизнесе. Если ты хочешь быть на передовой, это отличная область для изучения."
     ]
    },

    {'id': 6, 
     'title': 'Что такое Python и зачем он нужен?',
     'text': 'Привет! Я слышал, что Python — это один из самых популярных языков программирования, но что в нем такого особенного? Почему многие говорят, что Python лучше всего подходит для анализа данных, искусственного интеллекта и веб-разработки? Что стоит изучить, если я хочу работать с Python, и какие библиотеки наиболее полезны? Я знаю, что Python используется не только в науке и разработке ПО, но и в таких областях, как автоматизация процессов и работа с большими данными. Насколько мне будет полезно изучать Python в 2024 году, если я только начинаю?',
     'tags': ['Python', 'Programming', 'Web Development'],
     'image': '/static/images/6.webp',
     'answers': [
         "Python очень популярен из-за своей простоты и гибкости. Он идеально подходит для быстрого прототипирования и для решения различных задач, таких как анализ данных, ИИ, веб-разработка. Если ты начинаешь, изучи библиотеки, такие как NumPy, pandas, Flask или Django.",
         "Да, Python продолжает оставаться востребованным и в 2024 году. Особенно в области науки о данных, искусственного интеллекта и автоматизации. С его помощью ты можешь легко интегрировать решение для многих задач и сэкономить время на разработку."
     ]
    },

    {'id': 7, 
     'title': 'Какие основы нужно знать для разработки на JavaScript?',
     'text': 'Привет! Я начинаю изучать JavaScript и думаю, с чего стоит начать. Нужно ли сразу углубляться в фреймворки типа React или Vue, или стоит сначала освоить базовые принципы, такие как работа с DOM, событиями и функциями? В чем вообще состоит основное отличие фронтенд-разработки на JavaScript от других технологий? Может, стоит параллельно учить какой-то язык для серверной части, чтобы стать full-stack разработчиком? Какие практические навыки мне нужно развивать, чтобы стать уверенным разработчиком на JavaScript?',
     'tags': ['JavaScript', 'Web Development', 'Frontend'],
     'image': '/static/images/7.png',
     'answers': [
         "Начни с основ — DOM, функций, событий и базовых операторов. Не спеши переходить к фреймворкам, пока не разберешься в базовых концепциях JavaScript. Это поможет тебе понять, как работают такие фреймворки, как React и Vue.",
         "Для того чтобы стать уверенным разработчиком на JavaScript, важно также освоить асинхронное программирование, работать с API и научиться использовать инструменты разработки браузера. Это необходимые навыки для работы как с фронтендом, так и с бэкендом."
     ]
    },

    {'id': 8, 
     'title': 'Как повысить производительность работы с базами данных?',
     'text': 'Привет! У меня небольшой проект с базой данных, и я заметил, что с увеличением количества пользователей и запросов она начала работать медленно. Что можно сделать, чтобы улучшить производительность? Какие методы оптимизации баз данных вы используете? Например, стоит ли использовать индексацию и нормализацию, или нужно еще что-то сделать, чтобы улучшить отклик базы данных? Какие подходы к проектированию базы данных могут помочь в улучшении производительности, особенно в условиях масштабируемых приложений? Буду рад услышать советы!',
     'tags': ['Databases', 'SQL', 'Performance'],
     'image': '/static/images/8.webp',
     'answers': [
         "Использование индексации и нормализации — это хорошее начало для улучшения производительности. Также стоит оптимизировать запросы, чтобы они выполнялись быстрее, и использовать кэширование для часто запрашиваемых данных.",
         "Не забывай о шардинге и репликации. Эти методы особенно полезны для масштабируемых приложений, так как они помогают равномерно распределять нагрузку и повышать отказоустойчивость базы данных."
     ]
    },

    {'id': 9, 
     'title': 'Что такое микросервисы и как их использовать?',
     'text': 'Привет всем! Я слышал много о микросервисах, но пока не понимаю, почему они стали такими популярными. В чем плюсы архитектуры микросервисов? Почему она лучше подходит для крупных проектов, чем монолитная архитектура? Как организовать взаимодействие между микросервисами, и какие инструменты для этого использовать? Задумываюсь, стоит ли переходить на микросервисную архитектуру для моего проекта, или это слишком сложное решение для стартапа. Кто-нибудь может поделиться опытом внедрения микросервисов в реальные проекты?',
     'tags': ['Microservices', 'Software Architecture', 'Backend'],
     'image': '/static/images/0.webp',
     'answers': [
         "Микросервисы позволяют разделить сложные системы на независимые части, которые можно разрабатывать, развертывать и масштабировать отдельно. Это очень удобно для крупных проектов, так как повышает гибкость и упрощает тестирование.",
         "Если ты работаешь над стартапом, переход на микросервисы может быть слишком сложным. Лучше начать с монолитной архитектуры и только потом переходить к микросервисам, когда система станет более сложной."
     ]
    }
]


def index(request):
    page = pag(request, questions)
    context={'questions': page.object_list, 'page_obj': page}
    return render(request, 'index.html', context)

def hot(request):
    hot_questions = copy.deepcopy(questions)
    hot_questions.reverse()
    page = pag(request, hot_questions)

    context={'questions': page.object_list,'page_obj': page}
    return render(request, 'hot.html', context)

def question(request, question_id):
    question = questions[question_id]

    context = {'question': question, 'is_question_page': True}
    return render(request, 'question.html', context)


def tag(request, tag_title):
    questions_tag = search_tag(tag_title)
    page = pag(request, questions_tag)

    context={'questions': page.object_list, 'page_obj': page, 'is_tag_page': True, 'tag_title': tag_title}
    return render(request, 'tagpage.html', context)


def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def ask(request):
    return render(request, 'newquestion.html')

def setting(request):
    return render(request, 'setting.html')


def pag(request, q):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(q, 3)

    try:
        page = paginator.page(page_num)

    except PageNotAnInteger:
        page = paginator.page(1)

    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page

def search_tag(tag_title):
    questions_tag = []
    for question in questions:
        for tag in question.get('tags', []):
            if tag_title.lower() == tag.lower():
                questions_tag.append(question)
    
    return questions_tag