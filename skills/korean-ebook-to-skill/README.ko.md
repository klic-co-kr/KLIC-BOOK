# korean-ebook-to-skill

## 정체성 (스펙 §3.1)

book-to-skill 베이스 + 한국어 챕터 + **AI 판단추출층**. 산출 = **참조형 쿼리 스킬 1개/책**. book-to-skill과의 차이 = AI가 가치내용을 미리 판단·추출하고 근거를 부록C·원문§로 연쇄한다는 점. 발동스킬이 아니므로 FDE 매체불일치(IDE vs 회의) 문제 소멸.

## 설치

```bash
bash scripts/install.sh   # → $CLAUDE_SKILLS_HOME/korean-ebook-to-skill (심볼릭링크)
```

## 테스트

```bash
cd skills/korean-ebook-to-skill && python3 -m pytest tests/ -v
```
