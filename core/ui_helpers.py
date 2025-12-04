from PySide6.QtWidgets import QMessageBox

def show_warning(parent, title: str, message: str):
    """Show a warning message to the user.

    Behavior:
    - In normal runs: show a modal QMessageBox.warning(parent, title, message)
    - In pytest / CI: detect PYTEST_CURRENT_TEST env var and print the message instead
      to avoid blocking test runs with dialogs.
    """
    try:
        import os
        if os.environ.get('PYTEST_CURRENT_TEST'):
            # Running under pytest — print instead of showing a modal
            print(f"{title}: {message}")
            return
    except Exception:
        pass

    try:
        QMessageBox.warning(parent, title, message)
    except Exception:
        # Last resort fallback to printing if QMessageBox can't be shown (headless)
        print(f"{title}: {message}")

def show_info(parent, title: str, message: str):
    """Show an information message (non-blocking in tests)."""
    try:
        import os
        if os.environ.get('PYTEST_CURRENT_TEST'):
            print(f"{title}: {message}")
            return
    except Exception:
        pass

    try:
        QMessageBox.information(parent, title, message)
    except Exception:
        print(f"{title}: {message}")

def show_critical(parent, title: str, message: str):
    """Show a critical message (non-blocking in tests)."""
    try:
        import os
        if os.environ.get('PYTEST_CURRENT_TEST'):
            print(f"{title}: {message}")
            return
    except Exception:
        pass

    try:
        QMessageBox.critical(parent, title, message)
    except Exception:
        print(f"{title}: {message}")


def show_question(parent, title: str, message: str, buttons=None, default=None):
    """Show a question dialog and return the user's response.

    Parameters:
    - parent, title, message: forwarded to QMessageBox.question
    - buttons: optional button flags (e.g., QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    - default: optional default button when running under pytest (defaults to Yes)

    Behavior:
    - In pytest: print the question and return the default response
    - Otherwise: call QMessageBox.question and return the result
    """
    try:
        import os
        if os.environ.get('PYTEST_CURRENT_TEST'):
            # Running under pytest — print the question and return the default
            print(f"{title}: {message}")
            # Default to Yes if not specified to allow destructive actions in tests
            return default if default is not None else QMessageBox.StandardButton.Yes
    except Exception:
        pass

    try:
        if buttons is None and default is None:
            return QMessageBox.question(parent, title, message)

        # If buttons/default provided, pass them through
        if buttons is None:
            buttons = QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        if default is None:
            default = QMessageBox.StandardButton.No

        return QMessageBox.question(parent, title, message, buttons, default)
    except Exception:
        # If the dialog fails, fall back to returning default or Yes
        return default if default is not None else QMessageBox.StandardButton.Yes
