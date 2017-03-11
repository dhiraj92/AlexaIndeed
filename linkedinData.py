from linkedin import linkedin

API_KEY = '78w10iogyml222'
API_SECRET = 'dFozSQibPQX8KMDpG'
RETURN_URL = 'http://127.0.0.1:5000/'
authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, linkedin.PERMISSIONS.enums.values())
print authentication.authorization_url  # open this url on your browser
#application = linkedin.LinkedInApplication(authentication)
authentication.authorization_code = 'AQR4VuyVGf9T5MjtAJZIq5NQY0wv3C_bDI0dcSp4zEfsP32nrLVw8QnvlL2nbxDeWbuump12FiX9BphGK7ZRXno9cB5PV9qIYUH3d9Xh3EL-IkSAm4k'
print authentication.get_access_token()