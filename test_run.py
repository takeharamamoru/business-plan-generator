"""Test script for BaseAgent and TestAgent."""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.test_agent import TestAgent
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
    print(f"[{name}] {progress:.0%} ", end="", flush=True)


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
    print(f"進捗: {agent.progress:.0%}")
    print(f"トークン使用量: {agent.token_usage}")
    print("\n【出力内容】")
    print(result)

except Exception as e:
    print(f"\nエラーが発生しました: {e}")
    print(f"エージェント状態: {agent.status}")
    print(f"エラーメッセージ: {agent.error_message}")
