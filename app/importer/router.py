import asyncio

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from fastapi_cache.decorator import cache
from fastapi_versioning import version
import pandas as pd
import csv
import shutil
from typing import Annotated

from app.hotels.dao import HotelsDAO



router = APIRouter(
    prefix='/import',
    tags=['Импорт отелей']
)






@router.post('/hotels')
async def import_hotels(file: Annotated[UploadFile, File()]):
    file_name = file.filename.split('.')
    if file_name[-1] != 'csv':
        return JSONResponse(content={'msg': 'Файл должен быть формата CSV'})
    else:
        im_path = f'app/static/files/file.csv'
        with open(im_path, 'wb') as file_object:
            shutil.copyfileobj(file.file, file_object)
        with open('app/static/files/file.csv') as f:
            hotel = csv.DictReader(f)
            for i in hotel:
                await HotelsDAO.add(name=i['name'], location=i['location'], services=i['services'], rooms_quantity=int(i['rooms_quantity']), image_id=int(i['image_id']))