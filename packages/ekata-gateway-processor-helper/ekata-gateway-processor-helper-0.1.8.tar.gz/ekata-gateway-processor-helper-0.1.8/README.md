### Ekata Gateway Processor backend helper functions

#### Create form id

Use this function to create a form id from your backend, if successful it will return `form_id` and `created_on`.

```python
    from ekata_gateway_processor_helper import create_payment_form
    from ekata_gateway_processor_helper.exceptions import (
        InvalidAPIKeyException, InvalidProjectException, NoEnabledCurrencyException,
        InvalidArgumentsException
    )

    try:
        form_id, created_on = create_payment_form(
            amount=int(Decimal(amount) * 100) # Always provide in atomic amount of fiat currency,
            fiat_currency='USD',
            project_id='',
            api_key=''
        )
    except InvalidProjectException as e:
        print(e.message)
    except InvalidAPIKeyException as e:
        print(e.message)
    except NoEnabledCurrencyException as e:
        print(e.message)
    except InvalidArgumentsException as e:
        print(e.arguments)
```

#### Verify payment payload

Use this function to verify payment payload received after successful payment

```python
    from ekata_gateway_processor_helper import verify_payload
    if verify_payload(
        payload='' # payload received from frontend or webhook,
        signature_secret='' #payment signature secret
        ):
        # Proceed with checkout, like send success message to frontend etc
```
