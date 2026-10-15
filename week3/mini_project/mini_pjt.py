from pathlib import Path
import time

import duckdb
import pandas as pd


def find_input(filename: str, script_dir: Path) -> Path:
    """현재 폴더, 스크립트 폴더, 상위 week3 폴더에서 입력 파일 찾기."""
    candidates = [
        Path.cwd() / filename,
        script_dir / filename,
        script_dir.parent / filename,
    ]

    for path in candidates:
        if path.is_file():
            return path

    searched = "\n".join(f"- {path}" for path in candidates)
    raise FileNotFoundError(
        f"{filename} 파일을 찾지 못했습니다. 다음 위치를 확인했습니다:\n{searched}"
    )


def profile(df: pd.DataFrame, name: str) -> dict:
    """주문 데이터의 결측, 중복, 값 범위 위반 건수를 요약."""
    required = {"order_id", "price", "quantity", "category"}
    missing_columns = required - set(df.columns)

    if missing_columns:
        raise ValueError(f"필수 열이 없습니다: {sorted(missing_columns)}")

    price = pd.to_numeric(df["price"], errors="coerce")
    quantity = pd.to_numeric(df["quantity"], errors="coerce")

    return {
        "dataset": name,
        "rows": len(df),
        "duplicate_order_id": int(df["order_id"].duplicated().sum()),
        "null_price": int(price.isna().sum()),
        "null_quantity": int(quantity.isna().sum()),
        "null_category": int(df["category"].isna().sum()),
        "price_le_0": int((price <= 0).sum()),
        "quantity_ge_6": int((quantity >= 6).sum()),
        "category_values": int(df["category"].nunique(dropna=True)),
    }


def median_imputation(df: pd.DataFrame) -> pd.DataFrame:
    """가격·수량의 결측을 각 열의 중앙값으로 대체."""
    result = df.copy()

    for column in ("price", "quantity"):
        values = pd.to_numeric(result[column], errors="coerce")
        result[column] = values.fillna(values.median())

    return result


def drop_missing_rows(df: pd.DataFrame) -> pd.DataFrame:
    """가격·수량·카테고리 중 하나라도 결측인 행 제거."""
    return df.dropna(subset=["price", "quantity", "category"]).copy()


def compare_statistics(median_df: pd.DataFrame,
                       dropped_df: pd.DataFrame) -> pd.DataFrame:
    """두 결측 처리 방식의 행 수와 가격·수량 통계 비교."""
    rows = []

    for method, data in (
        ("median_imputation", median_df),
        ("drop_missing_rows", dropped_df),
    ):
        row = {"method": method, "rows": len(data)}

        for column in ("price", "quantity"):
            values = pd.to_numeric(data[column], errors="coerce")
            row[f"{column}_mean"] = values.mean()
            row[f"{column}_median"] = values.median()
            row[f"{column}_std"] = values.std()

        rows.append(row)

    return pd.DataFrame(rows)


def markdown_table(df: pd.DataFrame) -> str:
    """외부 패키지 없이 DataFrame을 Markdown 표로 변환."""
    headers = [str(column) for column in df.columns]
    rows = [
        ["" if pd.isna(value) else str(value) for value in row]
        for row in df.itertuples(index=False, name=None)
    ]

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)

    return "\n".join(lines)


def pandas_event_profile(path: Path) -> tuple[dict, float]:
    """이벤트 Parquet 품질 측정: 파일 읽기부터 계산까지 시간을 잼."""
    start = time.perf_counter()
    df = pd.read_parquet(path)

    required = {"event_id", "user_id", "event_type", "value", "ts"}
    missing_columns = required - set(df.columns)

    if missing_columns:
        raise ValueError(f"events.parquet 필수 열이 없습니다: {sorted(missing_columns)}")

    value = pd.to_numeric(df["value"], errors="coerce")
    user_id = pd.to_numeric(df["user_id"], errors="coerce")

    result = {
        "engine": "Pandas",
        "rows": len(df),
        "duplicate_event_id": int(df["event_id"].duplicated().sum()),
        "null_user_id": int(user_id.isna().sum()),
        "null_event_type": int(df["event_type"].isna().sum()),
        "null_value": int(value.isna().sum()),
        "null_ts": int(df["ts"].isna().sum()),
        "value_le_0": int((value <= 0).sum()),
        "value_gt_9900": int((value > 9900).sum()),
        "distinct_event_type": int(df["event_type"].nunique(dropna=True)),
    }

    elapsed = time.perf_counter() - start
    return result, elapsed


