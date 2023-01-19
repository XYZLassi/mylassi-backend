import os

from fastapi import APIRouter, Depends, UploadFile

from mylassi_data import db
from mylassi_data.models import UserModel, FileModel
from .security import get_current_active_user

router = APIRouter(tags=['Files'])

upload_path = os.environ['UPLOAD_DIR']


def upload_file():
    async def upload_file_helper(
            file: UploadFile,
            current_user: UserModel = Depends(get_current_active_user)):


        file_entry = FileModel()

        file_entry.filename = file.filename
        file_entry.owner = current_user

        db.session.add(file_entry)
        db.session.commit()

        try:
            fs_path = os.path.join(upload_path, file_entry.path)
            fs_dir = os.path.dirname(fs_path)

            os.makedirs(fs_dir, exist_ok=True)

            with open(fs_path, 'wb') as local_fs:
                while chunk := await file.read(1024):
                    local_fs.write(chunk)

            file_entry.ready = True
            db.session.commit()
        except:
            db.session.delete(file_entry)
            db.session.commit()
            raise Exception('Cannot upload file')

        return file_entry

    return upload_file_helper


@router.post('/files')
async def upload_file_to_filesystem(file: FileModel = Depends(upload_file())):
    return {'filename': file.filename}
