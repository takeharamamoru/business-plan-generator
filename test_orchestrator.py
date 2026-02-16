"""Test script for AgentOrchestrator."""

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
    """Run the orchestrator test."""
    print("=" * 70)
    print("AgentOrchestrator 動作確認テスト")
    print("=" * 70)
    print(f"\n対象企業: {test_context['company_name']}")
    print(f"事業説明: {test_context['business_description']}")
    print(f"計画期間: {test_context['plan_years']}年\n")
    
    # Create orchestrator
    orchestrator = AgentOrchestrator(context=test_context)
    
    print("実行中... (Phase 1: 4エージェント並列実行 → Phase 2: 統合)\n")
    
    try:
        # Run all phases
        result = orchestrator.run_all()
        
        # Display results
        print("=" * 70)
        print("実行完了")
        print("=" * 70)
        
        # Token usage
        token_usage = result["token_usage"]
        print(f"\n【トークン使用量】")
        print(f"  入力:   {token_usage['input']:,} tokens")
        print(f"  出力:   {token_usage['output']:,} tokens")
        print(f"  合計:   {token_usage['input'] + token_usage['output']:,} tokens")
        
        # Cost estimation
        print(f"\n【コスト推定】")
        print(f"  Sonnet 4.5 (Input: $3/MTok, Output: $15/MTok)")
        print(f"  推定コスト: ${result['estimated_cost_usd']:.4f} USD")
        
        # Execution time
        print(f"\n【実行時間】")
        print(f"  実行時間: {result['elapsed_seconds']:.2f}秒")
        
        # Sections summary
        sections = result["sections"]
        print(f"\n【Phase 1 出力サマリー】")
        for key, content in sections.items():
            if content.startswith("[生成エラー"):
                print(f"  ❌ {key}: {content}")
            else:
                print(f"  ✅ {key}: {len(content):,} chars")
        
        # Business plan summary
        business_plan = result["business_plan"]
        if business_plan.startswith("[生成エラー"):
            print(f"\n【Phase 2 出力】")
            print(f"  ❌ {business_plan}")
        else:
            print(f"\n【Phase 2 出力 (統合事業計画書)】")
            print(f"  ✅ 生成成功: {len(business_plan):,} chars")
            
            # Show first 500 chars of business plan
            print(f"\n【事業計画書の冒頭】")
            print("-" * 70)
            print(business_plan[:500])
            print("-" * 70)
        
        print("\n" + "=" * 70)
        print("✅ AgentOrchestrator テスト成功!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
