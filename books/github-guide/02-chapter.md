# 2장 팀 프로젝트의 기본 흐름

소규모 팀이나 KLIC 프로젝트에서는 한 레포에 팀원을 초대하고, 각자 branch를 만든 뒤 PR로 합치는 방식이 자연스럽습니다. GitHub 공식 문서도 이 방식을 작은 팀과 조직의 private project에 흔한 모델로 설명합니다. 

GitHub 협업 흐름도 Issue로 할 일을 정의하고, Branch를 만들어 AI와 사람이 작게 수정한 뒤 Commit과 Push로 GitHub에 공유합니다. 그 다음 Pull Request로 검토를 요청하고, 리뷰를 거쳐 main에 병합합니다. Issue 할 일 정의 Branch 작업 공간 분리 AI + 사람 작게 수정 Commit + Push GitHub에 공유 Pull Request 검토 요청 Review + Merge 확인 후 합치기

**한 줄 원칙** : main은 바로 고치지 않습니다. 작업마다 branch를 만들고, AI가 만든 변경도 PR에서 사람이 확인한 뒤 합칩니다.
