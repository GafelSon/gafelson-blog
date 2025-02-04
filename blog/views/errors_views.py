from django.views import View
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class BaseErrorView(View):
    """🔥 Universal Error Handler Base Class 🌌"""
    
    TEMPLATE_NAME: str = ""
    STATUS_CODE: int = 500
    SECURITY_HEADERS: Dict[str, str] = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'Content-Security-Policy': "default-src 'self'"
    }
    
    def _log_error(self, exception: Optional[Exception] = None) -> None:
        """📡 Universal error logging system"""
        logger.error(f"🌌 Cosmic anomaly detected: {exception or 'Unknown error'}")

    def _get_context(self) -> Dict[str, str]:
        """🧭 Base context for error templates"""
        return {'error_code': self.STATUS_CODE}

    def _get_headers(self) -> Dict[str, str]:
        """🛡️ Standard security headers for all errors"""
        return self.SECURITY_HEADERS.copy()

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """⚡ Central request handler for all errors"""
        return render(
            request,
            self.TEMPLATE_NAME,
            self._get_context(),
            status=self.STATUS_CODE,
        )

        response.headers.update(self._get_headers())

class NotFoundView(BaseErrorView):
    """👽 404 Handler: Galactic Pathfinder 🌠"""
    
    TEMPLATE_NAME = "404.html"
    STATUS_CODE = 400

    def get(self, request: HttpRequest, exception: Exception, *args, **kwargs) -> HttpResponse:
        """Handle lost space travelers with proper exception"""
        self._log_error(exception)
        return super().get(request, *args, **kwargs)

    def _get_context(self) -> Dict[str, str]:
        """🚀 Custom 404 context"""
        return {
            **super()._get_context(),
            'error_message': "This galaxy seems to be missing from our star charts",
        }

class ServerErrorView(BaseErrorView):
    """💥 500 Handler: Quantum Crash Investigator 🌪️"""
    
    TEMPLATE_NAME = "500.html"
    STATUS_CODE = 500

    def _get_context(self) -> Dict[str, str]:
        """🛠️ Custom 500 context"""
        return {
            **super()._get_context(),
            'error_message': "Our engineers are working FTL to fix this!",
        }