pick= -1
while pick != 0:
    try:
        pick = int(input("Enter your choice function: "))
    except Exception:
        print("(!) Invalid choice. Please try again.")
        continue
    break
print(pick)