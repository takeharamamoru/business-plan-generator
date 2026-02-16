"""TestAgent class for testing BaseAgent implementation."""

from agents.base import BaseAgent


class TestAgent(BaseAgent):
    """Test agent for verifying BaseAgent functionality.
    
    This simple agent is used to test the core streaming and progress
    tracking capabilities of the BaseAgent class.
    """

    def __init__(self) -> None:
        """Initialize TestAgent."""
        super().__init__(
            name="TestAgent",
            role="テスト用エージェント",
            model="claude-sonnet-4-5-20250929",
        )

    def get_system_prompt(self, context: dict) -> str:
        """Get system prompt for test agent.
        
        Args:
            context: Context dictionary (unused in test)
            
        Returns:
            System prompt string
        """
        return (
            "あなたは日本のビジネス市場に詳しい分析家です。"
            "簡潔かつ正確な回答をしてください。"
        )

    def get_user_prompt(self, context: dict) -> str:
        """Get user prompt for test agent.
        
        Args:
            context: Context dictionary (unused in test)
            
        Returns:
            User prompt string
        """
        return "日本のSaaS市場について3行で説明してください"


if __name__ == "__main__":
    # Test the agent
    import os
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Check if API key is set
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("エラー: ANTHROPIC_API_KEY が設定されていません")
        print(".env ファイルを作成して ANTHROPIC_API_KEY を設定してください")
        exit(1)
    
    # Create agent instance
    agent = TestAgent()
    
    # Progress callback
    def on_progress_callback(name: str, progress: float, chunk: str) -> None:
        """Print progress updates."""
        print(f"[{name}] {progress:.1%} - 受信: {chunk}", end="", flush=True)
    
    print("=" * 60)
    print("TestAgent 実行テスト")
    print("=" * 60)
    
    try:
        # Run the agent
        result = agent.run_sync(
            context={"max_tokens": 500},
            on_progress=on_progress_callback,
        )
        
        print("\n" + "=" * 60)
        print("実行完了")
        print("=" * 60)
        print(f"\nエージェント名: {agent.name}")
        print(f"状態: {agent.status}")
        print(f"進捗: {agent.progress:.1%}")
        print(f"トークン使用量: {agent.token_usage}")
        print("\n【出力内容】")
        print(result)
        
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
        print(f"エージェント状態: {agent.status}")
        print(f"エラーメッセージ: {agent.error_message}")
