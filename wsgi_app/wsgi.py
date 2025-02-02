# from urllib.parse import parse_qs

# def simple_app(environ, start_response):

#     method = environ['REQUEST_METHOD']
#     params = ""

#     if method == "GET":
#         query_params = parse_qs(environ.get('QUERY_STRING', ''))

#     status = '200 OK'
#     print("WSGI Environ:", environ)


#     print("Query Params:", query_params)

#     try:
#         content_length = int(environ.get('CONTENT_LENGTH', 0))
#     except (ValueError, TypeError):
#         content_length = 0

#     body = environ['wsgi.input'].read(content_length)
#     post_params = parse_qs(body.decode())
#     print("Parsed Body:", post_params)

#     response_headers = [('Content-type', 'text/plain')]
#     start_response(status, response_headers)
#     return [HELLO_WORLD]

from urllib.parse import parse_qs


def simple_app(environ, start_response):
    """
    Простое WSGI-приложение для обработки параметров GET и POST запросов
    """
    method = environ['REQUEST_METHOD']

    query_string = environ.get('QUERY_STRING', '')
    url_params = parse_qs(query_string)

    body_params = {}

    if method == "POST":
        try:
            content_length = int(environ.get('CONTENT_LENGTH', 0))
            post_data = environ['wsgi.input'].read(content_length).decode('utf-8')
            body_params = parse_qs(post_data)
        except (ValueError, KeyError):
            body_params = {"error": ["Ошибка при обработке POST данных"]}

    status = '200 OK'
    headers = [('Content-Type', 'text/plain; charset=utf-8')]
    start_response(status, headers)

    response = f"Метод: {method}\n\nПараметры в URL:\n"
    for key, value in url_params.items():
        response += f"{key}: {', '.join(value)}\n"

    if method == "POST":
        response += "\nПараметры в теле POST-запроса:\n"
        for key, value in body_params.items():
            response += f"{key}: {', '.join(value)}\n"

    return [response.encode('utf-8')]

application = simple_app
