# Large-Scale N-Queens Solver: SAT, CP, and ILP Comparative Benchmark

> **Bài tập lớn số 1 — Môn Các vấn đề hiện đại KHMT**  
> Trường Đại học Công nghệ, Đại học Quốc gia Hà Nội (VNU-UET)

---

## 📌 Giới thiệu đề tài (Overview)

Bài toán xếp $N$ quân Hậu ($N$-Queens Problem) là bài toán kinh điển trong lý thuyết tối ưu tổ hợp và lý thuyết ràng buộc: Tìm cách đặt $N$ quân Hậu trên bàn cờ $N \times N$ sao cho không có 2 quân Hậu nào ăn nhau (không cùng hàng, cùng cột hay cùng bất kỳ đường chéo nào).

Dự án này triển khai bộ giải chính xác quy mô lớn ($N \le 100$, tương đương bàn cờ $10.000$ ô cờ) trên 3 trường phái giải toán chính xác hiện đại:
1. **SAT Solving (PySAT)**: Mô hình hóa logic mệnh đề CNF với các bộ giải CDCL hàng đầu: `Glucose 4.0`, `CaDiCaL 1.5.3`, `MiniSat 2.2`.
2. **Constraint Programming (Google OR-Tools CP-SAT)**: Gồm 2 mô hình đối chứng:
   - `CP-AllDiff`: Mô hình 1D số nguyên với 3 ràng buộc toàn cục `AddAllDifferent`.
   - `CP-Boolean`: Mô hình lưới 2D biến nhị phân $0-1$.
3. **Integer Linear Programming (ILP/MIP)**: Mô hình quy hoạch nguyên tuyến tính $0-1$ sử dụng `SCIP` và `CBC`.

---

## 🚀 5 Kỹ thuật mã hóa At-Most-One (AMO) được triển khai

Theo đúng yêu cầu và khuyến khích của giảng viên, dự án cài đặt và đánh giá toàn diện **5 phương pháp mã hóa AMO**:
1. **Pairwise (Naive Quadratic)**: Cấm trực tiếp từng cặp biến $(\neg u \lor \neg v)$, số mệnh đề $O(k^2)$, 0 biến phụ.
2. **Sequential Counter (Sinz 2005)**: Dùng các biến tích lũy phụ, số mệnh đề $O(k)$, $O(k)$ biến phụ.
3. **Bitwise / Binary**: Mã hóa nhị phân chỉ số của literal, số mệnh đề $O(k \log k)$, $O(\log k)$ biến phụ.
4. **Commander Variable (Klieber & Gao 2007)**: Chia nhóm và đệ quy bầu biến chỉ huy, số mệnh đề $O(k)$.
5. **2-Product (Chen 2010)**: Sắp xếp các biến thành lưới ma trận $p \times q$, số mệnh đề chỉ $2k + O(\sqrt{k})$, $2\sqrt{k}$ biến phụ.

---

## 📊 Tóm tắt kết quả thực nghiệm nổi bật

### 1. So sánh giữa các trường phái ($N = 4 \dots 100$)
- **SAT (Glucose4)** và **CP-SAT** giải quyết bàn cờ $100 \times 100$ ($10.000$ ô cờ) cực kỳ nhanh trong **$1.29$ – $2.77$ giây**, đảm bảo nghiệm hợp lệ 100%.
- **ILP (SCIP)** bị **TIMEOUT (> 20 giây)** ở $N = 100$ do tính chất bài toán khi nới lỏng sang LP relaxation bị nghiệm phân số ($x = 1/N$), làm cây nhánh cận bị bùng nổ tổ hợp.

### 2. Khảo sát độ phức tạp mệnh đề (Ablation Study)
- Ở $N = 100$, cách mã hóa `Pairwise` bùng nổ tới **$1.646.900$ mệnh đề**.
- Trong khi đó, kỹ thuật `2-Product` chỉ tốn **$116.636$ mệnh đề** $\rightarrow$ **Giảm tới $92.9\%$ số lượng mệnh đề**, tiết kiệm tối đa bộ nhớ RAM.

