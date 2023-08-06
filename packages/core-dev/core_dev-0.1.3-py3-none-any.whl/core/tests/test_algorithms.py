

import pytest

# pip install pytest_cases
from pytest_cases import parametrize_with_cases
from pytest_cases import THIS_MODULE
from pytest_cases import parametrize as parametrize_testcase


# pip install pytest_steps
from pytest_steps.steps import test_steps


from _core.algorithms import float_eq
@pytest.mark.parametrize("x, y", [
    (.1 *3, .3),
])
def test_float_eq_returns_true(x: float, y: float):
    assert float_eq(x, y) == True


@pytest.mark.parametrize("x, y", [
    (.1 * 3, .4)
])
def test_float_eq_returns_false(x: float, y: float):
    assert float_eq(x, y) == False


from _core.algorithms import greatest_common_divisor as gcd

class TestCases4GCD:
    def case_1(self):
        return (1, 1, 1)

    def case_2(self):
        return (10, 1, 1)

    def case_3(self):
        return (1, 190, 1)

@parametrize_with_cases(
    "x, y, expected_result",
    cases=TestCases4GCD
)
def test_gcd(
    x: int,
    y: int,
    expected_result: int
):
    assert gcd(x, y) == expected_result



@pytest.mark.parametrize("x, y", [
    (777, 3456),
])
@test_steps('section 1', 'section 2', 'section 3')
def test_suite(x, y):
    # Step A
    print("step a")
    print(x, y)
    assert not False  # replace with your logic
    intermediate_a = 'hello'
    yield

    # Step B
    print("step b")
    assert not False  # replace with your logic
    yield

    # Step C
    print("step c")
    new_text = intermediate_a + " ... augmented"
    print(new_text)
    assert len(new_text) == 19
    yield
