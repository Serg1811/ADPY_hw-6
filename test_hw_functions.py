import pytest
from mock import patch
from main import command_table, entered_command, availability, people, shelf_number, shelf, list_, add_document_shelf, \
    del_document_shelf, add, delete, move, add_shelf, finish, quit_, documents, directories, commands


class TestFunctions:

    numbers_documents = (document['number'] for document in documents)

    def test_command_table(self):
        print()
        assert command_table() is True

    @patch('builtins.input', return_value='AaAa')
    def test_entered_command(self, mock):
        assert entered_command() == 'aaaa'

    @pytest.mark.parametrize('number_document, expected_result',
                             [(document, id_) for id_, document in enumerate(numbers_documents)] + [('', None)])
    def test_availability(self, number_document, expected_result):
        assert availability(number_document) == expected_result

    @pytest.mark.parametrize('number_document, expected_result',
                             [('s', 's'),
                              ('S', 's'),
                              ('11-2', 'p'),
                              ('0001', 'p')]
                             )
    def test_people(self, number_document, expected_result):
        assert people(number_document) == expected_result

    @pytest.mark.parametrize('number_document, expected_result',
                             [(document, directory) for directory, documents_ in directories.items()
                              for document in documents_] + [('', None)])
    def test_shelf_number(self, number_document, expected_result):
        assert shelf_number(number_document) == expected_result

    @pytest.mark.parametrize('number_document, expected_result',
                             [('p', 'p'),
                              ('P', 'p'),
                              ('11-2', 's'),
                              ('0001', 's')]
                             )
    def test_shelf(self, number_document, expected_result):
        assert shelf(number_document) == expected_result

    def test_list_(self):
        assert list_() is True

    @pytest.mark.parametrize('number_document, number_shelf, expected_result',
                             [
                                 ('Ая123456789', '1', '1'),
                                 ('Ая123456789', 'S', 's'),
                                 ('Ая123456789', 's', 's'),
                             ]
                             )
    def test_add_document_shelf(self, number_document, number_shelf, expected_result):
        if number_document.lower in self.numbers_documents:
            if number_shelf.lower in directories:
                result = add_document_shelf(number_document, number_shelf)
                assert number_document in directories[number_shelf]
        else:
            result = add_document_shelf(number_document, number_shelf)
        assert result == expected_result

    @patch('builtins.input', return_value='as')
    def test_add_document_shelf_not_shelf(self, mock):
        number_document = 'Ая123456789'
        number_shelf = '8'
        assert add_document_shelf(number_document, number_shelf) == number_shelf
        assert number_document in directories[number_shelf]

    @pytest.mark.parametrize('number_document, number_shelf',
                             [
                                 ('11-2', '1'),
                                 ('11-2', '2'),
                             ]
                             )
    def test_del_document_self(self, number_document, number_shelf):
        if number_document in directories[number_shelf]:
            del_document_shelf(number_document, number_shelf)
            assert number_document not in directories[number_shelf]
        else:
            with pytest.raises(ValueError):
                del_document_shelf(number_document, number_shelf)

    @pytest.mark.parametrize('document_type, document_number, document_name, number_shelf, expected_result',
                             [
                                 ('paSsWord', 'Ая123456789', 'хРиСТОфор кОлумБ', '3', 'a'),
                                 ('p', 'Ая123456789', 'хРиСТОфор кОлумБ', '3', 'p'),
                                 ('paSsWord', 'S', 'хРиСТОфор кОлумБ', '3', 's'),
                                 ('paSsWord', 'Ая12345678', 'L', '3', 'l'),
                                 ('paSsWord', 'Ая1234567', 'хРиСТОфор кОлумБ', 'D', 'd'),
                             ]
                             )
    def test_add(self, document_type, document_number, document_name, number_shelf, expected_result):
        result = add(document_type, document_number, document_name, number_shelf)
        assert result == expected_result
        if result == 'a' and availability(document_number):
            assert {'type': document_type.lower(), 'number': document_number.lower(), 'name': document_name.title()}\
                   in documents

    @pytest.mark.parametrize('document_number, expected_result',
                             [('p', 'p'),
                              ('P', 'p'),
                              ('11-2', 'd'),
                              ('0001', 'd')]
                             )
    def test_delete(self, document_number, expected_result):
        result = delete(document_number)
        old_shelf = shelf_number(document_number)
        assert result == expected_result
        if old_shelf:
            assert document_number not in directories[old_shelf]

    @pytest.mark.parametrize('document_number, request_shelf, expected_result',
                             [
                                 ('11-2', '1', 'm'),
                                 ('11-2', '2', 'm'),
                                 ('11-2', 'S', 's'),
                                 ('11-2', 's', 's'),
                                 ('S', '3', 's'),
                                 ('s', '3', 's'),
                                 ('11-2', 'S', 's'),
                             ]
                             )
    def test_move(self, document_number, request_shelf, expected_result):
        if document_number.lower in self.numbers_documents:
            old_shelf = shelf(document_number)
            print(old_shelf)
            if request_shelf.lower in directories:
                result = move(document_number, request_shelf)
                assert document_number in directories[request_shelf]
                assert document_number not in directories[old_shelf]
        else:
            result = move(document_number, request_shelf)
        assert result == expected_result

    @patch('builtins.input', return_value='as')
    def test_move_not_shelf(self, mock):
        document_number = '11-2'
        request_shelf = '8'
        assert move(document_number, request_shelf) == 'm'
        assert document_number in directories[request_shelf]
        assert document_number not in directories['1']

    @pytest.mark.parametrize('number, expected_result',
                             [('s', 's'),
                              ('S', 's'),
                              ('1', 'as'),
                              ('8', 'as')]
                             )
    def test_add_shelf(self, number, expected_result):
        number = number.lower()
        if number not in commands and number not in directories:
            result = add_shelf(number)
            assert number in directories
        else:
            result = add_shelf(number)
        assert result == expected_result

    def test_finish(self):
        assert finish() is True

    def test_quit_(self):
        assert quit_() is False
