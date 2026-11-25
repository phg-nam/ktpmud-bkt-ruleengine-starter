# KTPMUD BKT-1 (Track A) — Dr May Day: Rule Engine Sprint (Nhóm 11)

> **DISCLAIMER:** This project is for educational/synthetic purposes only — **NOT FOR CLINICAL USE**.
> Sản phẩm chỉ phục vụ học tập và nghiên cứu với dữ liệu giả lập (synthetic data), không được sử dụng cho mục đích chẩn đoán hay điều trị y tế thực tế.

---

## 1. Giới thiệu

Hệ thống **Rule Engine** hỗ trợ phân loại nguy cơ phản vệ và sốc phản vệ khẩn cấp dựa trên **Bảng quyết định WAO/EAACI V1** ([docs/decision-table.md](docs/decision-table.md)).
Hệ thống vận hành theo nguyên tắc **Zero PII** (bảo mật tuyệt đối, không nhận hay lưu trữ thông tin định danh) và có khả năng giải thích rõ ràng (Explainable).

---

## 2. Cài đặt và Chạy kiểm thử từ Clean Checkout (A-08)

Yêu cầu môi trường: Python 3.9+ (khuyến nghị Python 3.11 hoặc 3.13).

```bash
# 1. Tạo môi trường ảo
python -m venv .venv

# 2. Kích hoạt môi trường ảo
# Trên Windows:
.\.venv\Scripts\activate
# Trên Linux/macOS:
source .venv/bin/activate

# 3. Cài đặt các thư viện phụ thuộc
pip install -r requirements.txt

# 4. Chạy bộ kiểm thử tự động (61 test cases, 45 AC)
pytest -q
```

---

## 3. Chạy đo Hiệu năng (Benchmark Latency - A-10)

Hệ thống cung cấp script đo độ trễ độc lập bằng Python standard library:

```bash
python benchmark.py
```

- **Quy trình:** 200 lượt warm-up + 5.000 lượt đo chính thức bằng `time.perf_counter()`.
- **Kết quả thực tế:** $p50 \approx 0.0015\text{ ms}$, $p95 \approx 0.0021\text{ ms} \ll 100\text{ ms}$ (đạt xuất sắc tiêu chí đề ra).
- Kết quả chi tiết và thông số phần cứng được tự động ghi nhận vào [`submissions_Nhom11/TEST_REPORT.md`](submissions_Nhom11/TEST_REPORT.md).

---

## 4. Cấu trúc Thư mục

- `rule_engine/classifier.py`: Mã nguồn chính chứa logic 2 tầng phân loại (`classify`) và ghi Audit Trail (`classify_with_audit`).
- `tests/test_classifier.py`: Bộ kiểm thử tự động 61 test cases bao phủ toàn diện 45 Acceptance Criteria.
- `benchmark.py`: Script đo đạc hiệu năng và phân vị độ trễ ($p50, p95, p99$).
- `docs/decision-table.md`: Đặc tả bảng quyết định chuẩn WAO/EAACI V1.
- `submissions_Nhom11/`: Toàn bộ hồ sơ báo cáo và tài liệu kỹ thuật của Nhóm 11:
  - `REQUIREMENTS.md`: Tài liệu đặc tả yêu cầu chức năng, phi chức năng và 45 AC.
  - `DECISIONS.md`: Nhật ký quyết định thiết kế kiến trúc (ADR-001 đến ADR-004).
  - `TEST_PLAN.md`: Kế hoạch và ma trận kiểm thử chi tiết.
  - `TEST_REPORT.md`: Báo cáo kết quả kiểm thử tự động và đo lường hiệu năng.
  - `SECURITY_PRIVACY_CHECKLIST.md`: Báo cáo kiểm tra tuân thủ an toàn thông tin và Zero PII.
  - `AI_USE.md`: Báo cáo khai báo minh bạch việc sử dụng công cụ AI.
  - `CONTRIBUTIONS.md`: Bảng phân công và đóng góp của các thành viên.
- `progress/PROGRESS.md`: Nhật ký theo dõi tiến độ qua các mốc kiểm tra (PC-1, PC-2, Freeze).
