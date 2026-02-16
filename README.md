# 🤖 Agent Teams 事業計画ジェネレーター

エンタープライズグレードのAIエージェント協調型システムで、5体の専門AIエージェントが並列実行して高品質な事業計画書を自動生成します。

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python 3.11+](https://img.shields.io/badge/Python-3.11+-green.svg)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red.svg)
[![Tests](https://img.shields.io/badge/Tests-8%2F8%20Pass-brightgreen.svg)](TEST_RESULTS.md)

---

## 🎯 プロジェクト概要

このアプリケーションは、**Claude Sonnet 4.5** を搭載した5体の AI エージェントが連携して、わずかな入力から **わずか3～4分で** 本格的な事業計画書を生成します。

### 主な特徴

- ✅ **5体のAIエージェント並列実行** - 市場分析、プロダクト戦略、財務計画、GTM戦略、統合エディタ
- ✅ **複数業種テンプレート** - SaaS、Healthcare、Manufacturing、Retail、Custom
- ✅ **複数形式エクスポート** - Markdown、Excel（5シート）、PDF/HTML
- ✅ **リアルタイムプログレス表示** - 各エージェントの生成状況をライブ表示
- ✅ **トークン使用量・コスト推定** - 自動計算で透明性確保
- ✅ **グレースフルデグラデーション** - エージェント失敗時も他は継続、PDF未対応環境ではHTML出力
- ✅ **エンタープライズレディ** - エラーハンドリング、リトライ、レート制限対応

### 生成される事業計画書の構成

1. **Executive Summary** - 事業の概要と財務予測
2. **Market Analysis** - TAM/SAM/SOM、成長率、競争環境、規制、トレンド
3. **Product Strategy** - ビジョン、差別化、機能、技術スタック、ロードマップ
4. **Financial Modeling** - 収入予測、P&L、ユニットエコノミクス、資金調達シナリオ
5. **Go-To-Market** - 市場参入戦略、営業体制、チャネル、パートナーシップ
6. **Risk Analysis** - リスク評価と対策
7. **Implementation Roadmap** - 12～60ヶ月の実装計画
8. **Appendix** - 詳細資料

---

## 🚀 セットアップ手順

### 前提条件
- Python 3.11 以上
- Anthropic API キー（[https://console.anthropic.com](https://console.anthropic.com)）
- Git

### 1. リポジトリをクローン
```bash
git clone https://github.com/yourusername/business-plan-generator.git
cd business-plan-generator
```

### 2. 仮想環境を作成・有効化
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 3. 依存パッケージをインストール
```bash
pip install -r requirements.txt
```

### 4. 環境変数を設定
```bash
# .env ファイルをコピーして編集
cp .env.example .env

# エディタで .env を開き、ANTHROPIC_API_KEY を設定
# ANTHROPIC_API_KEY=sk-ant-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 5. Streamlit アプリを起動
```bash
streamlit run app.py
```

ブラウザが自動的に開き、`http://localhost:8501` にアクセスします。

---

## 📖 使い方

### ステップ1: テンプレート選択
サイドバーから業種テンプレートを選択します：
- **☁️ SaaS** - SaaS型サービス（MRR/ARR、LTV/CAC、Rule of 40対応）
- **🏥 Healthcare** - ヘルスケア・医療機器（規制対応、承認戦略）
- **🏭 Manufacturing** - 製造業（CapEx、サプライチェーン）
- **🛒 Retail** - 小売・EC（GMV、ロジスティクス）
- **📋 Custom** - カスタム（ユーザー定義）

### ステップ2: 企業情報を入力
必須項目：
- **企業名** - 例：MediFLow
- **事業説明** - 事業の簡単な説明（2～3行）

テンプレート固有フィールド：
- SaaS: ターゲット市場、価格帯、技術スタック
- Healthcare: 対象疾患、規制クラス、ターゲットユーザー
- その他も同様

### ステップ3: 生成実行
1. サイドバーの詳細設定で計画期間（3～7年）を調整
2. **Generate ボタン**をクリック
3. リアルタイムプログレスバーで進捗を確認

```
🔍 Market Researcher    ████████░░  80% 生成中...
💡 Product Strategist   ██████████ 100% ✅ 完了
📊 Financial Modeler    ████████░░  75% 生成中...
🤝 GTM Strategist       ██░░░░░░░░  20% 生成中...
📝 Integration Editor   ░░░░░░░░░░   0% 待機中
```

### ステップ4: 結果を確認・ダウンロード
3つのタブで結果を確認：

1. **📄 Markdown** - 統合事業計画書（Markdown形式）
   - テキストエディタで編集可能
   - GitHub/Notionで共有可能

2. **📊 Excel (本日は中止)**
   - 5シートで構成（サマリー、市場分析、プロダクト、財務、GTM）
   - セルの計算式は保持
   - レイアウト編集可能

3. **📥 PDF/HTML**
   - PDF（Linux/Docker環境）
   - HTML（Windows環境、ブラウザで印刷→PDF可能）
   - スタイル済みで印刷対応

### 詳細セクション確認
メインエリアのセクションexpanderで、各エージェントの詳細出力を確認できます：

```
▶ 【市場分析】 (Market Researcher)
  TAM/SAM/SOM分析、成長率、競争環境...
▶ 【プロダクト戦略】 (Product Strategist)
  ビジョン、差別化ポイント、技術スタック...
▶ 【財務計画】 (Financial Modeler)
  5年間の収入/支出/利益見通し...
▶ 【GTM戦略】 (GTM Strategist)
  市場参入方法、営業体制、マーケティング...
```

---

## 🏗️ アーキテクチャ

### システム構成図

```mermaid
graph TB
    User["👤 ユーザー"]
    UI["🎨 Streamlit UI<br/>sidebar + progress + tabs"]
    
    subgraph "📊 Orchestrator"
        Orch["AgentOrchestrator<br/>Phase 1 & 2 制御"]
    end
    
    subgraph "Phase 1: 並列実行 (4エージェント)"
        MR["🔍 MarketResearcher<br/>市場分析・TAM/SAM/SOM"]
        PS["💡 ProductStrategist<br/>プロダクト戦略"]
        FM["📊 FinancialModeler<br/>財務計画"]
        GS["🤝 GTMStrategist<br/>市場参入戦略"]
    end
    
    subgraph "Phase 2: 統合実行"
        IE["📝 IntegrationEditor<br/>5体の出力を統合"]
    end
    
    subgraph "🔌 外部サービス"
        API["🌍 Anthropic API<br/>Claude Sonnet 4.5"]
        Template["📋 テンプレート<br/>SaaS/Healthcare/etc"]
    end
    
    subgraph "💾 エクスポート"
        MD["📄 Markdown"]
        EX["📊 Excel"]
        PDF["📥 PDF/HTML"]
    end
    
    User -->|入力| UI
    UI -->|制御| Orch
    Orch -->|Phase 1 実行| MR
    Orch -->|Phase 1 実行| PS
    Orch -->|Phase 1 実行| FM
    Orch -->|Phase 1 実行| GS
    MR -->|streaming| API
    PS -->|streaming| API
    FM -->|streaming| API
    GS -->|streaming| API
    MR -->|会話履歴| Template
    Orch -->|Phase 2 実行| IE
    IE -->|統合入力| API
    IE -->|多言語対応| API
    MR -->|結果| Orch
    PS -->|結果| Orch
    FM -->|結果| Orch
    GS -->|結果| Orch
    IE -->|統合結果| UI
    UI -->|表示| User
    UI -->|エクスポート| MD
    UI -->|エクスポート| EX
    UI -->|エクスポート| PDF
    MD -->|ダウンロード| User
    EX -->|ダウンロード| User
    PDF -->|ダウンロード| User
```

### モジュール構成

```
business-plan-generator/
├── agents/                         # AI エージェント定義
│   ├── base.py                     # BaseAgent（共通機能）
│   ├── market_researcher.py        # 市場分析
│   ├── product_strategist.py       # プロダクト戦略
│   ├── financial_modeler.py        # 財務計画
│   ├── gtm_strategist.py           # GTM戦略
│   └── integration_editor.py       # 統合エディタ（Phase 2）
├── orchestrator/
│   └── runner.py                   # AgentOrchestrator（Phase制御）
├── templates/
│   └── catalog.py                  # テンプレート定義（5種類）
├── exporters/
│   ├── excel_exporter.py           # Excel → 5シート
│   └── pdf_exporter.py             # PDF/HTML エクスポート
├── ui/
│   ├── sidebar.py                  # 入力フォーム
│   └── progress.py                 # プログレス表示
├── app.py                          # Streamlit メインアプリ
├── requirements.txt                # 依存パッケージ
├── .env.example                    # 環境変数テンプレート
├── .gitignore                      # Git 除外設定
└── README.md                       # このファイル
```

### 実行フロー

```
1. ユーザー入力 (Streamlit UI)
   ├─ テンプレート選択
   ├─ 企業情報入力
   ├─ 計画期間設定
   └─ 詳細設定（モデル、トークン制限）

2. Phase 1: 4エージェント並列実行 (ThreadPoolExecutor)
   ├─ MarketResearcher → 市場分析（TAM/SAM/SOM）
   ├─ ProductStrategist → プロダクト戦略
   ├─ FinancialModeler → 財務計画（5年間の見通し）
   └─ GTMStrategist → GTM戦略

3. Phase 2: 統合エージェント実行
   └─ IntegrationEditor → Phase 1全出力を統合

4. エクスポート処理
   ├─ ExcelExporter → 5シート (openpyxl)
   ├─ PDFExporter → PDF or HTML (markdown2 + weasyprint/fallback)
   └─ Markdown としてそのまま利用可能

5. Streamlit UI で表示・ダウンロード
   ├─ リアルタイムプログレス表示
   ├─ トークン使用量・コスト表示
   ├─ セクション詳細 expander 表示
   └─ ファイルダウンロード
```

---

## 💰 コスト目安

### 料金体系（Claude Sonnet 4.5）

| 項目 | 価格 |
|-----|------|
| **入力** | $3 / 100万トークン |
| **出力** | $15 / 100万トークン |

### 事業計画書1件あたりの推定コスト

#### SaaS テンプレート（5年計画）
- **入力トークン**: 23,670
- **出力トークン**: 25,000
- **合計トークン**: 48,670
- **推定コスト**: **$0.44 USD** ≈ **¥65 円**
- **実行時間**: 196秒 (3分16秒)

#### Healthcare テンプレート（5年計画）
- **推定コスト**: **$0.35～$0.45 USD**
- **実行時間**: 180～200秒

#### Manufacturing テンプレート（5年計画）
- **推定コスト**: **$0.40～$0.50 USD**
- **実行時間**: 190～210秒

#### Retail テンプレート（5年計画）
- **推定コスト**: **$0.35～$0.45 USD**
- **実行時間**: 180～200秒

#### Custom テンプレート（3年計画）
- **推定コスト**: **$0.30～$0.35 USD**
- **実行時間**: 150～180秒

### 月額費用シミュレーション

| 使用頻度 | 月間事業計画数 | 月額推定コスト |
|--------|------------|-----------|
| **軽度** (週1回) | 4 | $1.76 USD ≈ ¥260 |
| **中度** (週3回) | 12 | $5.28 USD ≈ ¥790 |
| **頻繁** (毎日) | 30 | $13.20 USD ≈ ¥1,980 |

---

## 🔧 高度な使い方

### カスタムテンプレート作成

新しいテンプレートを追加するには `templates/catalog.py` を編集：

```python
TEMPLATES = {
    "custom_template": {
        "name": "🏢 カスタム業種",
        "icon": "🏢",
        "description": "あなたの業種に合わせた事業計画書",
        "context_fields": {
            "industry": "業種の詳細説明",
            "focus_area": "特に重視する領域",
        },
        "agent_hints": {
            "MarketResearcher": "この業種の市場規模は〜",
            # ... その他のエージェントへのヒント
        }
    }
}
```

### フロント側での API 利用

Streamlit 以外の Frontend から API として利用する場合、FastAPI ラッパーを追加可能：

```python
from fastapi import FastAPI, HTTPException
from orchestrator.runner import AgentOrchestrator

app = FastAPI()

@app.post("/generate")
async def generate_plan(context: dict):
    orchestrator = AgentOrchestrator(context)
    result = orchestrator.run_all()
    return result
```

---

## 🧪 テスト実行

### 統合テストの実行

```bash
# 全テストの実行（SaaS + Custom テンプレート）
python test_integration_full.py

# 個別エージェントのテスト
python agents/test_agent.py

# オーケストレーターのテスト
python test_orchestrator_phase1.py
```

### テスト結果

✅ **8/8 シナリオ パス**（詳細は [TEST_RESULTS.md](TEST_RESULTS.md) を参照）

---

## 📦 依存パッケージ

### Core
- `streamlit` - Web UI
- `anthropic` - Claude API
- `python-dotenv` - 環境変数管理
- `tenacity` - リトライロジック

### エクスポート
- `openpyxl` - Excel 生成
- `markdown` - Markdown パース
- `weasyprint` - PDF 生成（オプション）

### 開発
すべての依存は `requirements.txt` に含まれています：

```bash
pip install -r requirements.txt
```

---

## 🔐 セキュリティ

### API キー管理
- ✅ `.env` ファイルに API キーを保存（Git リポジトリに含めない）
- ✅ `.gitignore` で `.env` を除外
- ✅ Streamlit Cloud: Secrets 管理で安全に提供

### 入力検証
- ✅ 企業名・説明の長さ制限
- ✅ テンプレート選択肢の限定
- ✅ SQL インジェクション対策（N/A）

### エラーハンドリング
- ✅ APIキー未設定時の明確なエラーメッセージ
- ✅ ネットワークエラー時のリトライ（最大2回）
- ✅ レート制限（429）時の待機とリトライ
- ✅ 個別エージェント失敗時のグレースフルデグラデーション

---

## 📚 トラブルシューティング

### API キーエラー
```
❌ APIキーが設定されていません。
```
**解決方法**: `.env` ファイルを確認し、ANTHROPIC_API_KEY を設定してください。

### メモリ不足エラー
```
MemoryError: Unable to allocate ...
```
**解決方法**: 計画期間を短縮（7年 → 5年）するか、マシンのメモリを増加させてください。

### Streamlit ポート競合
```
Address already in use
```
**解決方法**: 別のポートでアプリを起動してください：
```bash
streamlit run app.py --server.port 8502
```

### PDF 生成エラー（Windows）
```
WeasyPrint could not import some external libraries.
```
**解決方法**: 自動的に HTML 出力にフォールバックされます。ブラウザで Ctrl+P → PDF を選択。

### ネットワークタイムアウト
```
ConnectionError: Connection timed out
```
**解決方法**: インターネット接続を確認し、Anthropic API へのアクセスが可能か確認してください。

---

## 🚀 デプロイ

### Streamlit Cloud での運用

1. GitHub リポジトリを作成
2. [Streamlit Cloud](https://streamlit.io/cloud) でログイン
3. **New app** → リポジトリを選択 → `app.py` を指定
4. Secrets で ANTHROPIC_API_KEY を設定

```toml
[secrets]
ANTHROPIC_API_KEY = "sk-ant-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

5. **Deploy** をクリック

### Docker でのデプロイ

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}

CMD ["streamlit", "run", "app.py"]
```

```bash
docker build -t business-plan-generator .
docker run -e ANTHROPIC_API_KEY="sk-ant-v1-..." -p 8501:8501 business-plan-generator
```

---

## 📄 ライセンス

このプロジェクトは **MIT License** の下で公開されています。

詳細は [LICENSE](LICENSE) ファイルを参照してください。

### 使用可能な方法
- ✅ 商用利用
- ✅ 改変
- ✅ 配布
- ✅ プライベート利用

### 条件
- ⚠️ ライセンスと著作権表示を含むこと

---

## 🤝 貢献

改善提案やバグ報告は Issue を作成してください。

プルリクエストも歓迎します！

---

## 📞 サポート

質問や問題がある場合：
1. [Issue](https://github.com/yourusername/business-plan-generator/issues) で既存の报告を確認
2. 新しい Issue を作成（詳細なエラーメッセージを含める）
3. [Discussions](https://github.com/yourusername/business-plan-generator/discussions) で質問

---

## 📊 プロジェクト統計

| 項目 | 数値 |
|-----|------|
| **コード行数** | ~2,500 行 |
| **AI エージェント数** | 5体 |
| **テンプレート数** | 5種類 |
| **エクスポート形式** | 3種類 |
| **テストシナリオ** | 8/8 パス ✅ |
| **ドキュメント** | 完全整備 |

---

## 🎉 クイックスタート

まだはじめていない方へ：

```bash
# 1. クローン
git clone https://github.com/yourusername/business-plan-generator.git
cd business-plan-generator

# 2. セットアップ
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # API キーを設定

# 3. 起動
streamlit run app.py

# 4. ブラウザで http://localhost:8501 を開く
```

たったこれだけで、プロフェッショナルな事業計画書が自動生成されます！

---

**Last Updated**: 2026年2月17日  
**Version**: 1.0.0  
**Status**: ✅ Production Ready
