"""Agent Orchestrator for managing parallel agent execution."""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Optional

from agents.market_researcher import MarketResearcher
from agents.product_strategist import ProductStrategist
from agents.financial_modeler import FinancialModeler
from agents.gtm_strategist import GTMStrategist
from agents.integration_editor import IntegrationEditor


class AgentOrchestrator:
    """Orchestrator for managing Phase 1 and Phase 2 agent execution.
    
    Phase 1: Parallel execution of 4 specialized agents
            - MarketResearcher
            - ProductStrategist
            - FinancialModeler
            - GTMStrategist
    
    Phase 2: Sequential execution of IntegrationEditor
    """

    # Pricing for Claude Sonnet 4.5 (in USD per million tokens)
    INPUT_COST_PER_MTOKEN = 3.0
    OUTPUT_COST_PER_MTOKEN = 15.0

    def __init__(self, context: dict, model: str = "claude-sonnet-4-5-20250929") -> None:
        """Initialize AgentOrchestrator.
        
        Args:
            context: Context dictionary with company and business info
            model: Claude model to use
        """
        self.context = context
        self.model = model
        
        # Initialize agents
        self.market_researcher = MarketResearcher()
        self.product_strategist = ProductStrategist()
        self.financial_modeler = FinancialModeler()
        self.gtm_strategist = GTMStrategist()
        self.integration_editor = IntegrationEditor()
        
        # Progress tracking for each agent
        self.progress_state = {
            "market": 0.0,
            "product": 0.0,
            "finance": 0.0,
            "gtm": 0.0,
            "integration": 0.0,
        }
        
        # Total token usage
        self.total_token_usage = {"input": 0, "output": 0}
        
        # Start time for elapsed tracking
        self.start_time: Optional[float] = None

    def _progress_callback(
        self, agent_key: str
    ) -> Callable[[str, float, str], None]:
        """Create a progress callback for an agent.
        
        Args:
            agent_key: Key for the agent (market, product, finance, gtm)
            
        Returns:
            Callback function that updates progress_state
        """
        def callback(name: str, progress: float, chunk: str) -> None:
            """Progress callback function."""
            self.progress_state[agent_key] = progress
        
        return callback

    def run_phase1(self) -> dict[str, str]:
        """Run Phase 1: parallel execution of 4 agents.
        
        Implements graceful degradation: if an agent fails, generates placeholder
        content so other agents can still produce a complete business plan.
        
        Returns:
            Dictionary with keys: market, product, finance, gtm
            Each value is either the generated content or graceful fallback
        """
        # Map of agent keys to (agent, callback)
        agent_tasks = {
            "market": (self.market_researcher, self._progress_callback("market")),
            "product": (self.product_strategist, self._progress_callback("product")),
            "finance": (self.financial_modeler, self._progress_callback("finance")),
            "gtm": (self.gtm_strategist, self._progress_callback("gtm")),
        }
        
        # Placeholder content for graceful degradation
        placeholder_content = {
            "market": "# 市場分析\n\n⚠️ 市場分析の生成に失敗しました。\n詳細は以下のゴールドマンテンプレートを参考にしてください。",
            "product": "# プロダクト戦略\n\n⚠️ プロダクト戦略の生成に失敗しました。\nあなたのプロダクトの独自性と差別化ポイントを明確にしてください。",
            "finance": "# 財務計画\n\n⚠️ 財務計画の生成に失敗しました。\n3年～5年の収入、支出、利益予測を作成してください。",
            "gtm": "# Go-To-Market 戦略\n\n⚠️ GTM戦略の生成に失敗しました。\n顧客獲得チャネルと営業体制を定義してください。",
        }
        
        results = {}
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            # Submit all tasks
            futures = {}
            for key, (agent, callback) in agent_tasks.items():
                future = executor.submit(
                    agent.run_sync,
                    self.context,
                    callback,
                )
                futures[future] = key
            
            # Process completed tasks
            for future in as_completed(futures):
                key = futures[future]
                try:
                    output = future.result()
                    results[key] = output
                    
                    # Update token usage
                    agent = agent_tasks[key][0]
                    self.total_token_usage["input"] += agent.token_usage.get("input", 0)
                    self.total_token_usage["output"] += agent.token_usage.get("output", 0)
                    
                    # Mark as complete
                    self.progress_state[key] = 1.0
                    
                except Exception as e:
                    # Graceful degradation: use placeholder content
                    agent = agent_tasks[key][0]
                    error_msg = agent.error_message or str(e)
                    
                    # Combine error info with placeholder
                    results[key] = f"{placeholder_content.get(key, '')}\n\n**エラー詳細**: {error_msg}"
                    
                    # Mark as failed but complete
                    self.progress_state[key] = 1.0
        
        return results

    def run_phase2(self, sections: dict) -> str:
        """Run Phase 2: integration and synthesis.
        
        Args:
            sections: Dictionary with Phase 1 results
                     (keys: market, product, finance, gtm)
        
        Returns:
            Integrated business plan as Markdown string
        """
        # Update context with sections from Phase 1
        phase2_context = {**self.context, "sections": sections}
        
        # Run integration editor
        output = self.integration_editor.run_sync(
            context=phase2_context,
            on_progress=self._progress_callback("integration"),
        )
        
        # Update token usage
        self.total_token_usage["input"] += self.integration_editor.token_usage.get("input", 0)
        self.total_token_usage["output"] += self.integration_editor.token_usage.get("output", 0)
        
        # Mark as complete
        self.progress_state["integration"] = 1.0
        
        return output

    def run_all(self) -> dict:
        """Run all phases and return comprehensive results.
        
        Returns:
            Dictionary with:
            - sections: Phase 1 results (dict)
            - business_plan: Phase 2 output (str)
            - token_usage: Total tokens used (dict)
            - estimated_cost_usd: Estimated cost in USD (float)
            - elapsed_seconds: Total elapsed time (float)
        """
        self.start_time = time.time()
        
        # Phase 1: Parallel execution
        sections = self.run_phase1()
        
        # Phase 2: Integration
        business_plan = self.run_phase2(sections)
        
        # Calculate elapsed time
        elapsed_seconds = time.time() - self.start_time
        
        # Estimate cost
        estimated_cost = self.estimate_cost()
        
        return {
            "sections": sections,
            "business_plan": business_plan,
            "token_usage": self.total_token_usage,
            "estimated_cost_usd": estimated_cost,
            "elapsed_seconds": elapsed_seconds,
        }

    def get_progress(self) -> dict[str, dict]:
        """Get current progress for all agents.
        
        Returns:
            Dictionary with agent status, progress, and error messages
        """
        agent_map = {
            "market": self.market_researcher,
            "product": self.product_strategist,
            "finance": self.financial_modeler,
            "gtm": self.gtm_strategist,
            "integration": self.integration_editor,
        }
        
        progress = {}
        for key, agent in agent_map.items():
            progress[key] = {
                "status": agent.status,
                "progress": self.progress_state.get(key, 0.0),
                "error_message": agent.error_message,
            }
        
        return progress

    def estimate_cost(self) -> float:
        """Estimate total cost in USD based on token usage.
        
        Uses Claude Sonnet 4.5 pricing:
        - Input: $3 per 1M tokens
        - Output: $15 per 1M tokens
        
        Returns:
            Estimated cost in USD
        """
        input_tokens = self.total_token_usage.get("input", 0)
        output_tokens = self.total_token_usage.get("output", 0)
        
        input_cost = (input_tokens / 1_000_000) * self.INPUT_COST_PER_MTOKEN
        output_cost = (output_tokens / 1_000_000) * self.OUTPUT_COST_PER_MTOKEN
        
        return input_cost + output_cost
