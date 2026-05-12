"""
Ticker detection cho Finpath Newsroom Editor.

Phase A: Regex 3 chữ uppercase (cheap, fast)
Phase B: LLM fallback nếu regex miss obvious cases (vd "Vietcombank" without "VCB")
"""

import re
from typing import Optional

# Regex pattern: 3 chữ cái uppercase đứng riêng (không phải part của 1 từ dài hơn)
TICKER_PATTERN = re.compile(r'\b([A-Z]{3})\b')


def detect_tickers(text: str) -> list[str]:
    """
    Detect ticker từ text bằng regex.
    
    Returns:
        List ticker (đã dedupe, giữ thứ tự xuất hiện)
    """
    if not text:
        return []
    
    matches = TICKER_PATTERN.findall(text)
    
    # Dedupe giữ thứ tự
    seen = set()
    result = []
    for t in matches:
        if t not in seen:
            seen.add(t)
            result.append(t)
    
    return result


def detect_tickers_with_position(text: str) -> list[tuple[str, int]]:
    """
    Detect tickers + position (for primary ticker rule).
    
    Returns:
        List of (ticker, first_position_in_text)
    """
    if not text:
        return []
    
    tickers_seen = {}
    for match in TICKER_PATTERN.finditer(text):
        ticker = match.group(1)
        if ticker not in tickers_seen:
            tickers_seen[ticker] = match.start()
    
    return sorted(tickers_seen.items(), key=lambda x: x[1])


def count_ticker_mentions(text: str, ticker: str) -> int:
    """Đếm số lần ticker xuất hiện trong text."""
    if not text or not ticker:
        return 0
    
    pattern = re.compile(rf'\b{re.escape(ticker)}\b')
    return len(pattern.findall(text))


