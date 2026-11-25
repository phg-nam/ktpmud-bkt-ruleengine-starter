"""Bo test tu dong 45 Acceptance Criteria (AC-01..AC-45) cho Rule Engine.

Chung minh classify() va classify_with_audit() tuan thu 100% dac ta tai:
- docs/decision-table.md
- submissions_Nhom11/REQUIREMENTS.md (v0.2)
- submissions_Nhom11/TEST_PLAN.md (v0.2)
- submissions_Nhom11/DECISIONS.md (ADR-001..ADR-004)
"""
from __future__ import annotations

import math
import uuid
import pytest

from rule_engine.classifier import classify, classify_with_audit


# ===========================================================================
# 1. TẦNG 2: PHẢN VỆ & THỨ TỰ ƯU TIÊN (AC-01..AC-08, AC-28)
# ===========================================================================

def test_ac01_r01_match():
    """AC-01: Khong nghi di nguyen, da/niem mac +, ho hap +, HATT binh thuong -> PHAN_VE, R01-PV."""
    res = classify({
        "tuoi": 25,
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
        "co_trieu_chung_tuan_hoan": False,
        "huyet_ap_tam_thu": 120,
    })
    assert res["muc_do"] == "PHAN_VE"
    assert res["rule_id"] == "R01-PV"


def test_ac02_r01_digestive_only_not_match():
    """AC-02: Khong nghi di nguyen, da/niem mac +, CHI co tieu hoa -> THEO_DOI (R01 can ho hap hoac tuan hoan)."""
    res = classify({
        "tuoi": 25,
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_tieu_hoa_nang": True,
        "co_trieu_chung_ho_hap": False,
        "co_trieu_chung_tuan_hoan": False,
        "huyet_ap_tam_thu": 120,
    })
    assert res["muc_do"] == "THEO_DOI"
    assert res["rule_id"] is None


def test_ac03_r01_no_skin_not_match():
    """AC-03: Khong nghi di nguyen, da/niem mac -, ho hap + -> THEO_DOI (R01 bat buoc phai co da/niem mac)."""
    res = classify({
        "tuoi": 25,
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": False,
        "co_trieu_chung_ho_hap": True,
        "huyet_ap_tam_thu": 120,
    })
    assert res["muc_do"] == "THEO_DOI"
    assert res["rule_id"] is None


def test_ac04_r02_two_systems():
    """AC-04: Nghi di nguyen, da/niem mac + va tieu hoa + (dung 2 he) -> PHAN_VE, R02-PV."""
    res = classify({
        "tuoi": 30,
        "co_di_nguyen_nghi_ngo": True,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_tieu_hoa_nang": True,
        "co_trieu_chung_ho_hap": False,
        "co_trieu_chung_tuan_hoan": False,
        "huyet_ap_tam_thu": 115,
    })
    assert res["muc_do"] == "PHAN_VE"
    assert res["rule_id"] == "R02-PV"


def test_ac05_r02_one_system_not_match():
    """AC-05: Nghi di nguyen, chi co da/niem mac (1 he) -> THEO_DOI (R02 can it nhat 2/4 he)."""
    res = classify({
        "tuoi": 30,
        "co_di_nguyen_nghi_ngo": True,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": False,
        "co_trieu_chung_tuan_hoan": False,
        "co_trieu_chung_tieu_hoa_nang": False,
        "huyet_ap_tam_thu": 115,
    })
    assert res["muc_do"] == "THEO_DOI"
    assert res["rule_id"] is None


def test_ac06_r03_respiratory_no_inhaled():
    """AC-06: Nghi di nguyen, chi ho hap +, khong hit (di_nguyen_qua_duong_hit=False) -> PHAN_VE, R03-PV."""
    res = classify({
        "tuoi": 20,
        "co_di_nguyen_nghi_ngo": True,
        "di_nguyen_qua_duong_hit": False,
        "co_trieu_chung_ho_hap": True,
        "co_ton_thuong_da_niem_mac": False,
        "co_trieu_chung_tuan_hoan": False,
        "co_trieu_chung_tieu_hoa_nang": False,
        "huyet_ap_tam_thu": 110,
    })
    assert res["muc_do"] == "PHAN_VE"
    assert res["rule_id"] == "R03-PV"


