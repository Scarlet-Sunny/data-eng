# 6주차 산출물 — 실시간 CDC 파이프라인

## 1. 구성
| 서비스 | 역할 | 포트 |
|---|---|---|
| kafka | 이벤트 중간 저장소 | 9092(외부) · 29092(내부) |
| mysql | 원천 DB | 3306 |
| connect | Debezium 소스 + S3 싱크 | 8083 |
| minio | 적재 대상 (S3 호환) | 9000 · 9001 |

## 2. 데이터 흐름
MySQL(binlog) → Debezium → Kafka(shop.shop.orders) → S3 Sink → MinIO(cdc-raw)

## 3. 토픽 구성
| 토픽 | 용도 |
|---|---|
| orders | 6-3 파이썬 실습용 |
| shop.shop.orders | CDC 변경 이벤트 |
| schema-changes.shop | 스키마 변경 이력 |
| connect_configs/offsets/statuses | Connect 내부 상태 |

## 4. 제출 파일
- docker-compose.yml
- register-mysql.json (Debezium 소스 커넥터)
- sink-minio.json (S3 싱크 커넥터)

## 5. 확인한 것
- op = r/c/u/d 네 종류를 모두 관찰
- MySQL INSERT → MinIO 파일 생성까지 엔드투엔드 통과
- flush.size 만큼 모여야 파일이 생기는 것을 확인

## 6. 남은 개선점
- (여기에 본인이 발견한 것을 적어 주세요)
