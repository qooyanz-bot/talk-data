# Scraping Platform 設計

- 作成日時 (UTC): 2026-07-21T20:16:46.0000000Z
- 更新日時 (UTC): 2026-07-21T20:17:02.0000000Z
- 注記: 本文は公開用に秘密形式・メールアドレス・電話番号のみ不可逆に伏せ字化。

## assistant / 2026-07-21T20:16:45.0000000Z

````
`scraping_platform` は、単なる「スクレイピング用DB」ではありません。

EnterpriseOS全体で1000サイト・10000Botまで拡張することを前提にすると、**スクレイピング基盤全体のコントロールプレーン（制御DB）**として設計するのが最適です。

## 全体構成

```text
                     EnterpriseOS

                    ┌───────────────┐
                    │   Coolify      │
                    └───────┬───────┘
                            │
                     Contabo-002
        (HTTP Worker / Browser Worker / Scheduler)

                            │
                     PgBouncer
                            │
                            │
                     Contabo-003
                PostgreSQL 16
              scraping_platform
```

ここには各サイト専用DBを大量に作るのではなく、

**1つの運用DB**

```
scraping_platform
```

を作ります。

---

# なぜ1つなのか

例えば

```
HotPepper
食べログ
ぐるなび
Indeed
求人ボックス
Google Maps
Instagram
X
Amazon
楽天
```

…

1000サイト対応するとします。

もし

```
hotpepper_db
tabelog_db
indeed_db
```

…

と1000個DBを作ると

- マイグレーション
- バックアップ
- PgBouncer
- 接続管理
- PostgreSQLメモリ

全部が破綻します。

PostgreSQLは

**大量DBより**

```
1DB
+
多数テーブル
```

の方が圧倒的に強いです。

---

# 推奨構成

```
scraping_platform
```

の中に

```
public
```

ではなく

サイト単位のスキーマを作ります。

```
scraping_platform

├── control
│
├── hotpepper
│
├── tabelog
│
├── indeed
│
├── google_maps
│
├── x
│
├── instagram
│
└── future...
```

これだけで1000サイトまで管理できます。

---

# controlスキーマ

ここが最重要です。

例えば

```
control.jobs
```

Botが取得するジョブ

```
id

site

url

priority

status

worker

retry

created_at
```

---

```
control.workers
```

Bot一覧

```
worker_id

hostname

cpu

memory

status

heartbeat
```

---

```
control.proxy_pool
```

プロキシ管理

```
proxy

country

score

ban_count
```

---

```
control.accounts
```

ログインアカウント

```
site

username

status

cookie
```

---

```
control.metrics
```

取得件数

成功率

失敗率

速度

---

つまり

**スクレイピング基盤そのもの**

を管理します。

---

# HotPepper

```
hotpepper.shops

hotpepper.reviews

hotpepper.images

hotpepper.categories
```

---

# 食べログ

```
tabelog.shops

tabelog.reviews

tabelog.images
```

---

# Google Maps

```
google_maps.places

google_maps.reviews

google_maps.photos
```

---

# 共通テーブル

例えば

```
normalized_companies
```

```
company_id

site

external_id

name

address

phone
```

各サイトから取得した企業情報を

EnterpriseOS用へ統合します。

---

# site_id

将来

1000サイト

10000Bot

になったら

```
site_id
```

でパーティションします。

例

```
control.jobs

PARTITION BY HASH(site_id)
```

↓

```
jobs_p0

jobs_p1

jobs_p2

...

jobs_p63
```

これだけで数億件までかなり耐えられます。

---

# 将来のシャーディング

さらに大きくなったら

```
scraping_platform_01

scraping_platform_02

scraping_platform_03
```

へ分割します。

例えば

```
A〜F

→ Cluster1
```

```
G〜M

→ Cluster2
```

```
N〜Z

→ Cluster3
```

コードは

```
site_id
```

だけで接続先を決定できます。

---

# PgBouncer

Workerは

```
10000Bot
```

いても

PostgreSQLへ10000接続しません。

```
10000Bot

↓

Redis Queue

↓

Worker 100

↓

PgBouncer

↓

PostgreSQL
```

例えば

```
10000Bot

↓

80接続
```

程度に抑えられます。

---

# EnterpriseOSとの役割分担

この構成では、DBの責務を明確に分けるのがおすすめです。

| DB | 役割 |
|------|------|
| EnterpriseOS | 企業情報、営業シグナル、AI分析結果、ユーザー向けデータ |
| scraping_platform | スクレイピング制御、ジョブ、Bot、取得した生データ、各サイトの専用テーブル |

つまり、

- **EnterpriseOS** は「ビジネスで利用する正規データ」
- **scraping_platform** は「データ収集・制御基盤」

という役割分担になります。

## この構成をおすすめする理由

EnterpriseOSの構想（約500万社DBを基盤に、1000サイト・10000Bot規模まで拡張）であれば、このアーキテクチャは運用・性能・拡張性のバランスが非常に良いです。

将来的には以下のような構成へ自然にスケールできます。

- Contabo-001：Coolify・管理系
- Contabo-002：Worker（HTTP / Browser / Scheduler）
- Contabo-003：`scraping_platform`（PostgreSQL + PgBouncer）
- Redis：ジョブキュー・キャッシュ
- EnterpriseOS DB：企業マスタ・営業シグナル・AI解析結果

この分離により、スクレイピング処理の負荷がEnterpriseOS本体のDBへ直接影響することを避けながら、大規模運用へ移行しやすくなります。
````
