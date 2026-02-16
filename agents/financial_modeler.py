"""FinancialModeler agent for financial planning."""

from agents.base import BaseAgent


class FinancialModeler(BaseAgent):
    """Financial Modeling Agent.
    
    Creates comprehensive financial projections including revenue forecasts,
    cost structures, unit economics, funding plans, and sensitivity analysis.
    """

    def __init__(self) -> None:
        """Initialize FinancialModeler agent."""
        super().__init__(
            name="FinancialModeler",
            role="財務モデリング専門家",
        )

    def get_system_prompt(self, context: dict) -> str:
        """Get system prompt for financial modeling.
        
        Args:
            context: Context dictionary containing company and business info
            
        Returns:
            System prompt for financial planning
        """
        return (
            "あなたは財務モデリングの専門家です。"
            "DetailedでRealisticな財務予測を以下の構造で提供してください:\n\n"
            "## 売上予測\n"
            "- 年次売上推移テーブル（Markdownテーブル形式）\n"
            "- ARR（Annual Recurring Revenue）、MRR、ASP、顧客数の推移\n"
            "- 成長仮定の詳細説明\n\n"
            "## コスト構造と損益計算書\n"
            "- 年次P/L（損益計算書）テーブル（Markdownテーブル形式）\n"
            "  * 売上高\n"
            "  * 売上原価（COGS）\n"
            "  * 販売費・一般管理費（SG&A：営業、マーケティング、給与など）\n"
            "  * R&D費用\n"
            "  * 減価償却費\n"
            "  * EBITDA / Operating Income / Net Income\n"
            "- 各コスト項目の根拠説明\n\n"
            "## ユニットエコノミクス\n"
            "- LTV（顧客生涯価値）計算式と値\n"
            "- CAC（顧客獲得単価）計算式と値\n"
            "- LTV/CACレシオ\n"
            "- ARPU / ARPA（平均顧客当たり収益）\n"
            "- チャーンレート（月次、年次）\n"
            "- ペイバック期間\n\n"
            "## 資金調達計画\n"
            "- 初期資金調達額（シード、Series A など）\n"
            "- 調達タイミングと用途\n"
            "- 推定ランウェイ（資金で何ヶ月動けるか）\n\n"
            "## 感度分析\n"
            "- 3つのシナリオ：ベースケース、アップサイド、ダウンサイド\n"
            "- 各シナリオの主要前提条件\n"
            "- 各シナリオの3年累積利益\n\n"
            "## 主要KPIサマリー\n"
            "- 重要なメトリクスの年次推移テーブル（Markdownテーブル形式）\n"
            "  * CAC、LTV、LTV/CAC\n"
            "  * Gross Margin、Operating Margin\n"
            "  * 顧客数、ARR、MRR\n"
            "  * Monthly Burn Rate、Runway\n\n"
            "【重要】\n"
            "- すべての数値テーブルは Markdown テーブル形式（|と-の記法）で出力すること\n"
            "- 各年で 売上 - コスト = 利益 が一致することを確認し、整合性を保つこと\n"
            "- 現実的で根拠のある仮定を使用すること\n"
            "- 通貨はJPY（日本円）または要件に応じてUSD（米ドル）を使用"
        )

    def get_user_prompt(self, context: dict) -> str:
        """Get user prompt for financial modeling.
        
        Args:
            context: Context dictionary with business details
            
        Returns:
            User prompt with company and business information
        """
        company_name = context.get("company_name", "企業")
        business_desc = context.get("business_description", "")
        plan_years = context.get("plan_years", 5)
        additional = context.get("additional_context", "")
        
        prompt = (
            f"企業名: {company_name}\n"
            f"事業説明: {business_desc}\n"
            f"計画期間: {plan_years}年\n"
        )
        
        if additional:
            prompt += f"追加情報: {additional}\n"
        
        prompt += (
            f"\n上記の企業について、{plan_years}年の詳細な財務予測モデルを作成してください。\n"
            "以下を含めてください：\n"
            f"1. {plan_years}年の年次売上・顧客数の推移（Markdownテーブル）\n"
            f"2. {plan_years}年の年次P/L予測（Markdownテーブル）\n"
            "3. LTV、CAC、チャーンレート等のユニットエコノミクス\n"
            "4. 資金調達計画（初期投資、調達タイミング）\n"
            "5. ベース/アップサイド/ダウンサイドの3シナリオ分析\n"
            "6. 主要KPIまとめ（Markdownテーブル）\n"
            "\n数値は現実的かつ根拠のあるものとしてください。"
        )
        
        return prompt
