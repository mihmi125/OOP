import pytest
from Primitiivne_isikliku_eelarve_süsteem import Budget, Entry

@pytest.mark.timeout(1.0)
def test_can_add_entry_validation():
    """Check if the system correctly rejects bad data (wrong dates, negative money) and accepts good data."""
    b = Budget("Test Budget", 5.0)

    # Amount less than min_amount
    assert b.can_add_entry(4.0, "Food", "Cheap", "kulu", "2025-02-13") is False

    # Negative amount
    assert b.can_add_entry(-10.0, "Food", "Cheap", "kulu", "2025-02-13") is False

    # Invalid entry_type
    assert b.can_add_entry(10.0, "Food", "Cheap", "vale", "2025-02-13") is False

    # Invalid date format
    assert b.can_add_entry(10.0, "Food", "Cheap", "kulu", "02-13-2025") is False

    # Correct input
    assert b.can_add_entry(10.0, "Food", "Cheap", "kulu", "2025-02-13") is True

@pytest.mark.timeout(1.0)
def test_add_entry_functionality():
    """Verify that entries are actually saved and each one gets its own unique ID number."""
    b = Budget("Test Budget", 1.0)
    b.add_entry(10.0, "Food", "Cheap", "kulu", "2025-02-13")
    entries = b.get_all_entries()

    assert len(entries) == 1
    assert isinstance(entries[0], Entry)

    b.add_entry(20.0, "Rent", "Home", "kulu", "2025-02-13")
    entries = b.get_all_entries()

    assert len(entries) == 2
    assert entries[0].entry_id != entries[1].entry_id

@pytest.mark.timeout(1.0)
def test_remove_entry_logic():
    """Ensure we can delete an entry by its ID and that deleting a non-existent ID doesn't break anything."""
    b = Budget("Test Budget", 1.0)
    b.add_entry(10.0, "Food", "Cheap", "kulu", "2025-02-13")
    entry_id = b.get_all_entries()[0].entry_id

    # Non-existent ID
    assert b.can_remove_entry(999) is False

    # Remove existing
    b.remove_entry(entry_id)
    assert len(b.get_all_entries()) == 0

    # Remove non-existent ID should not change budget size
    b.add_entry(20.0, "Rent", "Home", "kulu", "2025-02-13")
    b.remove_entry(999)
    assert len(b.get_all_entries()) == 1

@pytest.mark.timeout(1.0)
def test_sorting_descending():
    """Make sure the list puts the most expensive items (highest amounts) at the top."""
    b = Budget("Test Budget", 1.0)
    b.add_entry(10.0, "Kulu-a", "Kulu1", "kulu", "2025-02-13")
    b.add_entry(50.0, "Kulu-b", "Kulu2", "kulu", "2025-02-13")
    b.add_entry(100.0, "Tulu-a", "Tulu1", "tulu", "2025-02-13")
    b.add_entry(200.0, "Tulu-b", "Tulu2", "tulu", "2025-02-13")

    expenses = b.get_expenses_by_amount_desc()
    assert expenses[0].amount == 50.0
    assert expenses[1].amount == 10.0

    incomes = b.get_incomes_by_amount_desc()
    assert incomes[0].amount == 200.0
    assert incomes[1].amount == 100.0

@pytest.mark.timeout(1.0)
def test_averages():
    """Check that the average calculation for spending and earning is correct."""
    b = Budget("Test Budget", 1.0)
    b.add_entry(10.0, "Kulu-a", "Kulu1", "kulu", "2025-02-13")
    b.add_entry(20.0, "Kulu-b", "Kulu2", "kulu", "2025-02-13")
    b.add_entry(100.0, "Tulu-a", "Tulu1", "tulu", "2025-02-13")
    b.add_entry(300.0, "Tulu-b", "Tulu2", "tulu", "2025-02-13")

    assert b.get_average_expense() == 15.0
    assert b.get_average_income() == 200.0

@pytest.mark.timeout(1.0)
def test_biggest_smallest_entries():
    """Check if the system can find the absolute largest and smallest transactions."""
    b = Budget("Test Budget", 1.0)
    b.add_entry(10.0, "Kulu-a", "Kulu1", "kulu", "2025-02-13")
    b.add_entry(50.0, "Kulu-b", "Kulu2", "kulu", "2025-02-13")
    b.add_entry(100.0, "Tulu-a", "Tulu1", "tulu", "2025-02-13")
    b.add_entry(500.0, "Tulu-b", "Tulu2", "tulu", "2025-02-13")

    assert b.get_biggest_expense().amount == 50.0
    assert b.get_smallest_expense().amount == 10.0
    assert b.get_biggest_income().amount == 500.0
    assert b.get_smallest_income().amount == 100.0

@pytest.mark.timeout(1.0)
def test_total_and_recursion():
    """Verify that both calculation methods (normal and recursive) give the same final balance."""
    b = Budget("Test Budget", 1.0)
    b.add_entry(20.0, "Kulu-a", "Kulu1", "kulu", "2025-02-13")
    b.add_entry(30.0, "Kulu-b", "Kulu2", "kulu", "2025-02-13")
    b.add_entry(100.0, "Tulu", "Tulu", "tulu", "2025-02-13")

    # 100 - 30 - 20 = 50
    expected_total = 50.0
    assert b.get_total() == expected_total
    assert b.get_total_recursive() == expected_total