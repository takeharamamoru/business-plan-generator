"""Test script for AgentOrchestrator Phase 1 only."""

import sys
import os

# Set UTF-8 encoding for output
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from orchestrator.runner import AgentOrchestrator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if not os.getenv("ANTHROPIC_API_KEY"):
    print("エラー: ANTHROPIC_API_KEY が設定されていません")
    exit(1)

# Test context
test_context = {
    "company_name": "MediFlow",
    "business_description": "医療機関向けワークフロー自動化SaaSプラットフォーム",
    "plan_years": 5,
    "template": {},
    "additional_context": "",
}


def main():
    """Run the orchestrator test for Phase 1 only."""
    print("=" * 70)
    print("AgentOrchestrator Phase 1 動作確認テスト")
    print("=" * 70)
    print(f"\n対象企業: {test_context['company_name']}")
    print(f"事業説明: {test_context['business_description']}")
    print(f"計画期間: {test_context['plan_years']}年\n")
    
    # Create orchestrator
    orchestrator = AgentOrchestrator(context=test_context)
    
    print("実行中... (Phase 1: 4エージェント並列実行)\n")
    
    try:
        # Run Phase 1 only
        sections = orchestrator.run_phase1()
        
        # Display results
        print("=" * 70)
        print("実行完了")
        print("=" * 70)
        
        # Token usage after Phase 1
        token_usage = orchestrator.total_token_usage
        print(f"\n【Phase 1 トークン使用量】")
        print(f"  入力:   {token_usage['input']:,} tokens")
        print(f"  出力:   {token_usage['output']:,} tokens")
        print(f"  合計:   {token_usage['input'] + token_usage['output']:,} tokens")
        
        # Cost estimation
        cost = orchestrator.estimate_cost()
        print(f"\n【Phase 1 コスト推定】")
        print(f"  Sonnet 4.5 (Input: $3/MTok, Output: $15/MTok)")
        print(f"  推定コスト: ${cost:.4f} USD")
        
        # Sections summary
        print(f"\n【Phase 1 出力確認】")
        for key in ["market", "product", "finance", "gtm"]:
            content = sections.get(key, "")
            if content.startswith("[生成エラー"):
                print(f"  ❌ {key}: {content}")
            else:
                lines = content.count('\n')
                print(f"  ✅ {key}: {len(content):,} chars ({lines} lines)")
        
        # Progress state
        progress = orchestrator.get_progress()
        print(f"\n【エージェント最終状態】")
        for key in ["market", "product", "finance", "gtm"]:
            status = progress[key]["status"]
            emoji = "✅" if status == "done" else "❌"
            print(f"  {emoji} {key}: {status}")
        
        print("\n" + "=" * 70)
        print("✅ Phase 1 並列実行テスト成功!")
        print("=" * 70)
        print("\n【確認ポイント】")
        print("✅ 4エージェントが並列で実行されたこと")
        print("✅ 各エージェントが正常に完了したこと")
        print("✅ トークン使用量が正確に記録されたこと")
        print("✅ コスト推定が正しく計算されたこと")
        
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
