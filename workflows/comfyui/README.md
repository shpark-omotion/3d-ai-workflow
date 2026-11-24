# 선택: ComfyUI-Tripo 연결 (2.0.0 API v3 기준)

[공식 노드 가이드 및 원본 워크플로 PNG](https://developers.tripo3d.ai/ko/docs/comfyui-nodes)를 먼저 확인한다. 승인된 별도 테스트 환경에 공식 v2.0.0 노드와 호환 SDK를 설치하고 기존 회사 워크플로를 변경하지 않는다. API 키는 환경 변수 또는 승인된 로컬 설정으로만 제공한다. 모델 생성/처리는 외부 API 과금 및 데이터 전송이 발생한다.

단일: LoadImage → TripoAPIDraft(image_to_model) → Preview3D. 멀티뷰: 정면 필수, 왼쪽/오른쪽/후면 옵션. `model_file`은 미리보기/파일 전달, `MODEL_INFO`는 후처리 작업 컨텍스트다. UV는 Smart UV 입력 등가 삼각형 80,000 제한을 확인하고 필요한 저폴리 처리 후 실행. 텍스처·리그 노드는 공식 가이드의 `MODEL_INFO` 연결을 사용하며 각 단계별 비용 및 지원 spec을 확인한다. Refine/Stylize 사용 중지. Preview3D는 현재 core에서 구형으로 표시될 수 있으므로 실제 노드 확인 필요.

기술 담당자가 로컬 ComfyUI `/object_info` JSON을 작업 폴더에 저장한 후 아래와 같이 API prompt 초안을 생성한다. **웹 UI에서 가져오는 workflow JSON이 아니다. 실제 설치 스키마가 없으면 만들지 않는다. 제출하지 않는다.**

```bash
python scripts/comfy_plan.py --schema /approved-local/object_info.json --front front.png --back back.png --model P2-20260801 --texture --pbr --output /approved-local/prompt.json
```

이미지 파일명은 ComfyUI input 기준이다. 호환 스키마가 없거나 required 입력이 바뀌면 중단하고 공식 PNG 예제를 가져와 수정한다. `apikey`는 빈 값이며 키를 출력/저장하지 않는다. 담당자가 노드, 입력, 예상 비용, output 위치를 검토하고 reserve를 기록한 다음 한 번만 실행한다. 완료 후 실제 job ID/비용과 GLB를 reconcile/snapshot 한다. 후처리 및 LoRA 연결은 승인된 실제 워크플로로 검증한다. 이 스크립트는 단일/멀티뷰 생성 그래프 초안만 만들며 실제 큐, 인증, 생성 및 후처리 NOT_RUN이다.
