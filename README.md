# BOAZ 18주차 · Streamlit 기반 반응형 대시보드 만들기

Tableau로 만들던 대시보드를 **파이썬 코드로** 만들고, **클릭하면 반응하는 것**까지 해 봅니다.
데이터는 plotly에 내장된 Gapminder(142개국 · 1952~2007 · 5년 단위)라서 따로 다운받을 파일이 없어요.

## 오늘 만들 것

| STEP | 내용 | 핵심 함수 |
|---|---|---|
| 1 | 필터 (대륙 · 연도) | `st.sidebar`, `st.multiselect`, `st.select_slider` |
| 2 | KPI 카드 4개 | `st.columns`, `st.metric` |
| 3 | 버블 차트 · 애니메이션 · 지구본 · 표 속 미니 추이 | `px.scatter`, `px.choropleth`, `st.column_config.LineChartColumn` |
| 4 | 버블 클릭 → 아래 차트 연동 | `st.plotly_chart(on_select="rerun")` |

## 폴더 구조

```
├── app.py              # 완성본 (시연·배포용)
├── starter/            # 실습용: stepN.py = STEP 1~N-1 완성 + STEP N 빈칸
│   ├── step1.py ~ step4.py
├── solutions/          # 정답: stepN.py = STEP 1~N 완성
│   ├── step1.py ~ step4.py
├── requirements.txt
└── .streamlit/config.toml   # 다크 테마
```

## 설치 (세션 전에 꼭!)

```bash
pip install -r requirements.txt
streamlit hello        # 브라우저에 데모 페이지가 뜨면 성공 (Ctrl+C로 종료)
```

## 실습 방법

```bash
streamlit run starter/step1.py
```

1. `# TODO` 블록의 주석 처리된 코드를 드래그 → **Cmd+/** (윈도우 **Ctrl+/**) 로 주석 해제
2. `____` 빈칸 채우기
3. 저장하면 브라우저 오른쪽 위에 **Rerun** 버튼이 뜸 → 클릭 (또는 `R` 키)
4. 다음 STEP은 `starter/step2.py` 로 이어서. **앞 단계에서 막혀도 다음 starter 파일은 앞 단계가 다 채워져 있으니** 그대로 따라오면 돼요.

막히면 `solutions/stepN.py` 를 열어서 비교하세요.

## 자주 나는 오류

| 증상 | 해결 |
|---|---|
| `streamlit: command not found` | `python -m streamlit run starter/step1.py` |
| 버블 클릭해도 반응 없음 | `pip install -U streamlit` (1.45 이상 필요) |
| `NameError: name 'event' is not defined` | STEP 4-1에서 `st.plotly_chart` 줄을 `event = ...` 로 바꿨는지 확인 |
| 지구본이 안 보임 | 인터넷 연결 확인 (지도 모양 파일을 온라인으로 불러옴) |
| 대륙을 다 지우면 경고만 뜸 | 정상이에요 (`st.stop()` 으로 아래 코드 실행을 멈춤) |

## 배포 (Streamlit Community Cloud)

1. 이 폴더를 GitHub 레포로 올리기 (public)
2. [share.streamlit.io](https://share.streamlit.io) → GitHub 로그인 → **Create app**
3. Repository 선택, Branch `main`, Main file path `app.py` → **Deploy**
4. 1~2분 뒤 `https://<이름>.streamlit.app` 링크 생성 → 폰으로도 열림
