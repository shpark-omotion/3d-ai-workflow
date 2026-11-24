# 설치 및 연결 — 기술 담당자용

## 기본 경로

Codex 데스크톱 + 사용 가능한 Astra + Tripo Studio(웹) + Blender. Blender MCP는 실제 AI 조작용 권장 경로. Computer Use는 지원 시 선택. 새 작업용 PC를 강제하지 않으며 기존 환경을 재사용한다. 회사 정책과 설치 권한, 사용 가능한 클라이언트·계정·OS를 먼저 확인한다.

## 1. 읽기 전용 환경 조회

프로젝트에서 아래를 실행한다(Python 3.9+ 필요). Windows에서는 `py -3 scripts/doctor.py`, macOS/Linux에서는 `python3 scripts/doctor.py`. 필요하면 `--json`으로 구조화 결과 확인. Python이 없으면 수동으로 확인한다. 스크립트는 설치·네트워크·인증 조회·설정 변경을 하지 않는다. PATH에서 발견된 실행 파일과 미확인 런타임을 구분한다. GUI 설치 여부는 PATH 검사만으로 판단하지 않는다.

Codex에 다음을 요청한다.

```text
scripts/doctor.py를 실행 가능한 경우 실행해 주세요. 기존 앱/설정은 변경하지 마세요.
Astra의 실제 모델 표시, Blender 앱 버전, Tripo 로그인, MCP 도구 목록, Computer Use 활성화 상태, 로컬 Skill 로딩을 각각 확인해 주세요.
증거가 있는 것만 PASS, 확인할 수 없는 것은 NOT_RUN 또는 BLOCKED라고 보고해 주세요.
```

## 2. Tripo

