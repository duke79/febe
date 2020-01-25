from __future__ import print_function, unicode_literals

from examples import custom_style_2
from PyInquirer import prompt, print_json, Separator


def input_list(options, message="Choose an option"):
    questions = [
        {
            'type': 'list',
            'name': 'input_list',
            'message': message,
            'choices': options
        }
    ]

    answers = prompt(questions, style=custom_style_2)
    ret = answers["input_list"]
    return ret


def input_confirm(message="Do you want to continue?"):
    questions = [
        {
            'type': 'confirm',
            'name': 'input_confirm',
            'message': message,
            'default': False
        }
    ]

    answers = prompt(questions, style=custom_style_2)
    ret = answers["input_confirm"]
    return ret


def input_checkbox(options, message="Select options"):
    options = [{'name': option} for option in options]
    questions = [
        {
            'type': 'checkbox',
            'qmark': '😃',
            'message': message,
            'name': 'input_checkbox',
            'choices': options,
            'validate': lambda answer: 'You must choose at least one.' if len(answer) == 0 else True
        }
    ]

    answers = prompt(questions, style=custom_style_2)
    return answers["input_checkbox"]


def parse_args(*args, **kwargs):
    args_str = ""

    for arg in args:
        args_str += str(arg) + " "
    for key in kwargs.keys():
        if kwargs[key] is True:
            args_str += " --" + key
        else:
            args_str += " --" + key + " " + str(kwargs[key])

    print(args_str)
    return args_str
