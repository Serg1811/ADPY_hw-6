# documents = []
documents = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
]
directories = {
    '1': ['2207 876234', '11-2'],
    '2': ['10006'],
    '3': []
}
commands = ('p', 's', 'l', 'a', 'd', 'm', 'as', 'f', 'q', 't')
descriptions = ('Узнать ФИО владельца по № документа',
                'Узнать № полки по № документа',
                'Вывести весь список документов',
                'Добавить новый документ',
                'Удолить документ',
                'Переместить документ',
                'добавить полку',
                'завершить текущую операцию',
                'Завершить работу',
                'Показать таблицу команд')
commands_descriptions = tuple(zip(commands, descriptions))


def command_table():  # создаём таблицу
    def str_table(x0, x1, x2, x3, x4):
        print('{0}{1:^10}{2}{3:<40}{4}'.format(x0, x1, x2, x3, x4))
        return

    str_table(chr(int('250F', 16)), chr(int('2501', 16)) * 10, chr(int('2533', 16)), chr(int('2501', 16)) * 40,
              chr(int('2513', 16)))
    str_table(chr(int('2503', 16)), 'Команда', chr(int('2503', 16)), 'Описание операции'.center(40),
              chr(int('2503', 16)))
    for command, description in commands_descriptions:
        str_table(chr(int('2523', 16)), chr(int('2501', 16)) * 10, chr(int('254B', 16)), chr(int('2501', 16)) * 40,
                  chr(int('252B', 16)))
        str_table(chr(int('2503', 16)), command, chr(int('2503', 16)), description, chr(int('2503', 16)))
    str_table(chr(int('2517', 16)), chr(int('2501', 16)) * 10, chr(int('253B', 16)), chr(int('2501', 16)) * 40,
              chr(int('251B', 16)))
    return True


def entered_command(text='Введите команду:\n'):
    return input(text).lower()


def availability(
        document_number):  # проверяем есть ли № документа в списке documents. Результат: адрес в списке, либо None
    for id_, document in enumerate(documents):
        content = list(document.values())
        if document_number.lower() in content:
            return id_
    return None


def people(document_number=None):
    if not document_number:
        document_number = input('Введите № документа, или команду:\n')
    document_number = document_number.lower()
    document_in_list = availability(document_number)
    if document_number in commands:
        return document_number
    elif document_in_list is not None:
        print(
            '\n\033[36m\033[3m{0[type]:<10}№ {0[number]:<15}{0[name]}\033[0m\n'.format(documents[document_in_list]))
    else:
        print('\033[31m\033[5m\nДокумент не найден\033[0m\n')
    return 'p'


def shelf_number(document_number):
    for number, shelf_documents in directories.items():
        if document_number in shelf_documents:
            return number
    return None


def shelf(document_number=None):
    if not document_number:
        document_number = input('Введите № документа или команду:\n')
    document_number = document_number.lower()
    if document_number in commands:
        return document_number
    else:
        number = shelf_number(document_number)
        if number is not None:
            print(f'\033[36m\nДокумент с номером {document_number} находится на следующей полке: {number}\033[0m\n')
        else:
            print('\033[31m\033[5m\nДокумент не найден\033[0m\n')
        return 's'


def list_():
    print()
    if len(documents) > 0:
        for document in documents:
            content = list(document.values())
            print('\033[36m\033[3m{0[0]:<10}№ {0[1]:<15}{0[2]}\033[0m'.format(content))
    else:
        print('\033[31m\033[5mДокументов не найдено\033[0m')
    return True


def add_document_shelf(number_document, number_shelf):
    while True:
        if number_shelf is None:
            number_shelf = entered_command('Введите № полки где будет храниться документ, или команду\n')
        else:
            number_shelf = number_shelf.lower()
        if number_shelf in commands:
            return number_shelf
        elif number_shelf.strip() == '':
            print(f'\n\033[31m\033[5mОшибка: данные не введены. \033[0m\n')
            number_shelf = None
            continue
        elif number_shelf not in directories.keys():
            print('\n\033[31m\033[5mПолка не найдена\033[0m\n')
            command = entered_command(
                'Введите № полки где будет храниться документ заново, или добавьте полку(команда "as"), '
                'или вызовите иную команду\n')
            if command == 'as':
                directories[number_shelf] = []
            else:
                number_shelf = command
                continue
        break
    shelf_documents = list(directories[number_shelf]).copy()
    shelf_documents.append(number_document)
    directories[number_shelf] = shelf_documents
    return number_shelf


def del_document_shelf(number_document, number_shelf):
    shelf_documents = list(directories[number_shelf]).copy()
    shelf_documents.remove(number_document)
    directories[number_shelf] = shelf_documents
    return


