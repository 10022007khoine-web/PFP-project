# File_helper.py
import os
from Result import Result # Import the Result class

# ==============================================================================
# Custom Exception
# ==============================================================================

class FileIOException(Exception):
    """
    Custom Exception for File I/O errors.
    """
    pass
#End class

# ==============================================================================
# FileHelper Class
# ==============================================================================

class FileHelper:
    """
    Handles reading from and writing to the data file.
    Throws FileIOException on critical errors.
    """
    # Static constant for the filename
    __FILENAME = "products_data.txt"

    def save(self, products: list[Product]):
        """
        Saves product data to file.
        """
        try:
            # Use 'w' for writing, overwrites existing file content
            with open(self.__FILENAME, 'w', encoding='utf-8') as file:
                for p in products:
                    file.write(p.to_file_string() + "\n")
                #End for
        except IOError as e:
            # Catch file system errors and re-raise as a custom exception
            raise FileIOException(f"Could not open/write to file: {self.__FILENAME}. Details: {e}")
        #End try
    #End def

    def load(self) -> list[Product]:
        """
        Loads product data from file.
        """
        loaded_products = []
        try:
            # Use 'r' for reading
            with open(self.__FILENAME, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue # Skip empty lines
                    #End if

                    # Split the line by comma
                    segments = line.split(',')
                    
                    if len(segments) == 3:
                        try:
                            # Convert string segments to their respective types
                            name = segments[0]
                            price = float(segments[1])
                            quantity = int(segments[2])
                            
                            if price < 0 or quantity < 0:
                                print(f"(!) Warning: Skipping line with invalid non-negative data: {line}")
                                continue
                            #End if

                            # Use the Product constructor
                            loaded_products.append(Product(name, price, quantity))
                        except ValueError:
                            # Catch conversion errors
                            print(f"(!) Warning: Skipping corrupt data line due to value conversion error: {line}")
                        except Exception as e:
                            print(f"(!) Warning: Unexpected error reading product line: {e}")
                        #End try
                    else:
                        print(f"(!) Warning: Skipping corrupt data line (incorrect number of fields): {line}")
                    #End if
                #End for
        
        except FileNotFoundError:
            # File not found is common on first run, return empty list
            return loaded_products
        except IOError as e:
            # Catch other I/O errors during reading and re-raise
            raise FileIOException(f"Error reading file: {self.FILENAME}. Details: {e}")
        #End try
            
        return loaded_products
    #End def
#End class