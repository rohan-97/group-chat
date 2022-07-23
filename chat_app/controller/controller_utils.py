
def handle_exception(func):
    def wrapper(*args, **kwargs):
        try:
            res =  func(*args, **kwargs)
        except Exception as e:
            return False, str(e)
        return res
    return wrapper