def test_ac07_r03_respiratory_inhaled_not_match():
    """AC-07: Nghi di nguyen, chi ho hap +, CO HIT (di_nguyen_qua_duong_hit=True) -> THEO_DOI (R03 loai tru duong hit)."""
    res = classify({
        "tuoi": 20,
        "co_di_nguyen_nghi_ngo": True,
        "di_nguyen_qua_duong_hit": True,
        "co_trieu_chung_ho_hap": True,
        "co_ton_thuong_da_niem_mac": False,
        "co_trieu_chung_tuan_hoan": False,
        "co_trieu_chung_tieu_hoa_nang": False,
        "huyet_ap_tam_thu": 110,
    })
    assert res["muc_do"] == "THEO_DOI"
    assert res["rule_id"] is None


def test_ac08_r03_circulatory():
    """AC-08: Nghi di nguyen, chi tuan hoan + -> PHAN_VE, R03-PV."""
    res = classify({
        "tuoi": 20,
        "co_di_nguyen_nghi_ngo": True,
        "co_trieu_chung_tuan_hoan": True,
        "co_ton_thuong_da_niem_mac": False,
        "co_trieu_chung_ho_hap": False,
        "co_trieu_chung_tieu_hoa_nang": False,
        "huyet_ap_tam_thu": 110,
    })
    assert res["muc_do"] == "PHAN_VE"
    assert res["rule_id"] == "R03-PV"


def test_ac28_priority_r02_before_r03():
    """AC-28: Dong thoi thoa man ca R02 va R03, khong tut HA -> PHAN_VE, R02-PV (uu tien R02 > R03 theo ADR-002)."""
    # Nghi di nguyen (True)
    # Ho hap (khong hit) + Tuan hoan -> Thoa R03
    # Dong thoi co 2 he (ho hap, tuan hoan) -> Thoa R02
    res = classify({
        "tuoi": 25,
        "co_di_nguyen_nghi_ngo": True,
        "di_nguyen_qua_duong_hit": False,
        "co_trieu_chung_ho_hap": True,
        "co_trieu_chung_tuan_hoan": True,
        "co_ton_thuong_da_niem_mac": False,
        "co_trieu_chung_tieu_hoa_nang": False,
        "huyet_ap_tam_thu": 120,
    })
    assert res["muc_do"] == "PHAN_VE"
    assert res["rule_id"] == "R02-PV"


# ===========================================================================
# 2. TẦNG 1: SỐC PHẢN VỆ, CA BIÊN & CHUYỂN NHÓM TUỔI (AC-09..AC-18, AC-29..AC-36)
# ===========================================================================

@pytest.mark.parametrize(
    "tuoi, hatt, hatt_nen, expected_muc_do, ac_id",
    [
        (0.5, 69, None, "SOC_PHAN_VE", "AC-09: 0.5t HATT 69 < 70"),
        (0.5, 70, None, "PHAN_VE", "AC-10: 0.5t HATT 70 khong < 70"),
        (5.0, 79, None, "SOC_PHAN_VE", "AC-11: 5t HATT 79 < 70+2*5=80"),
        (5.0, 80, None, "PHAN_VE", "AC-12: 5t HATT 80 khong < 80"),
        (11.0, 89, None, "SOC_PHAN_VE", "AC-13: 11t HATT 89 < 90"),
        (11.0, 90, None, "PHAN_VE", "AC-14: 11t HATT 90 khong < 90"),
        (18.0, 89, None, "SOC_PHAN_VE", "AC-15: 18t HATT 89 < 90"),
        (18.0, 90, None, "PHAN_VE", "AC-16: 18t HATT 90 khong < 90"),
        (40.0, 104, 150, "SOC_PHAN_VE", "AC-17: 40t giam 30.67% > 30% (104 < 105)"),
        (40.0, 105, 150, "PHAN_VE", "AC-18: 40t giam dung 30% (105 khong < 105)"),
    ],
)
def test_shock_threshold_boundaries(tuoi, hatt, hatt_nen, expected_muc_do, ac_id):
    """Test cac ca bien tieu chi tut huyet ap Tang 1 theo AC-09..AC-18."""
    # Data nen thoa man R01: khong di nguyen, da +, ho hap +
    patient = {
        "tuoi": tuoi,
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
        "huyet_ap_tam_thu": hatt,
    }
    if hatt_nen is not None:
        patient["huyet_ap_tam_thu_nen"] = hatt_nen

    res = classify(patient)
    assert res["muc_do"] == expected_muc_do, f"Fail tai {ac_id}"
    if expected_muc_do == "SOC_PHAN_VE":
        assert res["rule_id"] == "R-SOC"
    else:
        assert res["rule_id"] == "R01-PV"


