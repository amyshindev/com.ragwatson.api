from pydantic import BaseModel, Field

from vision.app.constants.yolo_models import DEFAULT_YOLO_NANO_WEIGHTS


class FaceTrainRequestSchema(BaseModel):
    epochs: int = Field(10, ge=1, le=500)
    batch_size: int = Field(8, ge=1, le=128)
    imgsz: int = Field(640, ge=32, le=1280)
    device: str = Field("auto", description="auto | cpu | 0 | cuda | mps")
    base_weights: str = Field(
        DEFAULT_YOLO_NANO_WEIGHTS,
        description="yolo11n.pt (기본) | yolov8n.pt | 로컬 .pt 경로",
    )
    force_prepare: bool = Field(
        False,
        description="true이면 yolo_train 원본에서 YOLO 데이터셋을 다시 생성",
    )


class FaceTrainResponseSchema(BaseModel):
    ok: bool
    dataset_yaml: str
    weights_path: str | None
    save_dir: str | None
    message: str


class FaceDetectionItemSchema(BaseModel):
    class_id: int
    class_name: str
    confidence: float
    x1: float
    y1: float
    x2: float
    y2: float


class FaceDetectResponseSchema(BaseModel):
    source: str
    weights_path: str
    detections: list[FaceDetectionItemSchema]
