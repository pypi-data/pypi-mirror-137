from .router import users_router


@users_router.get('/confirm/{token_id}', name='confirm_user')
async def confirm_user(request):
    pass
