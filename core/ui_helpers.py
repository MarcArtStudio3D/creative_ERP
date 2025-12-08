import logging

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

        if os.environ.get("PYTEST_CURRENT_TEST"):
            # Running under pytest — log instead of showing a modal to avoid blocking
            logging.getLogger(__name__).warning("%s: %s", title, message)
            return
    except Exception:
        pass

    try:
        QMessageBox.warning(parent, title, message)
    except Exception:
        # Last resort fallback to logging if QMessageBox can't be shown (headless)
        logging.getLogger(__name__).exception("%s: %s", title, message)


def show_info(parent, title: str, message: str):
    """Show an information message (non-blocking in tests)."""
    try:
        import os

        if os.environ.get("PYTEST_CURRENT_TEST"):
            logging.getLogger(__name__).info("%s: %s", title, message)
            return
    except Exception:
        pass

    try:
        QMessageBox.information(parent, title, message)
    except Exception:
        logging.getLogger(__name__).exception("%s: %s", title, message)


def show_critical(parent, title: str, message: str):
    """Show a critical message (non-blocking in tests)."""
    try:
        import os

        if os.environ.get("PYTEST_CURRENT_TEST"):
            logging.getLogger(__name__).error("%s: %s", title, message)
            return
    except Exception:
        pass

    try:
        QMessageBox.critical(parent, title, message)
    except Exception:
        logging.getLogger(__name__).exception("%s: %s", title, message)


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

        if os.environ.get("PYTEST_CURRENT_TEST"):
            # Running under pytest — log the question and return the default
            logging.getLogger(__name__).info("%s: %s", title, message)
            # Default to Yes if not specified to allow destructive actions in tests
            return default if default is not None else QMessageBox.StandardButton.Yes
    except Exception:
        pass

    try:
        # Build a user-friendly, translatable question dialog using explicit button labels.
        # This ensures we show localized labels such as 'Sí' / 'No' instead of raw 'Yes' / 'No'.
        from PySide6.QtCore import QCoreApplication

        # If caller did not request custom buttons, provide localized Yes/No buttons.
        yes_label = QCoreApplication.translate("core.ui_helpers", "Sí")
        no_label = QCoreApplication.translate("core.ui_helpers", "No")

        # Create message box and add translated buttons. Use default role mapping to return StandardButton values.
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle(title)
        msg.setText(message)

        # Add custom translated buttons and keep references
        yes_btn = msg.addButton(yes_label, QMessageBox.AcceptRole)
        no_btn = msg.addButton(no_label, QMessageBox.RejectRole)

        # Choose default shown button
        try:
            if default == QMessageBox.StandardButton.Yes:
                msg.setDefaultButton(yes_btn)
            elif default == QMessageBox.StandardButton.No:
                msg.setDefaultButton(no_btn)
            else:
                # fallback default behaviour — choose No as safer default
                msg.setDefaultButton(no_btn)
        except Exception:
            pass

        msg.exec()
        clicked = msg.clickedButton()
        if clicked == yes_btn:
            return QMessageBox.StandardButton.Yes
        else:
            return QMessageBox.StandardButton.No
    except Exception:
        # If the dialog fails, fall back to returning default or Yes
        return default if default is not None else QMessageBox.StandardButton.Yes
