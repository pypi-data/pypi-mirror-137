from fastapi import APIRouter, Request

from eyja.interfaces.operators import (
    create_model_operator,
    ModelOperator,
)
from eyja.interfaces.db import (
    BaseStorageModel
)

from eyja_fastapi.decorators import admin_required, login_required


def set_auth_mode(auth: str, f):
    if auth == 'admin':
        f = admin_required(f)
    elif auth == 'user':
        f = login_required(f)

    return f

def model_api(model_cls: BaseStorageModel, operator: ModelOperator = None, auth: dict = {}) -> APIRouter:
    auth.setdefault('get', 'admin')
    auth.setdefault('count', 'admin')
    auth.setdefault('create', 'admin')
    auth.setdefault('delete', 'admin')
    auth.setdefault('find', 'admin')
    auth.setdefault('update', 'admin')

    router = APIRouter()
    if not operator:
        operator = create_model_operator(model_cls)

    async def get(request: Request):
        data = await operator.get(request.path_params.get('_id'))
        return data

    async def count(request: Request):
        json_data = await request.json()
        return await operator.count(json_data)

    async def create(request: Request):
        json_data = await request.json()
        return await operator.create(json_data)

    async def delete(request: Request):
        _id: str = request.path_params.get('_id')
        await operator.delete(_id)
        return {}

    async def find(request: Request):
        json_data = await request.json()
        return await operator.find(json_data)

    async def update(request: Request):
        json_data = await request.json()
        return await operator.update(
            request.path_params.get('_id'),
            json_data,
        )

    all_auth = auth.get('all')
    get_auth = auth.get('get') if not all_auth else all_auth
    count_auth = auth.get('count') if not all_auth else all_auth
    create_auth = auth.get('create') if not all_auth else all_auth
    delete_auth = auth.get('delete') if not all_auth else all_auth
    find_auth = auth.get('find') if not all_auth else all_auth
    update_auth = auth.get('update') if not all_auth else all_auth
    
    router.get('/{_id}')(set_auth_mode(get_auth, get))
    router.post('/count')(set_auth_mode(count_auth, count))
    router.post('/')(set_auth_mode(create_auth, create))
    router.delete('/{_id}')(set_auth_mode(delete_auth, delete))
    router.post('/find')(set_auth_mode(find_auth, find))
    router.patch('/{_id}')(set_auth_mode(update_auth, update))

    return router
