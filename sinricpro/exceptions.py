class exceptions:
    """
    Sinric Pro SDK exceptions.
    """
    class SinricProError(Exception):
        pass

    class InvalidAppKeyError(SinricProError):
        pass
    class InvalidAppSecretError(SinricProError):
        pass

    class InvalidSignatureError(SinricProError):
        pass
