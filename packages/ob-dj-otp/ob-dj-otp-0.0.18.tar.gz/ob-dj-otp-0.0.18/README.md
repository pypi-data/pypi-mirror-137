## OBytes Django OTP App

[![Build & Test](https://github.com/obytes/ob-dj-otp/workflows/Build%20&%20Test/badge.svg)](https://github.com/obytes/ob-dj-otp/actions)
[![pypi](https://img.shields.io/pypi/v/ob-dj-otp.svg)](https://pypi.python.org/pypi/ob-dj-otp)
[![license](https://img.shields.io/badge/License-BSD%203%20Clause-green.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![downloads](https://pepy.tech/badge/ob-dj-otp)](https://pepy.tech/project/ob-dj-otp)
[![python](https://img.shields.io/pypi/pyversions/ob-dj-otp.svg)](https://pypi.python.org/pypi/ob-dj-otp)
[![docs](https://github.com/obytes/ob-dj-otp/workflows/Docs/badge.svg)](https://github.com/obytes/ob-dj-otp/blob/main/docs/source/index.rst)
[![health-check](https://snyk.io/advisor/python/ob-dj-otp/badge.svg)](https://snyk.io/advisor/python/ob-dj-otp)

OTP is a Django app to conduct Web-based one true pairing, for authentication, registration and changing phone number.

## Quick start

1. Install `ob_dj_otp` latest version `pip install ob_dj_otp`

2. Add "ob_dj_otp" to your `INSTALLED_APPS` setting like this:

```python
   # settings.py
   INSTALLED_APPS = [
        ...
        "ob_dj_otp.core.otp",
   ]
   # Setting Twilio as SMS Provider
   OTP_PROVIDER = os.environ.get("OTP_PROVIDER", "twilio")
   # Passing Twilio Verify Service-ID
   OTP_TWILIO_SERVICE = os.environ.get("OTP_PROVIDER")
```


3. Include the OTP URLs in your project urls.py like this::

```python
    # urls.py
    path("otp/", include("ob_dj_otp.apis.otp.urls")),
```

4. Run ``python manage.py migrate`` to create the otp models.


### Extending API Serializers

OTP Verification serializer can be extended as following:

```python
# utils.py
from ob_dj_otp.apis.otp.serializers import OTPVerifyCodeSerializer
from rest_framework import serializers

class NewOTPVerifyCodeSerializer(OTPVerifyCodeSerializer):
    # write_only is required to prevent errors when reading from OTP Object for the attr
    email = serializers.CharField(max_length=100, required=True, write_only=True)

    class Meta:
        fields = OTPVerifyCodeSerializer.Meta.fields + ("email",)
        model = OTPVerifyCodeSerializer.Meta.model

# add path to Serializer to django settings
OTP_VERIFICATION_SERIALIZER = "full.path.NewOTPVerifyCodeSerializer"
```

## Developer Guide

1. Clone github repo `git clone [url]`

2. `pipenv install --dev`

3. `pre-commit install`

4. Run unit tests `pytest`


