# NopeCHA hCaptcha対応

- 作成日時 (UTC): 2026-07-24T13:54:21.0000000Z
- 更新日時 (UTC): 2026-07-24T14:12:23.0000000Z
- 注記: 本文は公開用に秘密形式・メールアドレス・電話番号のみ不可逆に伏せ字化。

## user / 2026-07-24T13:54:18.0000000Z

```
hCaptcha 回避 nopechaで対応してますか？
```

## assistant / 2026-07-24T13:54:23.0000000Z

```
はい。**NopeCHA は hCaptcha に対応しています。** 公式ドキュメントでは以下が明記されています。

- ✅ hCaptcha（Publisher / Pro / Enterprise）
- ✅ Recognition API（画像認識）
- ✅ Token API（トークン生成）
- ✅ Chrome拡張・Firefoxアドオンでも対応 citeturn0search0turn0search1turn0search4

また、hCaptcha のチャレンジタイプとして、少なくとも以下をサポートしています。

- 3×3画像選択
- Area Select（画像内をクリック・範囲指定）
- Multiple Choice（複数選択形式） citeturn0search19

ただし、実運用ではいくつか注意点があります。

- **hCaptcha Enterprise** はサイトによって追加のBot検知（TLSフィンガープリント、ブラウザ指紋、IP評価など）があり、CAPTCHAを解けてもログインやリクエストが成功するとは限りません。
- Enterpriseでは、**CAPTCHAを解く際に使うIPと、トークンを送信するIPを一致させるため、プロキシの指定を強く推奨**しています。 citeturn0search4

もし質問の意図が

- Playwrightで自動化したい
- Puppeteerで使いたい
- Browser Useで使いたい
- n8nから使いたい

のような実装レベルであれば、その構成に合わせて利用可否や実装方法も説明できます。
```

## assistant / 2026-07-24T13:54:23.0000000Z

```
null
```

## assistant / 2026-07-24T13:54:23.0000000Z

```
null
```

## user / 2026-07-24T13:55:28.0000000Z

```
indeedは追加のbot検知してる？
```

## assistant / 2026-07-24T13:55:30.0000000Z

```
はい。**Indeed は CAPTCHA だけでなく、多層的な Bot 検知を行っていると考えるのが妥当です。**

公開情報や実際の運用状況から、少なくとも次のような対策が確認できます。

- **CAPTCHA / hCaptcha・Cloudflare Challenge**
- **レートリミット（短時間の大量アクセス検知）**
- **ブラウザフィンガープリント**（TLS/JA3・HTTP/2・Canvas・WebGL・AudioContext・Navigator など）
- **JavaScript によるヘッドレスブラウザ検知**
- **IPレピュテーション**（データセンターIP・プロキシ・VPN）
- **アクセスパターン・行動分析**（スクロール、クリック、ページ遷移、滞在時間など） citeturn0search0turn0search3turn0search2

そのため、

> **NopeCHAでhCaptchaを解ける = Indeedを突破できる**

ではありません。

実際には、CAPTCHAを解いた後でも

- Challenge Loop（何度もCAPTCHAが出る）
- 403
- Access Denied
- Robot Check
- 一定時間ブロック

になるケースがあります。

また、スクレイピングコミュニティでも、Indeed は **Cloudflare とレートリミットを組み合わせた保護**があるため、単純な Playwright や Puppeteer だけでは安定しないと報告されています。citeturn0search9

---

### EnterpriseOSのような大量クロールの場合

あなたが以前話していたような**企業DBを継続的に更新する規模**で考えると、ボトルネックはCAPTCHAではありません。

優先順位は概ね次のようになります。

1. ブラウザフィンガープリント対策
2. セッション維持（Cookie・Storage）
3. IP品質（Residentialなど）
4. アクセス頻度・リクエストパターン制御
5. CAPTCHA対策（NopeCHAなど）

つまり、**CAPTCHA対策は全体の一要素**であり、安定運用ではそれ以外の検知回避が成功率を大きく左右します。
```

## assistant / 2026-07-24T13:55:30.0000000Z

