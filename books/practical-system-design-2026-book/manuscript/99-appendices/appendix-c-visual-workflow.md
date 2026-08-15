## 부록 C. 이미지 제작과 검수 흐름

1. 본문의 `figure-spec`과 `manifests/assets.yaml`이 일치하는지 확인한다.
2. 기술도는 `assets/specs/svg/`의 프롬프트로 순수 SVG를 생성한다.
3. Image2.0 장면은 `assets/prompts/image2/`의 프롬프트로 4K PNG master를 생성한다.
4. 차트는 `assets/specs/charts/`의 산식과 synthetic/실측 구분을 따라 코드로 생성한다.
5. 기술 검수에서 화살표·라벨·수치·출처를 확인한다.
6. 편집 검수에서 정보 계층·가독성·본문 연결을 확인한다.
7. 접근성 검수에서 caption·alt text·색상 외 구분을 확인한다.
8. 모든 검수를 통과한 자산만 `approved`로 변경한다.

현재 패키지는 119개 자산 모두 `specified` 상태이며 실제 이미지 바이너리는 포함하지 않는다.