# Common name → ticker mapping (cho LLM fallback context).
# CHỈ thêm alias an toàn (không gây false positive khi lowercase substring match).
# KHÔNG thêm "mb" lowercase — sẽ match "miễn bàn", "mb chi"... → false positive.
# Short-form ticker uppercase ("MB", "VCB"...) bắt qua TICKER_UPPER_REGEX bên dưới.
COMPANY_NAME_TO_TICKER = {
    # Bank HOSE (alias lowercase + Vietnamese variations)
    "techcombank": "TCB",
    "vietcombank": "VCB",
    "vietin": "CTG",
    "vietinbank": "CTG",
    "công thương": "CTG",
    "bidv": "BID",
    "đầu tư phát triển": "BID",
    "mbbank": "MBB",
    "mb bank": "MBB",
    "quân đội": "MBB",
    "acb": "ACB",
    "á châu": "ACB",
    "vpbank": "VPB",
    "việt nam thịnh vượng": "VPB",
    "hdbank": "HDB",
    "phát triển tp.hcm": "HDB",
    "sacombank": "STB",
    "sacom": "STB",
    "sài gòn thương tín": "STB",
    "shb": "SHB",
    "sài gòn-hà nội": "SHB",
    "eximbank": "EIB",
    "xuất nhập khẩu": "EIB",
    "tpbank": "TPB",
    "tiên phong bank": "TPB",
    "maritime bank": "MSB",
    "hàng hải": "MSB",
    "msb": "MSB",
    "lpbank": "LPB",
    "liên việt": "LPB",
    "lộc phát": "LPB",
    "ocb": "OCB",
    "phương đông": "OCB",
    "vib": "VIB",
    "quốc tế việt nam": "VIB",
    # Bank HNX
    "nam á bank": "NAB",
    "nam a": "NAB",
    "namabank": "NAB",
    "bắc á bank": "BAB",
    "bacabank": "BAB",
    "ncb": "NVB",
    "quốc dân": "NVB",
    "saigonbank": "SGB",
    "sài gòn công thương": "SGB",
    # Bank UPCOM
    "việt á bank": "VAB",
    "vietabank": "VAB",
    "bản việt bank": "BVB",
    "viet capital bank": "BVB",
    "abbank": "ABB",
    "an bình bank": "ABB",
    "kienlongbank": "KLB",
    "kiên long": "KLB",
    "vietbank": "VBB",
    "việt nam thương tín": "VBB",
    "pgbank": "PGB",
    "xăng dầu petrolimex": "PGB",
    "hợp tác xã": "HDF",
    # CK HOSE
    "ssi securities": "SSI",
    "vndirect": "VND",
    "hsc": "HCM",
    "tp.hcm securities": "HCM",
    "vietcap": "VCI",
    "bản việt ck": "VCI",
    "bản việt chứng khoán": "VCI",
    "vix": "VIX",
    "vietnam investment securities": "VIX",
    # CK HNX
    "shs": "SHS",
    "sài gòn-hà nội ck": "SHS",
    "mb securities": "MBS",
    "mbs": "MBS",
    "bảo việt ck": "BVS",
    "bvsc": "BVS",
    "bidv securities": "BSI",
    "bsc": "BSI",
    "agriseco": "AGR",
    "vietinbank securities": "CTS",
    "cts securities": "CTS",
    "apg securities": "APG",
    "everest securities": "EVS",
    "ivs": "IVS",
    "đầu tư việt nam ck": "IVS",
    "petrosetco": "PSI",
    "dầu khí ck": "PSI",
    "thiên việt ck": "TVS",
    "tvs": "TVS",
    "phố wall": "WSS",
    "wall street ck": "WSS",
    "tps": "ORS",
    "tiên phong ck": "ORS",
    "nhất việt ck": "VFS",
    "thành công ck": "TCI",
    # CK UPCOM
    "dsc": "DSC",
    "đông sài gòn ck": "DSC",
    "fpts": "FTS",
    "csi": "CSI",
    "kiến thiết ck": "CSI",
    "sbsc": "SBS",
    "sacombank securities": "SBS",
    "phú hưng ck": "PHS",
    "bos securities": "ART",
    "apec ck": "APS",
    "châu á thái bình dương ck": "APS",
    "bảo minh ck": "BMS",
    "smart invest": "AAS",
    "việt tín ck": "VTS",
    # BĐS (unchanged)
    "vinhomes": "VHM",
    "novaland": "NVL",
    "khang điền": "KDH",
    "đất xanh": "DXG",
    # Oil-Gas (10 mã)
    "pv gas": "GAS",
    "pvgas": "GAS",
    "khí việt nam": "GAS",
    "pv drilling": "PVD",
    "pvdrilling": "PVD",
    "ptsc": "PVS",
    "pv tech": "PVS",
    "dịch vụ kỹ thuật dầu khí": "PVS",
    "pv trans": "PVT",
    "vận tải dầu khí": "PVT",
    "bình sơn": "BSR",
    "lọc hóa dầu bình sơn": "BSR",
    "dung quất": "BSR",
    "petrolimex": "PLX",
    "xăng dầu việt nam": "PLX",
    "pv oil": "OIL",
    "pvoil": "OIL",
    "đạm phú mỹ": "DPM",
    "phú mỹ": "DPM",
    "đạm cà mau": "DCM",
    "cà mau": "DCM",
    "pv coating": "PVC",
    "bọc ống dầu khí": "PVC",
}