```
null
```

## assistant / 2026-07-24T13:55:30.0000000Z

```
null
```

## user / 2026-07-24T13:57:37.0000000Z

```
上から順番に解決策を提案して下さい
```

## assistant / 2026-07-24T13:57:39.0000000Z

````
EnterpriseOS規模（数十〜数千Bot）で考えるなら、**CAPTCHAから対策するのは順番が逆**です。

成功率に影響する順番で説明します。

## ① ブラウザフィンガープリント対策（最重要）

現在は

- User-Agent
- navigator
- Canvas
- WebGL
- AudioContext
- Fonts
- Screen
- Timezone
- Languages
- TLS(JA3/JA4)
- HTTP2 Fingerprint

これらを総合して判定されます。TLSのJA3/JA4フィンガープリントやHTTP/2の特徴は、CloudflareなどのBot対策でも利用されています。citeturn0search0turn0search1turn0search2

### EnterpriseOSなら

Playwrightをそのまま起動

↓

❌おすすめしません

代わりに

- 実Chrome
- 実UserData
- 実Profile

を使って毎回同じユーザーとして動かす設計が有利です。

---

## ② セッション維持

Indeedは

```
Cookie
LocalStorage
SessionStorage
```

を見ています。

毎回

```
新しいブラウザ
```

になると

```
Bot率が急上昇
```

します。

理想は

```
Bot001
Profile001

Bot002
Profile002

Bot003
Profile003
```

のように

**1Bot = 1プロフィール**

です。

---

## ③ IP品質

これが非常に重要です。

優先順位は

★★★★★ 家庭回線Residential

★★★★ ISP Proxy

★★ VPS

★ Datacenter

です。

同じIPで大量アクセスすると

```
IP Reputation
```

が下がります。

---

## ④ アクセス頻度

多くのBotは

```
2秒毎
```

のような一定間隔になります。

実際の人間は

```
1.2秒
5.8秒
0.9秒
7.4秒
```

のようにばらつきます。

さらに

- 戻る
- 少しスクロール
- 途中で止まる
- クリックしないページもある

など自然な閲覧パターンが特徴です。

---

## ⑤ JavaScript検知

最近は

```
navigator.webdriver
```

だけではありません。

例えば

- Permissions API
- Clipboard API
- GPU
- MediaDevices
- Plugins
- Touch
- Battery
- WebRTC

など複数の情報を組み合わせて矛盾がないか確認します。研究でも、単一の値より**複数のフィンガープリント間の一貫性**が検出精度を大きく左右することが示されています。citeturn0academia14turn0academia12

---

## ⑥ CAPTCHA

ここで初めて

```
NopeCHA
```

などが出番になります。

つまり

```
Bot検知
↓

Challenge

↓

hCaptcha
```

という流れです。

Bot判定されなければ

そもそもCAPTCHA自体が表示されないケースもあります。

---

# 私ならEnterpriseOSをこう設計します

```
Cloudflare Workers
      │
      │
Queue
      │
      ▼
Browser Pool
(実Chrome)
      │
      ├── Profile001
      ├── Profile002
      ├── Profile003
      ├── …
      │
Residential Proxy Pool
      │
Cookie Store
      │
Session Manager
      │
Indeed
```

その上で、

- Browser Pool（実Chrome）
- Profile Manager（永続プロファイル）
- Cookie Manager（セッション維持）
- Proxy Manager（IP管理）
- Scheduler（アクセス間隔・ジョブ制御）
- CAPTCHA Service（必要時のみ利用）

を独立したコンポーネントに分けます。

## EnterpriseOSなら最優先で作るべきもの

今までの構想を踏まえると、最初に力を入れるべきなのは**スクレイパー本体ではなく「Browser Orchestrator（ブラウザ管理基盤）」**です。

これを先に完成させれば、

- Indeed
- Green
- Wantedly
- doda
- 求人ボックス

など、他サイト向けにも共通利用できる基盤になります。一方で、サイトごとのクローラーだけを先に作ると、Bot対策の変更のたびに個別修正が必要になり、保守コストが大きく増えます。
````

