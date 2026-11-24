# 기술 리서치와 근거 — 2026-11-24

기존 실전 가이드 v2.0과 공개 자료를 바탕으로 요약. 공식 설명은 기능 제공 근거이며 회사 환경 동작 또는 품질 개선의 증거는 아니다.

| 자료 | 확인 내용 | 적용 |
|---|---|---|
| [Tripo P2.0 공식 튜토리얼](https://www.tripo3d.ai/tutorials/mesh-game-character-p-2) | 참조 정제, P2.0, 멀티뷰, 국소 메시 편집, UV·PBR·리깅 및 후처리. 한국어 페이지 재접근 실패, 영문 원본 확인 | 디자인 우선·부분 수정·제품 검증 |
| [Tripo × Astra](https://www.tripo3d.ai/ko/blog/gpt-6-astra-3d-character-workflow) | 몸·머리·헤어 분리 생성, Blender MCP 조립·리깅 및 모션 사례 | 분리 생성은 필요 시 선택 |
| [Tripo Codex Plugin](https://developers.tripo3d.ai/ko/docs/codex-plugin) | Codex에서 설치·인증, Node.js 20+ 안내 | Studio 대체 경로 |
| [Tripo ComfyUI](https://developers.tripo3d.ai/ko/docs/comfyui-nodes) / [GitHub](https://github.com/Tripo-Developer/ComfyUI-Tripo) | 공식 노드, 이미지/멀티뷰 생성, 후처리·리깅 등 | P4 비교; 외부 API 과금 및 데이터 전송 확인 |
| [Blender MCP](https://github.com/ahujasid/mcp-for-blender) | 커뮤니티 구현, 설치 명령 및 Codex STDIO 연결 안내, Blender Python 및 장면 조회 도구 | 실제 PC에서 버전 고정·보안·연결 검증 |
| [Computer Use](https://learn.chatgpt.com/docs/computer-use) | 지원 환경에서 데스크톱 앱 조작, Windows 활성 화면 점유 | 선택, 실제 앱별 권한 확인 |
| [Skills](https://learn.chatgpt.com/docs/build-skills) | 저장소 `.agents/skills` 탐색 및 SKILL.md 형식 | P2 로컬 Skill 초안 |
| [Hooks](https://learn.chatgpt.com/docs/hooks) | 런타임 이벤트 기반, 사후 이벤트는 완료된 부작용을 취소하지 못함 | P3 검사기 검증 후 |
| [Charakuru](https://github.com/nanocle/Charakuru) / [LICENSE](https://github.com/nanocle/Charakuru/blob/main/LICENSE) | VRM 중심 제작 도구, 9개 Skill 및 표정 지원 일부. 시선 애니메이션 제한. 매출/누적 자금조달 각각 1억 엔 기준, 어느 하나라도 이상이면 사업 이용 전 별도 계약; 재배포 별도 제한 | 회사 자격 확인 전 도입/복제 금지 |

## 기존 참고 사례 — 원문 재검증 미완료

- https://x.com/Dstudio_ai/status/2098760566672417240
- https://x.com/Dstudio_ai/status/2096475126942560677
- https://www.youtube.com/watch?v=gewSYpOqzJA
- https://youtu.be/AjbSRYIFhgE
- https://youtu.be/58UpDAnbdkM

이전 대화의 Computer Use 중심 사례는 도구 선택 가설로만 사용한다. 영상 전체 또는 X 원문을 이번 작업에서 재검증하지 않았으며, 특정 비율이나 생산성 수치를 검증된 사실로 채택하지 않는다. 도구 제공 사실과 회사의 실제 사용 현황은 구분한다.

## 도입 지원 관점의 재평가 (2026-11-24)

- [도구별 재사용 결정](RECOMMENDATION.md)과 [Charakuru 실습 안내](CHARAKURU-GUIDE.md)가 현재 추천 정본이다. 위 표의 기존 P3/P4 개발 계획은 과거 방향이며 현재 개발 범위가 아니다.
- 공개 [Charakuru 한국어 README](https://github.com/nanocle/Charakuru/blob/8eb22f6c6700dcc310896336596682594928024c/README.ko.md), [튜토리얼](https://github.com/nanocle/Charakuru/blob/8eb22f6c6700dcc310896336596682594928024c/docs/tutorial.ko.md), [라이선스](https://github.com/nanocle/Charakuru/blob/8eb22f6c6700dcc310896336596682594928024c/LICENSE), [v1.1.1 릴리스](https://github.com/nanocle/Charakuru/releases/tag/v1.1.1)를 직접 조회했다. 9개 Skill과 donor, UI는 공개 설명에 따른 제공 기능이다. 배포 ZIP 내부 및 실제 실행은 미검증이다.
- Tripo 공식 사례는 전신을 한 번에 만드는 경로와 Body/Head/Hair 분리 후 Blender로 조립하는 경로를 구분한다. Charakuru의 Head(헤어 포함)/Body 후보 방식은 다른 경로다. 어느 쪽이 더 좋은지는 동일 원본으로 비교한다.
- [Record & Replay](https://learn.chatgpt.com/docs/extend/record-and-replay)는 macOS와 Computer Use가 가능한 경우에만 반복 작업을 Skill로 기록할 후보로 둔다. [ComfyUI 공식 노드](https://developers.tripo3d.ai/ko/docs/comfyui-nodes)는 현재 문서상 2.0.0/API v3이며 기존 워크플로가 필요할 때만 연결한다.
- 이전 X 게시물과 영상 원문 접근 한계는 유지한다. 공식 화면 링크를 활용하되 이미지·코드·제작 자산을 복제하지 않는다. 실제 사례의 시간/품질 개선 수치는 입증되지 않았다.
