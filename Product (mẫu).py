# Product.py

class Product:
    """
    Represents information about a single Product with encapsulated attributes.
    """
    def __init__(self, name: str, price: float, quantity: int):
        """
        Full constructor for Product.
        """
        # Protected attributes (conventionally private)
        self._name = name
        self._price = price
        self._quantity = quantity
    #End def

    # --- Properties (Getters) ---
    @property
    def name(self) -> str:
        """Getter for product name (read-only once created)."""
        return self._name
    #End def

    @property
    def price(self) -> float:
        """Getter for product price."""
        return self._price
    #End def

    @property
    def quantity(self) -> int:
        """Getter for product quantity."""
        return self._quantity
    #End def
    
    # --- Setters ---
    @price.setter
    def price(self, new_price: float):
        """Setter for price, used by ProductManager update logic."""
        self._price = new_price
    #End def

    @quantity.setter
    def quantity(self, new_quantity: int):
        """Setter for quantity, used by ProductManager update logic."""
        self._quantity = new_quantity
    #End def

    # --- Utility Methods ---
    def to_file_string(self) -> str:
        """
        Helper for File I/O. Returns a comma-separated string representation.
        Uses properties for access.
        """
        # Access attributes via properties: self.name, self.price, self.quantity
        return f"{self.name},{self.price},{self.quantity}"
    #End def

    def print_info(self):
        """
        Prints formatted information of the product.
        Uses properties for access.
        """
        print(f"| {self.name:<30} | ${self.price:>8.2f} | {self.quantity:>10} |")
    #End def

    def __str__(self):
        """Override string representation for simple printing."""
        return self.to_file_string()
    #End def
#End class