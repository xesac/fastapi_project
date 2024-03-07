import asyncio

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from .dao import HotelsDAO

router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)


@router.get('')
async def get_hotels():
    return await HotelsDAO.find_all()


@router.get('/{location}')
async def get_hotel_by_location(location: str):
    return await HotelsDAO.find_by_location(location)