def duckdb_event_profile(path: Path) -> tuple[dict, float]:
    """이벤트 Parquet 품질 측정: 모든 지표를 DuckDB SQL로 계산."""
    escaped_path = str(path.resolve()).replace("'", "''")

    sql = f"""
        SELECT
            'DuckDB SQL' AS engine,
            COUNT(*) AS rows,
            COUNT(*) - COUNT(DISTINCT event_id) AS duplicate_event_id,
            COUNT(*) FILTER (WHERE user_id IS NULL) AS null_user_id,
            COUNT(*) FILTER (WHERE event_type IS NULL) AS null_event_type,
            COUNT(*) FILTER (WHERE value IS NULL) AS null_value,
            COUNT(*) FILTER (WHERE ts IS NULL) AS null_ts,
            COUNT(*) FILTER (WHERE value <= 0) AS value_le_0,
            COUNT(*) FILTER (WHERE value > 9900) AS value_gt_9900,
            COUNT(DISTINCT event_type) AS distinct_event_type
        FROM read_parquet('{escaped_path}')
    """

    start = time.perf_counter()

    with duckdb.connect() as connection:
        result = connection.execute(sql).fetchone()
        columns = [
            description[0]
            for description in connection.description
        ]

    elapsed = time.perf_counter() - start
    return dict(zip(columns, result)), elapsed


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    orders_path = find_input("orders.csv", script_dir)
    events_path = find_input("events.parquet", script_dir)

    output_dir = script_dir / "mini_project_output"
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. 주문 데이터 품질 프로파일
    orders = pd.read_csv(orders_path)
    median_df = median_imputation(orders)
    dropped_df = drop_missing_rows(orders)

    order_profile = pd.DataFrame([
        profile(orders, "before"),
        profile(median_df, "median_imputation"),
        profile(dropped_df, "drop_missing_rows"),
    ])
    order_profile.to_csv(output_dir / "order_profile.csv", index=False)

    # 2. 결측 처리 방식별 통계 비교
    statistics = compare_statistics(median_df, dropped_df)
    statistics.to_csv(
        output_dir / "imputation_comparison.csv",
        index=False,
    )

    # 3. 100만 행 이벤트 데이터: Pandas와 DuckDB SQL 비교
    pandas_result, pandas_seconds = pandas_event_profile(events_path)
    duckdb_result, duckdb_seconds = duckdb_event_profile(events_path)

    engine_comparison = pd.DataFrame([pandas_result, duckdb_result])
    engine_comparison["elapsed_seconds"] = [
        pandas_seconds,
        duckdb_seconds,
    ]
    engine_comparison.to_csv(
        output_dir / "events_engine_comparison.csv",
        index=False,
    )

    # 결과 요약 Markdown 작성. 외부 Markdown 패키지는 사용하지 않음.
    report = f"""# 데이터 품질 미니 프로젝트 결과

## 주문 데이터 품질 프로파일

{markdown_table(order_profile)}

## 결측 처리 방식별 통계 비교

{markdown_table(statistics)}

중앙값 대체는 가격과 수량의 결측을 각 열의 중앙값으로 채웁니다.
행 제거는 가격·수량·카테고리 중 하나라도 결측인 행을 제외합니다.
두 결과의 평균, 중앙값, 표준편차와 남은 행 수를 비교하세요.

## 이벤트 데이터 엔진별 측정 결과

{markdown_table(engine_comparison)}

측정 시간에는 Parquet 읽기와 품질 지표 계산이 포함됩니다.
실행 환경과 파일 캐시에 따라 시간이 달라질 수 있습니다.
"""
    (output_dir / "mini_project_report.md").write_text(
        report,
        encoding="utf-8",
    )

    print("주문 데이터 프로파일")
    print(order_profile.to_string(index=False))
    print("\n결측 처리 통계 비교")
    print(statistics.to_string(index=False))
    print("\n이벤트 데이터 엔진 비교")
    print(engine_comparison.to_string(index=False))
    print(f"\n결과 저장 위치: {output_dir}")


if __name__ == "__main__":
    main()
