"""Centralized error handling for the API."""
import logging
import traceback
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

logger = logging.getLogger(__name__)

class AgentDNAError(Exception):
    """Base exception for AgentDNA errors."""
    def __init__(self, message: str, code: str = 'internal_error', status_code: int = 500):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)

class RateLimitError(AgentDNAError):
    """Raised when rate limit is exceeded."""
    def __init__(self, limit_type: str):
        super().__init__(
            f'Rate limit exceeded: {limit_type}',
            code='rate_limit_exceeded',
            status_code=429
        )

class ValidationError(AgentDNAError):
    """Raised when validation fails."""
    def __init__(self, message: str):
        super().__init__(message, code='validation_error', status_code=422)

class NotFoundError(AgentDNAError):
    """Raised when resource not found."""
    def __init__(self, resource: str):
        super().__init__(
            f'Resource not found: {resource}',
            code='not_found',
            status_code=404
        )

def setup_error_handlers(app):
    """Register error handlers with FastAPI app."""
    
    @app.exception_handler(AgentDNAError)
    async def agentdna_error_handler(request: Request, exc: AgentDNAError):
        logger.error(f'AgentDNA error: {exc.code} - {exc.message}')
        return JSONResponse(
            status_code=exc.status_code,
            content={
                'error': exc.code,
                'message': exc.message,
                'path': str(request.url.path)
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        logger.warning(f'Validation error on {request.url.path}: {exc.errors()}')
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                'error': 'validation_error',
                'message': 'Request validation failed',
                'details': exc.errors(),
                'path': str(request.url.path)
            }
        )
    
    @app.exception_handler(Exception)
    async def general_error_handler(request: Request, exc: Exception):
        logger.error(
            f'Unhandled exception on {request.url.path}: {str(exc)}',
            exc_info=True
        )
        
        # Don't expose internal errors in production
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                'error': 'internal_server_error',
                'message': 'An unexpected error occurred',
                'path': str(request.url.path)
            }
        )
    
    logger.info('Error handlers registered')
