# 10장 fork는 언제 쓰나

fork는 팀 내부 협업의 기본값이 아닙니다. 보통 권한이 없는 외부 프로젝트에 기여하거나, 원본과 독립된 실험 공간이 필요할 때 씁니다. 

### 공동 레포 branch 방식

  * 팀원이 같은 레포에 초대되어 있음
  * KLIC 내부 팀 프로젝트에 적합
  * PR은 같은 레포의 branch끼리 생성

### fork 방식

  * 원본 레포에 push 권한이 없음
  * 오픈소스나 외부 프로젝트 참여에 적합
  * 내 계정의 fork에서 작업 후 원본으로 PR

### fork 방식 명령 예시

Terminal 복사
```bash
    gh repo fork OWNER/REPO --clone --remote
    cd REPO
    git switch -c fix-small-typo
    
    # 작업 후
    git add .
    git commit -m "docs: fix typo"
    git push -u origin fix-small-typo
    gh pr create --repo OWNER/REPO --base main --head 내아이디:fix-small-typo
```