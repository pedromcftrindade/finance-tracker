from database import db
from models import Expense
from datetime import date

def list_expenses() -> list:
    return Expense.query.order_by(Expense.data.desc()).all()


def add_expense(value, category, description) -> Expense:
    new = Expense(value=value, category=category, description=description)
    db.session.add(new)
    db.session.commit()
    return new




def calculate_total(expenses: list) -> float:
    return sum(e.value for e in expenses)


def calculate_total_by_month(expenses: list, month: int, year: int) -> float:
    filtered_expenses = [e for e in expenses if e.date.month == month and e.date.year == year]
    return calculate_total(filtered_expenses)


def calculate_total_by_year(expenses: list, year: int) -> float:
    filtered_expenses = [e for e in expenses if e.date.year == year]
    return calculate_total(filtered_expenses)


def calculate_total_by_category(expenses: list, category: str) -> float:
    filtered_expenses = [e for e in expenses if e.category == category]
    return calculate_total(filtered_expenses)


def calculate_total_by_date_range(expenses: list, start_date: date, end_date: date) -> float:
    filtered_expenses = [e for e in expenses if start_date <= e.date <= end_date]
    return calculate_total(filtered_expenses)


def calculate_average(expenses: list) -> float:
    if not expenses:
        return 0
    return calculate_total(expenses)/ len(expenses)


def calculate_average_by_month(expenses: list, month: int, year: int) -> float:
    filtered_expenses = [e for e in expenses if e.date.month == month and e.date.year == year]
    return calculate_average(filtered_expenses)




def calculate_category_breakdown(expenses: list) -> dict:
    totals = {}
    for e in expenses:
        totals[e.category] = totals.get(e.category,0) + e.value
    return totals


def calculate_monthly_breakdown(expenses: list) -> dict:
    totals = {}
    for e in expenses:
        key = (e.date.year, e.date.month)
        totals[key] = totals.get(key,0) + e.value
    return totals


def calculate_yearly_breakdown(expenses: list) -> dict:
    totals = {}
    for e in expenses:
        totals[e.date.year] = totals.get(e.date.year,0) + e.value
    return totals


def calculate_weekday_breakdown(expenses: list) -> dict:
    totals = {}
    for e in expenses:
        weekday = e.date.weekday()
        totals[weekday] = totals.get(weekday,0) + e.value
    return totals


def count_category_breakdown(expenses: list) -> dict:
    totals = {}
    for e in expenses:
        totals[e.category] = totals.get(e.category,0) + 1
    return totals


def calculate_category_average(expenses: list) -> dict:
    category_values = calculate_category_breakdown(expenses)
    category_quantity = count_category_breakdown(expenses)
    total_average = {}
    for c, t in category_values.items():
        total_average[c] = t / category_quantity[c]
    return total_average




def find_highest_expense(expenses: list) -> Expense | None:
    if not expenses:
        return None
    return max(expenses, key=lambda e: e.value)


def find_lowest_expense(expenses: list) -> Expense | None:
    if not expenses:
        return None
    return min(expenses, key=lambda e: e.value)




def filter_by_category(expenses: list, category: str) -> list:
    return [e for e in expenses if e.category == category]


def filter_by_month(expenses: list, month: int, year: int) -> list:
    return [e for e in expenses if e.date.month == month and e.date.year == year]


def filter_by_year(expenses: list, year: int) -> list:
    return [e for e in expenses if e.date.year == year]


def filter_by_value_range(expenses: list, min_value: float, max_value: float) -> list:
    return[e for e in expenses if min_value <= e.value <= max_value]


def filter_by_description(expenses: list, description: str) -> list:
    return[e for e in expenses if description in e.description]


def filter_expenses(expenses, category=None, month=None, year=None, 
                    min_value=None, max_value=None, description=None):
    result = expenses

    if category is not None:
        result = filter_by_category(result, category)
    
    if month is not None and year is not None:
        result = filter_by_month(result, month, year)
    
    if min_value is not None and max_value is not None:
        result = filter_by_value_range(result, min_value, max_value)
    
    if description is not None:
        result = filter_by_description(result, description)

    return result