"""Functions for Data Verification"""
    

def containsNum(value):
    """Check if command includes string integer when necessary

    Arguments:
    value -- the target value user put in (string)

    Boolean -- whether the command has integer string or not
    """
    if type(value) is not str:
        return False
    for character in value:
        if character == " ":
            return False
        elif character.isdigit() is False:
            return False
    return True