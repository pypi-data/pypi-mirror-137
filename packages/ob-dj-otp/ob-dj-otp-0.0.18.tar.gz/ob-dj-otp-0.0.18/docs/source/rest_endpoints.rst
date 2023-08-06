Rest Endpoints
======================

Registration
------------
The registration workflow starts with the ``OneTimePairingViewSet`` if the ``phone_number`` does not exists in the ``USER_AUTH_MODEL.phone_number`` the OTP will create a registration record with verification code.

The created code can be used in the user registration endpoint to pass the verification code and validate it.

.. code-block:: bash

    # A phone number that do not exists in User.phone_number
    curl -X POST -H "Content-Type: application/json" \
        -d '{"phone_number":"+965XXXXXXX"}'
        http://localhost/<otp-resource>
    # Will create a record in OneTimePairing model of type register

`ob-dj-otp` provides an endpoint for triggering the OneTimePairing for registration. The developer then can use `validate_verification_code` to validate that the given code for the phone number is correct.


.. code-block:: python

    # users/apis/serializers.py::UserSerializers
    class UserSerializer(serializers.ModelSerializer):
        verification_code = serializers.CharField(required=True, write_only=True)

        class Meta:
            model = get_user_model()

        def validate(self, attrs: typing.Dict):
            # validate_verification_code will mark the code as
            # used automatically if match is found
            if not validate_verification_code(
                phone_number=attrs["phone_number"],
                verification_code=attrs["verification_code"]
            ):
                raise serializers.ValidationError(_("Invalid verification code"))

            return attrs


Authentication
---------------

The authentication workflow starts with the ``OneTimePairingViewSet`` if the `phone_number` exists in the ``USER_AUTH_MODEL.phone_number`` the OTP will create an authentication record with verification code.

The created code can be used to generate authentication using the default back-end and return provider token.


.. code-block:: bash

    # A phone number that exists in User.phone_number
    # Will return 201 with success message
    curl -X POST -H "Content-Type: application/json" \
        -d '{"phone_number":"+965XXXXXXX"}'
        http://localhost/<otp-resource>
    # Submit the verification code to receive token from
    # the authentication provider
    curl -X POST -H "Content-Type: application/json" \
        -d '{"phone_number":"+965XXXXXXX", "verification_code": "11111"}'
        http://localhost/<otp-resource>