@pytest.mark.parametrize(
    "tuoi, hatt, hatt_nen, expected_muc_do, ac_id",
    [
        (0.99, 71, None, "PHAN_VE", "AC-29: 0.99t dung cong thuc <1t (nguong 70 -> 71 k tut)"),
        (1.0, 71, None, "SOC_PHAN_VE", "AC-30: 1.0t dung cong thuc 1-<11t (nguong 70+2*1=72 -> 71 tut)"),
        (1.0, 72, None, "PHAN_VE", "AC-31: 1.0t nguong 72 -> 72 khong < 72"),
        (10.9, 91, None, "SOC_PHAN_VE", "AC-32: 10.9t nguong 70+2*10.9=91.8 -> 91 tut"),
        (10.9, 92, None, "PHAN_VE", "AC-33: 10.9t nguong 91.8 -> 92 khong < 91.8"),
        (11.0, 91, None, "PHAN_VE", "AC-34: 11.0t nguong <90 -> 91 khong < 90"),
        (17.9, 100, 150, "PHAN_VE", "AC-35: 17.9t chi xet <90, KHONG dung tieu chi nen 30%"),
        (18.0, 100, 150, "SOC_PHAN_VE", "AC-36: 18.0t giam 33.3% > 30% -> SOC"),
    ],
)
def test_shock_age_group_transitions(tuoi, hatt, hatt_nen, expected_muc_do, ac_id):
    """Test cac cap ranh gioi chuyen giao giua cac nhom tuoi lien ke (AC-29..AC-36)."""
    patient = {
        "tuoi": tuoi,
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
        "huyet_ap_tam_thu": hatt,
    }
    if hatt_nen is not None:
        patient["huyet_ap_tam_thu_nen"] = hatt_nen

    res = classify(patient)
    assert res["muc_do"] == expected_muc_do, f"Fail tai {ac_id}"


# ===========================================================================
# 3. INPUT THIẾU, SAI KIỂU, POLICY KHÔNG HẠ MỨC (AC-19..AC-22, AC-37..AC-44)
# ===========================================================================

def test_ac19_missing_age():
    """AC-19: Thieu tuoi hoac tuoi=None -> THEO_DOI, khong bao loi (Q-02)."""
    res = classify({
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
        "huyet_ap_tam_thu": 120,
    })
    assert res["muc_do"] == "THEO_DOI"
    assert res["rule_id"] is None


def test_ac20_missing_bp_after_match():
    """AC-20: Da khop Tang 2, huyet_ap_tam_thu la None -> PHAN_VE (Q-03)."""
    res = classify({
        "tuoi": 25,
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
        "huyet_ap_tam_thu": None,
    })
    assert res["muc_do"] == "PHAN_VE"
    assert res["rule_id"] == "R01-PV"


@pytest.mark.parametrize("invalid_age", [-1, -0.5, "25", True, False, math.nan, math.inf])
def test_ac21_invalid_age(invalid_age):
    """AC-21: Tuoi am, sai kieu (chuoi, bool, nan, inf) -> THEO_DOI, khong crash."""
    res = classify({
        "tuoi": invalid_age,
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
    })
    assert res["muc_do"] == "THEO_DOI"
    assert res["rule_id"] is None


def test_ac22_pii_field_ignored():
    """AC-22: Input chua truong dinh danh la -> khong bi crash, khong anh huong ket qua."""
    res = classify({
        "tuoi": 25,
        "ho_va_ten": "Nguyen Van A",
        "so_cccd": "0123456789",
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
        "huyet_ap_tam_thu": 120,
    })
    assert res["muc_do"] == "PHAN_VE"
    assert res["rule_id"] == "R01-PV"


