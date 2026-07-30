"""Environment configuration validation for production safety."""
import os
import logging
from pathlib import Path
from typing import Dict, Any, List, Tuple

logger = logging.getLogger(__name__)

class ConfigError(Exception):
    """Raised when configuration validation fails."""
    pass

class ConfigValidator:
    """Validates environment configuration on startup."""
    
    REQUIRED_VARS: List[str] = [
        'AGENTDNA_LOCAL_ONLY',
        'AGENTDNA_RETENTION_DAYS',
    ]
    
    OPTIONAL_VARS: Dict[str, Any] = {
        'PORT': '8000',
        'AGENTDNA_MAX_SUGGESTIONS_PER_HOUR': '4',
        'AGENTDNA_LLM_MODE': 'mock',
        'AGENTDNA_LLM_BASE_URL': 'http://127.0.0.1:11434',
        'AGENTDNA_LLM_MODEL': 'llama3.2',
        'AGENTDNA_LLM_API_KEY': '',
        'AGENTDNA_APP_URL': 'http://127.0.0.1:8000',
        'AGENTDNA_APP_NAME': 'AgentDNA',
    }
    
    VALID_LLM_MODES = {'disabled', 'mock', 'ollama', 'openai_compatible', 'openrouter'}
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate(self) -> Tuple[bool, List[str], List[str]]:
        """Validate environment configuration.
        
        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        self._check_required_vars()
        self._check_optional_vars()
        self._validate_llm_config()
        self._validate_numeric_ranges()
        self._validate_paths()
        self._check_security_settings()
        
        is_valid = len(self.errors) == 0
        
        if not is_valid:
            logger.error(f'Configuration validation failed: {len(self.errors)} errors')
            for error in self.errors:
                logger.error(f'  - {error}')
        
        if self.warnings:
            logger.warning(f'Configuration warnings: {len(self.warnings)} warnings')
            for warning in self.warnings:
                logger.warning(f'  - {warning}')
        
        return is_valid, self.errors, self.warnings
    
    def _check_required_vars(self):
        """Check that all required environment variables are set."""
        for var in self.REQUIRED_VARS:
            if not os.getenv(var):
                self.errors.append(f'Missing required environment variable: {var}')
    
    def _check_optional_vars(self):
        """Set defaults for optional variables."""
        for var, default in self.OPTIONAL_VARS.items():
            if not os.getenv(var):
                os.environ[var] = str(default)
                logger.debug(f'Set default for {var}={default}')
    
    def _validate_llm_config(self):
        """Validate LLM provider configuration."""
        llm_mode = os.getenv('AGENTDNA_LLM_MODE', 'mock')
        
        if llm_mode not in self.VALID_LLM_MODES:
            self.errors.append(f'Invalid AGENTDNA_LLM_MODE: {llm_mode}. Must be one of {self.VALID_LLM_MODES}')
        
        if llm_mode in {'openrouter', 'openai_compatible'}:
            api_key = os.getenv('AGENTDNA_LLM_API_KEY')
            if not api_key or len(api_key) < 10:
                self.errors.append(f'AGENTDNA_LLM_MODE={llm_mode} requires valid AGENTDNA_LLM_API_KEY')
        
        if llm_mode == 'ollama':
            base_url = os.getenv('AGENTDNA_LLM_BASE_URL', '')
            if 'localhost' not in base_url and '127.0.0.1' not in base_url:
                self.warnings.append(f'Ollama base URL is not localhost: {base_url}')
    
    def _validate_numeric_ranges(self):
        """Validate numeric configuration values."""
        try:
            port = int(os.getenv('PORT', '8000'))
            if not (1024 <= port <= 65535):
                self.errors.append(f'PORT must be between 1024-65535, got {port}')
        except ValueError:
            self.errors.append(f'PORT must be a number, got {os.getenv("PORT")}')
        
        try:
            retention = int(os.getenv('AGENTDNA_RETENTION_DAYS', '30'))
            if not (1 <= retention <= 365):
                self.errors.append(f'AGENTDNA_RETENTION_DAYS must be 1-365, got {retention}')
        except ValueError:
            self.errors.append(f'AGENTDNA_RETENTION_DAYS must be a number')
        
        try:
            suggestions = int(os.getenv('AGENTDNA_MAX_SUGGESTIONS_PER_HOUR', '4'))
            if not (0 <= suggestions <= 100):
                self.errors.append(f'AGENTDNA_MAX_SUGGESTIONS_PER_HOUR must be 0-100, got {suggestions}')
        except ValueError:
            self.errors.append(f'AGENTDNA_MAX_SUGGESTIONS_PER_HOUR must be a number')
    
    def _validate_paths(self):
        """Validate file paths if specified."""
        db_path = os.getenv('AGENTDNA_DB_PATH')
        if db_path:
            db_dir = Path(db_path).parent
            if not db_dir.exists():
                try:
                    db_dir.mkdir(parents=True, exist_ok=True)
                    logger.info(f'Created database directory: {db_dir}')
                except Exception as e:
                    self.errors.append(f'Cannot create database directory {db_dir}: {e}')
    
    def _check_security_settings(self):
        """Check for insecure configuration."""
        local_only = os.getenv('AGENTDNA_LOCAL_ONLY', 'true').lower()
        if local_only != 'true':
            self.warnings.append('AGENTDNA_LOCAL_ONLY=false is insecure without proper authentication')
        
        app_url = os.getenv('AGENTDNA_APP_URL', '')
        if 'localhost' not in app_url and '127.0.0.1' not in app_url:
            self.warnings.append(f'AGENTDNA_APP_URL is not localhost: {app_url}. Ensure proper network security.')

def validate_config() -> None:
    """Validate configuration and raise error if invalid."""
    validator = ConfigValidator()
    is_valid, errors, warnings = validator.validate()
    
    if not is_valid:
        error_msg = 'Configuration validation failed:\n' + '\n'.join(f'  - {e}' for e in errors)
        raise ConfigError(error_msg)
    
    if warnings:
        logger.info('Configuration loaded with warnings. Review security settings.')
