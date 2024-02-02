from random import randint

def format_response(success, status, message, data = None):
    return {
        "success": success,
        "status": status,
        "message": message,
        "data": data 
    }

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)