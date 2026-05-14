"""Ticker universe constants — Finpath Newsroom V5.1.3 expansion (~139 mã).

Hot-path fallback list for ticker detection when Finpath sectors cache is
unavailable. Source-of-truth at runtime is `lib/finpath_sectors.py` reading
from data/pipeline.db cache + Finpath /api/stocks/v2/overview refresh; this
module is fallback only.

Extracted from former `lib/headline_scorer.py` (V5.1.8 Master self-title
refactor) so `lib/quality_gates.py` can keep its ticker check without
depending on the deleted scorer module.
"""

from __future__ import annotations

# Universe — synced with lib/finpath_sectors (139 tickers V5.1.3 cached).
ALL_TICKERS: list[str] = [
    # Bank 27
    "VCB", "CTG", "BID", "TCB", "MBB", "ACB", "VPB", "HDB",
    "STB", "SHB", "EIB", "TPB", "MSB", "LPB", "OCB", "VIB",
    "NAB", "BAB", "NVB", "SGB",
    "VAB", "BVB", "ABB", "KLB", "VBB", "PGB", "HDF",
    # CK 30
    "SSI", "VND", "HCM", "VCI", "VIX",
    "SHS", "MBS", "BVS", "BSI", "AGR", "CTS", "APG", "EVS",
    "IVS", "PSI", "TVS", "WSS", "ORS", "VFS", "TCI",
    "DSC", "FTS", "CSI", "SBS", "PHS", "ART", "APS", "BMS", "AAS", "VTS",
    # BĐS 4
    "VHM", "NVL", "KDH", "DXG",
    # V5.1.3 expansion — 7 new sectors
    "BSR", "PVS", "GAS", "POW", "PLX", "OIL", "PVD", "PVT",  # oilgas
    "GMD", "HAH", "VOS", "VSC", "PHP", "CDN", "HAX",  # logistics
    "VNM", "MSN", "SAB", "BHN", "KDC", "MCM", "QNS",  # fb
    "TCM", "MSH", "TNG",  # apparel
    "MWG", "FRT", "DGW", "PNJ", "AST",  # retail
    "VHC", "ANV", "MPC", "FMC", "IDI", "CMX",  # seafood
    "FPT", "REE", "PC1", "GEX", "ITD", "TRA", "DBD", "IMP", "ELC",  # defensive
    # materialContractor + bds expanded
    "HPG", "HSG", "NKG", "HBC", "CTD", "VCG", "HT1", "BCC", "BCM", "BMP",
    "CII", "DIG", "DPG", "GEG", "HQC", "HPX", "HUT", "IDC", "IJC", "ITA",
    "KBC", "KBS", "KHG", "KSB", "L14", "LCG", "LDG", "NLG", "NTC", "NTL",
    "PDR", "PTB", "SCR", "SIP", "SZC", "SZK", "TCH", "VGC", "VIC", "VIP", "VPI", "VRE",
    # other sectors
    "BWE", "CEO", "DBC", "DXS", "GVR", "HDC", "HDG", "HVN", "NCB", "NGK",
    "NT2", "PAN", "PET", "PGS", "PHR", "PPC", "PVC", "QTP", "SBT", "SCS",
    "SKG", "SMC", "SSB", "TDM", "VCS", "VGT", "VJC", "VTP",
]

GROUP_REFS: list[str] = ["Big4", "Big 4", "tư nhân top", "tư nhân", "Big5", "Big3"]

# Full brand names accepted alongside tickers in title craft + body parsers.
FULL_BRAND_NAMES: list[str] = [
    "Petrolimex",       # PLX
    "PV GAS",           # GAS
    "Vietcombank",      # VCB
    "Techcombank",      # TCB
    "Vietinbank",       # CTG
    "BIDV",             # BID
    "Sacombank",        # STB
    "VPBank",           # VPB
    "MB Bank",          # MBB
    "ACB",              # ACB (also ticker)
    "FPT Telecom",      # subsidiary of FPT
    "PetroVietnam",     # PVN umbrella
    "Vinamilk",         # VNM
    "Masan",            # MSN
    "Vincom",           # VRE
]
