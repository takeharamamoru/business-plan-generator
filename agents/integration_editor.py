"""IntegrationEditor agent for synthesizing business plan."""

from agents.base import BaseAgent


class IntegrationEditor(BaseAgent):
    """Integration Editor Agent.
    
    Phase 2 agent that synthesizes outputs from 4 agents (market researcher,
    product strategist, financial modeler, GTM strategist) into a coherent
    comprehensive business plan document.
    """

    def __init__(self) -> None:
        """Initialize IntegrationEditor agent."""
        super().__init__(
            name="IntegrationEditor",
            role="統合編集エキスパート",
        )

    def get_system_prompt(self, context: dict) -> str:
        """Get system prompt for integration and synthesis.
        
        Args:
            context: Context dictionary
            
        Returns:
            System prompt for synthesis
        """
        return (
            "あなたは事業計画書の統合編集の専門家です。\n"
            "複数のエージェントの出力を統合し、以下の構成で"
            "完全な事業計画書を作成してください:\n\n"
            "## 目次\n"
            "## 1. エグゼクティブサマリー\n"
            "新規作成。以下を含める:\n"
            "- ビジネスの概要（1段落）\n"
            "- 解決する課題と価値提案\n"
            "- 市場機会（TAM、SAM、SOM）\n"
            "- プロダクトの概要\n"
            "- 初年度から5年目の売上目標\n"
            "- 資金調達計画\n"
            "- リスクと主要成功要因\n\n"
            "## 2. 市場分析\n"
            "- Market Researcher の出力を編集・統合\n"
            "- 重複の削除、用語の統一\n\n"
            "## 3. プロダクト戦略\n"
            "- ProductStrategist の出力を編集・統合\n"
            "- 市場分析との整合性を確認\n\n"
            "## 4. 財務計画\n"
            "- FinancialModeler の出力を編集・統合\n"
            "- 売上、コスト、利益の整合性確認\n"
            "- データが正確に表示されていることを確認\n\n"
            "## 5. GTM・営業戦略\n"
            "- GTMStrategist の出力を編集・統合\n"
            "- 数値の整合性確認（CAC、LTV等）\n\n"
            "## 6. リスクと対策\n"
            "各セクションから技術的リスク、市場リスク、"
            "財務リスク、運営リスクを抽出・統合・優先順位付け\n\n"
            "## 7. 実行ロードマップ\n"
            "四半期ベースのマイルストーン\n"
            "プロダクト、営業、財務の観点から\n\n"
            "## 8. 付録\n"
            "- 前提条件一覧\n"
            "- 用語集\n"
            "- 参考資料リスト\n\n"
            "【重要な指示】\n"
            "- 重複する表現や内容は統合・削除すること\n"
            "- 用語を統一すること（例：顧客、ユーザー、エンドユーザーの区別を明確に）\n"
            "- すべての数値は整合性を保つこと\n"
            "- テーブルのMarkdown形式を保証すること\n"
            "- 論理的で読みやすい全体構成にすること"
        )

    def get_user_prompt(self, context: dict) -> str:
        """Get user prompt for synthesis.
        
        Args:
            context: Context dictionary including sections from Phase 1 agents
            
        Returns:
            User prompt with section contents
        """
        company_name = context.get("company_name", "企業")
        business_desc = context.get("business_description", "")
        plan_years = context.get("plan_years", 5)
        
        sections = context.get("sections", {})
        market_output = sections.get("market", "")
        product_output = sections.get("product", "")
        finance_output = sections.get("finance", "")
        gtm_output = sections.get("gtm", "")
        
        prompt = (
            f"企業名: {company_name}\n"
            f"事業説明: {business_desc}\n"
            f"計画期間: {plan_years}年\n\n"
            "以下の4つのエージェントの出力を統合して、"
            "完全な事業計画書を作成してください。\n\n"
            "---\n\n"
            "## 市場分析エージェントの出力\n"
            f"{market_output}\n\n"
            "---\n\n"
            "## プロダクト戦略エージェントの出力\n"
            f"{product_output}\n\n"
            "---\n\n"
            "## 財務モデルエージェントの出力\n"
            f"{finance_output}\n\n"
            "---\n\n"
            "## GTM戦略エージェントの出力\n"
            f"{gtm_output}\n\n"
            "---\n\n"
            "上記のセクションを統合し、完全な事業計画書を作成してください。\n"
            "エグゼクティブサマリーは新規作成し、"
            "各セクション間の整合性を確認してください。"
        )
        
        return prompt
