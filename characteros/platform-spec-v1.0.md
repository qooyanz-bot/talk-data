# CharacterOS Platform Specification v1.0

状態: K承認済み（2026-09-06 JST）

CharacterOSは、オリジナルAIキャラクターを作成、会話、記憶、音声、VRM 1.0アバター、販売、配信、運用するAPI-firstプラットフォームである。

## 採用モジュール

| モジュール | 確定責務 |
|---|---|
| CharacterOS-Engine | Character、Conversation、ChappyMemory、LLM routing、Speech、VRM/avatar、Motion、Camera Insight API。 |
| CharacterOS-Operation | 1人から1億人超までの段階的スケール、監視、安全、原価制御、障害対応。 |
| CharacterOS-Client | iOS、Android、Chrome、Unity、Unreal、Godot、Cocos2d-x、Swift/Xcode向けSDK/UI。 |
| CharacterOS-Tool | Web上のキャラクター制作、テスト、版管理、公開、API設定。 |
| CharacterOS-Pay | Apple IAP、Google Play Billing、Web Stripeのサーバー検証済み権利台帳、販売・売上分析。 |
| CharacterOS-Market | VRM、音声、モーション、人格・世界観等の作成、審査、ライセンス、販売、組合せ。 |
| CharacterOS-Gate | Web入口、会員、認証、同意、テナント、権限。 |
| CharacterOS-BASE | MFA・監査・二人承認を伴う運営専用管理Web。 |

## 固定した安全境界

- 全機能を版付きAPIで提供し、プロバイダーAPIキーはクライアントへ渡さない。
- 記憶は閲覧、訂正、エクスポート、停止、削除可能とする。AI推測は本人確認済み事実へ自動昇格させない。
- VRM 1.0を標準形式とし、リップシンク、表情、視線、モーションは意味論的な安全な指示へ限定する。
- カメラは端末内で表情・頭部トラッキングを行う既定とし、動画保存・顔識別テンプレート作成を行わない。
- 声だけによる真偽判定は実装・宣伝しない。
- 実在人物、既存IP、声の公開・販売には明示的な権利・同意確認を必須とする。
- 決済・権利・売上変更はサーバー検証、冪等性、監査ログを必須とする。

## 運用の固定方針

Cloudflareをエッジ/CDN/WAF/オブジェクト配信に、マネージドコンテナをコア実行に使う。初期はCloud RunまたはECS Fargate、持続負荷・GPU・複数リージョン要件が成立した場合にGKE AutopilotまたはECS/EKSへ移行する。VPSは開発・踏み台用途に限り、本番の認証・DB・唯一の状態保持には使わない。

## 公開前に必ず検証する事項

ストア審査、各国の決済・税務・消費者保護・個人情報法、Stripe Connectの国別対応、権利者削除手続、GPU供給枠、負荷・障害復旧・ペネトレーション・決済照合・悪用テストは外部依存または未検証である。対応機能は、これらの検証完了を公開ゲートとする。

詳細版は当該会話の成果物 `CharacterOS-Platform-Spec-v1.0.md` に保持する。
