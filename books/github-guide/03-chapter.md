# 3장 처음 한 번만 하는 설정

GitHub 계정, Git, GitHub CLI가 준비되어야 합니다. 이 문서는 CLI 기준이므로 `gh` 명령어를 사용합니다. 

### GitHub CLI 로그인

**이 단계는 직접 실행하세요.** 브라우저 인증과 계정 권한이 걸려 있으므로 AI에게 토큰이나 인증 코드를 맡기지 않습니다.

Terminal 복사
```bash
    gh auth login --web
    gh auth status
```
### Git 사용자 이름과 이메일 확인

Terminal 복사
```bash
    git config --global user.name
    git config --global user.email
```
값이 비어 있으면 아래처럼 설정합니다. 이메일은 GitHub 계정 이메일 또는 GitHub의 private noreply 이메일을 사용해도 됩니다.

Terminal 복사
```bash
    git config --global user.name "내 GitHub 이름"
    git config --global user.email "내이메일@example.com"
```
**SSH vs HTTPS** : 이 가이드는 `gh auth login --web`(HTTPS)를 기준으로 합니다. SSH 키를 이미 쓰고 있다면 그대로 SSH 주소로 clone해도 됩니다. 둘 중 하나만 쓰면 충분하므로 처음엔 HTTPS가 더 간단합니다.

### AI에게 환경 점검시키기

Claude Code / Codex / Cursor에 붙여넣기 복사
```bash
    이 컴퓨터에서 GitHub 협업을 할 준비가 되었는지 확인해줘.
    다음 항목을 검사하고, 부족한 것이 있으면 설치/설정 방법을 초보자도 이해할 수 있게 안내해줘.
    
    확인할 것:
    1. git 설치 여부와 버전
    2. gh(GitHub CLI) 설치 여부와 버전
    3. gh auth status 로그인 여부
    4. git user.name / user.email 설정 여부
    5. 현재 작업 폴더 위치
    
    주의:
    - 내 GitHub 인증 코드, 토큰, 비밀번호는 절대 대신 입력하지 마.
    - 실제 변경 명령을 실행하기 전에는 어떤 명령을 실행할지 먼저 보여줘.
```