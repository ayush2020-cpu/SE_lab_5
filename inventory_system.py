"""
Inventory Management System
----------------------------
A simple inventory tracking program that supports adding, removing,
saving, and loading item quantities securely and cleanly.
"""

import json
from datetime import datetime
from typing import Dict, List, Optional

# Global variable to store inventory data
stock_data: Dict[str, int] = {}


def add_item(item: str = "default", qty: int = 0, logs: Optional[List[str]] = None) -> None:
    """
    Add an item and quantity to the inventory.

    Args:
        item (str): Name of the item to add.
        qty (int): Quantity to add.
        logs (list, optional): Log list for recording actions.
    """
    if logs is None:
        logs = []

    if not isinstance(item, str) or not isinstance(qty, int):
        raise ValueError("Item name must be a string and quantity must be an integer.")

    stock_data[item] = stock_data.get(item, 0) + qty
    log_entry = f"{datetime.now()}: Added {qty} of {item}"
    logs.append(log_entry)


def remove_item(item: str, qty: int) -> None:
    """
    Remove a quantity of an item from inventory.

    Args:
        item (str): Item name to remove.
        qty (int): Quantity to remove.
    """
    try:
        if not isinstance(item, str) or not isinstance(qty, int):
            raise ValueError("Invalid input types.")

        if item not in stock_data:
            print(f"Warning: {item} not found in inventory.")
            return

        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except (ValueError, KeyError) as err:
        print(f"Error removing item: {err}")


def get_qty(item: str) -> int:
    """
    Get the current quantity of an item.

    Args:
        item (str): Item name.

    Returns:
        int: Quantity in stock.
    """
    if item not in stock_data:
        raise KeyError(f"Item '{item}' not found in inventory.")
    return stock_data[item]


def load_data(file: str = "inventory.json") -> None:
    """
    Load inventory data from a JSON file.

    Args:
        file (str): File path to load from.
    """
    global stock_data
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.load(f)
        print("Inventory loaded successfully.")
    except FileNotFoundError:
        print(f"File '{file}' not found. Starting with empty inventory.")
        stock_data = {}
    except json.JSONDecodeError as err:
        print(f"Error decoding JSON: {err}")
        stock_data = {}


def save_data(file: str = "inventory.json") -> None:
    """
    Save inventory data to a JSON file.

    Args:
        file (str): File path to save to.
    """
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=4)
        print("Inventory saved successfully.")
    except IOError as err:
        print(f"Error saving inventory: {err}")


def print_data() -> None:
    """Print all items and their quantities."""
    print("Items Report")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")


def check_low_items(threshold: int = 5) -> List[str]:
    """
    Return a list of items with quantity below the given threshold.

    Args:
        threshold (int): Quantity limit.

    Returns:
        list[str]: Items below threshold.
    """
    return [item for item, qty in stock_data.items() if qty < threshold]


def main() -> None:
    """Main function for demonstration."""
    try:
        logs: List[str] = []
        add_item("apple", 10, logs)
        add_item("banana", 2, logs)
        remove_item("apple", 3)
        remove_item("orange", 1)
        print(f"Apple stock: {get_qty('apple')}")
        print(f"Low items: {check_low_items()}")
        save_data()
        load_data()
        print_data()
    except Exception as err:  # pylint: disable=broad-except
        print(f"Unexpected error: {err}")


if __name__ == "__main__":
    main()
