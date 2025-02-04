# -*- coding: utf-8 -*-
"""Django's command-line utility for administrative tasks with Celery integration."""

from celery import Celery
import os
import sys
from typing import NoReturn


class DjangoCeleryManager:
    """Orchestrates Django and Celery configuration with cosmic harmony 🌌"""

    def __init__(self) -> None:
        self.celery_app: Celery = Celery("blog")
        self.setup_environment()

    def setup_environment(self) -> None:
        """Set up the universe (Django settings) 🌍"""
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    def configure_celery(self) -> None:
        """Wire up Celery with Django's settings ⚡"""
        self.celery_app.config_from_object("django.conf:settings", namespace="CELERY")
        self.celery_app.autodiscover_tasks()
        print("✅ Celery configured and tasks discovered!")

    def execute_django_commands(self) -> NoReturn:
        """Launch Django management commands 🚀"""
        try:
            from django.core.management import execute_from_command_line
        except ImportError as exc:
            raise ImportError(
                "❌ Django missing! Did you forget to:\n"
                "1. Install Django?\n"
                "2. Set PYTHONPATH?\n"
                "3. Activate virtualenv?"
            ) from exc

        execute_from_command_line(sys.argv)

    def run(self) -> None:
        """Main cosmic ignition sequence 🔥"""
        self.configure_celery()
        self.execute_django_commands()


def main() -> None:
    """Entry point to the galaxy 🌠"""
    manager = DjangoCeleryManager()
    manager.run()


if __name__ == "__main__":
    main()
