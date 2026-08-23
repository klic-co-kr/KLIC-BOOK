# 9장 리뷰 받고 수정하기

리뷰는 혼나는 과정이 아니라 main에 들어가기 전에 서로 확인하는 과정입니다. PR의 Conversation, Commits, Checks, Files changed 탭을 차례로 보면 상황을 이해하기 쉽습니다. 

**Conversation**

제목, 본문, 리뷰 댓글, 답글이 오가는 곳. 수정 요청도 여기에 쌓입니다.

**Commits**

이 PR에 담긴 commit 목록. 한 번에 몰아서 올렸는지, 작게 쪼갰는지 볼 수 있습니다.

**Checks (CI)**

자동 검사 결과. 빌드·테스트·린트가 설정되어 있으면 여기서 초록 체크·빨간 실패로 표시됩니다. 빨간 실패 표시가 있으면 원인을 확인한 뒤 다시 push합니다.

**Files changed**

실제 변경된 코드(diff)입니다. 줄별로 코멘트를 남기는 곳이며, 리뷰의 핵심입니다.

### 작성자가 할 일

  * 작은 PR로 올리기
  * 확인 방법 쓰기
  * 스스로 diff 먼저 보기
  * 리뷰 댓글에 답하거나 수정하기

### 리뷰어가 볼 것

  * issue 범위를 지켰는지
  * 화면이나 기능이 실제로 동작하는지
  * 관련 없는 변경이 섞였는지
  * 읽기 어려운 코드나 설명이 있는지

### 수정 요청이 오면

  * 새 branch를 만들지 않습니다.
  * 같은 branch에서 수정합니다.
  * commit 후 push하면 기존 PR이 자동 업데이트됩니다.

### 리뷰 댓글을 AI에게 정리시키기

리뷰 대응 프롬프트 복사
```bash
    PR 리뷰 댓글을 보고 수정 계획을 세워줘.
    
    입력:
    [리뷰 댓글을 붙여넣기]
    
    출력:
    1. 반드시 수정해야 하는 항목
    2. 질문에 답하면 되는 항목
    3. 수정할 파일 후보
    4. 각 항목의 위험도
    5. 내가 리뷰어에게 답글로 남길 문장 초안
    
    아직 코드는 수정하지 마.
```
### 수정 후 다시 push

Terminal 복사
```bash
    git status
    git add 파일경로
    git commit -m "fix: address review feedback"
    git push
```
### main 최신 변경 반영하기

Terminal 복사
```bash
    git switch main
    git pull
    git switch 내-작업-브랜치
    git merge main
```