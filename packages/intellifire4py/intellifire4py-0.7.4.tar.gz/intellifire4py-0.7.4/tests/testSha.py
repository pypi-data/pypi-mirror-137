import requests
from hashlib import sha256
import binascii


# user=0FA0B5FF756FFF9DBA64A4978663687F76295FB618CABD725D3217B4E8A758FB

# api_key='95A570BB467DBCC10DFC77BF40B3062D'
# challenge='C820201B9BD660CC2427A21478F6E8C1'
# payload='post:command=light&value=3'
#
#
# bin_api = binascii.unhexlify(api_key)
# bin_challenge = binascii.unhexlify(challenge)
#
# sha256(api_key+challenge+payload)
#
#
# sha1='3bf1bb10df95ab050b4aca602f5d18e7799ac229743b344650fa07c275dcdca2'
# sha2='ab4398d0b1ebc358ad6b9e668a6e2f434b83f6dd698ca895a67646d2dedd4742'


challenge = '565D94D3D3ED9EA99A19A9D10EB548A7'
api_key = '1303FBDB2D97B3DC7CEE8A8B05DD5FFA'
serial = '9CE2E834CE109D849CBB15CDDBAFF381'
user='4288E5DA5C74BD88ED1BC00716791092DE495232B69B4631CD79F90ADC10580E'

bin_api = binascii.unhexlify(api_key)
bin_challenge = binascii.unhexlify(challenge)
bin_cmd = binascii.a2b_uu("post:command=power&value=1")

sha1 = sha256(bin_api+bin_challenge+bin_cmd)

print(sha1)

str1 = f"{api_key}{challenge}post:command=power&value=1".encode()
str2 = sha256(str1)
str3 = sha256(f"{api_key}{str2}".encode())
print(str3)

# command='power'
# value='1'
# user='4288E5DA5C74BD88ED1BC00716791092DE495232B69B4631CD79F90ADC10580E'
# response='961801c78c652a05bf19dff18fd986aa04393bdcc46a0d81b6954953825a0166'



#<RequestsCookieJar[<Cookie auth_cookie=EE5C5BB6F7FA22C2FB1A51E0AB463515 for iftapi.net/>, <Cookie user=4288E5DA5C74BD88ED1BC00716791092DE495232B69B4631CD79F90ADC10580E for iftapi.net/>, <Cookie web_client_id=AE5C6E42749ECC199F058DCE08224B5B for iftapi.net/>]>




"""
curl 'http://iftapi.net/a/9CE2E834CE109D849CBB15CDDBAFF381//apppost' \
-X 'POST' \
-H 'Cookie: auth_cookie=8BB8B561999D32DD4AAA65C1C762D132; user=4288E5DA5C74BD88ED1BC00716791092DE495232B69B4631CD79F90ADC10580E; web_client_id=B54BB68B3F488303283C4971FA5F9014' \
--data-binary 'power=1'

curl 'http://iftapi.net/a/9CE2E834CE109D849CBB15CDDBAFF381//apppost' \
-X 'POST' \
-H 'Cookie: auth_cookie=EE5C5BB6F7FA22C2FB1A51E0AB463515; user=4288E5DA5C74BD88ED1BC00716791092DE495232B69B4631CD79F90ADC10580E; web_client_id=AE5C6E42749ECC199F058DCE08224B5B' \
--data-binary 'power=1'



-H 'Accept: */*' \
-H 'Content-Type: text/plain;charset=UTF-8' \
-H 'Origin: http://iftapi.net' \
-H 'Content-Length: 7' \
-H 'Accept-Language: en-US,en;q=0.9' \
-H 'Host: iftapi.net' \
-H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15' \
-H 'Referer: http://iftapi.net/webaccess/fireplace.html?serial=9CE2E834CE109D849CBB15CDDBAFF381' \
-H 'Accept-Encoding: gzip, deflate' \
-H 'Connection: keep-alive' \

"""