# === V5.1.3 NEW — universe expansion 61 → 139 (7 new sectors) ===
# Keys are lowercase (detect_via_company_name lowercases text before
# substring matching). Bare 3-char tickers omitted where redundant with
# TICKER_PATTERN regex. Bare "fpt" deliberately OMITTED to avoid substring
# collision with existing "fpts" (FTS) alias.
# HPG explicitly excluded (sector unverified — defer V5.2).
COMPANY_NAME_TO_TICKER.update({
    # --- oilGas sector ---
    "lọc hoá dầu bình sơn": "BSR",
    "lọc hóa dầu bình sơn": "BSR",
    "bình sơn": "BSR",
    "pv services": "PVS",
    "petrovietnam services": "PVS",
    "pv gas": "GAS",
    "tổng công ty khí": "GAS",
    "khí việt nam": "GAS",
    "pv power": "POW",
    "tổng công ty điện lực dầu khí": "POW",
    "petrolimex": "PLX",
    "tập đoàn xăng dầu": "PLX",
    "pv oil": "OIL",
    "pv drilling": "PVD",
    "khoan và dịch vụ khoan dầu khí": "PVD",
    "pv trans": "PVT",
    "vận tải dầu khí": "PVT",

    # --- logistics sector ---
    "gemadept": "GMD",
    "cảng gemadept": "GMD",
    "hải an": "HAH",
    "vận tải biển hải an": "HAH",
    "vận tải biển việt nam": "VOS",
    "cảng container việt nam": "VSC",
    "cảng hải phòng": "PHP",
    "cảng đà nẵng": "CDN",
    "logistics hàng xanh": "HAX",

    # --- fb (Tiêu dùng thực phẩm) ---
    "vinamilk": "VNM",
    "sữa việt nam": "VNM",
    "masan": "MSN",
    "tập đoàn masan": "MSN",
    "sabeco": "SAB",
    "bia sài gòn": "SAB",
    "bia hà nội": "BHN",
    "habeco": "BHN",
    "kido": "KDC",
    "bánh kẹo kido": "KDC",
    "mộc châu milk": "MCM",
    "sữa mộc châu": "MCM",
    "đường quảng ngãi": "QNS",

    # --- apparel (Dệt may) ---
    "thành công textile": "TCM",
    "dệt may thành công": "TCM",
    "may sông hồng": "MSH",
    "tng may": "TNG",
    "may tng": "TNG",
    "thái nguyên may": "TNG",

    # --- retail (Bán lẻ) ---
    "thế giới di động": "MWG",
    "bách hóa xanh": "MWG",
    "fpt retail": "FRT",
    "fpt shop": "FRT",
    "long châu": "FRT",
    "digiworld": "DGW",
    "phú nhuận": "PNJ",
    "trang sức phú nhuận": "PNJ",
    "phục vụ sân bay quốc tế": "AST",

    # --- seafood (Thuỷ sản) ---
    "vĩnh hoàn": "VHC",
    "thủy sản vĩnh hoàn": "VHC",
    "nam việt": "ANV",
    "thủy sản nam việt": "ANV",
    "minh phú": "MPC",
    "thủy sản minh phú": "MPC",
    "sao ta": "FMC",
    "thực phẩm sao ta": "FMC",
    "i.d.i": "IDI",
    "camimex": "CMX",

    # --- defensive (Phòng thủ) ---
    # NOTE: bare "fpt" OMITTED — would substring-collide with existing "fpts" → FTS.
    # FPT ticker still detected via 3-char regex + SHORT_FORM_TO_TICKER.
    "fpt corp": "FPT",
    "fpt software": "FPT",
    # NOTE: bare "ree" OMITTED — substring-collides with "wall street ck" (WSS).
    # REE still detected via 3-char regex.
    "cơ điện lạnh": "REE",
    "pc1": "PC1",
    "xây lắp điện 1": "PC1",
    "gex": "GEX",
    "gelex": "GEX",
    "tin học itd": "ITD",
    "traphaco": "TRA",
    "dược traphaco": "TRA",
    "bidiphar": "DBD",
    "imexpharm": "IMP",
    "elcom": "ELC",
})


