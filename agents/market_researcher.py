"""MarketResearcher agent for market analysis."""

from agents.base import BaseAgent


class MarketResearcher(BaseAgent):
    """Market Research Agent.
    
    Analyzes market size, growth, competition, regulatory environment,
    and market trends to provide comprehensive market analysis.
    """

    def __init__(self) -> None:
        """Initialize MarketResearcher agent."""
        super().__init__(
            name="MarketResearcher",
            role="市場調査エキスパート",
        )

    def get_system_prompt(self, context: dict) -> str:
        """Get system prompt for market research.
        
        Args:
            context: Context dictionary containing company and business info
            
        Returns:
            System prompt for market analysis
        """
        return (
            "あなたは市場分析の専門家です。"
            "以下の構造で日本市場またはグローバル市場の分析を提供してください:\n\n"
            "## TAM / SAM / SOM 分析\n"
            "- TAM（Total Addressable Market）の推定\n"
            "- SAM（Serviceable Addressable Market）の推定\n"
            "- SOM（Serviceable Obtainable Market）の推定\n"
            "- 各々の根拠と計算方法\n\n"
            "## 市場成長率\n"
            "- CAGRの推定（過去3年、今後3-5年）\n"
            "- 成長ドライバー\n\n"
            "## 競合分析\n"
            "- 主要3〜5社の分析（強み・弱み・市場シェア）\n"
            "- 競合の差別化ポイント\n"
            "- 当社の参入機会\n\n"
            "## 規制環境と法的要件\n"
            "- 業界特有の規制\n"
            "- コンプライアンス要件\n\n"
            "## 市場トレンド\n"
            "- 最新のトレンド（3-5点）\n"
            "- 顧客ニーズの変化\n\n"
            "Markdownフォーマットを使用し、見出し・表・箇条書きを活用してください。"
        )

    def get_user_prompt(self, context: dict) -> str:
        """Get user prompt for market research.
        
        Args:
            context: Context dictionary with business details
            
        Returns:
            User prompt with company and business information
        """
        company_name = context.get("company_name", "企業")
        business_desc = context.get("business_description", "")
        additional = context.get("additional_context", "")
        
        prompt = (
            f"企業名: {company_name}\n"
            f"事業説明: {business_desc}\n"
        )
        
        if additional:
            prompt += f"追加情報: {additional}\n"
        
        prompt += (
            "\n上記の企業について、TAM/SAM/SOM分析、市場成長率、競合分析、"
            "規制環境、市場トレンドを含めた詳細な市場分析を提供してください。"
        )
        
        return prompt
