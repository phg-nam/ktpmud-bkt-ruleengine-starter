"""Rule Engine WAO/EAACI - BKT-1 (Track A), mon KTPMUD.

Hien thuc ham classify() va classify_with_audit() theo dac ta:
- docs/decision-table.md
- submissions_Nhom11/REQUIREMENTS.md (v0.2)
- submissions_Nhom11/DECISIONS.md (ADR-001..ADR-004)
"""
from __future__ import annotations

import datetime
import math
import uuid
from typing import Any, Dict, List, Optional, Tuple, TypedDict


class PatientInput(TypedDict, total=False):
    """Input theo dung Data Dictionary trong docs/decision-table.md."""
    tuoi: float
    huyet_ap_tam_thu: Optional[int]
    huyet_ap_tam_thu_nen: Optional[int]
    co_di_nguyen_nghi_ngo: bool
    di_nguyen_qua_duong_hit: bool
    co_ton_thuong_da_niem_mac: bool
    co_trieu_chung_ho_hap: bool
    co_trieu_chung_tuan_hoan: bool
    co_trieu_chung_tieu_hoa_nang: bool


class ClassificationResult(TypedDict):
    """Dinh dang ket qua phan loai bat buoc cua dac ta."""
    muc_do: str  # "SOC_PHAN_VE" | "PHAN_VE" | "THEO_DOI"
    rule_id: Optional[str]  # "R-SOC" | "R01-PV" | "R02-PV" | "R03-PV" | None
    ly_do: str


class AuditRecord(TypedDict):
    """Ban ghi audit toi thieu 4 truong, Zero PII theo A-06 va ADR-004."""
    Timestamp: str
    User_UUID: str
    Action_Type: str
    Status: str


# ---------------------------------------------------------------------------
# Helper kiem tra kieu va tinh hop le (ADR-003: Policy input khong dung duoc)
# ---------------------------------------------------------------------------

def _is_valid_bool(val: Any) -> bool:
    """Chi chap nhan dung kieu bool (True/False), loai tru chuoi 'true', so 0/1."""
    return type(val) is bool


def _is_valid_age(val: Any) -> bool:
    """Tuoi phai la so thuc/nguyen huu han >= 0 va khong phai bool."""
    if _is_valid_bool(val):
        return False
    if isinstance(val, (int, float)):
        return math.isfinite(val) and val >= 0.0
    return False


def _is_valid_systolic_bp(val: Any) -> bool:
    """HATT phai la so nguyen duong > 0 va khong phai bool."""
    if _is_valid_bool(val):
        return False
    if isinstance(val, int) and not isinstance(val, bool):
        return val > 0
    return False


# ---------------------------------------------------------------------------
# Cac ham thuan danh gia tung rule (ADR-001)
# ---------------------------------------------------------------------------

def r01(
    co_di_nguyen_nghi_ngo: Optional[bool],
    co_ton_thuong_da_niem_mac: Optional[bool],
    co_trieu_chung_ho_hap: Optional[bool],
    co_trieu_chung_tuan_hoan: Optional[bool],
) -> bool:
    """Kich ban R01 - Khong ro di nguyen.

    Dieu kien: co_di_nguyen_nghi_ngo == False VÀ
               co_ton_thuong_da_niem_mac == True VÀ
               (co_trieu_chung_ho_hap == True HOẶC co_trieu_chung_tuan_hoan == True)
    """
    if co_di_nguyen_nghi_ngo is not False:
        return False
    if co_ton_thuong_da_niem_mac is not True:
        return False
    return (co_trieu_chung_ho_hap is True) or (co_trieu_chung_tuan_hoan is True)


def r02(
    co_di_nguyen_nghi_ngo: Optional[bool],
    co_ton_thuong_da_niem_mac: Optional[bool],
    co_trieu_chung_ho_hap: Optional[bool],
    co_trieu_chung_tuan_hoan: Optional[bool],
    co_trieu_chung_tieu_hoa_nang: Optional[bool],
) -> bool:
    """Kich ban R02 - Di nguyen nghi ngo, >=2 trong 4 he co quan.

    Dieu kien: co_di_nguyen_nghi_ngo == True VÀ
               tong so he dat True >= 2 (da, ho hap, tuan hoan, tieu hoa nang)
    """
    if co_di_nguyen_nghi_ngo is not True:
        return False
    systems = [
        co_ton_thuong_da_niem_mac is True,
        co_trieu_chung_ho_hap is True,
        co_trieu_chung_tuan_hoan is True,
        co_trieu_chung_tieu_hoa_nang is True,
    ]
    return sum(systems) >= 2


