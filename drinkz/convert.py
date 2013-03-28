def convert_ml(amount):
    total = 0.0
    amt, unit = amount.split()
    
    if unit == "oz":
        total += float(amt) * 29.5735
    elif unit == "gallon" or unit == "gallons":
        total += float(amt) * 3785.41
    elif unit == "liter" or unit == "liters":
        total += float(amt) * 1000
    else:
        total += float(amt)

    return total


