from hashlib import sha256




api_key='1303FBDB2D97B3DC7CEE8A8B05DD5FFA'
challenge='BE48F8761CF17446CC6C4FB3FC7282C9'
p1 = 'post:command=power&value=1'
p2 = 'post:command=power&value=0'

c1 = 'command=power&value=1&user=4288E5DA5C74BD88ED1BC00716791092DE495232B69B4631CD79F90ADC10580E&response=de4347ba2d21a08081c455e4c200cdde4ef5c1c838880d03729ac7f3690563df'

c2 = 'command=power&value=0&user=4288E5DA5C74BD88ED1BC00716791092DE495232B69B4631CD79F90ADC10580E&response=54a1a31b81f52ca7a85be520912fc04a31936df4bcf11dc7594d7881d52880a1'

api_key_bytes = bytes.fromhex(api_key)
challenge_bytes = bytes.fromhex(challenge)
p1_bytes = p1.encode()
p2_bytes = p2.encode()


hash1 = sha256(api_key_bytes + sha256(api_key_bytes + challenge_bytes + p1_bytes).digest())
hash2 = sha256(api_key_bytes + sha256(api_key_bytes + challenge_bytes + p2_bytes).digest())


print(hash1.hexdigest())
print(hash2.hexdigest())
assert hash1.digest() == 'de4347ba2d21a08081c455e4c200cdde4ef5c1c838880d03729ac7f3690563df'
assert hash2.digest()== '54a1a31b81f52ca7a85be520912fc04a31936df4bcf11dc7594d7881d52880a1'




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