import pandas as pd

df = pd.DataFrame({
    "price": [50000, 120000, 250000],
    "quantity": [2, 3, 1],
})

mask = df["price"] > 100000
print(mask.head())  # 각 행의 조건 만족 여부
print(df[mask].shape)  # 조건을 만족하는 행의 개수와 열의 개수

# 조건을 여러 개 연결할 때는 각 조건을 괄호로 감싸고 & 또는 | 를 사용합니다.
filtered = df[(df["price"] > 100000) & (df["quantity"] >= 3)]
print(filtered)
