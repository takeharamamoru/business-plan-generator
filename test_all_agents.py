"""Test script for all agents."""

import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Set UTF-8 encoding for output
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.market_researcher import MarketResearcher
from agents.product_strategist import ProductStrategist
from agents.financial_modeler import FinancialModeler
from agents.gtm_strategist import GTMStrategist
from agents.integration_editor import IntegrationEditor
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

# Progress tracking
def on_progress(name: str, progress: float, chunk: str) -> None:
    """Simple progress callback."""
    pass  # Silent progress


def test_single_agent(agent_class, agent_name: str) -> tuple:
    """Test a single agent.
    
    Args:
        agent_class: The agent class to test
        agent_name: The name of the agent for display
        
    Returns:
        Tuple of (agent_name, status, output_length, token_usage, error)
    """
    try:
        agent = agent_class()
        output = agent.run_sync(
            context=test_context,
            on_progress=on_progress,
        )
        
        return (
            agent_name,
            agent.status,
            len(output),
            agent.token_usage,
            None,
        )
    except Exception as e:
        return (agent_name, "error", 0, {}, str(e))


def test_all_agents_parallel():
    """Test all 4 Phase 1 agents in parallel."""
    agents_to_test = [
        (MarketResearcher, "MarketResearcher"),
        (ProductStrategist, "ProductStrategist"),
        (FinancialModeler, "FinancialModeler"),
        (GTMStrategist, "GTMStrategist"),
    ]
    
    print("=" * 70)
    print("Phase 1: 4エージェント並列テスト")
    print("=" * 70)
    print(f"\n対象企業: {test_context['company_name']}")
    print(f"事業説明: {test_context['business_description']}")
    print(f"計画期間: {test_context['plan_years']}年\n")
    
    results = {}
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(test_single_agent, agent_class, agent_name): (
                agent_class,
                agent_name,
            )
            for agent_class, agent_name in agents_to_test
        }
        
        for future in as_completed(futures):
            agent_class, agent_name = futures[future]
            name, status, output_len, token_usage, error = future.result()
            results[name] = {
                "status": status,
                "output_len": output_len,
                "token_usage": token_usage,
                "error": error,
            }
            
            if error:
                print(f"❌ {name}: {error}")
            else:
                input_tokens = token_usage.get("input", 0)
                output_tokens = token_usage.get("output", 0)
                total_tokens = input_tokens + output_tokens
                print(
                    f"✅ {name}: {status} "
                    f"({output_len} chars, {total_tokens} tokens)"
                )
    
    return results


def test_integration_phase2(phase1_results: dict):
    """Test Phase 2 integration with Phase 1 results.
    
    Args:
        phase1_results: Results dictionary from Phase 1 agents
    """
    print("\n" + "=" * 70)
    print("Phase 2: 統合編集テスト")
    print("=" * 70)
    
    # Create dummy sections from Phase 1 results
    # In production, these would be actual agent outputs
    sections = {
        "market": "# 市場分析\n[マーケット分析の詳細内容]\n",
        "product": "# プロダクト戦略\n[プロダクト戦略の詳細内容]\n",
        "finance": "# 財務計画\n[財務計画の詳細内容]\n",
        "gtm": "# GTM・営業戦略\n[GTM戦略の詳細内容]\n",
    }
    
    integration_context = {**test_context, "sections": sections}
    
    try:
        editor = IntegrationEditor()
        output = editor.run_sync(
            context=integration_context,
            on_progress=on_progress,
        )
        
        input_tokens = editor.token_usage.get("input", 0)
        output_tokens = editor.token_usage.get("output", 0)
        total_tokens = input_tokens + output_tokens
        
        print(
            f"✅ IntegrationEditor: {editor.status} "
            f"({len(output)} chars, {total_tokens} tokens)"
        )
        
    except Exception as e:
        print(f"❌ IntegrationEditor: {e}")


def main():
    """Run all tests."""
    try:
        # Phase 1: Test 4 agents in parallel
        results = test_all_agents_parallel()
        
        # Phase 2: Test integration (using dummy data for now)
        test_integration_phase2(results)
        
        print("\n" + "=" * 70)
        print("テスト完了")
        print("=" * 70)
        
    except KeyboardInterrupt:
        print("\n\nテストが中断されました")


if __name__ == "__main__":
    main()
