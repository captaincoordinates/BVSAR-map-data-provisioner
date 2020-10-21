from pydantic import BaseModel

from app.common.BBOX import BBOX


class ProjectProperties(BaseModel):
    bbox: BBOX
    zoom_min: int
    zoom_max: int
    name: str
