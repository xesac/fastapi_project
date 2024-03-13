import asyncio

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from fastapi_cache.decorator import cache
from fastapi_versioning import version
from .dao import HotelsDAO
import pandas as pd
import csv
import shutil
from typing import Annotated

router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)


@router.get('')
@version(1)
async def get_hotels():
    return await HotelsDAO.find_all()


@router.get('/{location}')
@version(1)
async def get_hotel_by_location(location: str):
    return await HotelsDAO.find_by_location(location)


