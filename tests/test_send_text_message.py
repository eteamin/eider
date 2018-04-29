from tests import test_fixture

f = test_fixture


async def test_add_user_info(f):
    resp = await f.get('/api/v1/')
    assert resp.status == 200
    assert await resp.json() == {'some_key': 'some_value'}