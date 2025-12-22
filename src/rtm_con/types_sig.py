from construct import (
    Construct,
    ValidationError,
    Struct,
    Int16ub,
    Enum,
    Prefixed,
    GreedyBytes,
    Int8ub)
try:
    # Import cryptography only if signature checking is needed
    import cryptography
except:
    cryptography = None

from rtm_con.utilities import HexAdapter

sig_algos = Enum(Int8ub, 
    sm2=1,
    rsa=2,
    ecc=3,
)

"""
GB/T 32960.3-2025 chp7.2.2 table8
"""

sig_con = Struct(
    "algo" / sig_algos,
    "r_value" / Prefixed(Int16ub, HexAdapter()),
    "s_value" / Prefixed(Int16ub, HexAdapter()),
)

class Signature(Construct):
    def __init__(self, *signed_items):
        super().__init__()
        self.signed_items = signed_items
        self.sig_len = 256 # 2048 bits
        self.base_con = sig_con

    @staticmethod
    def _find_key_in_context(context, key):
        """Recursively search for keys in nested Context."""
        curr = context
        while curr is not None:
            if key in curr:
                return curr[key]
            # Construct stores the parent context in '_'
            curr = curr.get("_")
        return None

    def _find_data_in_context(self, context):
        data = b""
        for name in self.signed_items:
            objdata = context[name]
            con = context._subcons[name]
            data += con.build(objdata)
        return data

    def _parse(self, stream, context, path):
        sig = self.base_con._parse(stream, context, path)
        public_key = self._find_key_in_context(context, "public_key")
        if public_key:
            if cryptography is None:
                raise ValidationError(f'If you need signature verification, install with extras "sig" or install cryptography manually')
            elif sig.algo=="rsa":
                # Verify signature only if public_key found in context
                signature_bytes = bytes.fromhex(sig.r_value)
                data_to_verify = self._find_data_in_context(context)
                try:
                    public_key.verify(
                        signature_bytes,
                        data_to_verify,
                        cryptography.hazmat.primitives.asymmetric.padding.PKCS1v15(),
                        cryptography.hazmat.primitives.hashes.SHA256()
                    )
                except cryptography.exceptions.InvalidSignature:
                    raise ValidationError(f"RSA Signature verification failed at path {path}")
            else:
                raise TypeError("The algorighm specified in message is not supported")
        return sig

    def _build(self, obj, stream, context, path):
        private_key = self._find_key_in_context(context, "private_key")
        if private_key:
            # Auto generate signature only if private key is provided
            if cryptography is None:
                raise ValidationError(f'If you need signature generation, install with extras "sig" or install cryptography manually')
            elif isinstance(private_key, cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey):
                data_to_sign = self._find_data_in_context(context)
                signature = private_key.sign(
                    data_to_sign,
                    cryptography.hazmat.primitives.asymmetric.padding.PKCS1v15(),
                    cryptography.hazmat.primitives.hashes.SHA256()
                )
                build_res = self.base_con.build({
                    "algo": "rsa",
                    "r_value": signature.hex(),
                    "s_value": "",
                })
                stream.write(build_res)
                return build_res
            else:
                raise ValidationError(f'The algorighm of private_key is not supported')
        # No private key, skip signing part
        return self.base_con._build(obj, stream, context, path)

class StructWithKey(Struct):
    """
    Works to ensure when pubkey or prikey is passed in with a wrong way, it fails fast
    You can still use msg.build(..., private_key=...) or msg.parse(..., public_key=...)
    But it will not raise any exception nor report any error if the keyword is mis-spelled or the key is None
    Check types_sig.py for the detailed signature stuffs
    """
    def check(self, byt_data, pubkey):
        """A more safer way to pass-in the pubkey for signature checking"""
        if pubkey==None:
            raise TypeError("pubkey is None!")
        return self.parse(byt_data, public_key=pubkey)

    def sign(self, obj_data, prikey):
        """A more safer way to pass-in the prikey for signature generation"""
        if prikey==None:
            raise TypeError("prikey is None!")
        return self.build(obj_data, private_key=prikey)
