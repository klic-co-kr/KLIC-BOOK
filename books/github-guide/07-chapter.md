# 7장 커밋과 푸시

commit은 팀원에게 보여주는 작업 저장 지점입니다. AI가 많은 파일을 바꿨다면 더더욱 관련 변경만 골라서 commit해야 합니다. 

### 변경 확인

Terminal 복사
```bash
    git status
    git diff
```
### AI에게 commit 전 검토시키기

AI self-review 프롬프트 복사
```bash
    git status와 git diff를 바탕으로 commit 전에 검토해줘.
    
    출력:
    1. 이번 변경 요약
    2. 관련 없는 변경이 섞였는지
    3. 위험하거나 되돌려야 할 변경 후보
    4. 실행해야 할 테스트/빌드 명령
    5. 추천 commit 메시지 3개
    
    아직 git add나 commit은 하지 마.
```
### commit과 push

Terminal 복사
```bash
    git add 파일경로1 파일경로2
    git commit -m "fix: clarify login error message"
    git push -u origin fix-login-error-copy
```
AI에게 commit 맡길 때 복사
```bash
    이번 issue와 관련된 변경만 stage하고 commit해줘.
    
    조건:
    - 먼저 git status와 git diff를 확인해.
    - 관련 없는 파일이 있으면 stage하지 말고 나에게 물어봐.
    - commit 메시지는 "type: 짧은 설명" 형식으로 제안하고, 내가 승인하면 commit해.
    - commit 후 push까지 진행해.
    
    추천 type:
    feat, fix, docs, style, refactor, test, chore
```