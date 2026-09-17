# Main.py
import sys
# Import classes and exceptions from other modules
from Console_io import ConsoleIO
from Product_manager import ProductManager, ProductManagerException
from Product import Product

def main():
    """
    Main function to run the Orders Management System.
    """
    io = ConsoleIO()
    manager = None

    # Initialize ProductManager and catch file loading errors
    try:
        manager = ProductManager()
        print("(*) System initialized successfully. Data loaded.")
    except ProductManagerException as e:
        # If loading fails, print the error and start with a new, empty manager
        print(f"(!) INITIALIZATION ERROR: {e}")
        print("(!) Program will start with an empty list.")
        
        # Create a new, empty manager instance to proceed
        try:
             manager = ProductManager()
        except ProductManagerException:
             # Should not happen on the second attempt unless file system is truly broken
             print("(!) Fatal error: Cannot initialize ProductManager.")
             sys.exit(1)
        #End try
    #End try


    choice = -1
    while choice != 0:
        io.show_menu()
        
        # Read choice safely
        try:
            choice = io.read_int("Enter your choice: ") 
        except Exception:
            print("(!) Invalid choice. Please try again.")
            continue 
        #End try

        try:
            if choice == 1: # Add Product
                print("\n--- Add New Product ---")
                name = io.read_string("Enter product name: ")
                price = io.read_double("Enter product price: ")
                quantity = io.read_int("Enter quantity in stock: ")
                
                # Create the Product object
                new_product = Product(name, price, quantity)
                manager.add_product(new_product)
                print("(*) Product added successfully.")
                
            elif choice == 2: # Update Product
                print("\n--- Update Product ---")
                name = io.read_string("Enter name of product to update: ")
                new_price = io.read_double("Enter new price: ")
                new_quantity = io.read_int("Enter new quantity in stock: ")
                
                if manager.update_product(name, new_price, new_quantity):
                    print("(*) Product updated successfully.")
                else:
                    print("(!) Update failed: Product not found.")
                #End if

            elif choice == 3: # Delete Product
                print("\n--- Delete Product ---")
                name = io.read_string("Enter name of product to delete: ")
                
                if manager.delete_product(name):
                    print("(*) Product deleted successfully.")
                else:
                    print("(!) Deletion failed: Product not found.")
                #End if

            elif choice == 4: # List Available Products
                io.display_products(manager.get_available_products(), "Available Products List")
                
            elif choice == 5: # Search Product by Name
                keyword = io.read_string("Enter product name keyword: ")
                io.display_products(manager.search_product_by_name(keyword), "Search Results")
                
            elif choice == 6: # Sort by Price Ascending
                # Get the sorted list, then display it
                sorted_list = manager.get_sorted_by_price()
                io.display_products(sorted_list, "List Sorted by Price (Ascending)")
                
            elif choice == 7: # Print All Products
                io.display_products(manager.get_all_products(), "List of All Products")
                
            elif choice == 8: # Save to File
                manager.save_products()
                print("(*) Data saved successfully.")
                
            elif choice == 0:
                print("Goodbye! Please save before exiting to ensure data integrity.")
                break # Exit the loop
                
            else:
                print("(!) Invalid choice. Please try again.")
            #End if

        except ProductManagerException as e:
            # Catch business logic errors from ProductManager
            print(f"(!) PROCESSING ERROR: {e}")
        except Exception as e:
            # Catch any other unexpected errors
            print(f"(!) An unexpected error occurred: {e}")
        #End try
    #End while
#End def
            
# Standard Python entry point
if __name__ == "__main__":
    main()
#End if