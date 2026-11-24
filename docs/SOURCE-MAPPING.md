# 공식 자료 → 제작 기능 매핑 (2026-11-24)

이전 조사와 이번 원문 확인을 연결한다. 기능 제공·실행 검증·사용권은 별개다. 외부 코드나 제한 라이선스 Skill/에셋을 복제하지 않았다.

| ID / 근거 | 확인한 방법과 적용 | 실제 파일 / 검증 |
|---|---|---|
| S01 [P2.0 튜토리얼](https://www.tripo3d.ai/tutorials/mesh-game-character-p-2) | 콘셉트 정제 후 베이스 메시, 지역 수정, UV, 재질, 리그, DCC/엔진 순서. 고밀도와 조립 비용을 고려하고 원본 특징을 보존한다. | PRODUCTION-GUIDE, EX-01; 외부 생성 NOT_RUN |
| S02 [Tripo × Astra](https://www.tripo3d.ai/ko/blog/gpt-6-astra-3d-character-workflow) (11/19 업데이트) | 바디/얼굴/헤어 분리, 접합면 참조, 바디 기준 정렬, 기존 리그 재사용, 표정 상태와 연속 변형 구분, 짧은 동작 후 국소 수정. | 제작 절차와 EX-02~06; static_offset.py 실제 제한 정적 편집 테스트, Blender 작업 NOT_RUN |
| S03 [Charakuru README](https://github.com/nanocle/Charakuru), [튜토리얼](https://github.com/nanocle/Charakuru/blob/main/docs/tutorial.md), [릴리스](https://github.com/nanocle/Charakuru/releases) | 헤어 포함 Head와 Body의 4방향 참조, 각 후보 비교 및 명시 선택, 후보 변경 때 사본 보존. 텍스처 분류와 물리 그룹을 분리하고 비율을 앞/옆에서 점검. 9개 Skill의 공개 설명만 확인. | harness.py의 버전/보호/원본 기록, EX-02,03,08; 실제 UI, 웨이트 전송, VRM·물리 미도입 |
| S04 [Charakuru 라이선스](https://github.com/nanocle/Charakuru/blob/main/LICENSE) | 매출 또는 누적 자금조달 1억 엔 이상 사업 이용에는 별도 서면 계약. 재배포 제한. 회사 적격성 미확인. | 배포 ZIP 내부/실행 미확인. 도입/복제 보류; 공개 방식의 독립 구현만 적용 |
| S05 [Tripo Codex Plugin](https://developers.tripo3d.ai/ko/docs/codex-plugin) | 공식 생성/게임용 에셋 기능, Node 20+, 브라우저 인증. 결과 모델·미리보기·작업 기록 활용. 생성마다 승인과 실제 크레딧 기록. | 기존 기능 재사용, reserve/reconcile/snapshot 연결; 공식 Skill 실제 로딩/생성 NOT_RUN |
| S06 [Blender MCP](https://github.com/ahujasid/mcp-for-blender), [PyPI](https://pypi.org/project/mcp-for-blender/) | UI/장면 조회, 구조 수정, 뷰포트. 2.3.1 후보 고정, localhost, safe mode, telemetry off 설정. 공식 Blender 도구가 아닌 커뮤니티 구현. | templates/blender-mcp.toml, SETUP; 설치·실제 장면 검증 NOT_RUN |
| S07 [ComfyUI-Tripo](https://developers.tripo3d.ai/ko/docs/comfyui-nodes) 2.0.0/API v3, [core Preview3D](https://github.com/Comfy-Org/ComfyUI/blob/master/comfy_extras/nodes_load_3d.py) | TripoAPIDraft 단일/멀티뷰, model_file vs MODEL_INFO, 후처리 연결. Refine/Stylize 제거. Preview3D는 core 버전에 따라 deprecated. | comfy_plan.py가 공급된 object_info로 API 초안 생성; 스키마 mock 2개 PASS, 실제 큐/호환성 NOT_RUN |
| S08 [Skills](https://learn.chatgpt.com/docs/build-skills), [Computer Use](https://learn.chatgpt.com/docs/computer-use) | 프로젝트 Skill, 실제 도구 확인, 중요한 수정 이후 화면/렌더. | SKILL.md, HARNESS, EX-10; 런타임 NOT_RUN |
| S09 [Hooks](https://learn.chatgpt.com/docs/hooks) | 프로젝트 신뢰·Stop 이벤트 JSON 계약 및 한 번의 계속 진행. GUI 출력 전체를 제어하지 못함. | release_hook.py, hooks.example.json; 어댑터 mock 2개 PASS, 실제 Codex NOT_RUN; 명시 gate 우선 |
| S10 [Record & Replay](https://learn.chatgpt.com/docs/extend/record-and-replay), [Plugins](https://learn.chatgpt.com/docs/skills-and-plugins) | macOS + Computer Use 지원 시 숙련자가 반복 작업(헤어 정렬 또는 웨이트 보정) 시연 → Skill 초안 → 기술 검토 → 두 번째 샘플 비교. 실제 기록 없이는 완료 아님. | 파일럿/배포 후보; NOT_RUN. 초기 ZIP 사용으로 충분하면 별도 Plugin 배포 보류 |

## 원작자 직접 사례 확인 한계

- https://x.com/Dstudio_ai/status/2098760566672417240 및 https://x.com/Dstudio_ai/status/2096475126942560677 : 이번 접근 403.
- https://www.youtube.com/watch?v=gewSYpOqzJA , https://youtu.be/AjbSRYIFhgE , https://youtu.be/58UpDAnbdkM : 원문 영상 재생 불가.

따라서 원작자의 Computer Use 사용 비율, 영상 결과 품질 및 작업시간은 검증되지 않았다. S02와 S03의 공개 문서에 근거한 제작 절차로 대체한다. 제한된 배포 키트 내용은 읽거나 실행하지 않았다.

## 재사용 결정

Tripo 생성/기본 리그/텍스처, Blender/MCP/Computer Use는 기존 도구를 사용한다. 자체 구현은 예산/작업 상태, 버전 보호, 제한 정적 수정, 기술 검사/렌더, 납품 Gate다. Charakuru의 9개 Skill은 기능 설계 비교만 수행했다. 실제 제품이 VRM이고 회사 이용권을 확인한 경우 기존 키트 사용과 자체 구현을 다시 비교한다. 사람의 디자인 승인과 실제 제품 규격은 대체하지 않는다.