## assistant / 2026-07-24T13:57:40.0000000Z

```
null
```

## assistant / 2026-07-24T13:57:40.0000000Z

```
null
```

## user / 2026-07-24T14:00:48.0000000Z

```
ブラウザ管理基盤とは何か説明と作れるかどうか判断して下さい。
```

## assistant / 2026-07-24T14:00:50.0000000Z

````
結論から言うと、

**はい、EnterpriseOS向けに「ブラウザ管理基盤（Browser Orchestrator）」は十分作れます。**

ただし、**Indeed専用**ではなく、**あらゆるWebサイトで使い回せる共通基盤**として設計するのが正しいです。

Playwright自体も、永続プロファイル（Persistent Profile）やBrowserContext（独立セッション）を提供しており、ブラウザ状態を保持・分離する設計を前提にしています。citeturn0search4turn0search1

---

# Browser Orchestratorとは

イメージとしては

```
EnterpriseOS
        │
        ▼
Browser Orchestrator
        │
 ┌──────┼──────────┐
 │      │          │
Profile Session   Proxy
 │      │          │
 └──────┼──────────┘
        │
 Browser Pool
        │
        ▼
Indeed
Wantedly
Green
求人ボックス
LinkedIn
```

クローラーは

「Indeedへ行け」

と命令するだけです。

残りは全部

Browser Orchestrator

が担当します。

---

# 役割① Browser Pool

例えば100Botあるなら

```
Chrome001

Chrome002

Chrome003

...

Chrome100
```

これらを管理します。

必要になれば

```
Chrome101
```

を自動生成。

不要なら終了。

つまり

ブラウザのライフサイクル管理です。

---

# 役割② Profile Manager

一番重要です。

例えば

```
Bot001
```

は

```
Profile001
```

を使います。

中には

```
Cookies

History

LocalStorage

SessionStorage

Cache

IndexedDB
```

が保存されています。

つまり

毎回

新規Chrome

ではなく

「昨日の自分」

になります。

Playwrightも永続プロファイル（`launchPersistentContext`）をサポートしており、CookieやLocalStorageなどをディスクに保持できます。citeturn0search4turn0search0

---

# 役割③ Session Manager

例えば

```
Indeedログイン済み

期限あと12時間
```

なら

ログインし直しません。

期限切れなら

```
再ログイン
```

を行います。

つまり

ログイン状態を管理します。

---

# 役割④ Task Queue

```
求人検索

↓

応募一覧取得

↓

企業ページ

↓

求人詳細
```

を

Queue

で管理。

Browserが空けば

次のJobを実行。

---

# 役割⑤ Scheduler

例えば

Bot001

```
22:01
```

アクセス

↓

```
22:01:08
```

↓

```
22:01:20
```

↓

```
22:02:01
```

ランダム性を持たせる。

また

```
夜だけ動く

昼は停止
```

なども担当。

---

# 役割⑥ Health Check

例えば

```
Browser43

Memoryリーク
```

↓

再起動

```
Browser12

固まった
```

↓

Kill

```
Browser18

Crash
```

↓

再生成

これを自動化。

---

# 役割⑦ Fingerprint管理

例えば

```
Profile001

UA
Timezone
Language
Screen
Fonts
GPU
```

これらを

毎回同じ

にします。

重要なのは

**一貫性**

です。

---

# 役割⑧ Proxy管理

例えば

```
Profile001

↓

Residential Proxy A
```

毎回

同じProxy

を使う。

急に

```
日本

↓

アメリカ
```

になるような切り替えは避けます。

---

# EnterpriseOS版なら私はこう設計します

```
enterprise-browser/
│
├── BrowserPool
├── ProfileManager
├── SessionManager
├── CookieManager
├── ProxyManager
├── FingerprintManager
├── QueueManager
├── Scheduler
├── Metrics
├── Dashboard
└── API
```

そして

```
POST

/browser/start

/browser/stop

/browser/task

/browser/profile

/browser/status
```

のようなAPIを持たせます。

すると

