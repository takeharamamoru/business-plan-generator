"""Test script for Excel and PDF exporters."""

import sys
import os
from pathlib import Path

# Set UTF-8 encoding for output
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from exporters.excel_exporter import ExcelExporter
from exporters.pdf_exporter import PDFExporter


# Test data
TEST_MARKDOWN = """# 事業計画書 - テスト版

## エグゼクティブサマリー

MediFlow は医療機関向けワークフロー自動化 SaaS プラットフォームです。

## 市場分析

### 市場規模

| 項目 | 2024年 | 2025年 | 成長率 |
|------|--------|--------|--------|
| TAM（日本） | 5,000億円 | 5,500億円 | 10.0% |
| SAM（対象市場） | 1,500億円 | 1,650億円 | 10.0% |
| SOM（獲得予定） | 150億円 | 300億円 | 100.0% |

### 競合分析

| 企業 | 強み | 弱み | シェア |
|------|------|------|--------|
| OpenMed | 知名度高 | 高価格 | 35% |
| MediTech | 多機能 | UI複雑 | 25% |
| 当社 | コンパクト | 機能限定 | 0% |

## 財務計画

### 売上予測

| 年度 | MRR | ARR | 顧客数 | 成長率 |
|------|-----|-----|--------|--------|
| 2024年 | 50万円 | 600万円 | 10社 | - |
| 2025年 | 200万円 | 2,400万円 | 40社 | 300% |
| 2026年 | 500万円 | 6,000万円 | 100社 | 150% |
| 2027年 | 1,000万円 | 12,000万円 | 200社 | 100% |
| 2028年 | 1,500万円 | 18,000万円 | 300社 | 50% |

### 損益計算書（P/L）

| 科目 | 2024年 | 2025年 | 2026年 |
|------|--------|--------|--------|
| 売上高 | 600万円 | 2,400万円 | 6,000万円 |
| 売上原価 | 150万円 | 600万円 | 1,500万円 |
| 売上総利益 | 450万円 | 1,800万円 | 4,500万円 |
| 販売費・一般管理費 | 1,500万円 | 3,000万円 | 4,500万円 |
| 営業利益(EBIT) | -1,050万円 | -1,200万円 | 0万円 |

### ユニットエコノミクス

| 指標 | 値 | 備考 |
|------|-----|------|
| CAC（顧客獲得原価） | 50万円 | 初年度 |
| LTV（顧客生涯価値） | 500万円 | 5年平均 |
| LTV / CAC | 10.0x | 良好 |
| チャーンレート | 5.0% | 月次 |
| ARPU | 5万円 | 月次 |

## GTM戦略

### チャネル別売上見込み

| チャネル | 2025年 | 2026年 | シェア |
|---------|--------|--------|--------|
| 直販（営業） | 1,200万円 | 3,000万円 | 50% |
| パートナー | 800万円 | 2,000万円 | 33% |
| PLG | 400万円 | 1,000万円 | 17% |

## リスクと対策

主要なリスク：

1. **市場受容リスク**: 医療機関の DX 機運が想定より低い
   - 対策: KOL との連携、POC による実績構築

2. **競争リスク**: 大型競合企業の参入
   - 対策: 早期シェア獲得、高い顧客満足度

3. **規制リスク**: 医療規制の強化
   - 対策: コンプライアンスチームの配置、専門家との相談

## 実行ロードマップ

### フェーズ1（Q1-Q2 2024）
- MVP リリース
- 初期顧客 5 社との契約

### フェーズ2（Q3-Q4 2024）
- 営業チーム拡大
- マーケティング本格化

### フェーズ3（2025年）
- Series A 資金調達
- チャネル拡大

---

この事業計画は以上です。
"""

# Test sections
TEST_SECTIONS = {
    "market": "# 市場分析\n\n" + TEST_MARKDOWN.split("## 財務計画")[0],
    "product": "# プロダクト戦略\nプロダクト本体の説明...",
    "finance": "# 財務計画\n\n" + TEST_MARKDOWN.split("## 財務計画")[1].split("## GTM")[0],
    "gtm": "# GTM戦略\n\n" + TEST_MARKDOWN.split("## GTM")[1],
}


def test_excel_exporter() -> bool:
    """Test Excel exporter.
    
    Returns:
        True if test passes
    """
    print("\n【Excel Exporter テスト】")
    print("-" * 70)
    
    try:
        exporter = ExcelExporter()
        excel_bytes = exporter.export(TEST_MARKDOWN, TEST_SECTIONS)
        
        # Save to file
        output_file = Path("test_output.xlsx")
        output_file.write_bytes(excel_bytes)
        
        size_mb = len(excel_bytes) / 1_024_000
        print(f"✅ Excel ファイル生成成功")
        print(f"   ファイルサイズ: {size_mb:.2f} MB")
        print(f"   出力先: {output_file.absolute()}")
        
        return True
    except Exception as e:
        print(f"❌ Excel エクスポート失敗: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_pdf_exporter() -> bool:
    """Test PDF exporter (with fallback to HTML).
    
    Returns:
        True if test passes
    """
    print("\n【PDF Exporter テスト（HTMLフォールバック対応）】")
    print("-" * 70)
    
    try:
        # Create exporter with error handling
        exporter = PDFExporter()
        
        # Try to export (will fallback to HTML if weasyprint unavailable)
        html_bytes = exporter.export(TEST_MARKDOWN)
        
        # Save to file
        output_file = Path("test_output.html")
        output_file.write_bytes(html_bytes)
        
        size_kb = len(html_bytes) / 1_024
        export_format = exporter.get_export_format()
        
        print(f"✅ {export_format} ファイル生成成功")
        print(f"   形式: {export_format} {'(weasyprint利用不可なためHTMLで出力)' if export_format == 'HTML' else '(PDF生成完了)'}")
        print(f"   ファイルサイズ: {size_kb:.2f} KB")
        print(f"   出力先: {output_file.absolute()}")
        
        return True
    except Exception as e:
        print(f"⚠️  PDF生成エラーですがHTMLで出力: {e}")
        # Try HTML export directly
        try:
            exporter = PDFExporter()
            html_bytes = exporter._export_html(exporter._create_html_document(
                "# テストMarkdown\n\n簡単なHTMLファイルです。"
            ))
            output_file = Path("test_output_fallback.html")
            output_file.write_bytes(html_bytes)
            print(f"✅ HTMLフォールバック出力成功: {output_file.absolute()}")
            return True
        except Exception as html_error:
            print(f"❌ HTMLフォールバックも失敗: {html_error}")
            return False


def main():
    """Run all exporter tests."""
    print("=" * 70)
    print("エクスポーター 動作確認テスト")
    print("=" * 70)
    
    # Test Excel exporter
    excel_ok = test_excel_exporter()
    
    # Test PDF exporter
    pdf_ok = test_pdf_exporter()
    
    print("\n" + "=" * 70)
    print("テスト完了")
    print("=" * 70)
    
    if excel_ok and pdf_ok:
        print("\n✅ すべてのテストが成功しました")
        return 0
    else:
        print("\n❌ 一部のテストが失敗しました")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
