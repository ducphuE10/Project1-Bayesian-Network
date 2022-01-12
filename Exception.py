
class NetworkException(Exception):
    def __init__(self, message):
        print("Error: " + message)
