__all__ = ['upload_file']

import hashlib
import mimetypes
import os
import shutil
from enum import Enum

from fastapi import APIRouter, Depends, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from PIL import Image

from mylassi_data.db import get_db, SessionLocal
from mylassi_data.models import *
from mylassi_data.restschema import *
from .security import get_current_active_user

router = APIRouter(tags=['Files'])

upload_path = os.environ['UPLOAD_DIR']


def delete_file(file_id: int):
    with SessionLocal() as session:
        fs_file = FSFileModel.get_or_404(session, file_id)
        fs_path = os.path.join(upload_path, fs_file.path)
        fs_dir = os.path.dirname(fs_path)
        shutil.rmtree(fs_dir)

        session.delete(fs_file)
        session.commit()


def check_file(file_id: int):
    with SessionLocal() as session:
        fs_file = FSFileModel.get_or_404(session, file_id)
        fs_path = os.path.join(upload_path, fs_file.path)

        with open(fs_path, 'rb') as fs:
            hash_value = hashlib.sha256(fs.read()).hexdigest()

        same_file = FSFileModel.first(session, hash_value=hash_value)
        if same_file:
            FileModel.q(session).filter(FileModel.fs_model_id == fs_file.id).update({'fs_model_id': same_file.id})
            session.commit()
            delete_file(fs_file.id)
            return

        fs_file.hash_value = hash_value
        session.commit()

        return


def upload_file():
    async def upload_file_helper(
            file: UploadFile,
            task: BackgroundTasks,
            session: Session = Depends(get_db),
            current_user: UserModel = Depends(get_current_active_user)) -> str:

        fs_file = FSFileModel()
        fs_file.mimetype = mimetypes.guess_type(file.filename)[0]

        session.add(fs_file)
        session.commit()

        try:
            fs_path = os.path.join(upload_path, fs_file.path)
            fs_dir = os.path.dirname(fs_path)

            os.makedirs(fs_dir, exist_ok=True)

            with open(fs_path, 'wb') as local_fs:
                while chunk := await file.read(1024):
                    local_fs.write(chunk)

            fs_file.ready = True

            if fs_file.is_image:
                image = Image.open(fs_path)
                fs_file.image_width, fs_file.image_height = image.size

            session.commit()
            task.add_task(check_file, fs_file.id)
        except:
            task.add_task(delete_file, fs_file.id)
            raise Exception('Cannot upload file')

        file_entry = FileModel()
        file_entry.origin_filename = file.filename
        file_entry.filename = file.filename
        file_entry.owner = current_user
        file_entry.fs_model = fs_file

        session.add(file_entry)
        session.commit()

        return file_entry.id

    return upload_file_helper


@router.post('/files', response_model=FileRestType)
async def upload_file_to_filesystem(
        session: Session = Depends(get_db),
        file: str = Depends(upload_file())):
    file = FileModel.get_or_404(session, file)
    return file.rest_type()


@router.get('/files/{file}/info', response_model=FileRestType)
async def get_file_info(file: str,
                        session: Session = Depends(get_db),
                        current_user: UserModel = Depends(get_current_active_user)):
    file = FileModel.get_or_404(session, file)
    return file.rest_type()


@router.get('/files/{file}', response_class=FileResponse)
async def download_file(file: str,
                        session: Session = Depends(get_db)):
    file = FileModel.get_or_404(session, file)

    fs_path = os.path.join(upload_path, file.path)
    return FileResponse(fs_path, filename=file.filename)


@router.get('/files/{file}/image', response_class=FileResponse)
async def download_image(file: str,
                         width: int = None,
                         height: int = None,
                         session: Session = Depends(get_db)):
    file = FileModel.get_or_404(session, file)
    assert file.is_image

    resize = False

    img_width = new_width = file.fs_model.image_width
    img_height = new_height = file.fs_model.image_height
    ratio = img_width / img_height

    file_path = os.path.join(upload_path, file.path)
    if width and width > 0:
        new_width = int((int(width / img_width * 10) + 1) / 10 * img_width)
        new_height = int(new_width / ratio)
        resize = True
    elif height and height > 0:
        new_height = int((int(height / img_height * 10) + 1) / 10 * img_height)
        new_width = int(ratio * new_height)
        resize = True

    if resize:
        sub_file = FSSubFileModel.first(session, width=new_width, height=new_height)
        if not sub_file:
            sub_file = FSSubFileModel()
            sub_file.width = new_width
            sub_file.height = new_height
            sub_file.fs_model = file.fs_model

            session.add(sub_file)
            session.commit()

            image = Image.open(file_path)

            file_path = os.path.join(upload_path, sub_file.path)
            new_image = image.resize((new_width, new_height))
            new_image.save(file_path, format=image.format)
        else:
            FSSubFileModel.q(session).filter(FSSubFileModel.id == sub_file.id) \
                .update(
                {
                    'access_count': FSSubFileModel.access_count + 1,
                })
            session.commit()
            file_path = os.path.join(upload_path, sub_file.path)

    return FileResponse(file_path, filename=file.filename)
