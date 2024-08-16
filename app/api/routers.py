from fastapi.routing import APIRouter

from .endpoints.city import router as city_router

main_router = APIRouter(prefix='/api/v1')
main_router.include_router(city_router, prefix='/city', tags=['city'])
