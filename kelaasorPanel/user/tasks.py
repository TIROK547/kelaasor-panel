import random
import requests
from django.core.cache import cache
from celery import shared_task

api_key = '314833384F37563970364B3766613442744D6B325877543645567353496B336A714257634F707652472B6F3D'

@shared_task
def get_verification_code(code, phone_number="09125994340"):
    """
    Sends a verification SMS code using Kavenegar API and caches the code for 2 minutes.
    """
    url = f'https://api.kavenegar.com/v1/{api_key}/sms/send.json'
    params = {
        'receptor': phone_number,
        'sender': '2000660110',
        'message': f'Your verification code on Kelaasor is {code}',
    }

    cache.set("validate_code", code, timeout=120)  # Cache code for 120 seconds

    try:
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        print(f"[Celery] Failed to send SMS: {e}")
        return {'status': 'error', 'message': str(e)}
