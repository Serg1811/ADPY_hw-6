import pytest
from YDisk import YDisk
from tokens import token_api_yndex

user = YDisk(token=token_api_yndex)


class TestYDisk:
    @pytest.mark.parametrize('directory, expected_result',
                             [
                                 ('dir1', True),
                                 ('dir1', 409),
                                 # ('11-2', 'p'),
                                 # ('0001', 'p'),
                             ]
                             )
    def test_create_directory(self, directory, expected_result):
        if user.get_resources(directory) == 404:
            assert user.create_directory(directory) == expected_result
            assert user.get_resources(directory) == 200
        elif user.get_resources(directory) == 200:
            assert user.create_directory(directory) == expected_result
