from datetime import datetime

class Entry:
    def __init__(self, entry_id: int, date: str, amount: float, category: str, description: str, entry_type: str):
        self.entry_id = entry_id
        self.date = date
        self.amount = amount
        self.category = category
        self.description = description
        self.entry_type = entry_type

class Budget:
    def __init__(self, name: str, min_amount: float):
        self.name = name
        self.min_amount = min_amount
        self.entries = []

    def generate_id(self) -> int:
        if not self.entries:
            return 1
        smallest_id = min(entry.entry_id for entry in self.entries) -1
        if smallest_id < 0:
            return smallest_id
        else:
            return max(entry.entry_id for entry in self.entries) +1

    def can_add_entry(self, amount: float, category: str, description: str, entry_type: str, date: str) -> bool:
        if not isinstance(amount, (int, float)) or amount >= self.min_amount or amount <= 0:
            return False
        if not entry_type in ["kulu", "tulu"]:
            return False
        if not category:
            return False

        try:
            date = datetime.strptime(date, "%y-%m-%d")
        except ValueError:
            return False

        return True

    def add_entry(self, amount: float, category: str, description: str, entry_type: str, date: str):
        if self.can_add_entry(amount, category, description, entry_type, date):
            new_entry = Entry((self.generate_id(), date, amount, category, description, entry_type))
            self.entries.append(new_entry)

    def can_remove_entry(self, entry_id: int) -> bool:
        for entry in self.entries:
            if entry.entry_id == entry_id:
                return True

        return False

    def remove_entry(self, entry_id: int):
        if self.can_remove_entry(entry_id):
            self.entries = [e for e in self.entries if e.entry_id != entry_id]

    def get_all_entries(self):
        return self.entries

    def get_expenses(self):
        return [e for e in self.entries if e.entry_type == "kulu"]

    def get_incomes(self):
        return [e for e in self.entries if e.entry_type == "tulu"]

    def get_expenses_by_amount_desc(self):
        return sorted(self.get_expenses(), key=lambda e: e.amount, reverse=True)

    def get_incomes_by_amount_desc(self):
        return sorted(self.get_incomes(), key=lambda e: e.amount, reverse=True)

    def get_average_expense(self):
        expenses = self.get_expenses()
        if not expenses:
            return 0.0
        return sum(e.amount for e in expenses) / len(expenses)

    def get_average_income(self):
        incomes = self.get_incomes()
        if not incomes:
            return 0.0
        return sum(e.amount for e in incomes) / len(incomes)

    def get_biggest_expense(self):
        return max(self.get_expenses(), key=lambda e: e.amount)

    def get_smallest_expense(self):
        return min(self.get_expenses(), key=lambda e: e.amount)

    def get_biggest_income(self):
        return max(self.get_incomes(), key=lambda e: e.amount)

    def get_smallest_income(self):
        return min(self.get_incomes(), key=lambda e: e.amount)

    def get_total(self):
        return sum(e.amount if e.entry_type == "tulu" else -e.amount for e in self.entries)

    def get_total_recursive(self, entries_list=None):
        if entries_list is None:
            entries_list = self.entries

        if not entries_list:
            return 0.0

        current = entries_list[0]
        value = current.amount if current.entry_type == "tulu" else -current.amount
        return value + self.get_total_recursive(entries_list[1:])

    def get_summary_by_category(self):
        summary = {}
        for e in self.entries:
            value = e.amount if e.entry_type == "tulu" else -e.amount
            summary[e.category] = summary.get(e.category, 0) + value

        return summary

    def get_most_common_category(self):
        if not self.entries:
            return []

        counts = {}
        for e in self.entries:
            counts[e.category] = counts.get(e.category, 0) + 1

        max_count = max(counts.values())
        return [c for c, count in counts.items() if count == max_count]