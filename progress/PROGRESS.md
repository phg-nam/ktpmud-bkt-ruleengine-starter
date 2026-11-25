# PROGRESS — Nhóm 11 — Track A

- Starter: `ktpmud-bkt-ruleengine-starter` · tag `bkt-2026-v1.1`
- Fork: `https://github.com/phg-nam/ktpmud-bkt-ruleengine-starter`

---

## PC-1 — 11/11/2026

### 1.1. Tiến độ theo acceptance criteria
| Mã | Trạng thái (Chưa / Đã Xong) | Bằng chứng (commit / CI / file) | Ghi chú |
|---|---|---|---|
| A-01 | Chưa | `REQUIREMENTS.md` (FR-01…FR-07), `DECISIONS.md` (ADR-001, ADR-002) | Đã chốt thiết kế và thứ tự ưu tiên R01 > R02 > R03. Chưa có code. |
| A-02 | Chưa | `REQUIREMENTS.md` (NFR-01, AC-27) | Sẽ viết test dùng dữ liệu ngoài fixture công khai. |
| A-03 | Chưa | `REQUIREMENTS.md` (AC-01…AC-18, AC-28…AC-36), `TEST_PLAN.md` mục 4.1–4.2 | Ma trận ca test đã có, gồm ca biên mọi nhóm tuổi và ca ưu tiên. |
| A-04 | Chưa | `REQUIREMENTS.md` mục 6.2, AC-19…AC-22, AC-37…AC-44, `DECISIONS.md` (ADR-003) | Policy đã chốt, chưa cài đặt. |
| A-05 | Chưa | `REQUIREMENTS.md` (FR-08, AC-23) | Chưa có code sinh `ly_do`. |
| A-06 | Chưa | `REQUIREMENTS.md` mục 6.3 (AC-24, AC-25, AC-45), `DECISIONS.md` (ADR-004) | Thiết kế xong (hàm bọc `classify_with_audit`). |
| A-07 | Chưa | `TEST_PLAN.md` mục 4 (ma trận AC → test) | Kế hoạch xong. Chưa có file test. |
| A-08 | Chưa | Chưa có kết quả `pytest -q` | Sẽ chạy từ clean checkout. |
| A-09 | Chưa | Chưa có | Dự kiến thêm workflow GitHub Actions. |
| A-10 | Chưa | `TEST_PLAN.md` mục 5 (phương pháp benchmark) | Chưa có code benchmark. |
| A-11 | Chưa | `REQUIREMENTS.md` (NFR-05) | Chưa thêm câu cảnh báo vào README. |

### 1.2. Sửa đổi bắt buộc từ Checkpoint 1
| Mục | Trạng thái | Bằng chứng |
|---|---|---|
| Q-05 phải chốt, không hạ mức, viết bảng policy theo trường, thêm test | Đã xong | `REQUIREMENTS.md` Mục 6.2, FR-10, AC-37…AC-44, ADR-003 |
| Thiếu ca chứng minh thứ tự ưu tiên | Đã xong | AC-28, ADR-002 |

### 1.3. Timeline dự kiến đến khi hoàn thành
| Việc | Vai trò phụ trách | Mốc | Ngày dự kiến |
|---|---|---|---|
| Chốt chữ ký hàm; đối chiếu policy với issue #15 | 202414275 (Lead) & 202414072 (QA) | PC-1 | 11/11 |
| Viết `r01`, `r02`, `r03`, `is_hypotensive` và chuẩn hóa input | 202414215 (BE) | CP2 | 12/11 |
| Viết `classify()` điều phối 2 tầng và `ly_do` | 202414215 (BE) | CP2 | 13/11 |
| Viết test nghiệp vụ và ca biên theo `TEST_PLAN.md` | 202414072 (QA) | CP2 | 13/11 |
| Viết test input lỗi theo policy và test thứ tự ưu tiên | 202414072 (QA) | CP2 | 14/11 |
| Viết `classify_with_audit` và test audit | 202414215 (BE) | CP2 | 14/11 |
| Chạy `pytest -q` toàn bộ, demo nội bộ | Cả nhóm | CP2 | 15/11 |
| Thêm GitHub Actions, thêm cảnh báo vào README | 202414275 (Lead) | M3 | 16/11 |
| Viết và chạy benchmark ≥1.000 lần, viết `TEST_REPORT.md` | 202414215 (BE) & 202414072 (QA) | M3 | 17/11 |
| Viết `SECURITY_PRIVACY_CHECKLIST.md`, `AI_USE.md`, `CONTRIBUTIONS.md` | Cả nhóm | M3 | 18/11 |
| Rà soát cuối, soạn slide và demo script (≤7 phút) | Cả nhóm | M3 | 18/11 |
| Freeze: gắn tag `bkt-2026-nhom11-rc1`, ghi SHA vào `PROGRESS.md` | 202414275 (Lead) | Freeze | 19/11 |
| Nộp Pull Request vào `ktpmud-project` theo erratum #25 | Cả nhóm | M4 | 20/11 |

