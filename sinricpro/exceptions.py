class exceptions:
    class SinricProError(Exception):
        pass

    class InvalidAppKeyError(SinricProError):
        pass
    class InvalidAppSecretError(SinricProError):
        pass

    class InvalidSignatureError(SinricProError):
        pass