Indeedクローラーは

```
Browserを貸して
```

と言うだけ。

他は全部

Browser基盤

が処理します。

---

# 技術的に作れるか？

**答えは「はい」です。**

ただし、難易度は高めです。

- **実装難易度:** ★★★★☆（4/5）
- **運用難易度:** ★★★★★（5/5）
- **EnterpriseOSへの価値:** ★★★★★（5/5）

理由は、この基盤は「一度作れば何度も使える」ためです。

- Indeed
- Green
- Wantedly
- LinkedIn
- 各種企業サイト

などに共通利用できます。

## 私からの提案

EnterpriseOSの中核資産として育てるなら、**クローラーを先に量産するのではなく、「Browser Orchestrator」を独立サービスとして先に完成させる**ことを勧めます。

その上に各サイト用の「Site Adapter（Indeed Adapter、Wantedly Adapterなど）」を載せる構造にすると、サイト側の変更が起きても影響範囲を限定でき、長期運用しやすいアーキテクチャになります。これは数年単位で保守するプロジェクトでは大きな差になります。 memcite
````

## assistant / 2026-07-24T14:00:51.0000000Z

```
null
```

## assistant / 2026-07-24T14:00:51.0000000Z

```
null
```

## user / 2026-07-24T14:07:03.0000000Z

```
/goal Browser Orchestratorを準備して計画を立て実行しながら不明点があればリサーチしながら高品質なサービスを完全させて下さい。
```

## assistant / 2026-07-24T14:07:05.0000000Z

```
EnterpriseOS内に、再利用可能なBrowser Orchestratorを実装する前提で進めます。まず現状のリポジトリ構成と既存基盤を確認し、設計・実装・テスト・運用ドキュメントまで一貫して仕上げます。
```

## assistant / 2026-07-24T14:07:26.0000000Z

```
null
```

## assistant / 2026-07-24T14:07:27.0000000Z

```
ローカル開発環境への接続が現在失敗しているため、GitHub上の正本を直接調査して進めます。まず既存設計を壊さないよう、ルート文書・構成・直近コミットを特定します。
```

## assistant / 2026-07-24T14:07:30.0000000Z

```
null
```

## assistant / 2026-07-24T14:07:55.0000000Z

```
現状は「ドキュメント優先・小さな垂直スライス」が明文化されており、いきなり大規模なBot回避基盤を入れるのは既存方針違反です。まず適法な取得・監査・セッション分離を中核にした仕様とADRを固定し、実装可能な最小サービスへ落とします。  
```

## assistant / 2026-07-24T14:08:04.0000000Z

```
null
```

## assistant / 2026-07-24T14:11:42.0000000Z

```
null
```

## assistant / 2026-07-24T14:11:43.0000000Z

````
## 実行結果

Browser Orchestratorの**基礎設計フェーズをEnterpriseOSへ追加**しました。