[Tripo Studio](https://studio.tripo3d.ai/)에 사용 승인된 계정으로 직접 로그인한다. 처음에는 수동 웹 생성만으로 충분하다. 계정 공유나 비밀키 채팅 입력 금지.

선택: [공식 Codex Tripo 3D Plugin](https://developers.tripo3d.ai/ko/docs/codex-plugin). 공식 가이드는 Node.js 20+ 및 Codex의 Plugins Directory에서 설치/활성화를 안내한다. 플러그인 발견 여부와 인증은 실제 PC에서 확인한다. 첫 테스트에서 생성 버튼을 누르지 않고 제공 기능과 비용 표시를 확인한다. Studio와 Plugin 중 하나만 사용한다. 과금·외부 전송 동의 후 실제 생성한다.

## 3. Blender MCP

[커뮤니티 구현](https://github.com/ahujasid/mcp-for-blender)이다. Blender Foundation 공식 도구는 아니다. 임의 Blender Python 실행 기능이 있으므로 의존성 출처·버전·회사 정책을 검토하고 승인받는다. 기존 애드온·설정 백업 후 적용한다. 동일 이름/포트 중복 서버를 만들지 않는다. 로컬 인터페이스에서만 연결하고 인터넷에 포트를 노출하지 않는다. 외부 에셋 공급자 기능은 필요한 경우에만 별도 승인한다.

1. Blender와 [uv](https://docs.astral.sh/uv/) 설치 여부를 확인한다. 공식 README의 요구 버전·릴리스·설치 절차를 대조한 뒤 승인된 버전을 선택한다. 버전 고정 및 실제 검증 전까지 재현 가능한 설치 완료라고 하지 않는다.
2. 공식 README 수동 설치 예시: `uvx mcp-for-blender install-addon`. **이 명령은 패키지 다운로드/실행 및 애드온 파일 변경 가능성이 있으므로 승인 후에만 실행한다.** 실환경에서는 검토한 버전으로 고정한다.
3. Blender `Edit → Preferences → Add-ons`에서 MCP for Blender 활성화. 3D View에서 N 키, MCP 탭의 서버 상태 확인.
4. Codex 데스크톱 `Settings → MCP servers → Add server`에서 STDIO 서버로 설정. 공식 예시는 이름 `blender`, 명령 `uvx mcp-for-blender`. 실제 설치 시 승인 버전·정확한 경로를 적용한다. CLI 대체 예시 `codex mcp add blender -- uvx mcp-for-blender`는 설정 쓰기이므로 승인 전 금지. 기존 설정이 정상이라면 재사용한다.
5. 재시작 후 테스트용 Blender 장면에서 실제 읽기 전용 도구를 호출한다. 현재 오브젝트 이름과 타입이 디자이너 화면과 일치해야 PASS. 포트가 열려 있거나 서버 등록만 된 상태는 PASS가 아니다.

```text
Blender MCP의 실제 장면 조회 도구로 열린 테스트 장면을 읽어 주세요.
Scene 및 Object 이름과 유형, Armature 유무를 보고하고 어떠한 변경이나 코드 실행도 하지 마세요.
실제 호출 결과가 없으면 연결 성공으로 보고하지 마세요.
```

실패 시: Blender 실행/애드온 활성/서버 상태/중복 인스턴스/uvx PATH/클라이언트 재시작 순서로 확인. 기존 환경 자동 수정 금지.

## 4. Computer Use(선택)

[공식 안내](https://learn.chatgpt.com/docs/computer-use)에 따라 지원 지역·클라이언트·권한을 확인한다. 데스크톱 Work 또는 Codex의 Settings → Computer use에서 사용할 앱을 확인한다. macOS는 화면 기록·손쉬운 사용 권한이 필요할 수 있고 Windows는 활성 화면을 점유한다. 승인되지 않은 앱은 제어하지 않는다.

테스트: 실제 Blender 창을 보고 현재 장면과 화면을 설명하게 한다. 변경하지 않는다. 브라우저 제어도 따로 확인한다. 미지원이면 Tripo 사이트는 사람이 조작하고 Blender는 MCP 또는 수작업으로 처리한다. Astra 모델 선택만으로 기능이 활성화된다고 판단하지 않는다.

## 5. Skill과 작업 폴더

프로젝트 루트에서 `.agents/skills/character-production/SKILL.md`가 발견되는지 확인한다. 동명 Skill 충돌과 기존 AGENTS.md의 범위를 확인한다. 재시작 후에도 미발견이면 직접 제작 가이드 전달로 대체하고 `SKILL_LOADED=NOT_RUN` 또는 실패로 남긴다. 회사 데이터는 승인된 작업 폴더(가능하면 저장소 밖)에 둔다. 접근 제한 때문에 내부 폴더가 필요하면 승인된 `work/`만 사용하고 Git 상태를 별도 확인한다. `.gitignore`는 보안 경계가 아니다.

## 6. 설치 종료 기준

`templates/runtime-check.md`를 채운다. 필수: 로컬 파일 작업 경로, Tripo 수동 생성 경로, Blender 수동 import, 실제 AI 작업 경로, Skill 발견/대체 경로. AI 수정 경로가 모두 불가능하면 수동 가이드로만 사용하며 AI 자동화 READY를 주장하지 않는다. 생산 자산 투입 전 허가된 샘플로 실험한다.

Hook, ComfyUI, Charakuru는 필수 설치 대상이 아니다. P3/P4 승인과 별도 검증을 거친다.

## 7. 최초 설치 확인과 인수인계

- Windows/macOS의 실제 설치 버전, 사용 클라이언트, 승인한 MCP 배포 버전 및 설정 범위를 기록한다. 기존 설정 파일은 보호하고 검토 전 자동 다운로드·실행하지 않는다.
- 실제 GUI에서 테스트용 기본 큐브의 이름을 바꿔 둔 다음 AI가 읽기 전용 도구로 이름을 일치시켜 보고하는지 확인한다. 설정 등록만으로 통과하지 않는다.
- 연결 확인 후 별도 승인된 테스트 사본에서 위치를 한 번 변경하고 새 파일로 저장한다. 원본은 그대로인지, 변경된 사본을 다시 열 수 있는지 확인한다. 이 테스트는 유료 생성이나 회사 원본 업로드 없이 가능하다.
- 화면 조작과 파일 도구에 동일한 작업 경계가 적용되는지 확인한다. 지원하지 않는 기능은 수동 절차로 넘기고, 도구 권한·승인 경계 검증을 생략하지 않는다.
- 디자이너에게 필요한 것은 [시작 가이드](START-HERE.md), 승인된 작업 폴더, 연결 확인 결과다. 기술 담당자는 환경과 설치 버전·실패 대응을 별도로 유지한다.

## v0.2 추가 준비

[검토용 MCP 설정](../templates/blender-mcp.toml)을 참고한다. PyPI 2.3.1은 확인된 버전 후보이지 이 PC의 호환 검증 결과가 아니다. 기존 설치를 확인하고 공식 배포 버전 및 애드온을 일치시킨 뒤 별도 승인으로만 설정한다. telemetry off와 safe mode를 적용하되 샌드박스로 보지 않는다. [HARNESS](HARNESS.md)의 실제 Blender 경로와 테스트를 확인한다. 자동 설치는 제공하지 않는다.
