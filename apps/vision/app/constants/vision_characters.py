VISION_CHARACTERS: list[dict[str, str]] = [
    {
        "id": "yolo",
        "stem": "optic_yolo_detector",
        "route": "yolo",
        "name": "요로 (YOLO)",
        "role": "실시간 객체 탐지 · 얼굴 인식",
    },
    {
        "id": "resnet",
        "stem": "optic_resnet_classifier",
        "route": "resnet",
        "name": "레즈넷 (ResNet)",
        "role": "이미지 분류",
    },
    {
        "id": "sam",
        "stem": "optic_sam_segmenter",
        "route": "sam",
        "name": "샘 (SAM)",
        "role": "세그멘테이션",
    },
    {
        "id": "clip",
        "stem": "optic_clip_embedder",
        "route": "clip",
        "name": "클립 (CLIP)",
        "role": "멀티모달 임베딩·유사도",
    },
    {
        "id": "ocr",
        "stem": "optic_ocr_reader",
        "route": "ocr",
        "name": "OCR 리더",
        "role": "문자·텍스트 인식",
    },
]