def r03(
    co_di_nguyen_nghi_ngo: Optional[bool],
    di_nguyen_qua_duong_hit: Optional[bool],
    co_trieu_chung_ho_hap: Optional[bool],
    co_trieu_chung_tuan_hoan: Optional[bool],
) -> bool:
    """Kich ban R03 - Di nguyen da biet.

    Dieu kien: co_di_nguyen_nghi_ngo == True VÀ
               ((di_nguyen_qua_duong_hit == False VÀ co_trieu_chung_ho_hap == True)
                HOẶC co_trieu_chung_tuan_hoan == True)
    """
    if co_di_nguyen_nghi_ngo is not True:
        return False
    respiratory_branch = (di_nguyen_qua_duong_hit is False) and (co_trieu_chung_ho_hap is True)
    circulatory_branch = co_trieu_chung_tuan_hoan is True
    return respiratory_branch or circulatory_branch


def is_hypotensive(
    tuoi: float,
    hatt: Optional[int],
    hatt_nen: Optional[int] = None,
) -> bool:
    """Kiem tra tieu chi tut huyet ap tam thu theo 4 nhom tuoi (Tang 1).

    Nguong so sanh dau < va > chat che theo dac ta:
    - 0 – <1 tuoi: HATT < 70 mmHg
    - 1 – <11 tuoi: HATT < 70 + 2*tuoi (mmHg)
    - 11 – <18 tuoi: HATT < 90 mmHg
    - >=18 tuoi: HATT < 90 mmHg HOAC giam > 30% so voi huyet_ap_tam_thu_nen
    """
    if hatt is None or not _is_valid_systolic_bp(hatt):
        return False

    if tuoi < 1.0:
        return hatt < 70
    elif tuoi < 11.0:
        threshold = 70.0 + 2.0 * float(tuoi)
        return float(hatt) < threshold
    elif tuoi < 18.0:
        return hatt < 90
    else:
        # Nguoi lon: tuoi >= 18
        if hatt < 90:
            return True
        if hatt_nen is not None and _is_valid_systolic_bp(hatt_nen):
            # Giam > 30% so voi nen nghia la: hatt < hatt_nen * 0.70
            # Dau so sanh nghiem ngat: giam dung 30% (hatt == hatt_nen * 0.7) KHONG coi la tut
            return float(hatt) < (float(hatt_nen) * 0.70)
        return False


# ---------------------------------------------------------------------------
# Ham dieu phoi chinh (classify)
# ---------------------------------------------------------------------------