def test_ac37_missing_bool_no_downgrade():
    """AC-37: Nghi di nguyen, da +, ho hap +, thieu khoa tieu hoa -> PHAN_VE, R02-PV (khong ha muc)."""
    res = classify({
        "tuoi": 25,
        "co_di_nguyen_nghi_ngo": True,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
        # thieu hoan toan khoa 'co_trieu_chung_tieu_hoa_nang'
        "huyet_ap_tam_thu": 120,
    })
    assert res["muc_do"] == "PHAN_VE"
    assert res["rule_id"] == "R02-PV"


def test_ac38_null_inhaled_circulatory_branch():
    """AC-38: Nghi di nguyen, tuan hoan +, di_nguyen_qua_duong_hit la None -> PHAN_VE, R03-PV."""
    res = classify({
        "tuoi": 25,
        "co_di_nguyen_nghi_ngo": True,
        "di_nguyen_qua_duong_hit": None,
        "co_trieu_chung_tuan_hoan": True,
        "co_ton_thuong_da_niem_mac": False,
        "co_trieu_chung_ho_hap": False,
        "huyet_ap_tam_thu": 120,
    })
    assert res["muc_do"] == "PHAN_VE"
    assert res["rule_id"] == "R03-PV"


def test_ac39_null_inhaled_respiratory_branch():
    """AC-39: Nghi di nguyen, chi ho hap +, di_nguyen_qua_duong_hit la None -> THEO_DOI (chua du du kien de thoa R03)."""
    res = classify({
        "tuoi": 25,
        "co_di_nguyen_nghi_ngo": True,
        "di_nguyen_qua_duong_hit": None,
        "co_trieu_chung_ho_hap": True,
        "co_ton_thuong_da_niem_mac": False,
        "co_trieu_chung_tuan_hoan": False,
        "co_trieu_chung_tieu_hoa_nang": False,
        "huyet_ap_tam_thu": 120,
    })
    assert res["muc_do"] == "THEO_DOI"
    assert res["rule_id"] is None


def test_ac40_missing_suspected_allergen():
    """AC-40: co_di_nguyen_nghi_ngo thieu hoac None, du cac trieu chung khac -> THEO_DOI."""
    res = classify({
        "tuoi": 25,
        "co_di_nguyen_nghi_ngo": None,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
        "huyet_ap_tam_thu": 120,
    })
    assert res["muc_do"] == "THEO_DOI"
    assert res["rule_id"] is None


@pytest.mark.parametrize("wrong_bool", ["true", "False", 1, 0, 1.0, [True]])
def test_ac41_wrong_type_bool(wrong_bool):
    """AC-41: Truong bool nhan chuoi hoac so (sai kieu) -> khong crash, khong tinh la True."""
    res = classify({
        "tuoi": 25,
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": wrong_bool,  # khong phai bool chuan
        "co_trieu_chung_ho_hap": True,
        "huyet_ap_tam_thu": 120,
    })
    assert res["muc_do"] == "THEO_DOI"
    assert res["rule_id"] is None


@pytest.mark.parametrize("invalid_bp", [-10, 0, "90", 85.5])
def test_ac42_invalid_bp_after_match(invalid_bp):
    """AC-42: HATT am, 0 hoac sai kieu, da khop Tang 2 -> coi nhu khong do duoc, tra PHAN_VE."""
    res = classify({
        "tuoi": 25,
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
        "huyet_ap_tam_thu": invalid_bp,
    })
    assert res["muc_do"] == "PHAN_VE"
    assert res["rule_id"] == "R01-PV"


def test_ac43_missing_baseline_adult():
    """AC-43: Tuoi >= 18, nen thieu, HATT=100 (chua <90), da khop Tang 2 -> PHAN_VE (Q-04)."""
    res = classify({
        "tuoi": 40,
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_ho_hap": True,
        "huyet_ap_tam_thu": 100,
        "huyet_ap_tam_thu_nen": None,
    })
    assert res["muc_do"] == "PHAN_VE"
    assert res["rule_id"] == "R01-PV"


@pytest.mark.parametrize("non_dict", [None, [], "patient", 123])
def test_ac44_non_dict_input(non_dict):
    """AC-44: Input khong phai dict -> THEO_DOI, khong crash."""
    res = classify(non_dict)  # type: ignore
    assert res["muc_do"] == "THEO_DOI"
    assert res["rule_id"] is None


