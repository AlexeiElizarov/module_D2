from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    if isinstance(value, str) and isinstance(arg, int):
        return str(value) * arg
    else:
        raise ValueError(f'Нельзя умножать {type(value)} на {type(arg)}')

@register.filter(name='censor')
def censor(value):
    unwanted_words = [
        'fuck',
        'bitch'
    ]
    lst = []
    for _ in unwanted_words:
        if _ in value:
            raise ValueError(f'Недопустимое слово: {_}')
        else:
            lst.append(True)
    if all(lst):
        return value

@register.filter(name='update_page')
def update_page(full_path: str, page: int):
    try:
        params_list = full_path.split('?')[1].split('&')
        params = dict([tuple(str(param).split('=')) for param  in params_list])
        params.update({'page': page})
        link = ''
        for key, value in params.items():
            link += (f"{key}={value}&")
        return link[:-1]
    except:
        return f"page={page}"

# http://127.0.0.1:8000/news/?author=2&date=&rating_post=
# http://127.0.0.1:8000/news/?page=2

@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()


FORBIDDIEN_WORDS = [
    'редиска'
]

@register.filter
def unwanted_words_filter(value):
    lst = []
    for word in value.split():
        result = ''
        if word in FORBIDDIEN_WORDS:
            result += word[0]
            for _ in word[1:-1]:
                result += '*'
            result += word[-1]
        else:
            result += word
        lst.append(result)
    return ' '.join(lst)
