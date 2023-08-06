from urllib import request, parse
import json
def send(channel, msg, ssl = True):
	api_uri = 'https://wav.cat/send/'
	if (ssl == False):
		api_uri = 'http://wav.cat/send/'
	ret = False
	payload = parse.urlencode({"msg": msg}).encode()
	with request.urlopen(request.Request(api_uri + channel, data=payload)) as response:
		ret = json.loads(response.read().decode('utf-8'))
	return ret