from scripts.ensure_precio_venta import select_targets


def test_select_targets_excludes_main_by_default():
    available = ["main", "current", "artstudio3d", "company_1"]
    targets = select_targets(available)
    assert "main" not in targets
    assert "current" not in targets
    assert "artstudio3d" in targets


def test_select_targets_allows_main_when_flag():
    available = ["main", "current", "artstudio3d"]
    targets = select_targets(available, allow_main=True)
    assert "main" in targets
    assert "current" in targets


def test_select_targets_respects_requested_list_and_companies():
    available = ["main", "artstudio3d"]
    targets = select_targets(available, requested_list=["artstudio3d"])
    assert targets == ["artstudio3d"]

    # include_companies should add new company keys
    targets2 = select_targets(
        available, requested_list=["artstudio3d"], include_companies=["company_99"]
    )
    assert "company_99" in targets2
