from fantomatic_engine.generic.vectors import *
import numpy as np


def test_vec2():
    vx = 2.5
    vy = .4
    res = vec2(vx, vy)
    assert isinstance(res, np.ndarray)
    assert len(res) == 2


def test_unit():
    tolerance = 0.0000001
    v = vec2(12, 58.2)
    u_vec = unit(v)
    assert abs(1 - np.sqrt(u_vec.dot(u_vec))) < tolerance


def test_sign_vec():
    assert np.array_equal(sign_vec(vec2(-3.1, 12.1)), (-1, 1))
    assert np.array_equal(sign_vec(vec2(0.0, -5.0)), (0, -1))
    assert np.array_equal(sign_vec(vec2(-0.0, 0.0)), (0, 0))


def test_magnitude():
    v = vec2(13.1, 52.4)
    assert magnitude(v) == sqrt(13.1**2 + 52.4**2)


def test_unit_length():
    assert not has_unit_length(vec2(12, 7))
    assert has_unit_length(vec2(0, 1))
    assert not has_unit_length(vec2(0, 0))
    assert has_unit_length(vec2(-1, 0))
    assert has_unit_length(unit(vec2(32, 78.2)))
    assert has_unit_length(unit(vec2(1, -1)))


def test_nul_float():
    assert float_is_nul(0.0)
    assert float_is_nul(0.00000000000000001)
    assert not float_is_nul(0.00001)
    assert not float_is_nul(5.1)
    assert not float_is_nul(-0.0001)
    assert not float_is_nul(-3.1)
    assert float_is_nul(-0.0000000000000000001)


def test_nul_vec():
    assert vec_is_nul(vec2())
    assert vec_is_nul(vec2(0.000000000001, 0.0000000000000001))
    assert not vec_is_nul(vec2(-1, -0.01))
    assert not vec_is_nul(vec2(0.001, 0.001))


def test_normal_vecs():
    v = vec2(12.2, -0.002)
    assert np.array_equal(normal_vecs(v)[0], (0.002, 12.2))
    assert np.array_equal(normal_vecs(v)[1], (-0.002, -12.2))
    v = vec2()
    assert np.array_equal(normal_vecs(v)[0], (0, 0))
    assert np.array_equal(normal_vecs(v)[1], (0, 0))
    v = vec2(0, 1)
    assert np.array_equal(normal_vecs(v)[0], (-1, 0))
    assert np.array_equal(normal_vecs(v)[1], (1, 0))


def test_vecs_list_add():
    v1 = vec2(.2, .5)
    v2 = vec2(5, 3)
    v3 = vec2(1, -1)
    vecs = [v1, v2, v3]
    addition = vecs_addition(vecs)
    assert np.array_equal(addition, v1 + v2 + v3)
    assert np.array_equal(addition, (6.2, 2.5))


def test_vec_is_in_list():
    v1 = vec2(.2, .5)
    v2 = vec2(5, 3)
    v3 = vec2(1, -1)
    vecs = [v1, v2, v3]
    assert vec_is_in_list((.2, .5), vecs)
    assert vec_is_in_list(v2, vecs)
    assert not vec_is_in_list((-2, 3), vecs)


def test_random_point_in_area():
    area = [10, 50, 300, 125]
    random_point = random_point_in_area(area)
    assert 10 <= random_point[0] <= 300 + 10
    assert 50 <= random_point[1] <= 300 + 125
