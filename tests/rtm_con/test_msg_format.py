import pytest

from message_and_data_samples import message_and_data_samples, prikey_pem_rsa2048, pubkey_pem_rsa2048

try:
    from cryptography.hazmat.primitives import serialization
    prikey = serialization.load_pem_private_key(prikey_pem_rsa2048, None)
    pubkey = serialization.load_pem_public_key(pubkey_pem_rsa2048)
except:
    prikey = None
    pubkey = None

@pytest.mark.parametrize(
    "msg_hex, target, check_build",
    message_and_data_samples.values(),
    ids=message_and_data_samples.keys(),
)
def test_msg_and_msg_checked(msg_hex:str, target:dict, check_build:bool):
    from rtm_con import msg, msg_checked
    from construct import Container, ListContainer

    def compare_container(parsed_data, py_obj):
        if isinstance(parsed_data, ListContainer):
            for value, value_target in zip(parsed_data, py_obj):
                compare_container(value, value_target)
        elif isinstance(parsed_data, Container):
            for key, value_target in py_obj.items():
                value = parsed_data[key]
                compare_container(value, value_target)
        else:
            assert parsed_data == py_obj, f"Parsed data doesn't match expectation\nparsed:\n{parsed_data}\ntarget:\n{py_obj}"
    for msg_con in (msg, msg_checked):
        print(msg_hex)
        print(target)
        msg_b = bytes.fromhex(msg_hex)
        if pubkey:
            msg = msg_con.check(msg_b, pubkey)
        else:
            msg = msg_con.parse(msg_b)
        compare_container(msg, target)
        if check_build:
            if prikey:
                build_hex = msg_con.sign(target, prikey).hex()
            else:
                build_hex = msg_con.build(target).hex()
            assert build_hex == msg_hex, f"Build data doesn't match orignal bytes\nbuild:\n{build_hex}\norignal:\n{msg_hex}"



