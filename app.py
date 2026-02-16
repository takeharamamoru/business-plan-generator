"""Main Streamlit application for business plan generator."""

import streamlit as st
import threading
import time
from pathlib import Path

from ui.sidebar import render_sidebar
from ui.progress import render_progress
from orchestrator.runner import AgentOrchestrator
from exporters.excel_exporter import ExcelExporter
from exporters.pdf_exporter import PDFExporter


# Page configuration
st.set_page_config(
    page_title="Agent Teams 事業計画ジェネレーター",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


def generate_business_plan(context: dict) -> None:
    """Generate business plan in a separate thread.
    
    Args:
        context: User input context dictionary
    """
    try:
        orchestrator = AgentOrchestrator(context=context, model=context.get("model"))
        
        # Run all phases
        result = orchestrator.run_all()
        
        # Save to session state
        st.session_state.generation_result = result
        st.session_state.orchestrator = orchestrator
        st.session_state.is_generating = False
        st.session_state.generation_error = None
        
    except ValueError as e:
        # Handle API key missing error
        st.session_state.generation_error = {
            "type": "api_key_error",
            "message": str(e)
        }
        st.session_state.is_generating = False
        
    except ConnectionError as e:
        st.session_state.generation_error = {
            "type": "network_error",
            "message": f"ネットワークエラー: {str(e)}"
        }
        st.session_state.is_generating = False
        
    except Exception as e:
        # Handle unexpected errors
        st.session_state.generation_error = {
            "type": "unknown_error",
            "message": f"{type(e).__name__}: {str(e)}"
        }
        st.session_state.is_generating = False


def main():
    """Main application entry point."""
    
    # Initialize session state
    if "generation_result" not in st.session_state:
        st.session_state.generation_result = None
    if "orchestrator" not in st.session_state:
        st.session_state.orchestrator = None
    if "is_generating" not in st.session_state:
        st.session_state.is_generating = False
    if "generation_error" not in st.session_state:
        st.session_state.generation_error = None
    if "generation_start_time" not in st.session_state:
        st.session_state.generation_start_time = None
    
    # Main title
    st.markdown("# 🤖 Agent Teams 事業計画ジェネレーター")
    st.markdown("*Anthropic Claude API + マルチエージェントシステムで事業計画書を自動生成*")
    st.markdown("---")
    
    # Get user input from sidebar
    context = render_sidebar()
    
    # Handle generation request
    if context and not st.session_state.is_generating and not st.session_state.generation_result:
        st.session_state.is_generating = True
        st.session_state.generation_start_time = time.time()
        
        # Start generation in a thread
        thread = threading.Thread(
            target=generate_business_plan,
            args=(context,),
            daemon=True,
        )
        thread.start()
    
    # Display progress while generating
    if st.session_state.is_generating and st.session_state.orchestrator is None:
        st.info("🚀 事業計画を生成中... 少々お待ちください（初回は最大3分かかる場合があります）")
        
        # Polling loop for progress updates
        progress_placeholder = st.empty()
        while st.session_state.is_generating:
            time.sleep(0.5)
            
            # Check if orchestrator is available
            if st.session_state.orchestrator:
                with progress_placeholder.container():
                    render_progress(st.session_state.orchestrator)
                break
    
    # Display generation result
    if st.session_state.generation_result:
        result = st.session_state.generation_result
        sections = result.get("sections", {})
        business_plan = result.get("business_plan", "")
        token_usage = result.get("token_usage", {})
        estimated_cost = result.get("estimated_cost_usd", 0.0)
        elapsed_time = result.get("elapsed_seconds", 0.0)
        
        st.success("✅ 事業計画書が完成しました！")
        st.markdown("---")
        
        # Display tabs
        tab1, tab2, tab3 = st.tabs(["📄 事業計画書", "📊 Excel", "📕 PDF"])
        
        with tab1:
            st.subheader("事業計画書")
            
            # Display markdown content
            st.markdown(business_plan)
            
            # Download button
            st.download_button(
                label="📥 Markdown（.md）をダウンロード",
                data=business_plan.encode('utf-8'),
                file_name="business_plan.md",
                mime="text/markdown",
                use_container_width=True,
            )
        
        with tab2:
            st.subheader("Excel ワークブック")
            st.info(
                "📊 **複数シートで構成されています:**\n"
                "- **サマリー**: 主要な情報まとめ\n"
                "- **市場分析**: 市場規模や競合分析\n"
                "- **プロダクト**: 製品戦略とロードマップ\n"
                "- **財務計画**: 売上予測と損益計算書\n"
                "- **GTM戦略**: Go-to-Market戦略"
            )
            
            # Generate Excel
            try:
                exporter = ExcelExporter()
                excel_bytes = exporter.export(business_plan, sections)
                
                st.download_button(
                    label="📥 Excel（.xlsx）をダウンロード",
                    data=excel_bytes,
                    file_name="business_plan.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                )
            except Exception as e:
                st.error(f"❌ Excel生成エラー: {e}")
        
        with tab3:
            st.subheader("PDF ドキュメント")
            st.info(
                "📕 **PDF形式でのダウンロード**\n"
                "（weasyprint が利用可能な環境では PDF、そうでない場合は HTML で提供）"
            )
            
            # Generate PDF/HTML
            try:
                exporter = PDFExporter()
                export_format = exporter.get_export_format()
                pdf_bytes = exporter.export(business_plan)
                
                file_ext = "pdf" if export_format == "PDF" else "html"
                mime_type = "application/pdf" if export_format == "PDF" else "text/html"
                
                st.download_button(
                    label=f"📥 {export_format}（.{file_ext}）をダウンロード",
                    data=pdf_bytes,
                    file_name=f"business_plan.{file_ext}",
                    mime=mime_type,
                    use_container_width=True,
                )
            except Exception as e:
                st.error(f"❌ PDF生成エラー: {e}")
        
        st.markdown("---")
        
        # Display metrics
        st.subheader("📈 実行結果")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="入力トークン",
                value=f"{token_usage.get('input', 0):,}",
            )
        
        with col2:
            st.metric(
                label="出力トークン",
                value=f"{token_usage.get('output', 0):,}",
            )
        
        with col3:
            st.metric(
                label="推定コスト",
                value=f"${estimated_cost:.4f}",
            )
        
        with col4:
            st.metric(
                label="生成時間",
                value=f"{elapsed_time:.1f}秒",
            )
        
        st.markdown("---")
        
        # Individual sections expander
        st.subheader("📋 個別セクション")
        
        section_names = {
            "market": "市場分析",
            "product": "プロダクト戦略",
            "finance": "財務計画",
            "gtm": "GTM戦略",
        }
        
        for section_key, section_name in section_names.items():
            with st.expander(f"🔍 {section_name}（Phase 1）"):
                section_content = sections.get(section_key, "")
                if section_content.startswith("[生成エラー"):
                    st.error(section_content)
                else:
                    st.markdown(section_content)
        
        # Reset button
        if st.button("🔄 別の事業計画を作成", use_container_width=True):
            st.session_state.generation_result = None
            st.session_state.orchestrator = None
            st.session_state.is_generating = False
            st.rerun()
    
    elif st.session_state.generation_error:
        error_info = st.session_state.generation_error
        
        if isinstance(error_info, dict):
            error_type = error_info.get("type", "unknown_error")
            error_msg = error_info.get("message", "不明なエラー")
            
            # Display error based on type
            if error_type == "api_key_error":
                st.error("❌ APIキーが設定されていません")
                st.markdown("""
                以下のいずれかの方法で ANTHROPIC_API_KEY を設定してください：
                
                **方法1: .env ファイル（推奨）**
                1. `.env.example` を `.env` にコピー
                2. `ANTHROPIC_API_KEY=sk-ant-v1-...` を追記
                3. ファイルを保存して Streamlit を再起動
                
                **方法2: Streamlit Secret（Streamlit Cloud）**
                1. Streamlit Cloud のプロジェクト設定へ移動
                2. Secrets 管理から `ANTHROPIC_API_KEY` を追加
                3. アプリを再デプロイ
                
                **方法3: 環境変数**
                ```bash
                export ANTHROPIC_API_KEY="sk-ant-v1-..."
                streamlit run app.py
                ```
                
                🔗 API キーは [https://console.anthropic.com](https://console.anthropic.com) から取得できます。
                """)
                
            elif error_type == "network_error":
                st.error("🌐 ネットワークエラーが発生しました")
                st.warning("""
                以下を確認してください：
                - インターネット接続状態
                - ファイアウォール設定
                - Anthropic API へのアクセス
                """)
                
            else:
                st.error(f"❌ エラーが発生しました")
                st.code(error_msg, language="plaintext")
        else:
            st.error(f"❌ 生成中にエラーが発生しました: {error_info}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 リトライ", use_container_width=True):
                st.session_state.generation_error = None
                st.rerun()
        with col2:
            if st.button("🏠 初期状態に戻す", use_container_width=True):
                st.session_state.generation_result = None
                st.session_state.orchestrator = None
                st.session_state.is_generating = False
                st.session_state.generation_error = None
                st.rerun()
    
    else:
        # Welcome message
        st.info(
            """
            👋 ようこそ！ **Agent Teams 事業計画ジェネレーター** へ
            
            このツールは Anthropic の Claude API と AI エージェント技術を使用して、
            複数の観点から詳細な事業計画書を自動生成します。
            
            **左のサイドバーから：**
            1. テンプレートを選択する
            2. 企業情報を入力する
            3. 🚀 生成ボタンを押す
            
            **生成されるもの：**
            - 市場分析（TAM/SAM/SOM、競合分析）
            - プロダクト戦略（ビジョン、ロードマップ）
            - 財務計画（売上予測、P/L、ユニットエコノミクス）
            - GTM戦略（営業体制、チャネル戦略）
            - 統合事業計画書（全セクション統合）
            
            **出力形式：**
            - 📄 Markdown
            - 📊 Excel（複数シート）
            - 📕 PDF/HTML
            """
        )
        
        st.markdown("---")
        st.caption("🔐 プライバシー: 入力情報は OpenAI API を通じて送信されます。フェデラルサーバーには保存されません。")


if __name__ == "__main__":
    main()
