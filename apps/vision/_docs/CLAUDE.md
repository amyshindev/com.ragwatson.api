---
tags:
  - harness/claude-vision
graph-group: claude-vision
---

# Vision App — CLAUDE.md

`backend/apps/vision/` — Sherlock Holmes / Titanic과 동일한 Hexagonal + Vertical Slice.

> **Import:** `from vision.adapter...` (`PYTHONPATH=apps`)

## 캐릭터 (introduce_myself)

| stem | prefix | 역할 |
|------|--------|------|
| `optic_yolo_detector` | `/vision/yolo` | 실시간 객체 탐지 |
| `optic_resnet_classifier` | `/vision/resnet` | 이미지 분류 |
| `optic_sam_segmenter` | `/vision/sam` | 세그멘테이션 |
| `optic_clip_embedder` | `/vision/clip` | 멀티모달 임베딩·유사도 |
| `optic_ocr_reader` | `/vision/ocr` | 문자·텍스트 인식 |

각 캐릭터: `GET /vision/{name}/myself` → `{ id, name }`.

## 라우트

- `GET /vision/yolo/myself` — 요로 (YOLO)
- `GET /vision/resnet/myself` — 레즈넷 (ResNet)
- `GET /vision/sam/myself` — 샘 (SAM)
- `GET /vision/clip/myself` — 클립 (CLIP)
- `GET /vision/ocr/myself` — OCR 리더

## 슬라이스 파일 세트

`{stem}_router.py` 기준으로 schema, dto, ports, interactor, provider, pg repository가 동일 stem으로 쌍을 이룹니다.

## References

- Titanic 아키텍처: [`../titanic/_docs/structure.md`](../titanic/_docs/structure.md)
