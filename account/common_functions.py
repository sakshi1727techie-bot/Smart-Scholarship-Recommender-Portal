import random
from django.core.mail import send_mail
from django.conf import settings


def generate_otp():
    """
    Generate a secure 6-digit OTP
    """
    otp = random.randint(100000, 999999)
    return str(otp)

def send_reset_otp_email(email, full_name, otp):

    subject = "Password Reset OTP - ScholarStep"

    message = f"""
Dear {full_name},

You requested to reset your password.

Your Password Reset OTP is:

{otp}

Do not share this OTP with anyone.

Regards,
ScholarStep Team
"""

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )

        return {"success": True}

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def send_otp_email(email, full_name, otp):
    """
    Send OTP email to user with proper formatting and error handling
    """

    subject = "Email Verification OTP - Smart Scholarship Recommender Portal"

    message = f"""
Dear {full_name},

Welcome to Smart Scholarship Recommender Portal!

To complete your email verification, please use the OTP below:

OTP: {otp}

This OTP is valid for a limited time. Do not share it with anyone.

If you did not request this, please ignore this email.

Regards,
Smart Scholarship Recommender Portal Team
"""

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )
        return {
            "success": True,
            "message": "OTP email sent successfully",
            "otp": otp
        }

    except Exception as e:
        return {
            "success": False,
            "message": "Failed to send OTP email",
            "error": str(e)
        }
    
from rest_framework import serializers
from .models import RegisterUser

class RegisterUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = RegisterUser
        fields = [
            'full_name',
            'email',
            'mobile_number',
            'state',
            'education_level',
            'category',
            'annual_family_income',
            'password',
            'confirm_password'
        ]

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({
                "confirm_password": "Passwords do not match"
            })
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return RegisterUser.objects.create(**validated_data)