"""
Unit tests cho module algo_core.
Kiểm tra tính đúng đắn của 9 thuật toán.
"""
import pytest
from app.algo_core.doitien import solve_doi_tien
from app.algo_core.day_con_tang_dai_nhat import solve_day_con_tang
from app.algo_core.nhanmatran import solve_nhan_ma_tran
from app.algo_core.timduongngannhat import solve_shortest_path_dag
from app.algo_core.timkiemrong import solve_bfs
from app.algo_core.timkiemsau import solve_dfs
from app.algo_core.tinhsotohop import solve_combinations
from app.algo_core.xauconchungnhat import solve_xau_con_chung
from app.algo_core.xepbalo import solve_xep_ba_lo


class TestDoiTien:
    def test_basic(self):
        result = solve_doi_tien([1, 5, 10], 11)
        assert result['success'] is True
        assert result['tong_so_to_tien'] == 2

    def test_exact_coin(self):
        result = solve_doi_tien([5, 10], 10)
        assert result['success'] is True
        assert result['tong_so_to_tien'] == 1

    def test_impossible(self):
        result = solve_doi_tien([5, 10], 3)
        assert result['success'] is False


class TestDayConTang:
    def test_basic(self):
        result = solve_day_con_tang([10, 22, 9, 33, 21, 50, 41, 60])
        assert result['success'] is True
        assert len(result['day_con']) == 5

    def test_sorted(self):
        result = solve_day_con_tang([1, 2, 3, 4, 5])
        assert result['success'] is True
        assert result['day_con'] == [1, 2, 3, 4, 5]

    def test_empty(self):
        result = solve_day_con_tang([])
        assert result['success'] is False


class TestNhanMaTran:
    def test_basic(self):
        result = solve_nhan_ma_tran([10, 20, 30, 5])
        assert result['success'] is True
        assert result['chi_phi_nho_nhat'] > 0

    def test_invalid(self):
        result = solve_nhan_ma_tran([])
        assert result['success'] is False


class TestTimDuongNganNhat:
    def test_basic(self):
        edges = [(0, 1, 5), (1, 2, 3), (0, 2, 10)]
        result = solve_shortest_path_dag(3, edges, 0)
        assert result['success'] is True
        assert 'khoang_cach_ngan_nhat' in result


class TestBFS:
    def test_basic(self):
        tree = {"value": 1, "left": {"value": 2}, "right": {"value": 3}}
        result = solve_bfs(tree)
        assert result['success'] is True
        assert result['thu_tu_duyet_BFS'] == [1, 2, 3]

    def test_empty(self):
        result = solve_bfs({})
        assert result['success'] is False


class TestDFS:
    def test_basic(self):
        tree = {"value": 1, "left": {"value": 2}, "right": {"value": 3}}
        result = solve_dfs(tree)
        assert result['success'] is True
        assert result['thu_tu_duyet_DFS'] == [1, 2, 3]

    def test_empty(self):
        result = solve_dfs({})
        assert result['success'] is False


class TestTinhSoToHop:
    def test_basic(self):
        result = solve_combinations(5, 2)
        assert result['success'] is True
        assert result['ket_qua'] == 'C(5, 2) = 10'

    def test_zero(self):
        result = solve_combinations(5, 0)
        assert result['success'] is True
        assert result['ket_qua'] == 'C(5, 0) = 1'

    def test_k_greater_than_n(self):
        result = solve_combinations(3, 5)
        assert result['success'] is False


class TestXauConChung:
    def test_basic(self):
        result = solve_xau_con_chung("ABCBDAB", "BDCABA")
        assert result['success'] is True
        assert result['do_dai_xau_chung'] == 4

    def test_no_common(self):
        result = solve_xau_con_chung("ABC", "XYZ")
        assert result['success'] is True
        assert result['do_dai_xau_chung'] == 0


class TestXepBaLo:
    def test_basic(self):
        result = solve_xep_ba_lo([10, 20, 30], [60, 100, 120], ["A", "B", "C"], 50)
        assert result['success'] is True
        assert result['tong_gia_tri_cao_nhat'] > 0
