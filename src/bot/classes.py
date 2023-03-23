import re

class MessageHandler():
    def __init__(self):
        self.handlers = {}

    def _add_to_handler_list(self, function, handler_data_dict):
        self.handlers.setdefault(function, {}).update(handler_data_dict)

    def _command(self, handler_type, handler_data):
        if isinstance(handler_data, str):
            handler_data = [handler_data]

        def decorator(function):
            self._add_to_handler_list(function, {handler_type: handler_data})
            return function
            # В классических декораторах тут должен быть wrapper
        return decorator

    def command(self, command=None):
        return self._command('command', command)

    def permission(self, permission=None):
        return self._command('permission', permission)

    def run(self, message):
        user_id = str(message['message']['from']['id'])
        message_command = message['message']['text'].split(' ')[0]
        message_text = message['message']['text']

        for func, handler_data in self.handlers.items():
            permissions = handler_data.get('permission', [])
            commands = handler_data.get('command', [])

            permission = not permissions or user_id in permissions
            command = not commands or message_command in commands

            if command and permission:
                func(message)
                break
