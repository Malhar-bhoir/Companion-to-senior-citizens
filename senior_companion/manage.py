#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # --- ADD THIS NEW LINE ---
    # This is the fix for the SynchronousOnlyOperation error.
    # It allows our sync views to make (safe) sync DB calls from
    # within the async ASGI server context.
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    # --- END OF ADDED LINE ---
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'senior_companion_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
