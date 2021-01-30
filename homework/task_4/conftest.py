import pytest


def pytest_addoption(parser):
    parser.addoption("--url", default="https://ya.ru",
                     help="This is request url"
    )

    parser.addoption("--status_code", type = int, default=200,
                     help="This is response status code"
    )


@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--url")


@pytest.fixture
def status_code(request):
    return request.config.getoption("--status_code")
