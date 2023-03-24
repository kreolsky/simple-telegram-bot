import re
import os

def parse_env_users_list(users_str):
    users_list = [x.strip() for x in os.getenv(users_str).split(',')]
    users_list = list(filter(lambda x: len(x) > 0, users_list))
    if not users_list[0]:
        return []
    return users_list


def dict_to_str(source, tab='', count=0):
    output = ''

    if not isinstance(source, dict):
        return source

    for key, value in source.items():
        end = ''
        if isinstance(value, dict):
            count += 1
            value = dict_to_str(value, ' ' * 4, count)
            end = '\n'
            count -= 1

        output += f'{tab * count}{str(key)}: {end}{str(value)}\n'

    return output[:-1]
