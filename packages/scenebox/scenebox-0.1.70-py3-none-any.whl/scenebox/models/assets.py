import io
from typing import NamedTuple, Optional, Union, List
from datetime import datetime

from ..models.annotation import Annotation


class Image(NamedTuple):
    image_path: Optional[str] = None
    id: Optional[str] = None
    image_url: Optional[str] = None
    image_uri: Optional[str] = None
    image_bytes: Optional[Union[io.BytesIO, bytes, str]] = None
    sensor: Optional[str] = None
    timestamp: Optional[Union[str, datetime]] = None
    session_uid: Optional[str] = None
    annotations: Optional[List[Annotation]] = None
    aux_metadata: Optional[dict] = None
