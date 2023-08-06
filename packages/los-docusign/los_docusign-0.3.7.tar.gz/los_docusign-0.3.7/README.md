# Django-DocuSign
Django wrapper app for DocuSign functionalities

`pip install django-docusign`

## Running Tests
We have a unit test defined for testing the los application.
This can be executed using the below command.

```
python manage.py test
```

## Usage
In order to use the system you must add los_docusign.apps.LosDocusignConfig to your installed apps in your settings.py file.
```python
INSTALLED_APPS = [
    'los_docusign'
]
```

Test file has the sample implementation of the test_app

## Functions in client.py
1.  generate_docusign_preview_url(dict)

    Params required in dict:
    -   "envelope_id"
    -   "authentication_method"
    -   "email"
    -   "user_name"
    -   "client_user_id"
    -   "return_url"

2. create_envelope(payload)

    Params required:
    -   DocuSign payload in JSON format

3. download_docusign_document(dict)

    Params required in dict:
    -   "envelope_id"
    -   "doc_download_option"
        -   Valid Values:
            1. archive - If the document to be downloaded in zip format.
            2. combined - If the document to be downloaded as a combined document.

4. process_docusign_webhook(xml_string)

    Params required:
    -   Webhook XML string received from Docusign.

    Response dict:
        {
            "envelopeId": "c57ec066-c5fa-4aa0-873d-6f285d70242a",
            "envelope_status": "sent",
            "recipients": [
                {
                    "recipient_id": "a7f73f21-c4ff-4bcb-97c4-b03c91b8528a",
                    "email": "test@test.com",
                    "name": "John Nash",
                    "status": "autoresponded"
                },
                {
                    "recipient_id": "511b2ad3-6650-4773-a6b4-47f64a0ccdaf",
                    "email": "jerry@test.com",
                    "name": "Jerry Tunes",
                    "status": "created"
                },
                {
                    "recipient_id": "0851505f-5af2-42df-bce4-9e0ebe8bd2e2",
                    "email": "tom@test.com",
                    "name": "Tom Tunes",
                    "status": "created"
                }
            ]
        }
