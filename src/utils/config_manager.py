"""
Create configuration management system with validation
Task T010: Create configuration management system with validation
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class ProcessingConfig:
    """Configuration for document processing"""
    chunk_size: int = 512
    chunk_overlap: int = 50
    request_timeout: int = 30
    max_retries: int = 3
    similarity_threshold: float = 0.5
    default_top_k: int = 5


@dataclass
class APIConfig:
    """Configuration for API access"""
    cohere_api_key: str
    qdrant_url: str
    qdrant_api_key: str
    openai_api_key: Optional[str] = None


@dataclass
class AgentConfig:
    """Configuration for agent behavior"""
    default_top_k: int = 3
    default_threshold: float = 0.3
    max_history_length: int = 10
    enable_context_awareness: bool = True


class ConfigManager:
    """Configuration management system with validation"""

    def __init__(self):
        self.processing_config = self._load_processing_config()
        self.api_config = self._load_api_config()
        self.agent_config = self._load_agent_config()

    def _load_processing_config(self) -> ProcessingConfig:
        """Load processing configuration from environment variables"""
        chunk_size = self._get_int_env('CHUNK_SIZE', 512)
        chunk_overlap = self._get_int_env('CHUNK_OVERLAP', 50)
        request_timeout = self._get_int_env('REQUEST_TIMEOUT', 30)
        max_retries = self._get_int_env('MAX_RETRIES', 3)
        similarity_threshold = self._get_float_env('SIMILARITY_THRESHOLD', 0.5)
        default_top_k = self._get_int_env('DEFAULT_TOP_K', 5)

        # Validate the configuration values
        if chunk_size <= 0:
            logger.warning(f"Invalid chunk_size: {chunk_size}, using default 512")
            chunk_size = 512

        if chunk_overlap < 0:
            logger.warning(f"Invalid chunk_overlap: {chunk_overlap}, using default 50")
            chunk_overlap = 50

        if request_timeout <= 0:
            logger.warning(f"Invalid request_timeout: {request_timeout}, using default 30")
            request_timeout = 30

        if max_retries <= 0:
            logger.warning(f"Invalid max_retries: {max_retries}, using default 3")
            max_retries = 3

        if not 0.0 <= similarity_threshold <= 1.0:
            logger.warning(f"Invalid similarity_threshold: {similarity_threshold}, using default 0.5")
            similarity_threshold = 0.5

        if default_top_k <= 0:
            logger.warning(f"Invalid default_top_k: {default_top_k}, using default 5")
            default_top_k = 5

        return ProcessingConfig(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            request_timeout=request_timeout,
            max_retries=max_retries,
            similarity_threshold=similarity_threshold,
            default_top_k=default_top_k
        )

    def _load_api_config(self) -> APIConfig:
        """Load API configuration from environment variables"""
        cohere_api_key = os.getenv('COHERE_API_KEY')
        qdrant_url = os.getenv('QDRANT_URL')
        qdrant_api_key = os.getenv('QDRANT_API_KEY')
        openai_api_key = os.getenv('OPENAI_API_KEY')

        # Validate required API keys
        missing_keys = []
        if not cohere_api_key:
            missing_keys.append('COHERE_API_KEY')
        if not qdrant_url:
            missing_keys.append('QDRANT_URL')
        if not qdrant_api_key:
            missing_keys.append('QDRANT_API_KEY')

        if missing_keys:
            raise ValueError(f"Missing required API configuration: {', '.join(missing_keys)}")

        return APIConfig(
            cohere_api_key=cohere_api_key,
            qdrant_url=qdrant_url,
            qdrant_api_key=qdrant_api_key,
            openai_api_key=openai_api_key
        )

    def _load_agent_config(self) -> AgentConfig:
        """Load agent configuration from environment variables"""
        default_top_k = self._get_int_env('AGENT_DEFAULT_TOP_K', 3)
        default_threshold = self._get_float_env('AGENT_DEFAULT_THRESHOLD', 0.3)
        max_history_length = self._get_int_env('AGENT_MAX_HISTORY_LENGTH', 10)
        enable_context_awareness_str = os.getenv('AGENT_ENABLE_CONTEXT_AWARENESS', 'true')
        enable_context_awareness = enable_context_awareness_str.lower() == 'true'

        # Validate the configuration values
        if default_top_k <= 0:
            logger.warning(f"Invalid AGENT_DEFAULT_TOP_K: {default_top_k}, using default 3")
            default_top_k = 3

        if not 0.0 <= default_threshold <= 1.0:
            logger.warning(f"Invalid AGENT_DEFAULT_THRESHOLD: {default_threshold}, using default 0.3")
            default_threshold = 0.3

        if max_history_length <= 0:
            logger.warning(f"Invalid AGENT_MAX_HISTORY_LENGTH: {max_history_length}, using default 10")
            max_history_length = 10

        return AgentConfig(
            default_top_k=default_top_k,
            default_threshold=default_threshold,
            max_history_length=max_history_length,
            enable_context_awareness=enable_context_awareness
        )

    def _get_int_env(self, key: str, default: int) -> int:
        """Get integer environment variable with default"""
        try:
            value = os.getenv(key)
            if value is not None:
                return int(value)
        except (ValueError, TypeError):
            logger.warning(f"Invalid integer value for {key}: {value}, using default {default}")
        return default

    def _get_float_env(self, key: str, default: float) -> float:
        """Get float environment variable with default"""
        try:
            value = os.getenv(key)
            if value is not None:
                return float(value)
        except (ValueError, TypeError):
            logger.warning(f"Invalid float value for {key}: {value}, using default {default}")
        return default

    def validate_config(self) -> bool:
        """Validate the entire configuration"""
        try:
            # Check that all required API keys are present
            if not self.api_config.cohere_api_key:
                logger.error("COHERE_API_KEY is required")
                return False

            if not self.api_config.qdrant_url:
                logger.error("QDRANT_URL is required")
                return False

            if not self.api_config.qdrant_api_key:
                logger.error("QDRANT_API_KEY is required")
                return False

            # Validate processing config values
            if self.processing_config.chunk_size <= 0:
                logger.error(f"Invalid chunk_size: {self.processing_config.chunk_size}")
                return False

            if self.processing_config.chunk_overlap < 0:
                logger.error(f"Invalid chunk_overlap: {self.processing_config.chunk_overlap}")
                return False

            if self.processing_config.request_timeout <= 0:
                logger.error(f"Invalid request_timeout: {self.processing_config.request_timeout}")
                return False

            if self.processing_config.max_retries <= 0:
                logger.error(f"Invalid max_retries: {self.processing_config.max_retries}")
                return False

            if not 0.0 <= self.processing_config.similarity_threshold <= 1.0:
                logger.error(f"Invalid similarity_threshold: {self.processing_config.similarity_threshold}")
                return False

            if self.processing_config.default_top_k <= 0:
                logger.error(f"Invalid default_top_k: {self.processing_config.default_top_k}")
                return False

            # Validate agent config values
            if self.agent_config.default_top_k <= 0:
                logger.error(f"Invalid agent default_top_k: {self.agent_config.default_top_k}")
                return False

            if not 0.0 <= self.agent_config.default_threshold <= 1.0:
                logger.error(f"Invalid agent default_threshold: {self.agent_config.default_threshold}")
                return False

            if self.agent_config.max_history_length <= 0:
                logger.error(f"Invalid agent max_history_length: {self.agent_config.max_history_length}")
                return False

            return True

        except Exception as e:
            logger.error(f"Configuration validation error: {e}")
            return False

    def get_config_dict(self) -> Dict[str, Any]:
        """Get configuration as a dictionary"""
        return {
            'processing': {
                'chunk_size': self.processing_config.chunk_size,
                'chunk_overlap': self.processing_config.chunk_overlap,
                'request_timeout': self.processing_config.request_timeout,
                'max_retries': self.processing_config.max_retries,
                'similarity_threshold': self.processing_config.similarity_threshold,
                'default_top_k': self.processing_config.default_top_k
            },
            'api': {
                'cohere_api_key_set': bool(self.api_config.cohere_api_key),
                'qdrant_url': self.api_config.qdrant_url,
                'qdrant_api_key_set': bool(self.api_config.qdrant_api_key),
                'openai_api_key_set': bool(self.api_config.openai_api_key)
            },
            'agent': {
                'default_top_k': self.agent_config.default_top_k,
                'default_threshold': self.agent_config.default_threshold,
                'max_history_length': self.agent_config.max_history_length,
                'enable_context_awareness': self.agent_config.enable_context_awareness
            }
        }

    def update_processing_config(self, **kwargs):
        """Update processing configuration values"""
        for key, value in kwargs.items():
            if hasattr(self.processing_config, key):
                setattr(self.processing_config, key, value)
                logger.info(f"Updated processing config {key} to {value}")