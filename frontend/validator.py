import re
 
def is_valid_email_phone_field(value):
     
    # 1) Begins with 0 or 91
    # 2) Then contains 6,7 or 8 or 9.
    # 3) Then contains 9 digits
    regex = re.compile("(0|91)?[6-9][0-9]{9}")
    if regex.match(value):
        return True
    else:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if(re.fullmatch(regex, value)):
            return True
    return False