# Bug A fix — Pass 2 detection: uppercase-only short-form ticker tokens.
# Chạy trên RAW text (trước lowercase) để bắt "MB" (2 chữ, regex 3-char miss)
# nhưng tránh false positive với "mb" lowercase trong "miễn bàn", "mb chi".
SHORT_FORM_TO_TICKER = {
    # Special case: 2-char "MB" maps to MBB (legacy alias)
    "MB": "MBB",
    # Bank HOSE
    "VCB": "VCB", "CTG": "CTG", "BID": "BID", "TCB": "TCB", "MBB": "MBB",
    "ACB": "ACB", "VPB": "VPB", "HDB": "HDB", "STB": "STB", "SHB": "SHB",
    "EIB": "EIB", "TPB": "TPB", "MSB": "MSB", "LPB": "LPB", "OCB": "OCB",
    "VIB": "VIB",
    # Bank HNX
    "NAB": "NAB", "BAB": "BAB", "NVB": "NVB", "SGB": "SGB",
    # Bank UPCOM
    "VAB": "VAB", "BVB": "BVB", "ABB": "ABB", "KLB": "KLB", "VBB": "VBB",
    "PGB": "PGB", "HDF": "HDF",
    # CK HOSE
    "SSI": "SSI", "VND": "VND", "HCM": "HCM", "VCI": "VCI", "VIX": "VIX",
    # CK HNX
    "SHS": "SHS", "MBS": "MBS", "BVS": "BVS", "BSI": "BSI", "AGR": "AGR",
    "CTS": "CTS", "APG": "APG", "EVS": "EVS", "IVS": "IVS", "PSI": "PSI",
    "TVS": "TVS", "WSS": "WSS", "ORS": "ORS", "VFS": "VFS", "TCI": "TCI",
    # CK UPCOM
    "DSC": "DSC", "FTS": "FTS", "CSI": "CSI", "SBS": "SBS", "PHS": "PHS",
    "ART": "ART", "APS": "APS", "BMS": "BMS", "AAS": "AAS", "VTS": "VTS",
    # BĐS (unchanged)
    "VHM": "VHM", "NVL": "NVL", "KDH": "KDH", "DXG": "DXG",
    # Oil-Gas (10 mã)
    "GAS": "GAS", "PVD": "PVD", "PVS": "PVS", "PVT": "PVT", "BSR": "BSR",
    "PLX": "PLX", "OIL": "OIL", "DPM": "DPM", "DCM": "DCM", "PVC": "PVC",
}

# Single source of truth: regex derived from dict keys.
# Sort longest-first để match "MBB" trước "MB" khi cả 2 eligible.
TICKER_UPPER_REGEX = re.compile(
    r'\b(' + '|'.join(sorted(SHORT_FORM_TO_TICKER, key=len, reverse=True)) + r')\b'
)


def detect_via_company_name(text: str) -> list[str]:
    """
    Fallback: detect ticker qua tên công ty (lowercase match).
    Cheap heuristic trước khi gọi LLM.
    """
    if not text:
        return []

    text_lower = text.lower()
    found = []
    seen = set()

    for name, ticker in COMPANY_NAME_TO_TICKER.items():
        if name in text_lower and ticker not in seen:
            seen.add(ticker)
            found.append(ticker)

    return found


def detect_short_form_uppercase(text: str) -> list[str]:
    """
    Bug A fix — Pass 2: detect short-form ticker uppercase trên RAW text.

    Bắt "MB" alone (2 chữ — TICKER_PATTERN 3-char miss) cùng các ticker 3-char
    khác. Case-sensitive: "mb" lowercase KHÔNG match (tránh false positive
    với "miễn bàn", "mb chi"...).

    Returns:
        List ticker (đã dedupe, giữ thứ tự xuất hiện). MB → MBB.
    """
    if not text:
        return []

    seen = set()
    result = []
    for match in TICKER_UPPER_REGEX.finditer(text):
        ticker = SHORT_FORM_TO_TICKER[match.group(1)]
        if ticker not in seen:
            seen.add(ticker)
            result.append(ticker)
    return result


def detect_combined(text: str) -> list[str]:
    """
    Combined detection: regex 3-char + uppercase short-form (Pass 2) + company name.
    Dedupe + giữ priority: 3-char regex → uppercase short-form → company name.
    """
    by_regex = detect_tickers(text)
    by_short_upper = detect_short_form_uppercase(text)  # Bug A fix
    by_name = detect_via_company_name(text)

    seen = set()
    result = []

    for source in (by_regex, by_short_upper, by_name):
        for t in source:
            if t not in seen:
                seen.add(t)
                result.append(t)

    return result


# Test
if __name__ == "__main__":
    sample = """
    Vietcombank (VCB) vừa công bố kết quả kinh doanh quý 3, 
    trong khi đó Techcombank cũng có thông báo. TCB và VCB là 2 ngân hàng lớn.
    """
    
    print("Regex only:", detect_tickers(sample))
    print("With position:", detect_tickers_with_position(sample))
    print("Mentions VCB:", count_ticker_mentions(sample, "VCB"))
    print("Company names:", detect_via_company_name(sample))
    print("Combined:", detect_combined(sample))
