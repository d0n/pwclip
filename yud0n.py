import yubico as yubi


def yud0n(challenge):
	key = yubi.find_yubikey(debug=False)
	chal = challenge.encode().ljust(64, b'\0')
	return key.challenge_response(chal, slot=2)
