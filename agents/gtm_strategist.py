"""GTMStrategist agent for go-to-market strategy."""

from agents.base import BaseAgent


class GTMStrategist(BaseAgent):
    """Go-To-Market Strategy Agent.
    
    Develops comprehensive GTM strategy including sales organization,
    sales channels, marketing strategy, and partnership approach.
    """

    def __init__(self) -> None:
        """Initialize GTMStrategist agent."""
        super().__init__(
            name="GTMStrategist",
            role="GTM・営業戦略専門家",
        )

    def get_system_prompt(self, context: dict) -> str:
        """Get system prompt for GTM strategy.
        
        Args:
            context: Context dictionary containing company and business info
            
        Returns:
            System prompt for GTM strategy
        """
        return (
            "あなたはGo-to-Market戦略の専門家です。"
            "以下の構造でGTM戦略を提供してください:\n\n"
            "## Go-to-Market 戦略\n"
            "- GTM全体ビジョン\n"
            "- Phase分け（Early Stage、Growth、Scale ）\n"
            "- 各Phaseでの目標と主要活動\n"
            "- Timeline\n\n"
            "## 営業組織体制と採用計画\n"
            "- 初期チーム構成\n"
            "- 年次採用計画（営業、CS、その他）\n"
            "- 組織図の推移\n"
            "- セールスコンプ・インセンティブ構造\n\n"
            "## チャネル戦略\n"
            "- 直販（Inside Sales / Field Sales）\n"
            "- パートナーセールス\n"
            "- PLG（Product-Led Growth）要素\n"
            "- リセラー / SI / コンサルティング会社\n"
            "- 各チャネルの数値的な売上予測\n\n"
            "## マーケティング戦略\n"
            "- マーケティング目標と予算配分\n"
            "- Demand Generation施策\n"
            "  * デジタルマーケティング（SEO、SEM、コンテンツマーケティング）\n"
            "  * イベント、展示会、ウェビナー\n"
            "  * PR、パブリシティ\n"
            "- 顧客獲得のマイルストーン\n"
            "- Key Marketing KPI（CAC、Conversion Rate、Pipeline生成）\n\n"
            "## パートナーシップ戦略\n"
            "- 戦略的パートナー候補\n"
            "- パートナーメリット\n"
            "- Go-to-Market支援の形態\n\n"
            "Markdownフォーマットを使用し、見出し・表・箇条書きを活用してください。"
        )

    def get_user_prompt(self, context: dict) -> str:
        """Get user prompt for GTM strategy.
        
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
            f"\n上記の企業について、{plan_years}年のGTM・営業戦略を提供してください。\n"
            "以下を含めてください：\n"
            "1. Go-to-Market戦略全体（Phase分け）\n"
            "2. 営業組織体制と採用計画\n"
            "3. チャネル戦略（直販、パートナー、PLGなど）と各チャネルの売上寄与度\n"
            "4. マーケティング戦略とKPI\n"
            "5. 主要パートナーシップ戦略\n"
            "\n顧客セグメント、営業サイクル、顧客獲得コストなどの実態を反映した戦略を提案してください。"
        )
        
        return prompt
