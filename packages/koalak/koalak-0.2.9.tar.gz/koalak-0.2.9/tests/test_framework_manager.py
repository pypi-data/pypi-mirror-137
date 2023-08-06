import koalak
import pytest
from koalak import exceptions, frameworks


def test_error_framework_already_exist():
    framework_name = koalak.generate_unique_framework_name()
    framework1 = koalak.mkframework(framework_name)  # noqa: F841

    with pytest.raises(exceptions.FrameworkAlreadyExistException):
        framework2 = koalak.mkframework(framework_name)  # noqa: F841


def test_contains_frameworks():
    framework1 = koalak.mkframework(koalak.generate_unique_framework_name())
    framework2 = koalak.mkframework(koalak.generate_unique_framework_name())

    assert framework1 in koalak.frameworks
    assert framework1.name in koalak.frameworks
    assert framework2 in koalak.frameworks
    assert framework2.name in koalak.frameworks


def test_get_frameworks():
    framework1 = koalak.mkframework(koalak.generate_unique_framework_name())
    framework2 = koalak.mkframework(koalak.generate_unique_framework_name())

    assert framework1 is koalak.frameworks[framework1.name]
    assert framework2 is koalak.frameworks[framework2.name]
    assert framework1 in list(koalak.frameworks)
    assert framework2 in list(koalak.frameworks)
