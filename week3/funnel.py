# funnel.py — 6단계 정답 예시(퍼널) 단독 파일
import duckdb

# 사용자별 첫 구매일을 SQL로 구하고, 첫 구매 주차별 사용자 수를 집계해 보세요.
# (힌트: min(ts) FILTER, date_trunc)

print(duckdb.sql("""
    WITH first_buys AS (
    SELECT
        user_id,
        min(date_trunc('week', ts)) FILTER (WHERE event_type = 'buy') AS first_buy_ts,
        event_type
    FROM 'events.parquet'
    GROUP BY user_id, event_type
    )
    SELECT
           event_type,
           first_buy_ts AS week,
           count(*) AS user_count
    FROM first_buys
    GROUP BY first_buy_ts, event_type
    ORDER BY week;
"""))

# 3-2에서 만든 orders_enriched.parquet를 SQL로 읽어 지역×카테고리 교차표를 만들어 보세요. 
# (힌트: PIVOT 또는 조건부 집계)
print(duckdb.sql("""
    PIVOT (
        SELECT region, category
        FROM 'orders_enriched.parquet'
    )
    ON category
    USING count(*)
    GROUP BY region
"""))


print(duckdb.sql("""
    WITH per_user AS (
        SELECT user_id,
               max(CASE WHEN event_type = 'view' THEN 1 ELSE 0 END) AS viewed,
               max(CASE WHEN event_type = 'cart' THEN 1 ELSE 0 END) AS carted,
               max(CASE WHEN event_type = 'buy'  THEN 1 ELSE 0 END) AS bought
        FROM 'events.parquet'
        GROUP BY user_id
    )
    SELECT sum(viewed) AS viewed,
           sum(carted) AS carted,
           sum(bought) AS bought,
           round(sum(carted) * 100.0 / sum(viewed), 1) AS view_to_cart,
           round(sum(bought) * 100.0 / sum(carted), 1) AS cart_to_buy
    FROM per_user
"""))

