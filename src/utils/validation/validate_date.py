def validate_date(date: str) -> bool:
    temp = date.split("-")
    if len(temp) != 3:
        return False
    
    if len(temp[0]) != 4 or len(temp[1]) != 2 or len(temp[2]) != 2:
        return False

    if int(temp[0]) > 9999 or int(temp[1]) > 12 or int(temp[2]) > 31:
        return False
    return True
