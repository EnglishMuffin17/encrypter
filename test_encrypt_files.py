from KnitCrypter import knitcrypt, knitpattern, KCE

input_file_path = 'test files\\test-original.txt'
output_file_path = 'test files\\test.txt'

braid = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456780.,] [:\n'


def test_func(x):
    try:
        return (x**3)//x
    except ZeroDivisionError:
        return x


new_pattern = knitpattern(braid, hex, func=test_func)

with knitcrypt(output_file_path, new_pattern) as blanket:
    try:
        blanket.stitch().all_lines()
        blanket.stitch().stamp_contents()
    except KCE.EncryptionError:
        blanket.unknit().all_lines()
        blanket.unknit().erase_stamp()
