"""ProductStrategist agent for product strategy."""

from agents.base import BaseAgent


class ProductStrategist(BaseAgent):
    """Product Strategy Agent.
    
    Defines product vision, differentiation, core features, technology stack,
    roadmap, and technical risk mitigation strategies.
    """

    def __init__(self) -> None:
        """Initialize ProductStrategist agent."""
        super().__init__(
            name="ProductStrategist",
            role="プロダクト戦略専門家",
        )

    def get_system_prompt(self, context: dict) -> str:
        """Get system prompt for product strategy.
        
        Args:
            context: Context dictionary containing company and business info
            
        Returns:
            System prompt for product strategy planning
        """
        return (
            "あなたはプロダクト戦略の専門家です。"
            "以下の構造でプロダクト戦略を提供してください:\n\n"
            "## プロダクトビジョンと差別化\n"
            "- ビジョンステートメント\n"
            "- ターゲット顧客セグメント\n"
            "- 主な差別化ポイント（3-5点）\n"
            "- 競合との比較表\n\n"
            "## コア機能と技術スタック\n"
            "- 必須機能（MVP）\n"
            "- 拡張機能（ロードマップ）\n"
            "- 推奨される技術スタック\n"
            "- インフラ・セキュリティ戦略\n\n"
            "## プロダクトロードマップ\n"
            "- Phase 1（初期版、〜6ヶ月）\n"
            "- Phase 2（成長期、6-18ヶ月）\n"
            "- Phase 3（拡大期、18-36ヶ月）\n"
            "各Phaseの主要マイルストーン\n\n"
            "## 技術的リスクと対策\n"
            "- 主要なリスク（スケーラビリティ、セキュリティなど）\n"
            "- 対策とベストプラクティス\n\n"
            "Markdownフォーマットを使用し、見出し・表・箇条書きを活用してください。"
        )

    def get_user_prompt(self, context: dict) -> str:
        """Get user prompt for product strategy.
        
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
            f"\n上記の企業について、{plan_years}年の事業計画に基づいたプロダクト戦略を提供してください。\n"
            "ビジョン、差別化ポイント、コア機能、技術スタック、年次ロードマップ、"
            "技術的リスクと対策を詳細に説明してください。"
        )
        
        return prompt
