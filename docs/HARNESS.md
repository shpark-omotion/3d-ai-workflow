# v0.2 실제 사용 방법 — 파일럿 검토본

## 디자이너: 최초 설정은 담당자에게 맡기세요

1. [설치 가이드](SETUP.md)에 따라 준비된 Codex 프로젝트를 열고 Astra와 실제 Blender 연결을 확인합니다. 기존 연결이 정상이라면 다시 설치하지 않습니다.
2. 원본 또는 기존 GLB를 준비합니다. 실제 회사 파일은 승인된 저장소 밖 작업 폴더에 둡니다. 외부 AI에 제공하기 전 별도 허가가 필요합니다.
3. 아래 요청을 보내세요. 실제 제품 규격이 미정이면 테스트용으로만 진행합니다.

```text
$character-production
이 원본으로 캐릭터를 제작하고 싶습니다. 얼굴과 헤어, 의상은 유지해 주세요.
AGENTS.md와 docs/HARNESS.md, docs/EXAMPLES.md를 읽고 현재 도구와 제작 카드를 먼저 확인해 주세요.
기존 GLB가 있다면 먼저 가져와 검사해 주세요. 아직 유료 생성은 하지 마세요.
작업 폴더와 목표 규격을 확인하고, scripts/harness.py로 프로젝트 상태를 관리해 주세요.
수정 전후 실제 렌더와 기술 검사 결과를 보여 주세요. 승인은 제가 직접 결정하겠습니다.
```

Skill 호출이 안 되면 `$character-production`을 빼고 동일 요청을 사용합니다. AI가 연결되지 않은 도구를 실행한 척하면 중단하고 담당자에게 전달합니다. 최종 작업본 `.blend`와 실제 납품 GLB는 구분합니다.

## 기술 담당자: 실제 실행 명령

Python 3.9+ 및 설치 승인된 Blender 4.x/5.x 실행 파일을 준비합니다. 버전 호환성은 아래 통합 테스트로 확인합니다. v0.2 도구는 외부 라이브러리 설치나 네트워크 호출 없이 상태 관리를 수행합니다. Blender 검사 자체는 설치된 Blender의 Python API를 사용합니다. Windows에서는 `python` 대신 `py -3`, macOS에서는 필요 시 `python3`을 사용하세요. 아래 경로는 예시이며 실제 절대경로로 교체합니다.

```bash
python scripts/doctor.py --json
python -m unittest discover -s tests -v
python examples/make_fixture.py /approved-local/demo.glb --hair-offset 0.2
python scripts/harness.py --project /approved-local/demo-project init --policy examples/policy.json
python scripts/harness.py --project /approved-local/demo-project snapshot /approved-local/demo.glb
python scripts/harness.py --project /approved-local/demo-project status
python scripts/harness.py --project /approved-local/demo-project qa --blender /approved-app/blender
```

예제 policy는 정적 테스트 전용이며 과금 허용량 0입니다. 실제 정책은 제품 담당자가 지정한 triangle 예산, UV/재질, 필수 본/표정, 모션·런타임 요구, 축, 허용 열린 메시 이름, 비용 상한을 사용합니다. `face_mesh`는 실제 확인한 얼굴 오브젝트 이름, `motion_frames`는 실제 애니메이션에서 확인할 프레임 번호입니다. 모션이 필수면 서로 다른 프레임 2개 이상과 실제 동작 검수가 필요합니다. 수치와 규격을 모르면 납품하지 않습니다. 새 프로젝트는 존재하지 않는 승인 경로에 만들고, 정책 변경은 별도 프로젝트 또는 후속 승인된 마이그레이션으로 처리합니다.

## 실제 생성, 수정, 검사, 승인

