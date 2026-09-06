# 2026-09-06 Address residual defense in depth

## 追加

- Resolution Gate の residual 構築で、`target_value.residual` の無効ラベル（空文字・非文字列）を安全にスキップし、非空文字列のみ `resolution.residual` にミラー。
- Response Contract が `resolution.residual` を「非空文字列の list」として機械検査（空文字・非文字列を拒否）。residual があるときの value=null 規則は従来どおり。

## 非変更

- 新規 golden なし。Value発見、R6-G実行、秘密・暗号・宇宙DB、Cortext9/CIVA は対象外。
