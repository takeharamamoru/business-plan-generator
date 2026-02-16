# business-plan-generator

## プロジェクト概要
Streamlit + Anthropic API で構築する「Agent Teams 事業計画ジェネレーター」。
5体のAIエージェントが並列で事業計画を作成し、Markdown/Excel/PDFでダウンロードできるWebアプリ。

## 技術スタック
- Frontend/Backend: Streamlit (Python 3.11+)
- AI: Anthropic API (claude-sonnet-4-5-20250929)
- Excel出力: openpyxl
- PDF出力: markdown + weasyprint
- 並列実行: concurrent.futures.ThreadPoolExecutor

## ディレクトリ構成
```
business-plan-generator/
├── CLAUDE.md
├── app.py                    # Streamlit エントリポイント
├── requirements.txt
├── .env.example
├── agents/
│   ├── __init__.py
│   ├── base.py               # BaseAgent（共通ロジック）
│   ├── market_researcher.py
│   ├── product_strategist.py
│   ├── financial_modeler.py
│   ├── gtm_strategist.py
│   └── integration_editor.py
├── orchestrator/
│   ├── __init__.py
│   └── runner.py             # 並列実行制御
├── templates/
│   ├── __init__.py
│   └── catalog.py            # 全テンプレート定義
├── exporters/
│   ├── __init__.py
│   ├── excel_exporter.py
│   └── pdf_exporter.py
└── ui/
    ├── __init__.py
    ├── sidebar.py
    └── progress.py
```

## コーディング規約
- 言語: Python、型ヒント必須
- docstring: Google スタイル
- UI テキスト: 日本語
- エラーメッセージ: 日本語
- 変数名・関数名: 英語（snake_case）
- クラス名: 英語（PascalCase）

## 重要な設計方針
1. 並列実行は ThreadPoolExecutor を使う（Streamlitとの相性が良い）
2. 各エージェントはストリーミングAPIを使い、進捗をコールバックで通知する
3. Phase 1（4エージェント並列）→ Phase 2（統合エージェント）の2フェーズ構成
4. コスト最適化: Sonnet 4.5 メイン、プロンプトキャッシュ活用
5. テンプレートは辞書ベースで定義し、追加が容易な構造にする
