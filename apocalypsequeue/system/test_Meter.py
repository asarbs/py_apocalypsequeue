from system import Meter


class TestMeter:
    def test_simple_meter_to_pixel_conversion(self):
        meter = Meter(1)
        assert 4 == meter.get_pixels()

    def test_addition(self):
        m1 = Meter(2)
        m2 = Meter(3)
        assert Meter(5) == (m1 + m2)

    def test_subtraction(self):
        m1 = Meter(2)
        m2 = Meter(3)
        assert Meter(-1) == (m1 - m2)

    def test_multiplication(self):
        m1 = Meter(2)
        assert Meter(4) == (m1 * 2)

    def test_division(self):
        m1 = Meter(20)
        assert Meter(10) == (m1 / 2)

    def test_power(self):
        m1 = Meter(5)
        assert Meter(25) == (m1 ** 2)

    def test_less_then(self):
        assert Meter(2) < Meter(5)
        assert not(Meter(3) < Meter(2))

    def test_less_or_equal(self):
        assert Meter(2) <= Meter(5)
        assert Meter(5) <= Meter(5)
        assert not(Meter(3) <= Meter(2))

    def test_not_equal(self):
        assert Meter(2) != Meter(3)

    def test_greater_then(self):
        assert Meter(5) > Meter(2)
        assert not(Meter(2) > Meter(3))

    def test_greater_or_equal(self):
        assert Meter(5) >= Meter(2)
        assert Meter(5) >= Meter(5)
        assert not(Meter(2) >= Meter(3))