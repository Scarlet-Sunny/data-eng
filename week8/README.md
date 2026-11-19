README 에 들어갈 것 
1. 아키텍처 한 장 그림

/아키텍쳐.png

2. airflow 컨테이너 변경
airflow-apiserver      ← 사람이 보는 화면 (8080) · 워커의 보고 창구
airflow-scheduler      ← 시각을 보고 태스크를 큐에 넣는다
airflow-dag-processor  ← dags/ 폴더의 파일을 읽어 DAG 로 올린다
airflow-worker         ← 큐에서 꺼내 실제로 실행한다
airflow-triggerer      ← 기다리는 일을 전담
postgres               ← 메타데이터 DB (실행 이력의 정본)
redis                  ← 스케줄러와 워커 사이의 큐

이 일곱이 한 묶음으로 떠야 Airflow다(Airflow 3 기준).

3. 실행 순서(7주차 컨테이너 셋 → network connect → compose up → DAG unpause → streamlit run)

3. 대조군 → 문서 투입 → 답변 반영 검증 시나리오와 내 숫자(11 → 12 · 0.253 → 0.517)

4. 제출 폴더 구성
- rag_pipeline_final.py · build_kb.py · minio_env.py · rag_env.py · app.py · requirements.txt · .env.example · README
주의
- .env(실제 키)는 .env.example 에서 확인 합니다.

6. 회고
- OPENAPI 에서 OLLAMA로 변경 하면서 lecture_kb 가 맞지 않아 lecture_kb로 재 설정 하며 오류가 많이 나 시간이 걸렸음
- 차원을 맞추고 컬렉션을 변경하면서 구조를 조금 더 이해하게 되었음
