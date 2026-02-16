"""Sidebar UI component for business plan generator."""

import streamlit as st
from templates.catalog import list_templates, get_template


def render_sidebar() -> dict | None:
    """Render sidebar and collect user input.
    
    Returns:
        Context dictionary if valid input provided, None otherwise
    """
    with st.sidebar:
        st.title("🤖 Agent Teams 事業計画ジェネレーター")
        st.markdown("---")
        
        # Template selection
        st.markdown("### 📋 テンプレート選択")
        templates = list_templates()
        template_options = {t["name"]: t["key"] for t in templates}
        selected_template_name = st.selectbox(
            "テンプレートを選択",
            options=list(template_options.keys()),
            index=0,
        )
        selected_template_key = template_options[selected_template_name]
        template = get_template(selected_template_key)
        
        st.markdown("---")
        
        # Basic information (Required)
        st.markdown("### 📌 基本情報（必須）")
        
        company_name = st.text_input(
            "企業名",
            placeholder="例: MediFlow, TechVenture",
            key="company_name",
        )
        
        business_description = st.text_area(
            "事業内容",
            placeholder="事業の詳細説明を記入してください。商品・サービス、ターゲット顧客、主要な特徴などを含めてください。",
            height=100,
            key="business_description",
        )
        
        # Template-specific fields
        if template and template.get("context_fields"):
            st.markdown("---")
            st.markdown("### ⚙️ テンプレート設定")
            
            for field in template["context_fields"]:
                field_key = f"{selected_template_key}_{field['key']}"
                
                if field["type"] == "text":
                    st.text_input(
                        field["label"],
                        placeholder=field.get("placeholder", ""),
                        key=field_key,
                    )
                elif field["type"] == "textarea":
                    st.text_area(
                        field["label"],
                        placeholder=field.get("placeholder", ""),
                        height=80,
                        key=field_key,
                    )
                elif field["type"] == "select" and field.get("options"):
                    st.selectbox(
                        field["label"],
                        options=field["options"],
                        key=field_key,
                    )
        
        st.markdown("---")
        
        # Plan duration
        st.markdown("### 📅 計画期間")
        plan_years = st.slider(
            "計画期間（年）",
            min_value=3,
            max_value=7,
            value=5,
            step=1,
            key="plan_years",
        )
        
        st.markdown("---")
        
        # Advanced settings
        with st.expander("⚙️ 詳細設定", expanded=False):
            st.markdown("#### モデル選択")
            model = st.radio(
                "Claude モデル",
                options=[
                    "Sonnet 4.5（推奨）",
                    "Opus 4.5（高品質）",
                ],
                index=0,
                key="model",
            )
            
            # Map model display to actual model names
            model_map = {
                "Sonnet 4.5（推奨）": "claude-sonnet-4-5-20250929",
                "Opus 4.5（高品質）": "claude-opus-4-1-20250805",
            }
            actual_model = model_map.get(model, "claude-sonnet-4-5-20250929")
            
            st.markdown("#### トークン設定")
            st.info("各エージェントの max_tokens（デフォルト値を推奨）")
            
            market_tokens = st.number_input(
                "Market Researcher max_tokens",
                value=4000,
                min_value=1000,
                step=500,
                key="market_tokens",
            )
            product_tokens = st.number_input(
                "Product Strategist max_tokens",
                value=5000,
                min_value=1000,
                step=500,
                key="product_tokens",
            )
            finance_tokens = st.number_input(
                "Financial Modeler max_tokens",
                value=5000,
                min_value=1000,
                step=500,
                key="finance_tokens",
            )
            gtm_tokens = st.number_input(
                "GTM Strategist max_tokens",
                value=4000,
                min_value=1000,
                step=500,
                key="gtm_tokens",
            )
            integration_tokens = st.number_input(
                "Integration Editor max_tokens",
                value=8000,
                min_value=2000,
                step=500,
                key="integration_tokens",
            )
        
        st.markdown("---")
        
        # Additional information (Optional)
        st.markdown("### 💭 追加情報（任意）")
        additional_context = st.text_area(
            "特に重視してほしい点があれば記入",
            placeholder="例: 特定の規制への対応、特定の地域への進出、特定の投資家層への対応など",
            height=80,
            key="additional_context",
        )
        
        st.markdown("---")
        
        # Generate button
        if st.button("🚀 事業計画を生成", type="primary", use_container_width=True):
            # Validation
            if not company_name or not company_name.strip():
                st.warning("⚠️ 企業名を入力してください")
                return None
            
            if not business_description or not business_description.strip():
                st.warning("⚠️ 事業内容を入力してください")
                return None
            
            # Collect template-specific fields
            template_fields = {}
            if template and template.get("context_fields"):
                for field in template["context_fields"]:
                    field_key = f"{selected_template_key}_{field['key']}"
                    template_fields[field["key"]] = st.session_state.get(field_key, "")
            
            # Build context dictionary
            context = {
                "company_name": company_name.strip(),
                "business_description": business_description.strip(),
                "plan_years": plan_years,
                "template": {
                    "key": selected_template_key,
                    "name": selected_template_name,
                    "fields": template_fields,
                    "hints": template.get("agent_hints", {}) if template else {},
                },
                "additional_context": additional_context.strip(),
                "model": actual_model,
                "max_tokens": {
                    "market": market_tokens,
                    "product": product_tokens,
                    "finance": finance_tokens,
                    "gtm": gtm_tokens,
                    "integration": integration_tokens,
                },
            }
            
            return context
    
    return None
