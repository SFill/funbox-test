from unittest.mock import patch
import pytest
from flask.testing import FlaskClient
from links.app import create_app, repository


@pytest.fixture
def client():
    test_url = 'redis://@localhost:6379/1'
    with patch('links.db.DEFAULT_URL', test_url):
        app = create_app()
    with app.test_client() as client:
        yield client
    repository.redis.flushdb()


def test_visited_links_success(client: FlaskClient):
    payload = {
        'links': [
            'https://ya.ru',
            'https://ya.ru?q=123',
            'funbox.ru',
            'https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor'  # noqa
        ]
    }
    response = client.post('/visited_links', json=payload)
    data = response.get_json()
    assert data['status'] == 'ok'


def test_visited_domains_success(client: FlaskClient):
    repository.add(
        5,
        {
            'ya.ru',
            'qwerty.ru',
            'mail.ru'
        }
    )
    repository.add(
        6,
        {
            'lost.ru',
            'qwerty.ru',
        }
    )
    payload = {
        'from': 5,
        'to': 6
    }
    response = client.get('/visited_domains', query_string=payload)
    data = response.get_json()
    assert data['status'] == 'ok'
    assert sorted(data['domains']) == ['lost.ru',
                                       'mail.ru', 'qwerty.ru',  'ya.ru']


def test_visited_links_shema_errors(client: FlaskClient):
    payloads = [
        {},
        {
            'links': ''
        },
        {
            'links': [
                '/qwerty',
            ]
        }
    ]
    for payload in payloads:
        response = client.post('/visited_links', json=payload)
        data = response.get_json()
        assert data['status'] == 'shema error'


def test_visited_domains_shema_errors(client: FlaskClient):
    payloads = [
        {},
        {
            'from': 1234
        },
        {
            'to': 12355
        },
        {
            'from': 'qweqw',
            'to': 'qweqwe'
        },
        {
            'from': 12345,
            'to': 333
        }
    ]
    for payload in payloads:
        response = client.get('/visited_domains', query_string=payload)
        data = response.get_json()
        assert data['status'] == 'shema error'


def test_http_methods_error(client: FlaskClient):
    response = client.get('/visited_links')
    data = response.get_json()
    assert data['status'] == 'The method is not allowed for the requested URL.'
    response = client.post('/visited_domains')
    data = response.get_json()
    assert data['status'] == 'The method is not allowed for the requested URL.'
