import pprint
from rtm_con import msg, flat_msg, MsgExcel, con_to_pyobj
try:
    import cryptography
    import cryptography.hazmat.primitives.serialization
except:
    cryptography = None

prikey = cryptography.hazmat.primitives.serialization.load_pem_private_key(
'''-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC1emb2Nbx8Hufl
XrKQ8NdayVwtC5M+j/4YH349Xn9+1eny54WK4ZbwvqG9/4bMxIy8iOKXyOLuIjAH
AUAlzkybRDMYMEnVOzy8FEs8jhHddq9hr2QRKJ8PI1Jsfwufe8eO0kR18HRRkLMU
if2vzM742OPsjliK61rLC8lP5QwZqEF7GBsl1x03KwQK/1w3yZU7+ZNLHluxuH3I
yqq7ln8n3tFRdNyH+P/AQxxaCK2UuYWtExdG7tpPr0zLqQYbWXDvPs5xv7rkv2MT
KCYlw0DAbhyer2nAhAGYQ3vtnJ6kij/xRBFMQUKcTKt3577vUhtrA1bZIdrhz59r
RF9GDoSLAgMBAAECggEAGhLkCCvgUNT/7GyWq0xvJJQZsj8fgLWfhEfCE38oQkjp
vASXo0SWMzCwfGPiMjlrHwtrwvMR57TxwY/kb4ocZ5J85NTLRt+j8kHYLXMcDf2n
ZRmV/wEfGUWx6fS27ssR+Oss+uT5UV7A3AqXcFK0yfwfgzVQc2UtPk8LNXdrLaRJ
E+FiNGly1zXGr0b22w2R/KFoh7hs4yc/YJlMiOuUA3fyIz1cy4qKxvets9sghnTe
PknbqR92LmBmiy6rXQUgfANGGC/RFB1HAHuFc/P0Dx6EgphkT4siUgOM9YgEDMBF
iOpJsFbBtRjCtq7Z+76j7m58sg2FTZN+YCl32Bc6wQKBgQDZO9ZhYZm9aTD5bpzc
HXw97azDML1CNrM1/w4ntLb6qBnFuutzltcerEC0EBgoumfgGfCjOORYuR86LIOi
HVtAELdctP/RDtdaMMNrNVkrb4RhzU7Y0QD/GDwfjLKJm+tky+K0tAvIT3MqFsL4
YfpXDU6iFWR9VxDKgDmmC1BL/wKBgQDV3RireKrMUfvWtT5yILTz2PleiUeGyW0t
eXWvHpPpAtDa/5qXdnqqca+hLaRGK0zzknq0yhhx/JwefKOU1G/Le3ajqzBT3qaz
CCuVU1bxWDzvNKR04Sv1T128s91sjrOskXvTfy8dUnAFosloFerOqxIloi8i8x/y
ndU3xfg3dQKBgGiGYDrvKXh4GvaKALPxBA0QRaaN1yL7CvQaS4dTbw/gvrXjoNM3
az75BxEdBWLjfoPYN29yOn1uZdYqARSKJ5QF9xSGiujeyUQ+XmlBfCxoNjyQ+zVc
K6ySzqsnmeiYu4T+jZEBaQHzKKjB1wKIslocrw9SV83vjMbDN/nrS7GlAoGAXWaY
NZsXjPBpOlYhlZpvLOgf0IfH8zfZNLkNCpQiKOuP53UmQOv/mpzYBV53liWnD+Fz
Ma3piy61yCLLFl7JDGc5YzWKf7aHuzzgO/EP0Yul4RpukJUeq54j5Bvxok2Ybs+C
8tVi8D1mqy9zIsAfsm7IGCOCzpK76yu/SQJu61kCgYAZTKkvJqfHSJUbQE20Rlr9
eqI+EiJgY1F/EMBhWrfojjSGlJjaonRIms0t3b2Tr9FA98A5/GzDuhfiUzcTkedo
VUwICyFybeU99Cqmc95gsSMmKQ1SVzMPL1l+cH4MYHF04C67yks3yv+SK7P6Gsc2
m23OmYZ2O3iTJO9gYQtRDw==
-----END PRIVATE KEY-----'''.encode("utf-8"), None) if cryptography else None

