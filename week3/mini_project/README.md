# Week 3 데이터 품질 미니 프로젝트

`orders.csv`와 100만 행 이벤트 Parquet 데이터를 대상으로 품질 규칙을 적용하고, 결측값 처리 방식과 실행 엔진에 따른 차이를 비교합니다.

## 프로젝트 과제

1. 주문 데이터 `profile()`에 값 범위 점검을 추가합니다.
   - 가격이 0 이하인 값의 건수
   - 수량이 6 이상인 값의 건수
   - 중복 주문 ID와 결측값 건수
2. 가격·수량의 결측값을 중앙값으로 채운 결과와 결측 행을 제거한 결과를 비교합니다.
   - 남은 행 수, 평균, 중앙값, 표준편차
3. `events.parquet`의 품질 지표를 Pandas와 DuckDB SQL로 각각 계산하고 시간을 비교합니다.
   - 중복 이벤트 ID, 결측값, 값 범위 위반, 이벤트 종류 수
   - Parquet 읽기와 지표 계산 시간

## 폴더 구조

```text
week3/
├── orders.csv
├── events.parquet
└── mini_project/
    ├── mini_pjt.py
    └── README.md
