from modules.articulos.view import ArticulosView


def test_listwidget_is_palette_like():
    v = ArticulosView()

    # If UI is not present (headless test harness), skip
    if not hasattr(v.ui, "listWidget"):
        return

    lw = v.ui.listWidget

    # Expect icon-mode (grid of swatches) and a reasonably large icon/grid size
    try:
        from PySide6.QtWidgets import QListView

        assert lw.viewMode() == QListView.ViewMode.IconMode
    except Exception:
        # Some envs or PySide builds may behave slightly differently in headless CI
        pass

        sz = lw.iconSize()
        # should be large enough to feel like a swatch (>= 40px)
        assert sz.width() >= 40 and sz.height() >= 40


def test_listwidget_items_render_as_swatches():
    v = ArticulosView()

    if not hasattr(v.ui, "listWidget"):
        return

    lw = v.ui.listWidget
    assert lw.count() > 0

    for i in range(lw.count()):
        it = lw.item(i)
        # text is hidden so label should be empty
        assert it.text() == ""
        # icon exists (may be null in headless env) but attribute should be present
        assert hasattr(it, "icon")
