# Omotion 3D AI Workflow — 기술 리서치 및 도입 가이드

기존 3D 제작 도구와 AI를 활용해 디자이너가 원하는 캐릭터를 더 쉽게 제작·수정·검수하도록 돕는 자료 모음이다. 자체 제작 플랫폼 개발 프로젝트가 아니다.

> 도입 검토본 · 2026-11-24. 실제 회사 PC에서의 설치, 유료 생성, 제작 결과 및 생산성은 아직 검증하지 않았다.

## 처음 시작하는 디자이너

[시작 가이드](docs/START-HERE.md)에서 현재 상황에 맞는 경로를 선택한다.

| 경로 | 언제 선택하나 |
|---|---|
| A. [Charakuru 활용](docs/CHARAKURU-GUIDE.md) | 회사 사용 권한과 VRM 적합성이 확인된 경우, 원작자 도구를 그대로 우선 평가 |
| B. [기존 Tripo + Codex + Blender](docs/PRODUCTION-GUIDE.md) | A가 아직 허용되지 않거나 기존 GLB/FBX 제작 환경을 유지해야 하는 경우 |

최초 연결은 기술 담당자가 지원한다. 디자이너는 원본과 수정 요구를 정하고, 실제 후보·동작을 확인해 승인한다.

## 필요한 자료

| 목적 | 문서 |
|---|---|
| 도구 선택과 재사용 판단 | [RECOMMENDATION](docs/RECOMMENDATION.md) |
| 원작자 키트의 화면·설치·사용 예제 | [CHARAKURU-GUIDE](docs/CHARAKURU-GUIDE.md) |
| 기존 도구 연결 및 오류 해결 | [SETUP](docs/SETUP.md) |
| 일반 제작·부분 수정·품질 확인 | [PRODUCTION-GUIDE](docs/PRODUCTION-GUIDE.md) · [QUALITY-GUIDE](docs/QUALITY-GUIDE.md) |
| 출처와 기존 기술 조사 | [RESEARCH](docs/RESEARCH.md) |
| 실습 및 비교 기록 | [PILOT](docs/PILOT.md) |
| 지원 범위와 남은 결정 | [ROADMAP](docs/ROADMAP.md) · [VALIDATION](docs/VALIDATION.md) |

## 제공 범위

기존 공식 도구와 Skill 활용법, 한국어 안내, 복사 가능한 요청문, 연결 진단 및 실습 계획을 제공한다. Charakuru는 원작자 공식 배포본을 별도로 받으며 이 저장소에 포함하지 않는다. 자체 Skill과 환경 조회기는 경로 B의 선택 보조 수단이다. 원작자 프로젝트에 기존 AGENTS.md나 Skill을 덮어쓰지 않는다.

[기존 v0.2 PoC Draft PR #1](https://github.com/shpark-omotion/3d-ai-workflow/pull/1)은 별도로 보존한다. 실제 필요성이 확인되기 전에는 자체 UI·리깅·QA·상태관리·Hook의 추가 개발이나 병합을 진행하지 않는다.

회사 내부 자료, 작업 에셋, 계정 정보, 비용 및 평가 결과는 승인된 비공개 작업 위치에 저장한다. 공개 Git에는 넣지 않는다.
