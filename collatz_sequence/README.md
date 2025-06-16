# Input
```txt
Make this C++.


def collatz_sequence(n):
    """
    コラッツ数列を計算して配列として返す
    """
    sequence = []
    
    while n != 1:
        sequence.append(n)
        if n % 2 == 0:
            n = n // 2  # 偶数の場合：2で割る
        else:
            n = n * 3 + 1  # 奇数の場合：3倍して1を足す
    
    sequence.append(1)  # 最後の1を追加
    return sequence

# 初期値を設定
initial_value = 27

# コラッツ数列を計算
result = collatz_sequence(initial_value)

# 結果を出力
print(f"初期値: {initial_value}")
print(f"コラッツ数列: {result}")
print(f"ステップ数: {len(result) - 1}")
print(f"最大値: {max(result)}")
```


# ！
- Gemini Diffusionは、Instant editを使用