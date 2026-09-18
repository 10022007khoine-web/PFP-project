# Console_io.py
from Product import Product # Import Product class

class ConsoleIO:
    """
    Handles all console input and output interactions.
    """
    def show_menu(self):
        """Displays the main menu options."""
        print("\n============================================")
        print("   ORDERS MANAGEMENT SYSTEM (OMS) ")
        print("============================================")
        print("1. Add New Product")
        print("2. Update Product")
        print("3. Delete Product")
        print("4. List Available Products")
        print("5. Search Product by Name")
        print("6. Sort Products by Price (Ascending)")
        print("7. Print All Products")
        print("8. Save Data to File")
        print("0. Exit")
        print("--------------------------------------------")
    #End def

    def read_string(self, prompt: str) -> str:
        """
        Helper: Safe string input reading.
        """
        # In Python, input() handles string reading simply
        return input(prompt).strip()
    #End def

    def read_double(self, prompt: str) -> float:
        """
        Helper: Safe float input reading (for price), ensures non-negative value.
        """
        while True:
            try:
                # Get the input, attempt to convert to float
                value = float(input(prompt))
                if value >= 0:
                    return value
                #End if
                print("(!) Invalid input. Please enter a non-negative double value.")
            except ValueError:
                print("(!) Invalid input. Please enter a number (e.g., 9.99).")
            #End try
        #End while
    #End def

    def read_int(self, prompt: str) -> int:
        """
        Helper: Safe integer input reading (for quantity/menu choice), ensures non-negative value.
        """
        while True:
            try:
                # Get the input, attempt to convert to int
                value = int(input(prompt))
                if value >= 0:
                    return value
                #End if
                print("(!) Invalid input. Please enter a non-negative integer value.")
            except ValueError:
                print("(!) Invalid input. Please enter a whole number.")
            #End try
        #End while
    #End def
    
    def display_products(self, products: list[Product], title: str):
        """
        Function to display any list of products.
        """
        print(f"\n--- {title} ({len(products)} item(s)) ---")
        if not products:
            print("No products to display.")
            return
        #End if

        # Print table header
        print("+--------------------------------+----------+------------+")
        print("| Name                           | Price    | Quantity   |")
        print("+--------------------------------+----------+------------+")
        
        # Print each product's info (uses Product.print_info, which uses properties)
        for p in products:
            p.print_info()
        #End for
            
        # Print table footer
        print("+--------------------------------+----------+------------+")
    #End def
#End class