---

## 📁 Cấu trúc thư mục (Repository Structure)

```text
├── src/                         # Mã nguồn các solver
│   ├── __init__.py
│   ├── sat_encodings.py         # 5 thuật toán mã hóa AMO + hàm dựng CNF
│   ├── sat_solver.py            # PySAT wrapper (Glucose, CaDiCaL)
│   ├── cp_solver.py             # OR-Tools CP-SAT (AllDiff & Boolean)
│   ├── ilp_solver.py            # OR-Tools MIP solver (SCIP, CBC)
│   └── utils.py                 # Hàm kiểm tra nghiệm & hiển thị bàn cờ
├── experiments/                 # Mã nguồn chạy thực nghiệm & biểu đồ
│   ├── benchmark.py             # Script tự động chạy toàn bộ dải N
│   ├── plot_results.py          # Script vẽ 3 biểu đồ độ phân giải cao 300 DPI
│   └── results/                 # Dữ liệu CSV và ảnh biểu đồ
│       ├── benchmark_solvers.csv
│       ├── benchmark_amo.csv
│       ├── table_solvers.tex
│       ├── table_amo.tex
│       ├── fig1_runtime_comparison.png (.pdf)
│       ├── fig2_clause_growth.png (.pdf)
│       └── fig3_amo_runtime.png (.pdf)
├── paper/                       # Báo cáo khoa học LaTeX chuẩn Elsevier
│   ├── cas-sc.cls               # Elsevier CAS Single-Column class
│   ├── cas-common.sty
│   ├── cas-model2-names.bst
│   ├── main.tex                 # Báo cáo chính thức đầy đủ nội dung
│   ├── references.bib           # Tài liệu tham khảo BibTeX
│   └── figures/                 # Hình ảnh nhúng trong bài báo
├── paper_overleaf.zip           # File ZIP đóng gói sẵn 1-click tải lên Overleaf
├── test_solvers.py              # Script test kiểm thử chéo tất cả các solver (N=8)
├── run_n100.py                  # Script chạy trực tiếp minh họa N=100
└── README.md                    # Hướng dẫn dự án
```

---

## 🛠 Hướng dẫn cài đặt & Chạy thực nghiệm

### 1. Cài đặt môi trường
Yêu cầu Python $\ge 3.10$:
```bash
pip install python-sat ortools matplotlib pandas numpy
```

### 2. Kiểm thử nhanh các solver
```bash
python test_solvers.py
```

### 3. Chạy giải bàn cờ lớn $N = 100$
```bash
python run_n100.py
```

### 4. Tái hiện toàn bộ thực nghiệm & Vẽ biểu đồ
```bash
python experiments/benchmark.py
python experiments/plot_results.py
```

### 5. Biên dịch bài báo LaTeX
- **Cách 1 (Nhanh nhất)**: Tải file `paper_overleaf.zip` lên [Overleaf](https://www.overleaf.com) và nhấn **Recompile**.
- **Cách 2 (Máy có TeX Live / MiKTeX)**:
  ```bash
  cd paper
  pdflatex main
  bibtex main
  pdflatex main
  pdflatex main
  ```

---

## 📜 Trích dẫn & Tài liệu tham khảo
1. Sinz, C. (2005). *Towards an optimal CNF encoding of boolean cardinality constraints*. CP 2005.
2. Klieber, W., & Gao, L. (2007). *A new efficient SAT encoding for at-most-one constraints*. SAT 2007 Workshops.
3. Chen, J. (2010). *A new SAT encoding of the at-most-one constraint*. ISORA 2011.
4. Ignatiev, A., Morgado, A., & Marques-Silva, J. (2018). *PySAT: A Python toolkit for prototyping with SAT oracles*. SAT 2018.