# ===========================================================================
# 4. GIẢI THÍCH, AUDIT TRAIL, ANTI-HARDCODE (AC-23..AC-27, AC-45)
# ===========================================================================

def test_ac23_reason_explainability():
    """AC-23: ly_do phai neu rule kich hoat, khong chua so lieu lam sang tho, khong khuyen dieu tri."""
    res = classify({
        "tuoi": 30,
        "co_di_nguyen_nghi_ngo": True,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_tieu_hoa_nang": True,
        "huyet_ap_tam_thu": 80,  # tut HA nguoi lon (<90)
    })
    assert res["muc_do"] == "SOC_PHAN_VE"
    assert "R02-PV" in res["ly_do"] or "R-SOC" in res["ly_do"]
    # Khong chua du lieu tho: tuoi, huyet ap
    assert "30" not in res["ly_do"]
    assert "80" not in res["ly_do"]
    # Khong co loi khuyen dieu tri
    for forbidden_word in ["tiem", "thuoc", "adrenaline", "epinephrine", "lieu"]:
        assert forbidden_word not in res["ly_do"].lower()


def test_ac24_audit_four_fields():
    """AC-24: classify_with_audit sinh dung 1 record co dung 4 khoa."""
    sink = []
    test_uuid = str(uuid.uuid4())
    classify_with_audit(
        {
            "tuoi": 25,
            "co_di_nguyen_nghi_ngo": False,
            "co_ton_thuong_da_niem_mac": True,
            "co_trieu_chung_ho_hap": True,
            "huyet_ap_tam_thu": 120,
        },
        user_uuid=test_uuid,
        audit_sink=sink,
    )
    assert len(sink) == 1
    record = sink[0]
    assert set(record.keys()) == {"Timestamp", "User_UUID", "Action_Type", "Status"}
    assert record["Action_Type"] == "CLASSIFY"
    assert record["Status"] == "OK"


def test_ac25_audit_zero_pii():
    """AC-25: Audit khong chua muc_do, rule_id, ly_do hay bat ky gia tri input lam sang nao."""
    sink = []
    test_uuid = str(uuid.uuid4())
    patient = {
        "tuoi": 25,
        "co_di_nguyen_nghi_ngo": True,
        "co_ton_thuong_da_niem_mac": True,
        "huyet_ap_tam_thu": 120,
    }
    classify_with_audit(patient, user_uuid=test_uuid, audit_sink=sink)
    record = sink[0]

    # Khong co cac khoa ket qua
    for k in ["muc_do", "rule_id", "ly_do", "tuoi", "huyet_ap_tam_thu"]:
        assert k not in record


def test_ac45_audit_uuid_validation():
    """AC-45: User_UUID dung gia tri truyen vao; UUID khong hop le -> ValueError va khong ghi record."""
    sink = []
    valid_uuid = "12345678-1234-5678-1234-567812345678"
    classify_with_audit(
        {"tuoi": 20, "co_di_nguyen_nghi_ngo": False},
        user_uuid=valid_uuid,
        audit_sink=sink,
    )
    assert sink[0]["User_UUID"] == valid_uuid

    # UUID sai
    with pytest.raises(ValueError):
        classify_with_audit(
            {"tuoi": 20, "co_di_nguyen_nghi_ngo": False},
            user_uuid="invalid-uuid-string",
            audit_sink=sink,
        )
    # So luong record van chi la 1 (khong ghi them ban ghi moi)
    assert len(sink) == 1


def test_ac27_anti_hardcode_synthetic_case():
    """AC-27: Test voi du lieu synthetic da dang khong co trong fixture mau."""
    # Mot ca synthetic dac thu: benh nhan cao tuoi 88.5 tuoi, di nguyen khong ro, ton thuong da + ngat
    res = classify({
        "tuoi": 88.5,
        "co_di_nguyen_nghi_ngo": False,
        "co_ton_thuong_da_niem_mac": True,
        "co_trieu_chung_tuan_hoan": True,
        "co_trieu_chung_ho_hap": False,
        "huyet_ap_tam_thu": 88,  # <90 o nguoi lon
    })
    assert res["muc_do"] == "SOC_PHAN_VE"
    assert res["rule_id"] == "R-SOC"
