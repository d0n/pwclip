"""yubikey wrapper lib testing"""
import yubico as yubi

def yud0n(challenge):
	"""yubikey testing"""
	key = yubi.find_yubikey(debug=False)
	chal = challenge.encode().ljust(64, b'\0')
	return key.challenge_response(chal, slot=2)
