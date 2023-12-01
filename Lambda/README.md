# HydroPico Garden Notification Lambda Function

This Lambda function sends email notifications using Amazon Simple Email Service (SES) to notify you when the soil moisture meter is reading low. It can be deployed manually, or you can deploy it automatically with the included cloudformation file

## Configuration

When deploying the Lambda function, set the following environment variables:

```python
SENDER_EMAIL = os.environ['SENDER_EMAIL']
RECIPIENT_EMAIL = os.environ['RECIPIENT_EMAIL']
```

This variable sets a time window after a reminder email is sent. Another reminder will not be set until
that time has elapsed to prevent sending multiple emails if you can't water the plant right away.

```
REMINDER_INTERVAL_HOURS = 6
```

## License

This Email Notification Lambda Function is licensed under the MIT License.
