from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from mylassi_data.models import ArticleFileModel


class ArticleFileGraphReturnType(BaseModel):
    file_id: str
    article_file_id: int
    file_usage: Optional[str]
    filename: str
    url: str

    mimetype: str
    image_width: Optional[int]
    image_height: Optional[int]

    @staticmethod
    def from_model(model: ArticleFileModel) -> ArticleFileGraphReturnType:
        return ArticleFileGraphReturnType(
            file_id=model.file.id,
            article_file_id=model.id,
            file_usage=model.file_usage,
            filename=model.file.filename,
            url=model.file.url,
            mimetype=model.file.fs_model.mimetype,
            image_width=model.file.fs_model.image_width,
            image_height=model.file.fs_model.image_height
        )
