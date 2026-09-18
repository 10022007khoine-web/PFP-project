# Product_manager.py
from Product import Product # Import Product class
from File_helper import FileHelper, FileIOException # Import FileHelper and related Exception

# ==============================================================================
# Custom Exception
# ==============================================================================

class ProductManagerException(Exception):
    """
    Custom Exception for business logic errors.
    """
    pass
#End class

# ==============================================================================
# ProductManager Class
# ==============================================================================

class ProductManager:
    """
    Manages the list of products and handles business logic.
    Encapsulates file operations via FileHelper.
    """
    def __init__(self):
        """
        Constructor: attempts to load data from file.
        """
        # Internal components are typically accessed via _
        self._file_helper = FileHelper()
        self._products: list[Product] = []
        
        try:
            # Load products from file
            self._products = self._file_helper.load()
        except FileIOException as e:
            # Re-raise as a Manager-level exception for main to catch
            raise ProductManagerException(f"Error loading data from file: {e}")
        #End try
    #End def

    def add_product(self, new_product: Product):
        """
        Query 1: Add a new product to the Store. 
        Raises ProductManagerException if product name already exists.
        """
        # Check if product name already exists (case-insensitive) using p.name property
        for product in self._products:
            if product.name.lower() == new_product.name.lower(): 
                raise ProductManagerException(f"Product already exists: {new_product.name}")
            #End if
        #End for
        
        self._products.append(new_product)
    #End def

    def update_product(self, name: str, new_price: float, new_quantity: int) -> bool:
        """
        Query 2: Update a product's price and quantity. 
        Returns True if updated, False if not found.
        """
        # Case-insensitive search using p.name property
        for p in self._products:
            if p.name.lower() == name.lower(): 
                # Use property setters
                p.price = new_price
                p.quantity = new_quantity
                return True
            #End if
        #End for
        return False # Not found
    #End def

    def delete_product(self, name: str) -> bool:
        """
        Query 3: Delete a product by name.
        Returns True if deleted, False if not found.
        """
        initial_length = len(self._products)
        
        # Filter out the product to be deleted (case-insensitive check)
        # Uses p.name property
        self._products = [p for p in self._products if p.name.lower() != name.lower()]
        
        # Check if the list length changed
        return len(self._products) < initial_length
    #End def
        
    def save_products(self):
        """
        Query 8: Save to file.
        """
        try:
            self._file_helper.save(self._products)
        except FileIOException as e:
            # Re-throw as a Manager-level exception
            raise ProductManagerException(f"File saving error: {e}")
        #End try
    #End def

    def get_all_products(self) -> list[Product]:
        """
        Query 7: Returns a list of all products.
        """
        return self._products[:]
    #End def

    def get_available_products(self) -> list[Product]:
        """
        Query 4: A list of all available products in the Store (quantity > 0).
        """
        # Use p.quantity property
        return [p for p in self._products if p.quantity > 0]
    #End def

    def search_product_by_name(self, keyword: str) -> list[Product]:
        """
        Query 5: Search product by name (simple substring search).
        """
        keyword_lower = keyword.lower()
        # Use p.name property
        return [p for p in self._products if keyword_lower in p.name.lower()]
    #End def

    def get_sorted_by_price(self) -> list[Product]:
        """
        Query 6: Sort all products by product price (ascending).
        """
        # Use p.price property for sorting key
        return sorted(self._products, key=lambda p: p.price)
    #End def
#End class