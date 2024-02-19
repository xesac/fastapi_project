from fastapi import APIRouter, UploadFile
import shutil

from app.task.tasks import process_pic



router = APIRouter(
    prefix='/images',
    tags=['Изображения']
)


@router.post('/hotels')
async def add_hotel_image(name: int, file: UploadFile):
    im_path = f'app/static/images/{name}.webp'
    with open(im_path, 'wb+') as file_object:
        shutil.copyfileobj(file.file, file_object)
    process_pic.delay(im_path)


