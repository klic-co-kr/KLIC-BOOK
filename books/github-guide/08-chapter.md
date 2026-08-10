# 8장 Pull Request 만들기

PR은 결과물 자랑이 아니라 검토 요청서입니다. 팀원이 빠르게 이해하도록 "왜, 무엇을, 어떻게 확인하면 되는지"를 씁니다. 

### CLI로 PR 만들기

Terminal 복사
```bash
    gh pr create \
      --base main \
      --head fix-login-error-copy \
      --title "fix: clarify login error message" \
      --body "## 요약
    - 로그인 실패 메시지를 상황별로 구분했습니다.
    - 모바일 화면에서 문구가 버튼과 겹치지 않도록 간격을 조정했습니다.
    
    ## 확인 방법
    - 잘못된 비밀번호로 로그인 시도
    - 네트워크를 끄고 로그인 시도
    - 모바일 폭에서 오류 문구 확인
    
    Closes #12"
```
### 준비 중인 PR은 draft로 올리기

작업이 덜 끝났지만 미리 보여주고 싶으면 **draft PR** 을 씁니다. draft PR은 리뷰·병합이 막혀 있고 "준비 완료" 표시를 해야 검토가 시작됩니다.

Terminal 복사
```bash
    gh pr create --draft --base main --head fix-login-error-copy \
      --title "WIP: clarify login error message" \
      --body "아직 작업 중입니다. 완료되면 ready for review로 바꿉니다."
    
    # 완료되면
    gh pr ready NUMBER
```
### AI에게 PR 본문 초안 만들게 하기

PR 초안 프롬프트 복사
```bash
    현재 branch의 변경사항으로 GitHub PR 제목과 본문 초안을 만들어줘.
    
    참고할 것:
    - git log main..HEAD
    - git diff main...HEAD
    - 연결된 issue가 있으면 issue 내용
    
    본문 형식:
    ## 요약
    - 
    
    ## 변경한 이유
    - 
    
    ## 확인 방법
    - [ ] 
    
    ## 스크린샷 또는 결과
    - 필요하면 어떤 화면을 캡처해야 하는지 알려줘.
    
    ## 리뷰어에게 묻고 싶은 점
    - 
    
    주의:
    - 과장하지 말고 실제 변경한 내용만 써.
    - 내가 실행하지 않은 테스트를 실행했다고 쓰지 마.
```
좋은 PR 제목
    `fix: clarify login error message`, `feat: add profile preview card`, `docs: add setup guide`

나쁜 PR 제목
    `update`, `final`, `AI가 수정함`, `여러가지 고침`
