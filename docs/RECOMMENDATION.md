# 기술 선택 — 기존 도구 우선

2026-11-24 공개 자료 비교에 따른 추천이다. 실제 환경 성능이나 회사 도입 승인을 의미하지 않는다.

## 기본 선택

- 경로 A: 회사 사용 권한이 있고 VRM 1.0 결과가 제품 요구와 맞으면 Charakuru 전체 배포본을 변경 없이 우선 평가한다.
- 경로 B: 위 조건이 미확인/부적합이면 팀의 기존 Tripo Studio + Blender에 실제 사용 가능한 Codex/Astra, Blender MCP를 연결한다. 기존 작업본이 있으면 생성 없이 수정·검수부터 한다.
- Charakuru에서 사용하는 브라우저 조작 경로를 별도 Tripo Plugin이나 ComfyUI로 임의 교체하지 않는다. 동일 기능을 서로 다른 경로로 중복 호출하지 않는다.
- 새로운 Agent 서버, 자체 UI, 리깅 엔진, 자동 QA 플랫폼은 이번 범위 밖이다.

| 기술 | 역할 | 결정 / 근거 |
|---|---|---|
| [Charakuru](https://github.com/nanocle/Charakuru) | 사용자 승인, 후보 비교, VRM 제작 과정 | 전체 사용 우선 평가, 권한 및 실환경 미확인 |
| [Tripo P2.0](https://www.tripo3d.ai/tutorials/mesh-game-character-p-2) | 3D 생성·후처리 | 공식 기능 그대로 사용. 모델·옵션은 실제 환경 확인 |
| [Tripo × Astra](https://www.tripo3d.ai/blog/gpt-6-astra-3d-character-workflow) | 파트별 생성 후 Blender 제작 | B에서 얼굴·헤어 분리 및 기존 리그 활용 |
| [Tripo Codex Plugin](https://developers.tripo3d.ai/ko/docs/codex-plugin) | 자연어 생성·파일 저장 | B의 선택 경로. Node 20+, 실제 Plugin 및 로그인 확인 |
| [Blender MCP](https://github.com/ahujasid/mcp-for-blender) | 장면·메시·본 조회 및 편집 | 기존 연결 재사용, 커뮤니티 구현이므로 출처·권한 점검 |
| [Computer Use](https://learn.chatgpt.com/docs/computer-use) | 화면 확인과 시각적 조작 | 필요 시 사용. Windows 전경 점유, 앱별 승인; 브라우저 조작과 구분 |
| [ComfyUI-Tripo](https://developers.tripo3d.ai/ko/docs/comfyui-nodes) | 기존 이미지/멀티뷰 워크플로 연결 | 팀이 이미 ComfyUI/LoRA를 사용하는 경우에만. 문서 기준 2.0.0/API v3, 실제 노드 버전 대조 |
| [Skills](https://learn.chatgpt.com/docs/build-skills) | 반복 작업 전문 지침 | 원작자 Skill 우선. 자체 Skill은 B 또는 실제 공백에만 |
| [Hooks](https://learn.chatgpt.com/docs/hooks) | 특정 실행 이벤트에 검증 연결 | 반복 검수 누락이 증명될 때만. GUI 전체를 통제하지 못함 |
| [Record & Replay](https://learn.chatgpt.com/docs/extend/record-and-replay) | 숙련자 시연을 Skill로 전환 | macOS 및 Computer Use 지원 시 선택, Windows 지원 가정 금지 |

## 자체 산출물 처리

유지: 리서치·제작/검수 가이드·환경 조회기·기존 연결 안내. 선택: 자체 Skill, ComfyUI 연동. 보류: [v0.2 PoC](https://github.com/shpark-omotion/3d-ai-workflow/pull/1)의 상태관리, 정적 GLB 이동, Blender QA, 납품 Gate, Hook. PoC는 자기완결 GLB 중심이며 VRM·스킨·물리·표정 계약을 자동 보존한다고 볼 수 없다. 원작자의 프로젝트와 별도 상태 정본을 동시에 운영하지 않는다.

원작자의 내장 donor 및 제한 자료를 분리해서 재사용하지 않는다. 기존 키트가 해결한 제작 기능을 다시 구현하지 않는다. 실제 파일럿에서 반복되는 문제 하나가 확인되면 기존 도구 설정이나 간단한 연결부터 제안한다.

## 도입 결정 기준

| 판단 | 조건 |
|---|---|
| A 전체 채택 | 적법한 사용 + VRM/Blend 호환 + 실제 캐릭터 검수 + 팀이 운영 가능 |
| 일부 연결 | 기존 도구는 유지하고 필요한 연동만 개선할 수 있음 |
| B 유지 | 권한·포맷·품질·비용·사용성이 A에 부적합 또는 미확인 |

최종 품질 기준과 실제 제작은 3D 팀이 담당한다. 기술 담당자는 초기 설정과 비교 실험만 지원한다. [실습 계획](PILOT.md)에 결과를 기록한다.
