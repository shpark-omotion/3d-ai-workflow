# v0.1 검토본 검증 기록 — 2026-11-24

## 이번 검증

- 환경: Linux 작업 컨테이너 / Python 3.13.5 / Git 2.47.3. 디자이너 PC 아님.
- 기존 초안 ZIP 18개 파일 복원 및 전체 텍스트 검토. 기존 제작 순서·기술 조사·양식 재사용.
- `python3 -m unittest discover -s tests -v`: 4개 PASS (기존 3개 + 필수 가이드/양식 누락 검출 1개).
- `python3 scripts/doctor.py --json`: 실행 PASS. 필수 파일 11개 존재. codex/blender는 PATH에서 발견되지 않음. 런타임 점검은 모두 NOT_RUN.
- Markdown 상대 링크 19개: 누락 0건. Skill frontmatter 구조 PASS(실제 로딩 아님).
- 임시 Git 저장소에서 `.gitignore` 제외 20개·허용 6개 사례 PASS. 작업용 Blender 폴더 제외 누락을 보완했다.
- 전체 텍스트 수동 검토 및 일반적인 비밀키/토큰/내부 설정 문자열 패턴 검사: 발견 없음. 비밀정보 부재나 공개 적격성을 완전히 보증하는 검사는 아니며 회사 정책 확인은 별도다.
- 공식 자료는 이전 리서치 확인 결과를 재사용했다. 이번 수정에서 외부 도구 버전 및 라이선스를 새로 검증하거나 설치하지 않았다. 설치 직전 원문을 다시 확인한다.

## 아직 확인하지 않은 범위

- 실제 Astra 선택, Computer Use, Blender MCP 장면 조회 및 수정, Tripo 생성, Skill 자동 호출, Blender 파일 재가져오기, 실제 사용자 및 제품 테스트: NOT_RUN.
- 설치 자동화, 실제 QA 검사기, Hook, ComfyUI 워크플로: 미구현.
- 독립 검토: NOT_RUN. 위 결과는 작성자 자체 검증이다.
- 원격 반영: 최초 파일 생성 요청이 403으로 거절되어 BLOCKED. 재조회에서 빈 저장소 상태를 확인했다. 공개 범위는 변경하지 않았다.
- 운영 적용, 유료 생성 및 회사 자산 업로드: 미실행.

## v0.2 Writer 검증 (2026-11-24)

위 v0.1 원격 403 기록은 해결됐으며 base d59b321f3749481d2ad6e31659f19cd6f81d45e0에 반영되었다. v0.2는 별도 구현 브랜치에서 검토한다.

- Linux/Python 3.13.5에서 `python -m unittest discover -s tests -v`: 총 21개, 17 PASS, Blender 통합 4 skip.
- 테스트 자체 생성 GLB를 trimesh로 독립 로드: Head/Body/Hair 노드, 12면 닫힌 공유 큐브 메시 확인. 실제 정적 Hair 위치 변경 및 원본/비대상 노드/BIN 보존 단위 테스트 PASS.
- Gate·Hook·ComfyUI 테스트에서 외부 서비스와 Blender 보고서는 mock이다. 실제 Blender 검사 결과라고 해석하지 않는다.
- Blender/Codex 실행 파일 없음, bpy 미설치. 공식 바이너리/모듈 확보 시도 실패. 실제 QA·렌더·리그·표정·Tripo 생성·Computer Use·Skill 로딩·Hook·ComfyUI 실행·제품·디자이너 파일럿 NOT_RUN. 유료 작업/회사 데이터 업로드 없음.
- [EXAMPLES](EXAMPLES.md)의 EX별 판정과 [SOURCE-MAPPING](SOURCE-MAPPING.md)을 참조한다. 독립 Reviewer는 미실행.
