def check_range(value,range,name="Unknown"):
    if value < range[0] or value>range[1]:
        raise ValueError("Value {0} for '{3}' is outside of the authroized boundaries {1}-{2}".format(value,range[0],range[1],name))
    return value

def check_type(value,type,name="Unknown"):
    if not isinstance(value,type):
        raise TypeError("Value {0} for '{2}' is not of type {1}".format(value,type,name))
    return value
    