def classify(patient: PatientInput) -> ClassificationResult:
    """Phan loai muc do theo docs/decision-table.md va ADR-001..ADR-003.

    - Q-02: Thieu hoac sai tuoi -> THEO_DOI, rule_id = null
    - Tang 2 xet truoc: R01 > R02 > R03 (ADR-002, issue #15)
    - Neu khop Tang 2: xet tiep Tang 1 (tut huyet ap theo tuoi)
      + Tut HA -> SOC_PHAN_VE, rule_id = "R-SOC"
      + Khong tut HA (hoac thieu HA) -> PHAN_VE, giu rule_id cua Tang 2
    - Khong khop Tang 2 -> THEO_DOI, rule_id = null
    """
    # 1. Kiem tra input co phai dict
    if not isinstance(patient, dict):
        return {
            "muc_do": "THEO_DOI",
            "rule_id": None,
            "ly_do": "Du lieu dau vao khong dung dinh dang doi tuong.",
        }

    # 2. Xu ly truong tuoi (Q-02, AC-19, AC-21)
    raw_age = patient.get("tuoi")
    if raw_age is None or not _is_valid_age(raw_age):
        return {
            "muc_do": "THEO_DOI",
            "rule_id": None,
            "ly_do": "Chua du du kien ket luan: thieu hoac sai thong tin tuoi benh nhan.",
        }
    tuoi = float(raw_age)

    # 3. Chuan hoa cac truong boolean theo policy khong ha muc (ADR-003)
    # Neu thieu hoac sai kieu thi coi la None (unknown), khong bao gio tinh la True
    def get_clean_bool(key: str) -> Optional[bool]:
        val = patient.get(key)
        return val if _is_valid_bool(val) else None

    co_di_nguyen_nghi_ngo = get_clean_bool("co_di_nguyen_nghi_ngo")
    di_nguyen_qua_duong_hit = get_clean_bool("di_nguyen_qua_duong_hit")
    co_ton_thuong_da_niem_mac = get_clean_bool("co_ton_thuong_da_niem_mac")
    co_trieu_chung_ho_hap = get_clean_bool("co_trieu_chung_ho_hap")
    co_trieu_chung_tuan_hoan = get_clean_bool("co_trieu_chung_tuan_hoan")
    co_trieu_chung_tieu_hoa_nang = get_clean_bool("co_trieu_chung_tieu_hoa_nang")

    # Chuan hoa huyet ap
    raw_hatt = patient.get("huyet_ap_tam_thu")
    hatt = raw_hatt if _is_valid_systolic_bp(raw_hatt) else None

    raw_hatt_nen = patient.get("huyet_ap_tam_thu_nen")
    hatt_nen = raw_hatt_nen if _is_valid_systolic_bp(raw_hatt_nen) else None

    # 4. Danh gia Tang 2 (Phan ve) theo thu tu uu tien: R01 > R02 > R03 (ADR-002)
    matched_tang2_rule: Optional[str] = None
    tang2_reason: Optional[str] = None

    if r01(
        co_di_nguyen_nghi_ngo,
        co_ton_thuong_da_niem_mac,
        co_trieu_chung_ho_hap,
        co_trieu_chung_tuan_hoan,
    ):
        matched_tang2_rule = "R01-PV"
        tang2_reason = "Thoa man tieu chi phan ve kich ban R01: khong ro di nguyen, co ton thuong da niem mac va trieu chung ho hap hoac tuan hoan."
    elif r02(
        co_di_nguyen_nghi_ngo,
        co_ton_thuong_da_niem_mac,
        co_trieu_chung_ho_hap,
        co_trieu_chung_tuan_hoan,
        co_trieu_chung_tieu_hoa_nang,
    ):
        matched_tang2_rule = "R02-PV"
        tang2_reason = "Thoa man tieu chi phan ve kich ban R02: co di nguyen nghi ngo va ton thuong tu 2 he co quan tro len."
    elif r03(
        co_di_nguyen_nghi_ngo,
        di_nguyen_qua_duong_hit,
        co_trieu_chung_ho_hap,
        co_trieu_chung_tuan_hoan,
    ):
        matched_tang2_rule = "R03-PV"
        tang2_reason = "Thoa man tieu chi phan ve kich ban R03: co di nguyen da biet va bieu hien trieu chung ho hap khong qua duong hit hoac tuan hoan."

    # Neu khong khop bat ky rule nao cua Tang 2 -> THEO_DOI
    if matched_tang2_rule is None:
        return {
            "muc_do": "THEO_DOI",
            "rule_id": None,
            "ly_do": "Chua du du kien ket luan: khong thoa man cac kich ban phan ve cua bang quyet dinh.",
        }

    # 5. Danh gia Tang 1 (Soc phan ve) khi da khop Tang 2
    if is_hypotensive(tuoi, hatt, hatt_nen):
        return {
            "muc_do": "SOC_PHAN_VE",
            "rule_id": "R-SOC",
            "ly_do": f"Thoa man tieu chi phan ve kich ban {matched_tang2_rule} kem theo tut huyet ap tam thu theo do tuoi.",
        }

    # Neu khong tut huyet ap hoac huyet ap null -> Tra ve PHAN_VE
    return {
        "muc_do": "PHAN_VE",
        "rule_id": matched_tang2_rule,
        "ly_do": tang2_reason,
    }


# ---------------------------------------------------------------------------
# Ham boc ghi Audit Trail (A-06, ADR-004)
# ---------------------------------------------------------------------------

_GLOBAL_AUDIT_SINK: List[AuditRecord] = []


def classify_with_audit(
    patient: PatientInput,
    user_uuid: str,
    audit_sink: Optional[List[AuditRecord]] = None,
) -> ClassificationResult:
    """Ham boc goi classify() dong thoi ghi audit trail toi thieu 4 truong.

    - user_uuid bat buoc phai hop le theo chuan UUID (RFC 4122); neu sai nem ValueError.
    - Ban ghi audit gom dung 4 khoa: Timestamp, User_UUID, Action_Type, Status.
    - Zero PII: Tuyet doi khong ghi du lieu lam sang hay muc do chan doan vao log.
    """
    if audit_sink is None:
        audit_sink = _GLOBAL_AUDIT_SINK

    # Kiem tra tinh hop le cua user_uuid
    try:
        val = uuid.UUID(str(user_uuid))
        formatted_uuid = str(val)
    except (ValueError, AttributeError, TypeError):
        raise ValueError(f"User_UUID khong hop le theo chuan UUID: {user_uuid}")

    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

    try:
        result = classify(patient)
        audit_sink.append({
            "Timestamp": timestamp,
            "User_UUID": formatted_uuid,
            "Action_Type": "CLASSIFY",
            "Status": "OK",
        })
        return result
    except Exception as exc:
        audit_sink.append({
            "Timestamp": timestamp,
            "User_UUID": formatted_uuid,
            "Action_Type": "CLASSIFY",
            "Status": "ERROR",
        })
        raise exc
