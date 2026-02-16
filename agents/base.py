"""BaseAgent class for business plan generation agents."""

from typing import Callable, Optional
from abc import ABC, abstractmethod
import anthropic
from tenacity import retry, stop_after_attempt, wait_exponential


class BaseAgent(ABC):
    """Abstract base class for all business plan generation agents.
    
    This class handles common functionality for AI agents including:
    - Anthropic API client initialization
    - Status and progress tracking
    - Streaming response handling
    - Error handling with retry logic
    - Token usage tracking
    """

    def __init__(
        self,
        name: str,
        role: str,
        model: str = "claude-sonnet-4-5-20250929",
    ) -> None:
        """Initialize a BaseAgent instance.
        
        Args:
            name: Agent name (e.g., "MarketResearcher")
            role: Agent role description (e.g., "Market Analysis Expert")
            model: Claude model to use. Defaults to claude-sonnet-4-5-20250929
        """
        self.name = name
        self.role = role
        self.model = model
        self.client = anthropic.Anthropic()
        
        # State management
        self.status: str = "waiting"  # "waiting" | "running" | "streaming" | "done" | "error"
        self.progress: float = 0.0  # 0.0 ~ 1.0
        self.output: str = ""
        self.token_usage: dict = {"input": 0, "output": 0}
        self.error_message: Optional[str] = None

    @abstractmethod
    def get_system_prompt(self, context: dict) -> str:
        """Get the system prompt for this agent.
        
        Must be implemented by subclasses.
        
        Args:
            context: Context dictionary containing task information
            
        Returns:
            System prompt string
            
        Raises:
            NotImplementedError: Always raises as this must be implemented by subclass
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement get_system_prompt()"
        )

    @abstractmethod
    def get_user_prompt(self, context: dict) -> str:
        """Get the user prompt for this agent.
        
        Must be implemented by subclasses.
        
        Args:
            context: Context dictionary containing task information
            
        Returns:
            User prompt string
            
        Raises:
            NotImplementedError: Always raises as this must be implemented by subclass
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement get_user_prompt()"
        )

    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    def run(
        self,
        context: dict,
        on_progress: Optional[Callable[[str, float, str], None]] = None,
    ) -> str:
        """Run the agent with streaming API.
        
        Uses Anthropic's streaming API to generate responses with real-time
        progress callbacks. Implements retry logic for transient failures.
        
        Args:
            context: Context dictionary with task information
            on_progress: Optional callback function with signature:
                        (agent_name: str, progress: float, chunk: str) -> None
                        
        Returns:
            Complete response text from API
            
        Raises:
            anthropic.APIError: After maximum retries if API call fails
        """
        try:
            self.status = "running"
            self.output = ""
            self.error_message = None
            self.progress = 0.0
            
            # Check API key is set
            try:
                import os
                api_key = os.getenv("ANTHROPIC_API_KEY")
                if not api_key or api_key.strip() == "":
                    self.status = "error"
                    self.error_message = (
                        "❌ APIキーが設定されていません。\n"
                        "以下のいずれかの方法で設定してください：\n"
                        "1. .env ファイルに ANTHROPIC_API_KEY=sk-ant-v1-... を追記\n"
                        "2. Streamlit Secret に ANTHROPIC_API_KEY を設定\n"
                        "3. export ANTHROPIC_API_KEY=sk-ant-v1-... （環境変数）"
                    )
                    raise ValueError(self.error_message)
            except ValueError:
                raise
            
            # Get prompts from subclass implementation
            system_prompt = self.get_system_prompt(context)
            user_prompt = self.get_user_prompt(context)
            
            # Get max_tokens from context or use default
            max_tokens = context.get("max_tokens", 5000)
            
            # Create system message with cache control
            system_with_cache = [
                {
                    "type": "text",
                    "text": system_prompt,
                    "cache_control": {"type": "ephemeral"},
                }
            ]
            
            self.status = "streaming"
            total_chars = 0
            
            # Stream the message
            with self.client.messages.stream(
                model=self.model,
                max_tokens=max_tokens,
                system=system_with_cache,
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt,
                    }
                ],
            ) as stream:
                for text in stream.text_stream:
                    self.output += text
                    total_chars += len(text)
                    
                    # Update progress - estimate based on character count
                    # Assuming avg 4 chars per token
                    self.progress = min(
                        total_chars / (max_tokens * 4),
                        0.99,
                    )
                    
                    # Call progress callback if provided
                    if on_progress:
                        on_progress(self.name, self.progress, text)
                
                # Get final message object with token usage
                final_message = stream.get_final_message()
            
            # Record token usage
            self.token_usage = {
                "input": final_message.usage.input_tokens,
                "output": final_message.usage.output_tokens,
            }
            
            self.progress = 1.0
            self.status = "done"
            
            return self.output
            
        except anthropic.APIStatusError as e:
            # Handle API status errors (429 rate limit, 401 auth, etc.)
            self.status = "error"
            if e.status_code == 429:
                self.error_message = (
                    "⏱️ レート制限に達しました。\n"
                    "1分後に再試行してください。"
                )
            elif e.status_code == 401:
                self.error_message = (
                    "❌ APIキーが無効です。\n"
                    ".env ファイルを確認してください。"
                )
            elif e.status_code == 500:
                self.error_message = (
                    "⚠️ Anthropic API サーバーエラー。\n"
                    "少ししてから再試行してください。"
                )
            else:
                self.error_message = f"APIエラー ({e.status_code}): {e.message}"
            raise
            
        except (ConnectionError, TimeoutError) as e:
            # Handle network errors
            self.status = "error"
            self.error_message = (
                f"🌐 ネットワークエラー: {type(e).__name__}\n"
                "インターネット接続を確認してください。"
            )
            raise
            
        except Exception as e:
            # Handle unexpected errors
            self.status = "error"
            self.error_message = f"❌ 予期しないエラー: {type(e).__name__}: {str(e)}"
            raise

    def run_sync(
        self,
        context: dict,
        on_progress: Optional[Callable[[str, float, str], None]] = None,
    ) -> str:
        """Synchronous wrapper for run() method for use with ThreadPoolExecutor.
        
        This method is designed to be used with concurrent.futures.ThreadPoolExecutor
        for parallel execution of multiple agents.
        
        Args:
            context: Context dictionary with task information
            on_progress: Optional callback function with signature:
                        (agent_name: str, progress: float, chunk: str) -> None
                        
        Returns:
            Complete response text from API
        """
        return self.run(context, on_progress)