def add(document_type=None, document_number=None, document_name=None, number_shelf=None):

    document_new = {
        'type': document_type,
        'number': document_number,
        'name': document_name,
    }
    request_tuple = (('type', 'Введите тип документа'),
                     ('number', 'Введите № документа'),
                     ('name', 'Введите ФИО владельца документа'))
    for i, j in request_tuple:
            while True:
                if document_new[i] is None:
                    print(f'{j}, или команду')
                    request = entered_command('')
                else:
                    request = document_new[i].lower()
                if request in commands:
                    return request
                elif request.strip() == '':
                    print(f'\n\033[31m\033[5mОшибка: данные не введены. \033[0m\n')
                    continue
                elif i == request_tuple[1][0]:
                    if availability(request) is not None:
                        print(f'\n\033[31m\033[5mДокумент с таким номером уже есть\033[0m\n')
                        document_new[i] = None
                        continue
                    document_new[i] = request
                elif i == request_tuple[2][0]:
                    document_new[i] = request.title()
                else:
                    document_new[i] = request
                break
    number_shelf = add_document_shelf(document_new['number'], number_shelf)
    if number_shelf in commands:
        return number_shelf
    documents.append(document_new)
    print(
        '\033[36m\033[3m\nДокумент: {0[type]:<10}№ {0[number]:<15}{0[name]}\nуспешно добавлен на полку '
        '{1}\n\033[0m'.format(document_new, number_shelf))
    return 'a'


def delete(document_number=None):
    if document_number is None:
        document_number = entered_command('Введите № документа, или команду:\n')
    else:
        document_number = document_number.lower()
    document_in_list = availability(document_number)
    if document_number in commands:
        return document_number
    elif document_in_list is not None:
        del_document = documents.pop(document_in_list)
        number = shelf_number(document_number)
        del_document_shelf(document_number, number)
        print(
            '\033[36m\033[3m\nДокумент: {0[type]:<10}№ {0[number]:<15}{0[name]} удалён с полки '
            '{1}\n\033[0m'.format(del_document, number))
    else:
        print('\033[31m\033[5m\nДокумент не найден\033[0m\n')
    return 'd'


def move(document_number=None, request_shelf=None):
    number = None
    logic = True
    while logic:
        if document_number is None:
            document_number = entered_command('Введите № документа, или команду:\n')
        else:
            document_number = document_number.lower()
        if document_number in commands:
            return document_number
        elif document_number.strip() == '':
            document_number = None
            print(f'\n\033[31m\033[5mОшибка: данные не введены. \033[0m\n')
            continue
        number = shelf_number(document_number)
        if number is None:
            print('\033[31m\033[5m\nДокумент не найден\033[0m\n')
            document_number = None
        else:
            logic = False
    while True:
        if request_shelf is None:
            request_shelf = entered_command('Введите № полки куда будет перемещён документ, или иную команду\n')
        else:
            request_shelf = request_shelf.lower()
        if request_shelf in commands:
            return request_shelf
        elif request_shelf.strip() == '':
            request_shelf = None
            print(f'\n\033[31m\033[5mОшибка: данные не введены. \033[0m\n')
            continue
        elif number == request_shelf:
            print('\033[36m\033[3m\nДокумент № {0:<15}остаётся на прежней полке '
                  '{1}\n\033[0m'.format(document_number, number))
        else:
            new_number = add_document_shelf(document_number, request_shelf)
            if new_number in commands:
                return new_number
            del_document_shelf(document_number, number)
            print(
                '\033[36m\033[3m\nДокумент № {0:<15}перемещён с полки {1} на полку '
                '{2}\n\033[0m'.format(document_number, number, new_number))
        return 'm'


def add_shelf(number=None):
    if number is None:
        number = entered_command('Введите № добовляемой полки или команду:\n')
    if number in directories.keys():
        print('\n\033[31m\033[5mПолка с таким номером существует\033[0m\n')
    elif number in commands:
        return number
    else:
        directories[number] = []
        print(f'\033[36m\033[3m\nПолка № {number} успешно добавлена\n\033[0m')
    return 'as'


def finish():
    return True


def quit_():
    return False


if __name__ == '__main__':
    command_menu = {
        True: entered_command,
        commands[0]: people,
        commands[1]: shelf,
        commands[2]: list_,
        commands[3]: add,
        commands[4]: delete,
        commands[5]: move,
        commands[6]: add_shelf,
        commands[7]: finish,
        commands[8]: quit_,
        commands[9]: command_table
    }
    the_entered_command = command_table()
    while the_entered_command:
        if the_entered_command in command_menu:
            the_entered_command = command_menu[the_entered_command]()
        else:
            the_entered_command = entered_command('\n\033[31m\033[5mКоманда не определена\033[0m\n\nВведите команду:\n')
    print('\nДо новой встречи')
