from flask_request_validator import AbstractRule
from email_validator import validate_email, EmailNotValidError


class EmailRule(AbstractRule):

    def validate(self, value):
        errors = []
    
        try:
            # Validate.
            validate_email(value)

        except EmailNotValidError as e:

            errors.append(str(e))
   

        return errors
