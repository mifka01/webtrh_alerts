import random
import string

def get_symbol():
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(4))
    
    return result_str