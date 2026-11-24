---
name: character-production
description: 승인 원본을 기준으로 3D 캐릭터의 제작, 기존 모델의 국소 수정, 리깅·표정·동작 및 납품 검수를 수행한다. Tripo, Blender MCP/Python, Computer Use의 실제 가용 도구를 선택한다. 일반 소프트웨어 개발이나 단순 기술 질문에는 사용하지 않는다.
---

# Character production

프로젝트 루트의 AGENTS.md, docs/PRODUCTION-GUIDE.md, docs/QUALITY-GUIDE.md를 읽는다. 최초 실행 또는 재개 시 실제 도구와 작업 폴더 확인. 템플릿은 `templates/`에 있다. AI 초보자에게는 한 번에 필요한 행동과 선택지만 한국어로 안내한다.

## Intent and state

- 신규 제작: plan → reference → generate → design review → assembly → technical/rig → expressions/motion(필요 시) → export QA → artist approval.
- 부분 수정: baseline audit → scoped repair → regression review → affected QA → artist approval. 불필요한 재생성 금지.
- 검수 전용: 읽기 전용 우선. 원본/납품본 수정, 유료 생성 금지. 시험이 필요하면 작업 사본 승인 후 진행.
- 재개: `run-state.md`를 읽고 실제 파일·버전·작업 ID·승인 범위를 재확인. 미확인 과금 작업을 다시 제출하지 않는다.

## Runtime and safety

1. 사용 모델·Skill 로딩·Computer Use·MCP·Plugin은 요청과 실효를 구분한다. 가능한 도구를 실제 목록/호출로 확인한다. 미지원이면 수동 대안 제시.
2. 제작 카드를 채운다. 필수 유지 특징, 허용 변경, 대상 포맷/리그, 외부 전송·비용 상한, 승인자 및 작업 경로를 확인한다. 미정 요구사항은 납품 PASS에 사용하지 않는다.
3. 원본/승인본 보존. 작업 폴더와 파일의 실제 경로를 확인하고 모든 변경은 승인된 작업 사본에만 수행. 비용·외부 제공·전체 재생성·파괴적 변경·환경 변경은 명시 승인 범위 내에서만. 새로운 후보는 기본 1개까지 계획하고 생성 승인 확인.
4. UI 관찰에는 Computer Use, 구조 읽기/수정에는 승인된 Blender MCP 또는 검토된 Python, 생성에는 실제 연결된 Tripo 경로 하나를 선택한다. 임의 스크립트 설치, 외부 에셋 취득, 인증정보 요청, 원격 게시 금지.

## Stage gates

| 단계 | 필수 결과 | 진행 조건 |
|---|---|---|
| Plan/reference | 제작 카드와 다각도 참조, 누락 방향, 실제 도구 | 원본 및 승인 범위 확정 |
| Generate | 원본 파일, 작업 ID(가능한 경우), 비용 상태, 비교 렌더 | 유료 작업 승인 및 성공 확인 |
| Design review | 불일치 부위와 근거, 수정 제안 | 디자이너 디자인 승인 |
| Assembly/repair | 버전 사본, 변경 부위, 동일 조건 전후 비교 | 정상 부위 회귀 없음 또는 별도 승인 |
| Rig/face/motion | 필요한 포즈·표정 테스트 근거 | 제품 규격과 필수 항목 결과 확인 |
| Export QA | 실제 출력, 재가져오기, 기술 상태, 미해결 결함 | 필요한 검사 PASS 및 규격 충족 |
| Artist approval | 디자이너 승인 기록 | 최종 상태 APPROVED, 그 전에는 CANDIDATE |

단계별 결과를 보고하고 다음 단계가 승인 범위 내이며 선행 Gate를 충족하면 이어갈 수 있다. 불필요한 확인을 반복하지 않는다. 디자인 판단, 예산 확대, 파괴적 변경 및 최종 승인은 사람이 결정한다. 기술 검사는 별도 증거가 필요하며 Skill 자체가 검사를 수행했다고 간주하지 않는다. 파일 버전 또는 해시와 검사 근거를 연결한다. 변경 후 영향받은 검사와 디자인 승인은 재확인한다.

## Failure routing

레퍼런스 불일치 → 참조 보강. 전체 형태 불일치 → 모델/생성 전략 검토. 국소 형태 → 해당 파트만. 웨이트/리그 → 동일 포즈 재검사. 텍스처 → UV/재질 검사. 외부 작업 상태 불확실 → 상태 확인. 실패 2회 연속 → 자동 복구 중단. 상세 기준은 QUALITY-GUIDE. 새 생성/재생성 비용은 별도 승인.

## Report

한국어로 목적, 실제 실행/수정 범위, 후보 경로, 증거, PASS/FAIL/NOT_RUN/NOT_REQUIRED, 디자인 승인 상태, 비용·재시도 및 다음 행동을 기록한다. 독립 검수자가 따로 있는 경우 Writer 자기 검토와 혼동하지 않는다. 기술 검증·미적 승인·실제 제품 적합성을 구분한다.

## Capability fallback

Tripo 로그인 및 유료 실행이 불가하면 생성은 사용자에게 넘긴다. Blender 제어가 불가하면 조작 방법을 제시하고 실제 실행은 NOT_RUN으로 기록한다. Skill 자동 로딩이 불가하면 저장소 지침을 읽은 사실과 로딩 실패를 구분한다. 단순 수동 안내를 자동화 완료라고 판정하지 않는다.
