import codecs

# text = "शिक्षा का अधिकार"
from lib.encode_kruti_dev_to_unicode import kru2uni

text = "f'k{kk dk vf/kdk"
print(kru2uni(text))
for c in text:
    ascii_c = ord(c)
    print(ascii_c)
    hindi_c = chr(ascii_c)
    print(hindi_c)

text = bytes(text, encoding="utf-8")
print(text)
text = codecs.encode(text, "hex")
print(text)
