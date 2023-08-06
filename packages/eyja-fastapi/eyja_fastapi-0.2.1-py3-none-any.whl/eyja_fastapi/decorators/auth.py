from fastapi import Request, HTTPException


def login_required(f):
    async def wrapper(request: Request):
        allow = all((
            'current_user' in request.scope,
            getattr(request.scope.get('current_user'), 'is_active', False),
        ))
        if not allow:
            raise HTTPException(
                status_code=401,
                detail='ACCESS_DENIED',
            )
        return await f(request)
    
    return wrapper

def admin_required(f):
    async def wrapper(request: Request):
        allow = all((
            'current_user' in request.scope,
            getattr(request.scope.get('current_user'), 'is_active', False),
            getattr(request.scope.get('current_user'), 'is_admin', False),
        ))
        if not allow:
            raise HTTPException(
                status_code=401,
                detail='ACCESS_DENIED',
            )
        return await f(request)
    
    return wrapper