pubkey = cryptography.hazmat.primitives.serialization.load_pem_public_key(
'''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtXpm9jW8fB7n5V6ykPDX
WslcLQuTPo/+GB9+PV5/ftXp8ueFiuGW8L6hvf+GzMSMvIjil8ji7iIwBwFAJc5M
m0QzGDBJ1Ts8vBRLPI4R3XavYa9kESifDyNSbH8Ln3vHjtJEdfB0UZCzFIn9r8zO
+Njj7I5YiutaywvJT+UMGahBexgbJdcdNysECv9cN8mVO/mTSx5bsbh9yMqqu5Z/
J97RUXTch/j/wEMcWgitlLmFrRMXRu7aT69My6kGG1lw7z7Ocb+65L9jEygmJcNA
wG4cnq9pwIQBmEN77ZyepIo/8UQRTEFCnEyrd+e+71IbawNW2SHa4c+fa0RfRg6E
iwIDAQAB
-----END PUBLIC KEY-----'''.encode('utf-8')) if cryptography else None

if __name__=='__main__':
    test_msgs = (
        # Login test
        '242401fe484155563442474e365335303032323139010036190a1b140202000c3839383630393234373930303233313636363036010130524a50454130304841553041414631333130303139353596',
        '242401fe484155563442474e365335303032323139010067190a1b140202000c383938363039323437393030323331363636303602010230524a50454130304841553041414631333130303139353530524a50454130304841553041414631333130303139353630524a504541303048415530414146313331303031393537c7',
        '232301fe484155563442474e365335303032323139010066190a1b140202000c3839383630393234373930303233313636363036031830524a50454130304841553041414631333130303139353530524a50454130304841553041414631333130303139353630524a504541303048415530414146313331303031393537dc',
        # Logout test
        '232304fe484155563442474e365335303032323139010008190a1b1402020802c8',
        '242404fe484155563442474e365335303032323139010008190a1b1402020802c8',
        # Whole message test
        '232302fe484155563442474e365335303032323139010239190a0b13081201010301007a00000a1d1e81274355011e19990010020201013851794e343d1e4b272402023751894cdb401e4b26f7050000000000000000000601020fdf01140fdc01013a010a38070000000000000000000801011e81274300c00001c00fdd0fdf0fde0fde0fdd0fdd0fdd0fde0fdf0fde0fdd0fdd0fde0fde0fdd0fdd0fdd0fde0fdd0fdc0fdd0fdd0fdd0fde0fdd0fde0fde0fdd0fdf0fde0fde0fdd0fdd0fdd0fde0fdd0fde0fde0fdd0fde0fde0fdd0fdd0fdd0fde0fde0fde0fdd0fdd0fde0fdc0fdc0fdd0fdd0fde0fdd0fdd0fdc0fdd0fdd0fdd0fde0fdd0fde0fde0fde0fde0fdd0fde0fdd0fdd0fdd0fde0fde0fdf0fdf0fdf0fdf0fdd0fdd0fde0fdd0fdd0fde0fde0fdf0fde0fdd0fde0fdd0fdf0fde0fdf0fdf0fdf0fdf0fde0fde0fde0fde0fdd0fde0fdd0fde0fdd0fdd0fde0fdc0fdd0fdd0fdd0fde0fdc0fde0fdd0fdd0fdd0fde0fdd0fdd0fde0fdd0fde0fdc0fde0fde0fde0fde0fde0fdc0fdc0fdd0fdd0fdd0fdd0fde0fdc0fdd0fdd0fdc0fde0fde0fde0fdd0fdd0fdf0fde0fdf0fde0fde0fde0fdf0fde0fdf0fde0fdf0fde0fdf0fde0fdf0fdd0fdd0fde0fde0fde0fde0fdd0fde0fdd0fde0fdd0fdd0fde0fde0fdd0fdd0fde0fde0fdd0fdd0fdf0fde0fdd0fde0fde0fde0fde0fde0fde0fde0fdf0fde09010100303a393a3a393939393938393939393939393a3939393a3a3a3a393a3a39393939393939393839393939393939393a3a3a82001d000007ff0107fd01047a0107fd01000100010001000101010001069a015d',
        '242402FE484155563442474E365335303032323139010323190A1C0E2D2F010103010000000261061BE275464B011F199902020103477D0000030D404A0203497D0000030D3B45050102000000000000000006000000000000000003000800020009002500090026000701011BE2754600B40F750F780F760F790F770F760F790F7A0F7A0F7C0F7B0F7C0F7D0F7D0F7D0F7A0F7A0F7A0F7B0F7A0F7B0F7B0F7C0F7D0F7C0F7C0F7E0F7C0F7C0F7A0F7B0F7B0F7D0F7B0F7D0F7D0F7D0F7D0F7D0F7C0F7D0F7C0F7C0F7C0F7D0F790F780F760F7C0F7B0F7C0F7C0F7C0F7C0F7C0F770F7D0F780F7D0F7C0F7C0F7D0F7A0F7F0F7A0F7D0F7C0F7B0F7C0F7C0F7D0F7C0F7C0F7F0F7D0F7D0F7E0F7D0F7D0F7E0F7D0F7E0F7E0F7D0F7D0F7D0F7D0F7D0F7E0F7E0F7B0F7C0F7C0F7C0F7B0F7B0F780F7C0F7D0F7A0F7C0F7C0F7C0F7C0F7C0F7C0F7D0F7A0F7B0F7A0F7A0F7C0F7D0F7C0F7D0F7D0F7C0F7C0F7B0F7D0F790F7C0F7B0F7A0F7C0F7C0F7C0F7B0F7C0F7D0F7B0F7D0F7C0F7C0F7C0F790F7C0F7C0F7B0F7C0F7A0F7D0F7B0F7B0F7C0F7C0F7C0F7D0F7B0F7B0F7A0F7C0F7B0F7C0F7C0F7D0F7C0F7B0F7B0F7C0F7B0F7C0F7C0F7C0F7C0F7B0F7C0F7C0F7D0F7C0F7C0F7C0F7C0F7C0F7C0F7D0F7D0F7D0F7D0F7D0801010030464646454646464645444545464645444646464646464646464746464646464645444646444544434546454545454645820023000004190104230103DD0103F70100010001000100010101000105DB0100FFFFFF0101FF0201005F28A29FC19044A46D51A315D954697BA0E9F09E0AEC8C12F8CB14DDBA8B34339F4F5DFA18631041F0809E94110C41EB69DD8ACFF99461390C1157785E9E3353969A86C4AC1BA92BCF0AA9E347633B1EF9AA448C7601C65DCF62F61FCC3B05CE398C0ECE6D72F30D656F7769DD93C2D9FEE50838BAACEEBD1B983F8CB644E358544570E04C8B637304E38EA5877E387098056C6D648074E3130889DB420311A62072CA57E435610C47F980A8603E984285FE300A27BCF2A7E52F8CB10B2F80BD9D9C4D68280FD7D6642DA7EFB590BEEFD3C3D7E8A72B3BFF8DD619E1229D128B1787C69CC8E3A1922695666C80D9C6A50EFD1A46FE80EDE2D6246EB4F9582F8B0000E7',
    )

    print("===============================")
    print("= Basic parsing features demo =")
    print("===============================")

    for msg_hex in test_msgs:
        print("Test for: ", msg_hex)
        input("\npress enter to see the parsed construct object...")
        if pubkey:
            msg_obj = msg.check(bytes.fromhex(msg_hex), pubkey)
        else:
            msg_obj = msg.parse(bytes.fromhex(msg_hex))
        print(msg_obj)
        input("\npress enter to see as python object...")
        msg_py_obj = con_to_pyobj(msg_obj)
        pprint.pp(msg_py_obj)
        input("\npress enter to see the re-built msg hexsting...")
        if prikey:
            msg_hex_new = msg.sign(msg_py_obj, prikey)
        else:
            msg_hex_new = msg.build(msg_py_obj)
        print(msg_hex_new.hex())
        input("\npress enter to see flattened message...")
        flat_dict = flat_msg(msg_obj)
        for k,v in flat_dict.items():
            print(f"{k:<50}{v}")
            print(f"{"":<50}{flat_dict.pathdict[k]}")
        input("\npress enter to see next message(if any)...\n\n")
    
    print("=============================")
    print("= Excel output feature demo =")
    print("=============================")
    user_input = input('Give me a name for save the file(no ext needed, press enter for use the default name "demo"):\n')
    name = user_input if user_input else "demo"
    output_excel_file = f"{name}.xlsx"
    print(f'Preparing the excel file "{output_excel_file}"...')
    excel_writer = MsgExcel(rawmsg_key="Msg", logtime_key="LogTime")
    for msg_hex in test_msgs:
        # Normally you will have another timestamp from the recorder besides the one from message
        # But we fill it unkown here for the logtime
        # You can also put whatever you like in the line_dict
        # Which will be output as addtional columns
        line_dict = {"Msg":msg_hex, "LogTime":"unkown"}
        msg_obj = msg.parse(bytes.fromhex(msg_hex))
        msg_dict = flat_msg(msg_obj)
        line_dict.update(msg_dict)
        excel_writer.write_line(line_dict, pathdict=msg_dict.pathdict)
    print(f"Saving the excel file...")
    excel_writer.save(output_excel_file)
    print(f"Excel file has been written")