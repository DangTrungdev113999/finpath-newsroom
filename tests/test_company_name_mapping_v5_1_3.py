"""Test COMPANY_NAME_TO_TICKER covers 78 V5.1.3 new tickers.

Task F-5.5: extend alias dict cho universe expansion 61 → 139.

NOTE on key casing — deviation from task spec:
- Task spec proposed Title-Case keys (e.g. "Vinamilk", "Lọc hoá dầu Bình Sơn").
- Runtime convention (ticker_detection.py:detect_via_company_name) lowercases
  text BEFORE substring match: `name in text_lower`. Mixed-case keys would be
  dead code (never match against lowercased text).
- Resolution: store lowercase keys + lowercase test alias strings. Test still
  verifies coverage; runtime detection works.

NOTE on file location — deviation from task spec:
- Task spec said modify `routing.py`, but COMPANY_NAME_TO_TICKER lives in
  `ticker_detection.py` (routing.py only re-imports it).
- Update applied to ticker_detection.py.

NOTE on collision avoidance:
- Bare "fpt" alias OMITTED — would substring-collide with existing "fpts"
  (text "FPTS công bố" would falsely trigger BOTH FTS and FPT). FPT ticker
  is still detected via 3-char regex + SHORT_FORM_TO_TICKER. Test below
  explicitly verifies no FPT/FPTS collision.
"""
import sys
from pathlib import Path

import pytest

# Use direct file import since dotted path with hyphens isn't valid module syntax
SCRIPTS_DIR = (
    Path(__file__).parent.parent
    / ".claude"
    / "skills"
    / "finpath-newsroom-editor"
    / "scripts"
)
sys.path.insert(0, str(SCRIPTS_DIR))

import ticker_detection  # noqa: E402

MAPPING = ticker_detection.COMPANY_NAME_TO_TICKER


@pytest.mark.parametrize(
    "alias,expected_ticker",
    [
        # oilGas sector
        ("lọc hoá dầu bình sơn", "BSR"),
        ("pv gas", "GAS"),
        ("pv power", "POW"),
        ("petrolimex", "PLX"),
        ("pv drilling", "PVD"),
        ("khí việt nam", "GAS"),
        # logistics
        ("gemadept", "GMD"),
        ("hải an", "HAH"),
        ("cảng hải phòng", "PHP"),
        # fb (tiêu dùng thực phẩm)
        ("vinamilk", "VNM"),
        ("masan", "MSN"),
        ("sabeco", "SAB"),
        ("bia hà nội", "BHN"),
        ("kido", "KDC"),
        # apparel
        ("thành công textile", "TCM"),
        ("may sông hồng", "MSH"),
        ("tng may", "TNG"),
        # retail
        ("thế giới di động", "MWG"),
        ("fpt retail", "FRT"),
        ("digiworld", "DGW"),
        ("phú nhuận", "PNJ"),
        # seafood
        ("vĩnh hoàn", "VHC"),
        ("nam việt", "ANV"),
        ("minh phú", "MPC"),
        ("sao ta", "FMC"),
        # defensive
        ("fpt corp", "FPT"),
        ("fpt software", "FPT"),
        # NOTE: bare "ree" OMITTED — substring-collides with "wall street ck" (WSS).
        # REE still detected via 3-char regex; assert on disambiguating alias instead.
        ("cơ điện lạnh", "REE"),
        ("pc1", "PC1"),
        ("gex", "GEX"),
        ("traphaco", "TRA"),
    ],
)
def test_alias_maps_to_ticker(alias, expected_ticker):
    assert MAPPING.get(alias) == expected_ticker, (
        f"Alias '{alias}' should map to {expected_ticker}, "
        f"got {MAPPING.get(alias)}"
    )


def test_no_fpt_fpts_collision():
    """FPT alias must not substring-match inside 'fpts' (existing alias for FTS).

    detect_via_company_name iterates dict and checks `name in text_lower`.
    If bare 'fpt' were a key, text 'FPTS công bố' would lowercase to 'fpts công bố'
    and falsely trigger BOTH FTS (legit) and FPT (false positive substring).

    Bare 'fpt' deliberately omitted to avoid this — FPT still detected via
    3-char regex + SHORT_FORM_TO_TICKER.
    """
    assert "fpt" not in MAPPING, (
        "Bare 'fpt' key would collide with existing 'fpts' alias — drop it. "
        "FPT ticker still detected via 3-char regex."
    )
    # Functional sanity: FPTS text should detect FTS only, not FPT
    detected = ticker_detection.detect_via_company_name("FPTS công bố doanh thu Q1")
    assert "FTS" in detected
    assert "FPT" not in detected


def test_no_ree_wss_collision():
    """REE alias must not substring-match inside 'wall street ck' (WSS alias).

    Bare 'ree' would substring-collide with 'wall street ck' (contains 'ree'
    in 'st*ree*t'). Text 'Wall Street CK báo cáo' would falsely trigger both
    WSS (legit) and REE (false positive). Bare 'ree' deliberately omitted.
    REE still detected via 3-char regex.
    """
    assert "ree" not in MAPPING, (
        "Bare 'ree' key would collide with existing 'wall street ck' alias. "
        "REE ticker still detected via 3-char regex."
    )
    detected = ticker_detection.detect_via_company_name("Wall Street CK báo cáo Q1")
    assert "WSS" in detected
    assert "REE" not in detected


def test_v5_1_3_aliases_cover_7_new_sectors():
    """Spot-check that at least one alias per sector exists in dict."""
    sector_probes = {
        "oilGas": "petrolimex",
        "logistics": "gemadept",
        "fb": "vinamilk",
        "apparel": "may sông hồng",
        "retail": "thế giới di động",
        "seafood": "vĩnh hoàn",
        "defensive": "traphaco",
    }
    for sector, probe in sector_probes.items():
        assert probe in MAPPING, f"Sector {sector} missing probe alias '{probe}'"
