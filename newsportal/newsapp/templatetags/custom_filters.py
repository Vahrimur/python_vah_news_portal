from django import template

register = template.Library()

SWEAR_WORDS = {'хуй', 'хуе', 'хуя', 'пизд', 'бля', 'еб', 'ёб', 'пидор'}


class FilterException(Exception):
    pass


@register.filter()
def censor(value):
    if type(value) != str:
        raise FilterException(f'Невозможно применить фильтр цензуры к переменной типа {type(value)}')
    else:
        split_text = value.split(' ')
        joined_text = ''
        temp_word = ''
        for word in split_text:
            for s_word in SWEAR_WORDS:
                if s_word in word.lower():
                    check_word = ''
                    for symbol in word:
                        if symbol.isalpha():
                            check_word += symbol
                        else:
                            if s_word in check_word.lower():
                                temp_word += check_word[0] + (len(check_word) - 1) * '*'
                                check_word = ''
                            temp_word += symbol
                    if word[len(word) - 1].isalpha():
                        temp_word += check_word[0] + (len(check_word) - 1) * '*'
            if temp_word == '':
                joined_text += word + ' '
            else:
                joined_text += temp_word + ' '
            temp_word = ''

        return joined_text