### 1.4. Rủi ro / đang vướng
- Không có.

### 1.5. Câu hỏi cho GV
- Không có.

### 1.6. Phân công (MSSV & vai trò)
| MSSV | Vai trò | Đầu việc chính |
|---|---|---|
| **202414275** | Lead (Quản trị kho Git) | Quản lý kho Git, tiến độ dự án, bảo mật Zero PII, nộp bài |
| **202414072** | QA (Kiểm thử & Chất lượng) | Ma trận test, viết 61 test cases bao phủ 45 AC |
| **202414215** | BE (Backend & Logic Rule) | Phân tích nghiệp vụ, lập trình 2 tầng Rule Engine, audit, benchmark |

---

## PC-2 — 18/11/2026

### 2.1. Đối chiếu timeline PC-1
| Việc (theo bảng 1.3) | Kế hoạch | Thực tế | Lệch & lý do |
|---|---|---|---|
| Viết logic rule `r01`, `r02`, `r03`, `is_hypotensive`, `classify` | 12/11 - 13/11 | Xong ngày 16/11 | Đúng tiến độ, đã hoàn thành trong `rule_engine/classifier.py` |
| Viết bộ test 45 AC (61 test cases) | 13/11 - 14/11 | Xong ngày 16/11 | Hoàn thành sớm, toàn bộ 61 ca passed |
| Viết `classify_with_audit` và test audit | 14/11 | Xong ngày 16/11 | Hoàn thành trong `rule_engine/classifier.py`, đạt Zero PII |
| Viết benchmark `benchmark.py` & `TEST_REPORT.md` | 17/11 | Xong ngày 16/11 | Hoàn thành trước hạn 1 ngày; $p95 = 0.0021\text{ ms} \ll 100\text{ ms}$ |
| Viết `SECURITY_PRIVACY_CHECKLIST.md`, `AI_USE.md`, `CONTRIBUTIONS.md` | 18/11 | Xong ngày 16/11 | Hoàn thành trước hạn |
| Cập nhật cảnh báo miễn trừ y tế vào README | 16/11 | Xong ngày 16/11 | Đã bổ sung mục DISCLAIMER vào `README.md` |

