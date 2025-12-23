from message_and_data_samples import prikey_pem_rsa2048, pubkey_pem_rsa2048

try:
    from cryptography.hazmat.primitives import serialization
    prikey = serialization.load_pem_private_key(prikey_pem_rsa2048, None)
    pubkey = serialization.load_pem_public_key(pubkey_pem_rsa2048)
except:
    prikey = None
    pubkey = None

def test_Signature():
    from rtm_con.types_sig import Signature
    from rtm_con.types_struct_ext import StructExt
    from rtm_con.types_exceptions import PayloadSignatureVerificationError
    from construct import Tell, Bytes
    test_con = StructExt(
        "_signing_start" / Tell,
        "data" / Bytes(4),
        "_signing_end" / Tell,
        "sig" / Signature("_signing_start", "_signing_end"),
    )
    test_dict = {"data": b"test", "sig": None}
    signed_bytes = test_con.sign(test_dict, prikey)
    checked_dict = test_con.check(signed_bytes, pubkey)
    assert checked_dict["data"] == test_dict["data"]
    assert checked_dict["sig"] is not None
    missinged_bytes = test_con.build(checked_dict | {"data": b"FAIL"})
    try:
        test_con.check(missinged_bytes, pubkey)
        assert False, "Signature verification should fail but passed"
    except PayloadSignatureVerificationError:
        pass