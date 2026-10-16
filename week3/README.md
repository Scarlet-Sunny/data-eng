1. Week 3 — 데이터 처리와 분석

3주차 실습에서는 Pandas와 Parquet을 이용한 데이터 정리, DuckDB 기반 분석, 데이터 품질 점검을 다룹니다. 주문·고객 데이터와 이벤트 데이터를 여러 형식으로 처리하고 단계별 결과를 비교합니다.

| 실습 | 주제 | 주요 입력·결과 |
|---|---|---|
| 3-1 | Pandas 기본기와 데이터 타입 | `orders.csv` → `orders_step1.parquet` |
| 3-2 | 그룹화, 병합, 시계열 재표본화 | `customers.csv` → `orders_enriched.parquet` |
| 3-3 | DuckDB와 열 지향 저장 형식 비교 | `events.csv`, Parquet 파일, [실측 기록](실측기록_3-3.md) |
| 3-4 | SQL 분석 결과를 Pandas로 왕복 처리 | `user_segments.parquet` |
| 3-5 | 하이브리드 파이프라인과 데이터 품질 | `orders_clean.parquet`, 품질 리포트 |


2. 산출물

1) orders_clean.parquet
2) (quality_report.csv + quality_report.md)

3. 주요 파일

- `make_orders.py`, `make_customers.py`, `make_events.py`: 실습용 데이터 생성
- `explore.py`, `analyze.py`, `query.py`, `sql_analysis.py`: 데이터 탐색 및 분석
- `transform.py`, `clean_orders.py`: 데이터 변환과 정제
- `quality_report.py`, `validate_test.py`, `order_test.py`, `check_return.py`, `crosscheck.py`: 품질 및 결과 검증
- `speed.py`, `df_cost.py`, `roundtrip.py`: 성능·크기·형식 변환 실험
- `events_parted/`: 분할 저장한 이벤트 데이터
- `quality_report.md`, `quality_report.csv`: 품질 점검 결과

3. 실행방법
   - source .venv/bin/activate        # Windows(WSL2)·macOS·리눅스 같습니다
   # 실습용 데이터 생성
   - python3 make_orders.py 
   - python3 make_events.py
   - python3 make_customers.py
   # 데이터 변환 및 정제
   - python3 clean_orders.py
   - python3 quality_report.py 
   # 품질 및 결과 검증
   - python3 quality_report.py