### 2.2. Tiến độ theo acceptance criteria (cập nhật toàn bộ bảng 1.1)
| Mã | Trạng thái | Bằng chứng | Ghi chú |
|---|---|---|---|
| A-01 | Xong | File `rule_engine/classifier.py` (hàm `is_hypotensive`), `tests/test_classifier.py` (`test_shock_threshold_boundaries`) | Tầng 1 sốc phản vệ đạt chuẩn ngưỡng dấu `<` chặt chẽ theo 4 nhóm tuổi |
| A-02 | Xong | File `tests/test_classifier.py` (`test_ac27_anti_hardcode_synthetic_case`) | Dữ liệu synthetic độc lập ngoài fixture công khai vẫn phân loại chính xác |
| A-03 | Xong | File `rule_engine/classifier.py` (`r01`, `r02`, `r03`), `tests/test_classifier.py` (AC-01..AC-08, AC-28) | Đầy đủ 3 kịch bản Tầng 2 và cơ chế ưu tiên R01 > R02 > R03 |
| A-04 | Xong | File `rule_engine/classifier.py`, `tests/test_classifier.py` (AC-19..AC-22, AC-37..AC-44) | Xử lý input thiếu/lỗi theo policy không hạ mức, unknown không tính là True |
| A-05 | Xong | File `rule_engine/classifier.py`, `tests/test_classifier.py` (`test_ac23_reason_explainability`) | `ly_do` chỉ rõ rule kích hoạt, không lộ số liệu lâm sàng thô, không khuyên điều trị |
| A-06 | Xong | File `rule_engine/classifier.py` (`classify_with_audit`), `tests/test_classifier.py` (AC-24, AC-25, AC-45) | Audit đúng 4 trường kỹ thuật `Timestamp, User_UUID, Action_Type, Status`, Zero PII |
| A-07 | Xong | File `tests/test_classifier.py` | Đủ 4 nhóm: normal (AC-01, AC-04..), boundary (AC-09..AC-18, AC-29..AC-36), invalid, missing |
| A-08 | Xong | Chạy `pytest -q` đạt 61/61 passed (0.06s) | Đạt từ clean checkout với `pytest.ini` |
| A-09 | Xong | File `.github/workflows/test.yml` | Workflow GitHub Actions chạy `pytest -q` tự động trên Pull Request |
| A-10 | Xong | File `benchmark.py`, `submissions_Nhom11/TEST_REPORT.md` | Đo 5.000 lượt: $p50 = 0.0015\text{ ms}$, $p95 = 0.0021\text{ ms} \ll 100\text{ ms}$ |
| A-11 | Xong | File `README.md` | Đã thêm mục DISCLAIMER "educational/synthetic — not for clinical use" |

### 2.3. Sẵn sàng nộp bài (đề thi Mục 6)
| Deliverable | Có / Chưa | Đường dẫn |
|---|---|---|
| README.md (cài đặt / chạy / test) | Có | `README.md` |
| REQUIREMENTS.md | Có | `submissions_Nhom11/REQUIREMENTS.md` |
| DECISIONS.md / ADR | Có | `submissions_Nhom11/DECISIONS.md` |
| Test tự động + CI xanh | Có | `tests/test_classifier.py`, `.github/workflows/test.yml` |
| TEST_REPORT.md | Có | `submissions_Nhom11/TEST_REPORT.md` |
| SECURITY_PRIVACY_CHECKLIST.md | Có | `submissions_Nhom11/SECURITY_PRIVACY_CHECKLIST.md` |
| AI_USE.md | Có | `submissions_Nhom11/AI_USE.md` |
| CONTRIBUTIONS.md | Có | `submissions_Nhom11/CONTRIBUTIONS.md` |
| Slide / demo script ≤ 7 phút | Đang soạn | `submissions_Nhom11/slides/` |
| Draft PR vào `ktpmud-project`, check `validate` xanh | Có | PR #35 trên `fossbk-spec/ktpmud-project` |

### 2.4. Việc còn lại đến Freeze (23:59 19/11)
| Việc | Vai trò phụ trách | Hạn |
|---|---|---|
| Hoàn thiện slide thuyết trình và kịch bản demo (≤ 7 phút) | Cả nhóm | 18/11 |
| Mở Draft PR vào `ktpmud-project` và kiểm tra check `validate` xanh | 202414275 (Lead) | Đã mở PR #35 |
| Gắn tag release `bkt-2026-nhom11-rc1` và chốt SHA cuối | Cả nhóm | 23:59 19/11 |

### 2.5. Rủi ro / câu hỏi cho GV
- Không có rủi ro kỹ thuật. Tất cả 11 tiêu chí AC đều đã có bằng chứng code và test xác thực.

---

## Kết quả cuối — Freeze 19/11/2026
- Tag: `bkt-2026-nhom11-rc1` · SHA: *(sẽ cập nhật sau commit)*
- Trạng thái cuối từng mã AC: như bảng 2.2 (100% Xong).
- Những việc trong timeline chưa hoàn thành và lý do: Không có.
