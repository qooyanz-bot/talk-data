# Export memories request

- 作成日時 (UTC): 2026-07-13T06:26:15.0000000Z
- 更新日時 (UTC): 2026-07-13T06:26:26.0000000Z
- 注記: 本文は公開用に秘密形式・メールアドレス・電話番号のみ不可逆に伏せ字化。

## user / 2026-07-13T06:25:53.0000000Z

```
Export all of my stored memories and any context you've learned about me from past conversations. Preserve my words verbatim where possible, especially for instructions and preferences.

## Categories (output in this order):

1. **Instructions**: Rules I've explicitly asked you to follow going forward — tone, format, style, "always do X", "never do Y", and corrections to your behavior. Only include rules from stored memories, not from conversations.

2. **Identity**: Name, age, location, education, family, relationships, languages, and personal interests.

3. **Career**: Current and past roles, companies, and general skill areas.

4. **Projects**: Projects I meaningfully built or committed to. Ideally ONE entry per project. Include what it does, current status, and any key decisions. Use the project name or a short descriptor as the first words of the entry.

5. **Preferences**: Opinions, tastes, and working-style preferences that apply broadly.

## Format:

Use section headers for each category. Within each category, list one entry per line, sorted by oldest date first. Format each line as:

[YYYY-MM-DD] - Entry content here.

If no date is known, use [unknown] instead.

## Output:
- Wrap the entire export in a single code block for easy copying.
- After the code block, state whether this is the complete set or if more remain.
```

## assistant / 2026-07-13T06:26:21.0000000Z

````
```text
# 1. Instructions

[2026-02-02] - Use Japanese.
[2026-02-02] - Prefer conclusion → reason → steps.
[2026-02-02] - Be concise; use bullets where appropriate.
[2026-02-02] - If something is ambiguous, ask at most one clarifying question.

# 2. Identity

[2026-07-11] - 英語は中1レベル; 仕事/プレゼンで使う英単語を発音と意味つきで学びたい。
[2026-07-11] - 海外向けSaaS・プレゼン・営業に役立つ単語を優先したい; プロジェクト名として「DealVane」を海外展開したい。

# 3. Career

[unknown] - バイブコーダー

# 4. Projects

[2026-06-16] - KijiPort — AI content CMS for creators; manages ideas, article writing, platform-specific images, scheduling, and performance analytics across note, X, Threads, YouTube, Substack, Medium, and Hashnode. Desired UI style: calm, professional, editorial, dense but readable, left sidebar + main workspace + right inspector.
[2026-07-11] - DealVane仕様リポジトリ — GitHubに初期仕様リポジトリを用意済み。内容はAGENTS.md、PLANS.md、contracts、schemas、openapi、adr、memory、evals、tasksを含む。
[2026-07-11] - DealVane仕様レビュー — Codexレビュー結果として、SQL/OpenAPI/contracts間の矛盾を記録済み。TA[REDACTED_SECRET].mdとPREIMPLEMENTATION-VALIDATION.mdに不整合・未確定事項を整理し、TASK-0001/0002の実装順序と受入テスト対応表も作成済み。
[2026-07-11] - EnterpriseOS — Working project name. Persistent project memory file `PROJECT_MEMORY.md`; repository includes `AGENTS.md`, `README.md`, `docs/index.md`; 79 files restored from a Git bundle; repository check passed; brand name still undecided, and EnterpriseOS is not the final brand name.

# 5. Preferences

[2026-06-20] - `C:\Users\user\.codex` is the permitted DevSpace workspace folder.
```

This is **not the complete set** of information I've ever learned across conversations. It is the complete set of **stored long-term memories and retrieved persistent context** available to me for export. Temporary conversation history, expired context, and information that was never saved as long-term memory are not included and cannot be exported verbatim.
````

## assistant / 2026-07-13T06:26:21.0000000Z

```
null
```

## assistant / 2026-07-13T06:26:21.0000000Z

```
null
```
