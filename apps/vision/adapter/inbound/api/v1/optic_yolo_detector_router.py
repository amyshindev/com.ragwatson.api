from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from vision.adapter.inbound.api.schemas.face_detector_schema import (
    FaceDetectResponseSchema,
    FaceDetectionItemSchema,
    FaceTrainRequestSchema,
    FaceTrainResponseSchema,
)
from vision.adapter.inbound.api.schemas.optic_yolo_detector_schema import YoloDetectorSchema
from vision.app.dtos.yolo_train_dto import YoloTrainHyperparams
from vision.app.dtos.optic_yolo_detector_dto import YoloDetectorResponse
from vision.app.ports.input.optic_yolo_detector_use_case import YoloDetectorUseCase
from vision.app.ports.input.train_yolo_use_case import TrainYoloUseCase
from vision.app.use_cases.detect_face_interactor import DetectFaceInteractor
from vision.dependencies.face_detector_train_provider import (
    get_detect_face_interactor,
    get_train_yolo_use_case,
)
from vision.dependencies.optic_yolo_detector_provider import get_optic_yolo_detector_use_case

optic_yolo_detector_router = APIRouter(prefix="/vision/yolo", tags=["vision", "yolo"])


@optic_yolo_detector_router.get("/myself")
async def introduce_myself(
    character: YoloDetectorUseCase = Depends(get_optic_yolo_detector_use_case),
) -> YoloDetectorResponse:
    return await character.introduce_myself(
        YoloDetectorSchema(id=1, name="요로 (YOLO)")
    )


@optic_yolo_detector_router.post("/train", response_model=FaceTrainResponseSchema)
async def train_face_detector(
    body: FaceTrainRequestSchema,
    trainer: TrainYoloUseCase = Depends(get_train_yolo_use_case),
) -> FaceTrainResponseSchema:
    try:
        result = trainer.execute(
            YoloTrainHyperparams(
                base_weights=body.base_weights,
                epochs=body.epochs,
                batch_size=body.batch_size,
                imgsz=body.imgsz,
                device=body.device,
            ),
            force_prepare=body.force_prepare,
        )
        return FaceTrainResponseSchema(
            ok=result.ok,
            dataset_yaml=result.dataset_yaml,
            weights_path=result.weights_path,
            save_dir=result.save_dir,
            message=result.message,
        )
    except (RuntimeError, FileNotFoundError) as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@optic_yolo_detector_router.post("/detect", response_model=FaceDetectResponseSchema)
async def detect_faces(
    file: UploadFile = File(...),
    detector: DetectFaceInteractor = Depends(get_detect_face_interactor),
) -> FaceDetectResponseSchema:
    import tempfile
    from pathlib import Path

    suffix = Path(file.filename or "upload.jpg").suffix or ".jpg"
    try:
        data = await file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(data)
            tmp_path = tmp.name

        result = detector.execute(tmp_path)
        return FaceDetectResponseSchema(
            source=file.filename or tmp_path,
            weights_path=result.weights_path,
            detections=[
                FaceDetectionItemSchema(
                    class_id=item.class_id,
                    class_name=item.class_name,
                    confidence=item.confidence,
                    x1=item.x1,
                    y1=item.y1,
                    x2=item.x2,
                    y2=item.y2,
                )
                for item in result.detections
            ],
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
