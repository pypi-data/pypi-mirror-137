Installation
======================


1. You'll need to install ``ob-dj-otp`` using pip:

.. code-block:: bash

   pip install ob-dj-otp


2. This app is using ``django-rest-framework`` to provide API endpoints, which means the app will need to be added to the list of installed apps.

   The app will automatically install ``django-rest-framework`` if it's not installed.
   ``ob_dj_otp`` also needs to be added to the list of installed apps:


.. code-block:: python
   :emphasize-lines: 4

   # settings.py
   INSTALLED_APPS = [
        ...
        'django_otp',
        'rest_framework'
   ]
   # Setting Twilio as SMS Provider
   OTP_PROVIDER = os.environ.get("OTP_PROVIDER", "twilio")
   # Passing Twilio Verify Service-ID
   OTP_TWILIO_SERVICE = os.environ.get("OTP_PROVIDER")



.. code-block:: bash

   # Twilio Client will require passing following env variables
   export TWILIO_ACCOUNT_SID=XYZ
   export TWILIO_AUTH_TOKEN=xyz
   # We can configure the way the package sends the SMS through these env variables
   # for the Twilio verification service we have to export this one
   export OTP_TWILIO_SERVICE=xyz
   # for the Twilio messaging service we have to export this one
   export TWILIO_MESSAGING_SERVICE_ID=xyz

3. Include `Django On Demand URLconf` in your project ``urls.py`` like this:

.. code-block:: python

   # urls.py
   path('otp/', include('ob_dj_otp.apis.otp.urls')),


4. Run ``python manage.py migrate`` to create the models.


5. Visit http://127.0.0.1:8000/otp/ to test the new API.