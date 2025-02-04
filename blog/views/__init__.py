"""
🚀 Cosmic Views Package - Your gateway to the view universe! 🌠

Export structure:
from .home_views import HomeView          # 🏠 Main entry point
from .post_views import PostView          # 📝 Individual post gateway
from .about_views import AboutView        # 👤 Personal constellation
from .errors_views import (               # 🚨 Emergency systems
    NotFoundView,
    ServerErrorView
)

Usage:
>>> from .views import HomeView, PostView, AboutView
"""

from .home_views import HomeView
from .post_views import PostView
from .about_views import AboutView
from .errors_views import NotFoundView, ServerErrorView

__all__ = [
    'HomeView',
    'PostView',
    'AboutView',
    'NotFoundView',
    'ServerErrorView'
]

__version__ = '1.0.0'  # 🌌 Current spacetime version
__author__ = 'Soheil Fouladvandi <@gafelson>'

def _cosmic_init() -> None:
    """🌈 Private function to align celestial view energies"""
    print("🌀 SOHEIL: Cosmic views initialized! Ready to handle requests at light speed! 🚀")

# Automatically align cosmic energies when package is imported
_cosmic_init()