- [PR #2：Browser Orchestrator基盤設計](https://github.com/qooyanz-bot/EnterpriseOS/pull/2)
- [Issue #1：Milestone 1 実装タスク](https://github.com/qooyanz-bot/EnterpriseOS/issues/1)
- 作業ブランチ：`feat/browser-orchestrator-foundation`

追加した内容は以下です。

### 1. ADR 0013

`docs/adr/0013-browser-orchestrator-governed-acquisition.md`

Browser Orchestratorを、各クローラーが自由にブラウザを起動する仕組みではなく、以下を一元管理する**統制された実行境界**として定義しました。

- ブラウザ・Contextのライフサイクル
- テナント分離
- ジョブ受付とリース
- ソース別ポリシー判定
- レート・同時実行数・予算制限
- 証拠保存と監査ログ
- タイムアウト・クラッシュ回復
- CAPTCHAやアクセス拒否の検知
- Site Adapterの権限制限

重要なのは、**CAPTCHA回避やBot検知回避を中核機能にしなかったこと**です。

EnterpriseOSには「ダークスクレイピング禁止」が明記されています。 fileciteturn3file0L57-L65  
したがって、チャレンジが発生した場合は自動突破ではなく、停止・記録・手動審査へ送る設計にしています。

### 2. Specification 0007

`specs/active/0007-browser-orchestrator-foundation.md`

実装可能なレベルまで以下を固定しました。

- `BrowserJob`
- `SourcePolicy`
- `BrowserLease`
- `SessionRef`
- `AcquisitionResult`
- `EvidenceArtifact`
- `AuditEvent`
- `ChallengeEvent`

状態遷移も定義済みです。

```text
submitted
  → policy_denied
  → queued
queued
  → leased
  → cancelled
leased
  → running
  → queued（lease失効）
running
  → succeeded
  → failed
  → manual_review_required
  → cancelled
```

受入条件には以下を含めています。

- 未承認ソースではブラウザを起動しない
- 許可URL外ではブラウザを起動しない
- 重複ジョブを冪等処理する
- テナント間でContext・Session・Artifactを共有しない
- タイムアウト時にContextとLeaseを確実に解放する
- Challenge検知後は処理を停止する
- ログや証拠から秘密情報を除去する
- 外部サイトではなくローカル疑似ページだけで統合テストする

PlaywrightのBrowserContextは、Cookie、LocalStorage、SessionStorageなどを独立させたセッションを同一ブラウザ内に作れるため、初期実装の分離単位として適しています。 citeturn737556search2turn737556search3

### 3. Source Acquisition Policy Template

`docs/architecture/source-acquisition-policy-template.md`

サイトごとに以下を審査するテンプレートです。

- 利用目的
- APIや正規フィードで代替できない理由
- 利用規約・robots・契約上の許可
- URL許可範囲
- 取得可能データ
- 個人情報区分
- 同時実行数
- アクセス頻度
- 保存期間
- 403・429・CAPTCHA時の挙動
- 停止スイッチ
- 法務・セキュリティ承認

**ポリシーが存在しないソースはデフォルト拒否**です。

## 採用した構成

```text
packages/browser-contracts
        ↑
packages/browser-policy
        ↑
packages/browser-runtime
        ↑
apps/browser-worker

packages/browser-adapter-sdk
packages/browser-testing
```

初期版は分散システムにしません。

EnterpriseOSの既存方針も、スケール要件が明確になるまではモジュラーモノリスまたは少数のデプロイ単位を採用する方針です。 fileciteturn5file0L32-L41

PlaywrightテストではローカルWebサーバーを起動できるため、Indeed等へ接続せずに、正常ページ、403、429、ログインループ、Challenge、遅延、クラッシュを再現できます。 citeturn737556search0

## 率直な完成度判断

**設計・仕様・安全境界・実装計画は完成しました。サービス本体はまだ完成していません。**

今回、DevSpaceのローカル作業環境へ接続しようとしましたが、アカウント接続エラーで開けませんでした。そのため、以下を確認せずにTypeScriptコードを投入するのは危険だと判断しました。

- 現在の`package.json`
- `pnpm-workspace.yaml`
- 実際のモノレポ構造
- 使用中のテストランナー
- Zod等の既存依存
- Playwright導入状況
- CI構成
- 既存Queue・Audit・Artifact抽象化

ここを無視してコードを追加すると、以前のクローラーと同じく、**見かけ上動くが既存構成と統合できないコード**になります。

## 次の実装順序

優先順位は確定しています。

1. Runtime schema・ポリシー評価・状態機械
2. In-memory Queue／Lease／Audit／Artifact
3. Restricted Adapter SDK
4. Playwright Chromium Runtime
5. ローカル疑似サイト統合テスト
6. クラッシュ・Timeout・Challenge試験
7. EnterpriseOS既存Worker／Evidence基盤との統合
8. 許可を確認できた最初の実サイトAdapter

Indeed Adapterはこの後です。先にIndeedを実装すると、基盤ではなく再びIndeed専用クローラーになります。これは保守性と法的リスクの両面で悪手です。
````

## assistant / 2026-07-24T14:11:47.0000000Z

```
null
```

## assistant / 2026-07-24T14:11:47.0000000Z

```
null
```
