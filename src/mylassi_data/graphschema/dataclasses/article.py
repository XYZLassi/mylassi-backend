from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from mylassi_data.models import ArticleFileModel


class ArticleFileGraphReturnType(BaseModel):
    id: int
    file_usage: Optional[str]
    filename: str
    url: str

    @staticmethod
    def from_model(model: ArticleFileModel) -> ArticleFileGraphReturnType:
        return ArticleFileGraphReturnType(
            id=model.id,
            file_usage=model.file_usage,
            filename=model.file.filename,
            url=model.file.url,
        )
