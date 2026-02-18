from random import randint
from datetime import datetime


class Entry:
    """Represents a single budget transaction."""

    def __init__(self, entry_id: int, date: str, amount: float, category: str, description: str, entry_type: str):
        """Initialize entry with ID, date, amount, category, description, and type."""
        self.entry_id = entry_id
        self.date = date
        self.amount = amount
        self.category = category
        self.description = description
        self.entry_type = entry_type


class Budget:
    """Manages budget entries and provides financial analysis."""

    def __init__(self, name: str, min_amount: float):
        """Initialize budget with name and minimum transaction amount."""
        self.name = name
        self.min_amount = min_amount
        self.entries = []

    def generate_id(self) -> int:
        """Generates a unique random ID"""
        while True:
            new_id = randint(1000, 99999)
            if not any(entry.entry_id == new_id for entry in self.entries):
                return new_id

    def can_add_entry(self, amount: float, category: str, description: str, entry_type: str, date: str) -> bool:
        """Validate if entry data meets budget requirements."""
        if not isinstance(amount, (int, float)) or amount < self.min_amount or amount <= 0:
            return False
        if entry_type not in ["kulu", "tulu"]:
            return False
        if not category:
            return False

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            return False

        return True

    def add_entry(self, amount: float, category: str, description: str, entry_type: str, date: str):
        """Add a new entry if validation passes."""
        if self.can_add_entry(amount, category, description, entry_type, date):
            new_entry = Entry(self.generate_id(), date, amount, category, description, entry_type)
            self.entries.append(new_entry)

    def can_remove_entry(self, entry_id: int) -> bool:
        """Check if an entry ID exists in the budget."""
        return any(entry.entry_id == entry_id for entry in self.entries)

    def remove_entry(self, entry_id: int):
        """Remove entry by ID if present."""
        if self.can_remove_entry(entry_id):
            self.entries = [e for e in self.entries if e.entry_id != entry_id]

    def get_all_entries(self):
        """Return all entries."""
        return self.entries

    def get_expenses(self):
        """Return only expense entries."""
        return [e for e in self.entries if e.entry_type == "kulu"]

    def get_incomes(self):
        """Return only income entries."""
        return [e for e in self.entries if e.entry_type == "tulu"]

    def get_expenses_by_amount_desc(self):
        """Return expenses sorted by amount descending."""
        return sorted(self.get_expenses(), key=lambda e: e.amount, reverse=True)

    def get_incomes_by_amount_desc(self):
        """Return incomes sorted by amount descending."""
        return sorted(self.get_incomes(), key=lambda e: e.amount, reverse=True)

    def get_average_expense(self):
        """Return average expense amount or 0.0."""
        expenses = self.get_expenses()
        if not expenses:
            return 0.0
        return sum(e.amount for e in expenses) / len(expenses)

    def get_average_income(self):
        """Return average income amount or 0.0."""
        incomes = self.get_incomes()
        if not incomes:
            return 0.0
        return sum(e.amount for e in incomes) / len(incomes)

    def get_biggest_expense(self):
        """Return the highest expense entry."""
        return max(self.get_expenses(), key=lambda e: e.amount, default=None)

    def get_smallest_expense(self):
        """Return the lowest expense entry."""
        return min(self.get_expenses(), key=lambda e: e.amount, default=None)

    def get_biggest_income(self):
        """Return the highest income entry."""
        return max(self.get_incomes(), key=lambda e: e.amount, default=None)

    def get_smallest_income(self):
        """Return the lowest income entry."""
        return min(self.get_incomes(), key=lambda e: e.amount, default=None)

    def get_total(self):
        """Calculate net balance (incomes - expenses)."""
        return sum(e.amount if e.entry_type == "tulu" else -e.amount for e in self.entries)

    def get_total_recursive(self, entries_list=None):
        """Calculate net balance using recursion."""
        if entries_list is None:
            entries_list = self.entries

        if not entries_list:
            return 0.0

        current = entries_list[0]
        value = current.amount if current.entry_type == "tulu" else -current.amount
        return value + self.get_total_recursive(entries_list[1:])

    def get_summary_by_category(self):
        """Return a dictionary of net totals per category."""
        summary = {}
        for e in self.entries:
            value = e.amount if e.entry_type == "tulu" else -e.amount
            summary[e.category] = summary.get(e.category, 0.0) + value
        return summary

    def get_most_common_category(self):
        """Return a list of the most frequent categories."""
        if not self.entries:
            return []

        counts = {}
        for e in self.entries:
            counts[e.category] = counts.get(e.category, 0) + 1

        max_count = max(counts.values())
        return [c for c, count in counts.items() if count == max_count]