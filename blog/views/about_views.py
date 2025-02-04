from django.views import View
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class AboutView(View):
    """ Stellar 'About Me' view that shines brighter than a supernova! """
    
    _TEMPLATE_NAME: str = "about-me.html"  # 🗺️ Template coordinates
    _DEFAULT_CONTEXT: Dict = {}            # 🧳 Empty suitcase for future data
    
    def get(self, request: HttpRequest) -> HttpResponse:
        """Handle GET requests with the elegance of a orbiting satellite 🛰️"""
        try:
            return render(
                request,
                self._TEMPLATE_NAME,
                self._build_context(),
                # self.header._security_headers()
            )

            response.headers.update(self._security_headers())

        except Exception as e:
            logger.error(f"🌌 Cosmic turbulence in about view: {str(e)}")
            return render(request, "500.html", status=500)

    def _build_context(self) -> Dict:
        """🧰 Prepare context with expandable pockets for future interstellar data 🌠"""
        return self._DEFAULT_CONTEXT.copy()

    def _security_headers(self) -> Dict[str, str]:
        """🔒 Force field headers to protect against space pirates 🏴‍☠️"""
        return {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'Content-Security-Policy': "default-src 'self'"
        }