- `reference FILE --view front --note "유지할 특징"`으로 원본을 복사·해시 기록합니다. 이미지 품질·형태 일치 여부는 사람이 확인합니다.
- 생성 전 사용자가 선택한 경로, 모델/옵션, 비용, 외부 업로드 허용을 확인합니다. `reserve --route studio|plugin|comfyui --credits N --actor 실제승인자 --request "모델 및 옵션"`로 예산을 기록합니다. 도구는 생성하지 않습니다. 공식 서비스에서 한 번 생성한 후 `reconcile ID --status SUCCESS --actual N --task-id 실제ID --note "확인 근거"`로 기록합니다. 시간 초과는 UNKNOWN, 확인된 실패는 FAILED. UNKNOWN 상태에서는 새 예약을 거부합니다. API 자체의 중복 실행 방지는 아님을 유의합니다.
- 다운로드한 자기완결 GLB를 `snapshot FILE --attempt 예약ID`(기존 모델은 `snapshot FILE`)로 등록합니다. 후보마다 새 버전을 저장합니다. AI는 Blender에서 승인된 작업 사본만 수정하고 다시 GLB로 출력합니다. `qa` 후 `snapshot NEW.glb --protect Head --protect Body`로 보호 대상 기준을 유지할 수 있습니다. 이전 QA가 실패해도 보고·렌더가 완전하면 보호 대상을 선정할 수 있습니다.
- 정적 독립 파트의 위치만 고칠 때 `move-static Hair --delta -0.2 0 0 --actor 실제승인자 --note "헤어 정렬"`를 실행할 수 있습니다. glTF 좌표계(Y-up)이며 실제 값은 사전 확인합니다. 스킨·모프·애니메이션·확장 GLB에는 적용하지 않습니다. 원본 및 비대상 노드와 BIN 청크를 유지하고 새 버전을 생성합니다. 리깅된 캐릭터는 Blender 사본에서 수정합니다.
- `qa --blender 실제실행파일`은 새 Blender 프로세스로 후보 GLB를 가져와 구조 검사와 4방향 렌더, 설정된 얼굴 확대와 모션 프레임을 만듭니다. 종료 0은 해당 구조 검사와 증거 성공, 2는 검사 FAIL, 1은 실행/계약 BLOCKED입니다. Workbench 렌더는 구조 프리뷰이며 텍스처 표현·표정 자연스러움·관통·제품 동작을 보증하지 않습니다. `state.json`의 qa.report에서 결과와 로그를 찾습니다.
- 실제 디자이너 확인 후에만 `approve design --actor 승인자 --note "확인 내용"` 및 `approve appearance ...`를 기록합니다. 필수 Shape Key가 있으면 expression, 모션이 필수면 motion, 제품용이면 runtime 승인도 필요합니다. 표정 중간값·동작 전체 구간·실제 대상 엔진 확인을 기록합니다. AI가 승인자 이름을 임의로 넣지 않습니다.
- `gate`는 현재 파일·정책·검사기·보호 기준·렌더 해시·원본 해시·수동 승인·생성 예산을 확인합니다. `deliver`는 같은 Gate를 다시 호출한 뒤 새 폴더에 해당 GLB를 복사합니다. 검사 실패나 변경 후 이전 승인 재사용은 거부합니다. Blender에서 직접 출력하거나 JSON을 임의 조작하는 행위를 막는 보안 경계는 아닙니다.

`state.json`의 candidate, versions, references, attempts, qa, approvals, deliveries가 작업 이력입니다. 후보 파일은 수정하지 말고 사본을 수정하세요. 동일 프로젝트에서 동시에 작업하지 않습니다. `.writer-lock`은 이 CLI의 동시 쓰기만 막습니다. 프로세스 중단으로 남은 락은 모든 Writer 종료를 담당자가 확인하기 전 제거하지 않습니다. 재개는 status로 시작하고 실제 파일 및 미해결 작업부터 확인합니다.

## 선택 설정 및 Hook

MCP의 [검토용 설정](../templates/blender-mcp.toml)은 2026-11-24 PyPI에서 확인한 mcp-for-blender 2.3.1을 후보로 고정합니다. 안전 모드와 텔레메트리 비활성화를 요청하지만 실제 보안 샌드박스는 아닙니다. 기존 서버·애드온·uvx 경로·버전을 확인한 담당자만 승인 후 병합하세요. 파일을 두는 것만으로 활성화되지 않습니다. 읽기/사본 수정/재가져오기 테스트까지 해야 연결 PASS입니다. Computer Use와 Tripo Plugin은 실제 앱에서 선택·인증합니다.

[Hook 예제](../templates/hooks.example.json)는 자동 활성화하지 않습니다. 지원되는 Codex에서 절대 실행 경로로 수정하고 프로젝트 `.codex/hooks.json`에 승인 후 적용, `/hooks`로 신뢰 확인합니다. 명시적으로 납품 확인 세션에서 `OMOTION_RELEASE_HOOK=1`, `OMOTION_PROJECT=실제 절대경로`를 설정했을 때 Stop 어댑터가 gate를 호출합니다. 실패 시 한 번만 계속해서 차단 사유를 보고하도록 요청합니다. Hook이 실행되지 않아도 deliver는 자체 검사합니다. Codex 실제 Hook 실행은 NOT_RUN입니다.

[ComfyUI 사용법](../workflows/comfyui/README.md)은 선택입니다. Charakuru 및 Record & Replay는 [출처 매핑](SOURCE-MAPPING.md)을 참조하세요.

## 문제 해결

- Blender 경로가 없거나 실행 실패: 기존 QA를 통과로 재사용하지 말고 로그 확인. headless 렌더 GPU/디스플레이 지원 필요 시 담당자에게 이관.
- GLB 외부 리소스/포맷 오류: 승인된 Blender에서 self-contained GLB를 다시 출력하고 새 버전으로 등록.
- 보호 메시 실패: 변경 범위를 재검토하고 이전 후보 복원 또는 새 승인 범위로 작업. 보호 기준을 삭제해 통과시키지 않음.
- 디자인/동작이 부자연스러움: 해당 결함의 실제 화면을 보여 주고 국소 보정; 자동 시각 승인 금지.
- 이전 생성 상태 UNKNOWN: 실제 서비스 이력과 비용을 확인하기 전 재생성 금지.
