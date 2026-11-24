# Charakuru — 디자이너용 도입·실습 안내

> 원작자의 공개 문서를 기준으로 작성한 독립적인 도입 안내다. 키트 내부 코드·Skill·화면을 복제하지 않았다. 실제 실행은 NOT_RUN이다.

## 1. 설치 전 확인 (기술 담당자)

업무용 사용은 라이선스 확인 후에만 한다. [영문 LICENSE 정본](https://github.com/nanocle/Charakuru/blob/8eb22f6c6700dcc310896336596682594928024c/LICENSE) v1.2 기준으로 최근 종료 회계연도의 사업 전체 매출과 누적 조달 자금이 각각 1억 엔 미만이어야 표준 라이선스의 업무용 사용 조건을 충족한다. 어느 하나라도 이상이면 업무용 테스트도 별도 서면 계약이 선행되어야 한다. 사업 목적 대출 및 지배 기업 그룹 등 상세 산정은 정본과 담당 부서 확인이 필요하다. 현재 회사 적격성은 미확인이다.

공개 문서 읽기와 GitHub 내부의 허용된 Fork는 업무용 실행 허가와 별개다. 재배포 권한, 내장 donor·샘플·표정 자료의 독립적 사용 권한은 별도로 판단한다. 회사 조건이 미확인인 경우 설치·실행·업무 목적 배포본 내부 분석은 보류하고 [경로 B](START-HERE.md)를 이용한다. 권리자 문의처는 LICENSE 제11조에서 확인한다.

## 2. 공식 배포본과 연결

- [v1.1.1 Releases](https://github.com/nanocle/Charakuru/releases/tag/v1.1.1) (2026-11-02)
- [전용 배포 ZIP](https://github.com/nanocle/Charakuru/releases/download/v1.1.1/charakuru-1.1.1-2026-11-02T09-36-05-842Z.zip) — 일반 Source code ZIP이 아니다.
- [Technical Notes](https://github.com/nanocle/Charakuru/releases/download/v1.1.1/charakuru-1.1.1-technical-notes.en.md) · [Update Guide](https://github.com/nanocle/Charakuru/releases/download/v1.1.1/charakuru-1.1.1-update-guide.en.md)

공개 릴리스 메타데이터의 ZIP SHA-256은 `130efef11e087263729842b5523e67d660b33d160e8c118df1c96a9ce50faf3d` (12,024,159 bytes). 이전 다운로드 실패로 실제 파일 및 내부 내용은 검증하지 못했다. 다운로드 허용 후 담당자가 해시를 대조하고 보안 검사를 수행한다. Windows는 PowerShell `Get-FileHash -Algorithm SHA256 -LiteralPath "실제 ZIP 경로"`, macOS는 `shasum -a 256 "실제 ZIP 경로"`를 사용한다.

[공식 한국어 README](https://github.com/nanocle/Charakuru/blob/8eb22f6c6700dcc310896336596682594928024c/README.ko.md)의 요구 환경은 Node.js 22+, Chromium 브라우저, 이미지 생성·브라우저 제어를 지원하는 Codex, Tripo 로그인, Blender 5.2 및 VRM Add-on과 Blender MCP다. 릴리스 내부 문서가 다르면 해당 버전의 계약을 먼저 확인한다. 현재 회사 PC의 호환성은 NOT_RUN이다.

권한이 확인되면 별도의 승인된 로컬 폴더에 풀고 기존 키트의 AGENTS.md를 유지한다. 기술 담당자는 실제 Node/Blender 버전, VRM 애드온, 브라우저 조작, MCP 읽기 호출, 작업 폴더 권한을 확인한다. [일반 연결 안내](SETUP.md)를 참고하되 원작자 설치 계약이 우선이다. 원격 서비스·계정 비밀은 채팅에 입력하지 않는다.

Codex에서 압축을 푼 원작자 폴더를 열고 아래 요청을 보낸다.

```text
이 키트의 루트 AGENTS.md와 실제 포함된 제작 Skill을 읽어 주세요.
한국어로 안내하고 현재 환경과 연결된 도구만 확인해 주세요.
이미 승인된 설치 범위 안에서 로컬 앱의 실행 방법을 안내해 주세요.
추가 설치, 유료 생성, 외부 업로드 및 전역 설정 변경은 먼저 승인을 받으세요.
```

공개 튜토리얼에는 승인된 키트 폴더에서 `npm start` 후 로컬 브라우저의 `http://127.0.0.1:8766`을 열고 Settings → Language에서 한국어를 선택하는 흐름이 안내된다. 일반 실행에 별도 npm install이 필요 없다고 명시한다. 실제 설치본 확인 전에는 명령을 자동 실행하지 않는다. 로컬 포트를 외부에 공개하지 않는다.

## 3. 첫 제작 — 실제 원작자 화면과 함께 보기

아래 링크는 원작자의 공개 화면이다. 우리 테스트 캡처가 아니며 이미지 파일을 이 저장소에 재배포하지 않는다. 전체 [한국어 공식 튜토리얼](https://github.com/nanocle/Charakuru/blob/8eb22f6c6700dcc310896336596682594928024c/docs/tutorial.ko.md)을 함께 연다.

| 단계 | 디자이너 행동 | 공식 화면 |
|---|---|---|
| 시작 | 로컬 앱을 열고 작업할 프로젝트 선택 | [시작 화면](https://github.com/nanocle/Charakuru/blob/8eb22f6c6700dcc310896336596682594928024c/docs/images/ko/01-start.jpg) |
| 원본 | 권리가 있는 일러스트 등록, 보존 특징 전달 | [원본 등록](https://github.com/nanocle/Charakuru/blob/8eb22f6c6700dcc310896336596682594928024c/docs/images/ko/02-original.jpg) |
| 요청 | 앱의 다음 단계 요청문을 복사해 Codex에 전송 | [요청 창](https://github.com/nanocle/Charakuru/blob/8eb22f6c6700dcc310896336596682594928024c/docs/images/ko/03-request-images.jpg) |
| 참조 확인 | 얼굴·헤어·의상·좌우 비대칭 등 검수, 필요 시 한 장만 수정 | [참조 검수](https://github.com/nanocle/Charakuru/blob/8eb22f6c6700dcc310896336596682594928024c/docs/images/ko/05-images-front.jpg) |
| 후보 선택 | 머리와 몸 각각 후보를 돌려 보고 확정 | [후보 비교](https://github.com/nanocle/Charakuru/blob/8eb22f6c6700dcc310896336596682594928024c/docs/images/ko/09-candidates-head.jpg) |
| 재질 및 비율 | 파트 조립 후 앞/옆에서 비교, 승인 | [정면](https://github.com/nanocle/Charakuru/blob/8eb22f6c6700dcc310896336596682594928024c/docs/images/ko/14-placement-front.jpg) · [측면](https://github.com/nanocle/Charakuru/blob/8eb22f6c6700dcc310896336596682594928024c/docs/images/ko/15-placement-side.jpg) |
| 동작 및 저장 | 리그·표정·물리 확인, VRM 및 편집본 보관 | [동작 검수](https://github.com/nanocle/Charakuru/blob/8eb22f6c6700dcc310896336596682594928024c/docs/images/ko/17-review-walk.jpg) |

앱의 진행 버튼은 요청문을 만들어 줄 뿐이다. 복사한 요청을 채팅에 실제 전송하고 앱을 열어 둔다. 후보나 외형은 AI가 대신 최종 승인하지 않는다.

### 원작자 제작법에서 배울 점

공개 사례는 머리(헤어 포함)·몸 각각 네 방향의 참조와 전신 삼면도를 활용한다. 참조부터 사람이 검수하면 생성 이후의 수정 부담을 줄일 가능성이 있다. 후보는 각각 네 개를 비교하는 예시이며, 고정 필수 생성 횟수나 회사 예산이 아니다. 생성 전 실제 크레딧과 옵션을 확인한다. 한국어 튜토리얼은 P2.0과 사각면 25,000개를 예시로 제시하지만 회사 납품 규격으로 채택하지 않는다.

비율 검수는 앞과 옆에서 목 접합 및 머리 크기를 확인한다. 재질 일관성을 위한 그룹과 움직임을 위한 메시 분리를 별도로 판단한다. 예컨대 치마와 다리는 함께 색상 참조를 쓰되 치마의 물리는 분리할 수 있다. 4K 재텍스처 및 기존 본 위치·내장 donor의 웨이트 활용은 원작자 제작법의 일부이며 모든 모델에 적합한지는 검증해야 한다. 내장 자료는 키트 밖으로 추출하지 않는다.

v1.1.1 릴리스는 손가락 웨이트, upperChest, 기본 포즈와 충돌, 표정 26종 및 기존 모델 업데이트 개선을 설명한다. README에는 이전 표정 제한도 남아 있다. 실제 배포본에서 표현 가능 범위를 재확인하고 시선·립싱크를 지원한다고 단정하지 않는다. VRM 출력과 제품 런타임 적합성은 별개다.

## 4. AI에게 추가로 요청할 예제 (자체 작성)

앱이 생성하는 공식 단계 요청을 우선 사용한다. 아래는 해당 요청에 붙이는 보조 문구다.

**참조 이미지 하나 수정**
```text
캐릭터의 왼쪽 측면 머리 참조만 수정해 주세요. 헤어 길이와 얼굴 특징은 원본과 맞추고 다른 방향 이미지 및 승인본은 유지해 주세요. 변경 후 같은 방향으로 비교해 주세요.
```

**비율 및 국소 수정**
```text
채택한 얼굴과 의상은 유지하고 목 접합과 앞머리 위치만 확인해 주세요. 먼저 정면·측면의 실제 결과와 수정 계획을 보여 주세요. 승인된 사본에서 수정하고 기존 프로젝트를 보존해 주세요.
```

**표정과 동작 확인**
```text
현재 키트 버전에서 실제 지원하는 표정과 동작을 확인해 주세요. 중립, 눈 감기, 미소 및 걷기에서 어깨·무릎·헤어·치마의 변형을 보여 주세요. 수행하지 못한 검사는 미실행으로 남겨 주세요.
```

## 5. 실패 대응

| 상황 | 행동 |
|---|---|
| 앱이 시작되지 않음 | Node 버전·실행 폴더·공식 오류 안내 확인. 임의 설치나 권한 완화 금지 |
| 요청 복사 후 아무 일도 없음 | Codex에 요청을 전송했는지, 앱이 열려 있는지 확인 |
| Windows에서 start 요청 차단 | 업데이트된 앱의 begin 요청을 다시 받는다. 재차 차단되면 우회하지 않고 담당자에게 전달 |
| 생성 실패/시간 초과 | 기존 Tripo 작업과 크레딧 이력을 먼저 조회, 무단 재제출 금지 |
| 후보가 마음에 들지 않음 | 참조 또는 해당 파트 후보만 재검토. 이미 후처리한 경우 원작자 앱의 사본 분기 기능을 우선 확인 |
| 동작이 부자연스러움 | 발생 부위와 포즈·프레임을 명시하고 디자이너에게 수정 판단 요청 |
| 재개/PC 이동 | 전체 작업 폴더 및 편집용 Blend와 내보내기 파일을 보존. project.charakit 하나만 옮기지 않음 |

[기존 모델 업데이트 및 복구용 공식 가이드](https://github.com/nanocle/Charakuru/releases/download/v1.1.1/charakuru-1.1.1-update-guide.en.md)는 파일 확보 후 해당 버전에 맞게 사용한다. 아직 내용을 확인하지 못했다.

## 6. 완료와 다음 행동

첫 실습에서 실제 원본, 채택 후보, 완성 VRM/Blend, 기술 및 외형 검수 결과를 승인된 작업 위치에 기록한다. 제품이 VRM을 사용하지 않으면 변환 및 제품 적용을 별도 검증하며 포맷 이름만 바꾸지 않는다. [실습 비교](PILOT.md)로 채택 여부를 판단한다.
