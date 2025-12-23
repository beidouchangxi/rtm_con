class PayloadSignatureVerificationError(Exception):
    """If signature verification fails."""
    pass

class MissingCryptographyError(Exception):
    """If the dependency of cryptography is missing."""
    pass