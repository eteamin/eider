from pytest import fixture
from aiohttp.web_app import Application


def make_app():
    app = Application()
    # Config your app here
    return app


@fixture
def test_fixture(loop, test_client):
    """Test fixture to be used in test cases"""
    app = make_app()
    return loop.run_until_complete(test_client(app))
