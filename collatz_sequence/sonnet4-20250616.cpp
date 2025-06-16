#include <iostream>
#include <vector>
#include <algorithm>

/**
 * コラッツ数列を計算して配列として返す
 */
std::vector<int> collatz_sequence(int n) {
    std::vector<int> sequence;
    
    while (n != 1) {
        sequence.push_back(n);
        if (n % 2 == 0) {
            n = n / 2;  // 偶数の場合：2で割る
        } else {
            n = n * 3 + 1;  // 奇数の場合：3倍して1を足す
        }
    }
    
    sequence.push_back(1);  // 最後の1を追加
    return sequence;
}

int main() {
    // 初期値を設定
    int initial_value = 27;
    
    // コラッツ数列を計算
    std::vector<int> result = collatz_sequence(initial_value);
    
    // 結果を出力
    std::cout << "初期値: " << initial_value << std::endl;
    
    std::cout << "コラッツ数列: [";
    for (size_t i = 0; i < result.size(); i++) {
        std::cout << result[i];
        if (i < result.size() - 1) {
            std::cout << ", ";
        }
    }
    std::cout << "]" << std::endl;
    
    std::cout << "ステップ数: " << result.size() - 1 << std::endl;
    std::cout << "最大値: " << *std::max_element(result.begin(), result.end()) << std::endl;
    
    return 0;
}