"""Progress display component for business plan generator."""

import streamlit as st
from orchestrator.runner import AgentOrchestrator


AGENT_ICONS = {
    "market": "🔍",
    "product": "💡",
    "finance": "📊",
    "gtm": "🤝",
    "integration": "📝",
}

AGENT_NAMES_JA = {
    "market": "市場調査",
    "product": "プロダクト",
    "finance": "財務モデル",
    "gtm": "GTM戦略",
    "integration": "統合編集",
}


def render_progress(orchestrator: AgentOrchestrator) -> None:
    """Render progress display for agents.
    
    Args:
        orchestrator: AgentOrchestrator instance
    """
    st.markdown("## 📊 生成進捗")
    
    # Get progress data
    progress_data = orchestrator.get_progress()
    
    # Create 5 columns for the 5 agents (4 phase 1 + 1 phase 2)
    cols = st.columns(5)
    
    agent_keys = ["market", "product", "finance", "gtm"]
    
    for idx, agent_key in enumerate(agent_keys):
        with cols[idx]:
            agent_info = progress_data.get(agent_key, {})
            status = agent_info.get("status", "waiting")
            progress = agent_info.get("progress", 0.0)
            error_msg = agent_info.get("error_message")
            
            # Agent name with icon
            icon = AGENT_ICONS.get(agent_key, "⚙️")
            name_ja = AGENT_NAMES_JA.get(agent_key, "エージェント")
            st.markdown(f"**{icon} {name_ja}**")
            
            # Progress bar
            st.progress(progress, text=f"{progress:.0%}")
            
            # Status text
            if status == "done":
                st.success("✅ 完了")
            elif status == "error":
                st.error("❌ エラー")
                if error_msg:
                    st.caption(error_msg[:50])  # Show first 50 chars
            elif status == "running" or status == "streaming":
                st.info("⏳ 生成中...")
            else:
                st.info("⏱️ 待機中")
    
    # Integration editor in last column
    with cols[4]:
        integration_info = progress_data.get("integration", {})
        status = integration_info.get("status", "waiting")
        progress = integration_info.get("progress", 0.0)
        
        icon = AGENT_ICONS.get("integration", "⚙️")
        name_ja = AGENT_NAMES_JA.get("integration", "統合編集")
        st.markdown(f"**{icon} {name_ja}**")
        st.markdown("*(Phase 2)*")
        
        st.progress(progress, text=f"{progress:.0%}")
        
        if status == "done":
            st.success("✅ 完了")
        elif status == "error":
            st.error("❌ エラー")
        elif status == "running" or status == "streaming":
            st.info("⏳ 統合中...")
        else:
            st.info("⏱️ 待機中")
    
    st.markdown("---")
