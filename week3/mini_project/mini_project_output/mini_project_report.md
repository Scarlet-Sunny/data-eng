# 데이터 품질 미니 프로젝트 결과

## 주문 데이터 품질 프로파일

| dataset | rows | duplicate_order_id | null_price | null_quantity | null_category | price_le_0 | quantity_ge_6 | category_values |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| before | 1015 | 15 | 30 | 0 | 0 | 0 | 0 | 5 |
| median_imputation | 1015 | 15 | 0 | 0 | 0 | 0 | 0 | 5 |
| drop_missing_rows | 985 | 15 | 0 | 0 | 0 | 0 | 0 | 5 |

## 결측 처리 방식별 통계 비교

| method | rows | price_mean | price_median | price_std | quantity_mean | quantity_median | quantity_std |
| --- | --- | --- | --- | --- | --- | --- | --- |
| median_imputation | 1015 | 100365.5172413793 | 101000.0 | 55949.5704279174 | 2.935960591133005 | 3.0 | 1.425617080972931 |
| drop_missing_rows | 985 | 100346.19289340102 | 101000.0 | 56795.945444425604 | 2.947208121827411 | 3.0 | 1.426112040182496 |

중앙값 대체는 가격과 수량의 결측을 각 열의 중앙값으로 채웁니다.
행 제거는 가격·수량·카테고리 중 하나라도 결측인 행을 제외합니다.
두 결과의 평균, 중앙값, 표준편차와 남은 행 수를 비교하세요.

## 이벤트 데이터 엔진별 측정 결과

| engine | rows | duplicate_event_id | null_user_id | null_event_type | null_value | null_ts | value_le_0 | value_gt_9900 | distinct_event_type | elapsed_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Pandas | 1000000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0.09850313799961441 |
| DuckDB SQL | 1000000 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0.05942614500054333 |

측정 시간에는 Parquet 읽기와 품질 지표 계산이 포함됩니다.
실행 환경과 파일 캐시에 따라 시간이 달라질 수 있습니다.
