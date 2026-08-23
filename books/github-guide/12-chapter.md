# 12장 자주 막히는 상황

막혔을 때는 에러 메시지를 지우지 말고 그대로 복사해서 AI에게 설명을 요청합니다.

`gh: command not found`

GitHub CLI가 설치되어 있지 않습니다.

AI에게 설치 요청 복사
```bash
    현재 운영체제에 GitHub CLI(gh)를 설치하는 방법을 안내해줘.
    가능하면 공식 설치 방법을 기준으로 하고, 설치 후 gh --version과 gh auth status 확인까지 도와줘.
```
`fatal: not a git repository`

현재 위치가 Git 프로젝트 폴더가 아닙니다. `pwd`, `ls`로 위치를 확인하고 clone한 폴더로 이동합니다.

Terminal 복사
```bash
    pwd
    ls
    cd REPO
```
push가 거절됩니다

대부분 원격 저장소에 새 변경이 먼저 올라왔거나, 내 branch에 push 권한이 없을 때 발생합니다.

AI에게 진단 요청 복사
```bash
    git push가 실패했습니다. 아래 에러를 읽고 원인을 설명해줘.
    
    [에러 메시지 붙여넣기]
    
    원하는 출력:
    1. 원인
    2. 안전한 해결 순서
    3. 실행할 명령어
    4. 작업 내용이 사라질 위험이 있는 명령어가 있다면 경고
```
merge conflict가 났습니다

같은 부분을 서로 다르게 고친 상황입니다. 먼저 충돌 파일을 확인하고, 어떤 내용을 살릴지 결정합니다.

Terminal 복사
```bash
    # 1. 충돌이 난 파일 목록 보기
    git status
    
    # 2. 파일을 열면 아래 같은 표시가 있음. 원하는 쪽만 남기고 표시를 지운다
    # <<<<<<< HEAD
    # 내가 고친 내용
    # ========
    # 상대방이 고친 내용
    # >>>>>>> 브랜치이름
    
    # 3. 표시를 다 지우고 저장한 뒤
    git add 파일경로
    
    # 4. (merge 중이었다면) 계속 진행
    git status   # "all conflicts fixed" 확인
    git merge --continue
    
    # 처음부터 그만두고 싶으면
    git merge --abort
```
**주의** : 충돌 표시(`<<<<<<<`, `=======`, `>>>>>>>`)가 하나라도 남으면 commit이 막힙니다. 파일을 저장하기 전에 꼭 확인합니다.

AI에게 conflict 설명 요청 복사
```bash
    merge conflict가 났습니다.
    
    먼저 충돌 파일 목록을 확인하고, 각 충돌 블록에서 양쪽 변경이 무엇을 의미하는지 초보자도 이해하게 설명해줘.
    내가 어떤 쪽을 선택할지 결정할 수 있게 선택지를 제시해줘.
    
    주의:
    - 내가 선택하기 전에는 파일을 수정하지 마.
    - 해결 후에는 어떤 테스트를 해야 하는지 알려줘.
```
AI가 너무 많은 파일을 바꿨습니다

바로 commit하지 말고 변경 목록부터 분리합니다.

AI에게 변경 분류 요청 복사
```bash
    이번 변경이 너무 커졌습니다. git diff를 보고 변경을 분류해줘.
    
    분류:
    1. issue와 직접 관련 있는 변경
    2. 관련은 있지만 별도 PR로 빼는 게 좋은 변경
    3. 되돌리는 게 좋은 변경
    
    각 분류별 파일 목록과 이유를 알려줘.
    아직 되돌리거나 commit하지 마.
```
되돌리고 싶습니다

되돌리기는 작업 단계에 따라 방법이 다릅니다. commit 전과 commit 후를 구분해야 합니다.

Terminal 복사
```bash
    # 1. commit 전: 특정 파일의 변경을 버리기
    git restore 파일경로
    
    # 2. commit 전: 전체 변경을 버리기 (신중)
    git restore .
    
    # 3. commit 후, 아직 push 안 함: 마지막 commit 취소, 변경은 유지
    git reset --soft HEAD~1
    
    # 4. commit 후 push까지 한 상태: 기록을 지우지 않고 되돌리기 (안전, 추천)
    git revert HEAD
    git push
    
    # 주의 — 아래는 작업과 기록을 영구 삭제. 절대 혼자 결정하지 마세요
    # git reset --hard
    # git push --force
```
AI에게 안전하게 되돌리기 요청 복사
```bash
    작업을 되돌리고 싶습니다.
    
    먼저 현재 상태를 확인해줘:
    - git status
    - git log --oneline -5
    - git diff
    
    그 다음 내 상황이 commit 전인지, commit 후인지, push 후인지 구분해서 가장 안전한 되돌리기 방법을 설명해줘.
    작업이 사라지는 명령은 실행하기 전에 반드시 나에게 확인받아.
```