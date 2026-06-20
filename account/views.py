import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import (
    UserRole,
    User,
    RegisterUser,
    Scholarship,
    SavedScholarship,
    ScholarshipApplication,
    ScholarshipProvider,
    Notification,
    ActivityLog,
)

from django.db.models import Max, Min, Avg


from .common_functions import (
    generate_otp,
    send_otp_email,
    send_reset_otp_email
)


# ---------------------------------------------------
# USER ROLE APIs
# ---------------------------------------------------

@csrf_exempt
def create_user_role(request):
    if request.method == "POST":
        data = json.loads(request.body)

        user_role_name = data.get("user_role_name")
        user_role_description = data.get("user_role_description", "")

        user_role = UserRole.objects.create(
            user_role_name=user_role_name,
            user_role_description=user_role_description
        )

        return JsonResponse({
            "message": "User role created successfully",
            "user_role_id": user_role.user_role_id
        }, status=201)

    return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
def get_all_user_roles(request):
    if request.method == "GET":
        roles = UserRole.objects.all()

        data = list(roles.values(
            "user_role_id",
            "user_role_name",
            "user_role_description"
        ))

        return JsonResponse({"user_roles": data}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
def get_user_role_by_id(request, user_role_id):
    if request.method == "GET":

        role = UserRole.objects.filter(user_role_id=user_role_id).first()

        if not role:
            return JsonResponse({"error": "User role not found"}, status=404)

        return JsonResponse({
            "user_role": {
                "user_role_id": role.user_role_id,
                "user_role_name": role.user_role_name,
                "user_role_description": role.user_role_description
            }
        }, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
def update_user_role(request):
    if request.method == "PUT":

        data = json.loads(request.body)

        user_role_id = data.get("user_role_id")
        name = data.get("user_role_name")
        desc = data.get("user_role_description")

        role = UserRole.objects.filter(user_role_id=user_role_id).first()

        if not role:
            return JsonResponse({"error": "User role not found"}, status=404)

        role.user_role_name = name
        role.user_role_description = desc
        role.save()

        return JsonResponse({"message": "Updated successfully"}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
def delete_user_role_update(request):
    if request.method == "DELETE":

        data = json.loads(request.body)
        user_role_id = data.get("user_role_id")

        role = UserRole.objects.filter(user_role_id=user_role_id).first()

        if not role:
            return JsonResponse({"error": "User role not found"}, status=404)

        role.is_deleted = True
        role.save()

        return JsonResponse({"message": "Deleted successfully"}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=400)


# ---------------------------------------------------
# USER + OTP SYSTEM
# ---------------------------------------------------

@csrf_exempt
def create_user(request):
    if request.method == "POST":

        data = json.loads(request.body)

        full_name = data.get("full_name")
        email = data.get("email")
        phone_number = data.get("phone_number")
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        user_role_id = data.get("user_role_id")

        if password != confirm_password:
            return JsonResponse({"error": "Passwords do not match"}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already exists"}, status=400)

        role = UserRole.objects.filter(user_role_id=user_role_id).first()

        if not role:
            return JsonResponse({"error": "User role not found"}, status=404)

        user = User.objects.create(
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            password=password,
            confirm_password=confirm_password,
            user_role=role
        )

        otp = generate_otp()

        user.email_otp = otp
        user.save()

        email_response = send_otp_email(email, full_name, otp)

        if email_response["success"]:
            return JsonResponse({
                "message": "User created and OTP sent successfully",
                "user_id": user.user_id
            }, status=201)

        return JsonResponse({
            "error": "User created but OTP failed",
            "details": email_response["error"]
        }, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
def verify_email_otp(request):
    if request.method == "POST":

        data = json.loads(request.body)

        email = data.get("email")
        otp = data.get("otp")

        if not email or not otp:
            return JsonResponse({"error": "Email and OTP required"}, status=400)

        user = User.objects.filter(email=email).first()

        if not user:
            return JsonResponse({"error": "User not found"}, status=404)

        if user.email_otp == otp:

            user.email_otp = None
            user.save()

            return JsonResponse({
                "message": "Email verified successfully"
            }, status=200)

        return JsonResponse({"error": "Invalid OTP"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=400)



@csrf_exempt
def get_active_user_roles(request):
    if request.method == 'GET':
        active_user_roles = UserRole.objects.filter(is_deleted=False)
        
        active_user_roles_data = list(active_user_roles.values('user_role_name', 'user_role_id', 'user_role_description'))
        return JsonResponse({'active_user_roles': active_user_roles_data }, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method. only GET is allowed.'}, status=400)
    
@csrf_exempt
def get_inactive_user_roles(request):
    if request.method == 'GET':
        inactive_user_roles = UserRole.objects.exclude(is_deleted=False)
        
        inactive_user_roles_data = list(inactive_user_roles.values('user_role_name', 'user_role_id', 'user_role_description'))
        return JsonResponse({'inactive_user_roles': inactive_user_roles_data }, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method. only GET is allowed.'}, status=400)
    
@csrf_exempt
def get_user_roles_order_by_asc(request):
    if request.method == 'GET':
        user_roles = UserRole.objects.all().order_by('user_role_name')

        user_roles_data = list(user_roles.values('user_role_name', 'user_role_id', 'user_role_description'))
        return JsonResponse({'user_roles': user_roles_data }, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method. only GET is allowed.'}, status=400)
    
@csrf_exempt
def get_user_roles_order_by_desc(request):
    if request.method == 'GET':
        user_roles = UserRole.objects.all().order_by('-user_role_name')

        user_roles_data = list(user_roles.values('user_role_name', 'user_role_id', 'user_role_description'))
        return JsonResponse({'user_roles': user_roles_data }, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method. only GET is allowed.'}, status=400)
    
@csrf_exempt
def create_scholarship(request):

    if request.method == "POST":

        data = json.loads(request.body)

        scholarship = Scholarship.objects.create(
            scholarship_name=data.get("scholarship_name"),
            provider_name=data.get("provider_name"),
            amount=data.get("amount"),
            category=data.get("category"),
            state=data.get("state"),
            education_level=data.get("education_level"),
            eligibility=data.get("eligibility"),
            description=data.get("description"),
            application_deadline=data.get("application_deadline")
        )

        return JsonResponse({
            "message": "Scholarship created successfully",
            "scholarship_id": scholarship.scholarship_id
        }, status=201)

    return JsonResponse({
        "error": "Invalid request method"
    }, status=400)



@csrf_exempt
def get_all_scholarships(request):

    if request.method == "GET":

        scholarships = Scholarship.objects.filter(
            is_deleted=False
        )

        data = list(
            scholarships.values(
                "scholarship_id",
                "scholarship_name",
                "provider_name",
                "amount",
                "category",
                "state",
                "education_level",
                "application_deadline"
            )
        )

        return JsonResponse({
            "scholarships": data
        }, status=200)

    return JsonResponse({
        "error": "Invalid request method"
    }, status=400)
    
@csrf_exempt
def get_scholarship_by_id(request, scholarship_id):

    if request.method == "GET":

        scholarship = Scholarship.objects.filter(
            scholarship_id=scholarship_id,
            is_deleted=False
        ).first()

        if not scholarship:
            return JsonResponse({
                "error": "Scholarship not found"
            }, status=404)

        return JsonResponse({
            "scholarship": {
                "scholarship_id": scholarship.scholarship_id,
                "scholarship_name": scholarship.scholarship_name,
                "provider_name": scholarship.provider_name,
                "amount": str(scholarship.amount),
                "category": scholarship.category,
                "state": scholarship.state,
                "education_level": scholarship.education_level,
                "eligibility": scholarship.eligibility,
                "description": scholarship.description,
                "application_deadline": str(scholarship.application_deadline)
            }
        }, status=200)

    return JsonResponse({
        "error": "Invalid request method"
    }, status=400)

@csrf_exempt
def update_scholarship(request):

    if request.method == "PUT":

        data = json.loads(request.body)

        scholarship_id = data.get("scholarship_id")

        scholarship = Scholarship.objects.filter(
            scholarship_id=scholarship_id,
            is_deleted=False
        ).first()

        if not scholarship:
            return JsonResponse({
                "error": "Scholarship not found"
            }, status=404)

        scholarship.scholarship_name = data.get(
            "scholarship_name",
            scholarship.scholarship_name
        )

        scholarship.provider_name = data.get(
            "provider_name",
            scholarship.provider_name
        )

        scholarship.amount = data.get(
            "amount",
            scholarship.amount
        )

        scholarship.category = data.get(
            "category",
            scholarship.category
        )

        scholarship.state = data.get(
            "state",
            scholarship.state
        )

        scholarship.education_level = data.get(
            "education_level",
            scholarship.education_level
        )

        scholarship.eligibility = data.get(
            "eligibility",
            scholarship.eligibility
        )

        scholarship.description = data.get(
            "description",
            scholarship.description
        )

        scholarship.application_deadline = data.get(
            "application_deadline",
            scholarship.application_deadline
        )

        scholarship.save()

        return JsonResponse({
            "message": "Scholarship updated successfully"
        }, status=200)

    return JsonResponse({
        "error": "Invalid request method"
    }, status=400)

@csrf_exempt
def delete_scholarship(request):

    if request.method == "DELETE":

        data = json.loads(request.body)

        scholarship_id = data.get("scholarship_id")

        scholarship = Scholarship.objects.filter(
            scholarship_id=scholarship_id
        ).first()

        if not scholarship:
            return JsonResponse({
                "error": "Scholarship not found"
            }, status=404)

        scholarship.is_deleted = True
        scholarship.save()

        return JsonResponse({
            "message": "Scholarship deleted successfully"
        }, status=200)

    return JsonResponse({
        "error": "Invalid request method"
    }, status=400)


@csrf_exempt
def get_saved_scholarships(request):

    if request.method == "GET":

        user_id = request.GET.get("user_id")

        saved_scholarships = SavedScholarship.objects.filter(
            user_id=user_id
        )

        data = []

        for item in saved_scholarships:

            data.append({
                "saved_id": item.saved_id,
                "scholarship_id": item.scholarship.scholarship_id,
                "scholarship_name": item.scholarship.scholarship_name,
                "provider_name": item.scholarship.provider_name,
                "amount": str(item.scholarship.amount),
                "state": item.scholarship.state,
                "category": item.scholarship.category
            })

        return JsonResponse({
            "saved_scholarships": data
        }, status=200)

    return JsonResponse({
        "error": "Invalid request method"
    }, status=400)

@csrf_exempt
def remove_saved_scholarship(request):

    if request.method == "DELETE":

        data = json.loads(request.body)

        saved_id = data.get("saved_id")

        saved_scholarship = SavedScholarship.objects.filter(
            saved_id=saved_id
        ).first()

        if not saved_scholarship:
            return JsonResponse({
                "error": "Saved scholarship not found"
            }, status=404)

        saved_scholarship.delete()

        return JsonResponse({
            "message": "Saved scholarship removed successfully"
        }, status=200)

    return JsonResponse({
        "error": "Invalid request method"
    }, status=400)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .common_functions import RegisterUserSerializer

@api_view(['POST'])
def register_user(request):
    serializer = RegisterUserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response({
            "success": True,
            "message": "User registered successfully"
        }, status=status.HTTP_201_CREATED)

    return Response({
        "success": False,
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


from .models import RegisterUser
from django.contrib.auth.hashers import check_password

@csrf_exempt
def login_user(request):
    if request.method == "POST":

        data = json.loads(request.body)

        email_or_mobile = data.get("email_or_mobile")
        password = data.get("password")

        user = RegisterUser.objects.filter(
            email=email_or_mobile
        ).first()

        if not user:
            user = RegisterUser.objects.filter(
                mobile_number=email_or_mobile
            ).first()

        if not user:
            return JsonResponse(
                {"error": "User not found"},
                status=404
            )

        if user.password != password:
            return JsonResponse(
                {"error": "Invalid password"},
                status=400
            )

        return JsonResponse({
            "message": "Login successful",
            "full_name": user.full_name,
            "email": user.email
        }, status=200)

    return JsonResponse(
        {"error": "Invalid request method"},
        status=400
    )


@csrf_exempt
def forgot_password(request):

    if request.method == "POST":

        data = json.loads(request.body)

        email = data.get("email")

        user = RegisterUser.objects.filter(
            email=email
        ).first()

        if not user:
            return JsonResponse(
                {"error": "User not found"},
                status=404
            )

        otp = generate_otp()

        user.reset_otp = otp
        user.save()

        email_response = send_reset_otp_email(
            user.email,
            user.full_name,
            otp
        )

        if email_response["success"]:

            return JsonResponse({
                "message": "Reset OTP sent successfully"
            }, status=200)

        return JsonResponse({
            "error": "Failed to send OTP"
        }, status=500)

    return JsonResponse(
        {"error": "Invalid request method"},
        status=400
    )

@csrf_exempt
def verify_reset_otp(request):

    if request.method == "POST":

        data = json.loads(request.body)

        email = data.get("email")
        otp = data.get("otp")

        user = RegisterUser.objects.filter(
            email=email
        ).first()

        if not user:
            return JsonResponse(
                {"error": "User not found"},
                status=404
            )

        if user.reset_otp != otp:
            return JsonResponse(
                {"error": "Invalid OTP"},
                status=400
            )

        return JsonResponse({
            "message": "OTP verified successfully"
        }, status=200)

    return JsonResponse(
        {"error": "Invalid request method"},
        status=400
    )

@csrf_exempt
def reset_password(request):

    if request.method == "POST":

        data = json.loads(request.body)

        email = data.get("email")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")

        user = RegisterUser.objects.filter(
            email=email
        ).first()

        if not user:
            return JsonResponse(
                {"error": "User not found"},
                status=404
            )

        if new_password != confirm_password:
            return JsonResponse(
                {"error": "Passwords do not match"},
                status=400
            )

        user.password = new_password
        user.reset_otp = None
        user.save()

        return JsonResponse({
            "message": "Password reset successfully"
        }, status=200)

    return JsonResponse(
        {"error": "Invalid request method"},
        status=400
    )

@csrf_exempt
def save_scholarship(request):

    if request.method == "POST":

        data = json.loads(request.body)

        user_id = data.get("user_id")
        scholarship_id = data.get("scholarship_id")

        user = RegisterUser.objects.filter(
            id=user_id
        ).first()

        scholarship = Scholarship.objects.filter(
            scholarship_id=scholarship_id
        ).first()

        if not user:
            return JsonResponse({
                "error": "User not found"
            }, status=404)

        if not scholarship:
            return JsonResponse({
                "error": "Scholarship not found"
            }, status=404)

        already_saved = SavedScholarship.objects.filter(
            user=user,
            scholarship=scholarship
        ).exists()

        if already_saved:
            return JsonResponse({
                "message": "Scholarship already saved"
            }, status=200)

        SavedScholarship.objects.create(
            user=user,
            scholarship=scholarship
        )

        return JsonResponse({
            "message": "Scholarship saved successfully"
        }, status=201)

    return JsonResponse({
        "error": "Invalid request method"
    }, status=400)


@csrf_exempt
def apply_scholarship(request):

    if request.method == "POST":

        data = json.loads(request.body)

        user_id = data.get("user_id")
        scholarship_id = data.get("scholarship_id")

        user = RegisterUser.objects.filter(
            id=user_id
        ).first()

        scholarship = Scholarship.objects.filter(
            scholarship_id=scholarship_id
        ).first()

        if not user:
            return JsonResponse({
                "error": "User not found"
            }, status=404)

        if not scholarship:
            return JsonResponse({
                "error": "Scholarship not found"
            }, status=404)

        already_applied = ScholarshipApplication.objects.filter(
            user=user,
            scholarship=scholarship
        ).exists()

        if already_applied:
            return JsonResponse({
                "error": "Already applied"
            }, status=400)

        application = ScholarshipApplication.objects.create(
            user=user,
            scholarship=scholarship
        )

        return JsonResponse({
            "message": "Scholarship applied successfully",
            "application_id": application.application_id
        }, status=201)

    return JsonResponse({
        "error": "Invalid request method"
    }, status=400)


@csrf_exempt
def my_applications(request):

    if request.method == "GET":

        user_id = request.GET.get("user_id")

        applications = ScholarshipApplication.objects.filter(
            user_id=user_id
        )

        data = []

        for app in applications:

            data.append({
                "application_id": app.application_id,
                "scholarship_name": app.scholarship.scholarship_name,
                "provider_name": app.scholarship.provider_name,
                "status": app.application_status,
                "applied_at": app.applied_at
            })

        return JsonResponse({
            "applications": data
        }, status=200)

    return JsonResponse({
        "error": "Invalid request method"
    }, status=400)


@csrf_exempt
def application_tracker(request, application_id):

    if request.method == "GET":

        application = ScholarshipApplication.objects.filter(
            application_id=application_id
        ).first()

        if not application:
            return JsonResponse({
                "error": "Application not found"
            }, status=404)

        return JsonResponse({
            "application_id": application.application_id,
            "scholarship_name": application.scholarship.scholarship_name,
            "provider_name": application.scholarship.provider_name,
            "status": application.application_status,
            "applied_at": application.applied_at
        }, status=200)

    return JsonResponse({
        "error": "Invalid request method"
    }, status=400)

@csrf_exempt
def provider_dashboard(request):

    if request.method == "GET":

        total_scholarships = Scholarship.objects.filter(
            is_deleted=False
        ).count()

        total_applications = ScholarshipApplication.objects.count()

        pending_applications = ScholarshipApplication.objects.filter(
            application_status="Pending"
        ).count()

        approved_applications = ScholarshipApplication.objects.filter(
            application_status="Approved"
        ).count()

        return JsonResponse({

            "total_scholarships": total_scholarships,

            "total_applications": total_applications,

            "pending_applications": pending_applications,

            "approved_applications": approved_applications

        }, status=200)

    return JsonResponse({
        "error": "Invalid request method"
    }, status=400)

@csrf_exempt
def provider_scholarships(request):

    if request.method == "GET":

        scholarships = Scholarship.objects.filter(
            is_deleted=False
        )

        data = []

        for scholarship in scholarships:

            data.append({

                "scholarship_id": scholarship.scholarship_id,
                "scholarship_name": scholarship.scholarship_name,
                "provider_name": scholarship.provider_name,
                "amount": str(scholarship.amount),
                "category": scholarship.category,
                "state": scholarship.state,
                "education_level": scholarship.education_level,
                "application_deadline": scholarship.application_deadline

            })

        return JsonResponse({
            "scholarships": data
        }, status=200)

    return JsonResponse({
        "error": "Invalid request method"
    }, status=400)


@csrf_exempt
def manage_applications(request):

    if request.method == "GET":

        applications = ScholarshipApplication.objects.all()

        data = []

        for application in applications:

            data.append({

                "application_id": application.application_id,

                "student_name": application.user.full_name,

                "scholarship_name":
                application.scholarship.scholarship_name,

                "status":
                application.application_status,

                "applied_at":
                application.applied_at

            })

        return JsonResponse({
            "applications": data
        }, status=200)

    return JsonResponse({
        "error": "Invalid request method"
    }, status=400)

@csrf_exempt
def application_review(request, application_id):

    if request.method == "GET":

        application = ScholarshipApplication.objects.filter(
            application_id=application_id
        ).first()

        if not application:
            return JsonResponse({
                "error": "Application not found"
            }, status=404)

        return JsonResponse({

            "application_id": application.application_id,

            "student_name":
            application.user.full_name,

            "student_email":
            application.user.email,

            "scholarship_name":
            application.scholarship.scholarship_name,

            "provider_name":
            application.scholarship.provider_name,

            "status":
            application.application_status,

            "applied_at":
            application.applied_at

        }, status=200)

    return JsonResponse({
        "error": "Invalid request method"
    }, status=400)

@csrf_exempt
def update_application_status(request):

    if request.method == "PUT":

        data = json.loads(request.body)

        application_id = data.get("application_id")
        status_value = data.get("status")

        application = ScholarshipApplication.objects.filter(
            application_id=application_id
        ).first()

        if not application:
            return JsonResponse({
                "error": "Application not found"
            }, status=404)

        application.application_status = status_value
        application.save()

        return JsonResponse({
            "message": "Application status updated successfully"
        }, status=200)

    return JsonResponse({
        "error": "Invalid request method"
    }, status=400)

@csrf_exempt
def admin_dashboard(request):

    if request.method == "GET":

        total_students = RegisterUser.objects.count()

        total_scholarships = Scholarship.objects.filter(
            is_deleted=False
        ).count()

        total_applications = ScholarshipApplication.objects.count()

        total_saved_scholarships = SavedScholarship.objects.count()

        return JsonResponse({

            "total_students": total_students,

            "total_scholarships": total_scholarships,

            "total_applications": total_applications,

            "total_saved_scholarships": total_saved_scholarships

        }, status=200)

    return JsonResponse({
        "error": "Invalid request method"
    }, status=400)

@csrf_exempt
def manage_users(request):

    if request.method == "GET":

        users = RegisterUser.objects.all()

        data = []

        for user in users:

            data.append({

                "id": user.id,

                "full_name": user.full_name,

                "email": user.email,

                "mobile_number": user.mobile_number,

                "state": user.state,

                "education_level": user.education_level,

                "category": user.category,

                "annual_family_income": str(
                    user.annual_family_income
                )

            })

        return JsonResponse({
            "users": data
        }, status=200)

    return JsonResponse({
        "error": "Invalid request method"
    }, status=400)

@csrf_exempt
def create_provider(request):

    if request.method == "POST":

        data = json.loads(request.body)

        provider = ScholarshipProvider.objects.create(

            organization_name=data.get(
                "organization_name"
            ),

            contact_person=data.get(
                "contact_person"
            ),

            email=data.get(
                "email"
            ),

            mobile_number=data.get(
                "mobile_number"
            ),

            address=data.get(
                "address"
            )

        )

        return JsonResponse({

            "message":
            "Scholarship Provider created successfully",

            "provider_id":
            provider.provider_id

        }, status=201)

    return JsonResponse({
        "error": "Invalid request method"
    }, status=400)

@csrf_exempt
def manage_providers(request):

    if request.method == "GET":

        providers = ScholarshipProvider.objects.all()

        data = []

        for provider in providers:

            data.append({

                "provider_id":
                provider.provider_id,

                "organization_name":
                provider.organization_name,

                "contact_person":
                provider.contact_person,

                "email":
                provider.email,

                "mobile_number":
                provider.mobile_number,

                "is_approved":
                provider.is_approved

            })

        return JsonResponse({
            "providers": data
        }, status=200)

    return JsonResponse({
        "error": "Invalid request method"
    }, status=400)

@csrf_exempt
def approve_provider(request):

    if request.method == "PUT":

        data = json.loads(request.body)

        provider_id = data.get(
            "provider_id"
        )

        provider = ScholarshipProvider.objects.filter(
            provider_id=provider_id
        ).first()

        if not provider:

            return JsonResponse({
                "error":
                "Provider not found"
            }, status=404)

        provider.is_approved = True

        provider.save()

        return JsonResponse({

            "message":
            "Provider approved successfully"

        }, status=200)

    return JsonResponse({
        "error": "Invalid request method"
    }, status=400)

@csrf_exempt
def admin_manage_scholarships(request):

    if request.method == "GET":

        scholarships = Scholarship.objects.filter(
            is_deleted=False
        )

        data = []

        for scholarship in scholarships:

            data.append({

                "scholarship_id":
                scholarship.scholarship_id,

                "scholarship_name":
                scholarship.scholarship_name,

                "provider_name":
                scholarship.provider_name,

                "amount":
                str(scholarship.amount),

                "category":
                scholarship.category,

                "state":
                scholarship.state,

                "education_level":
                scholarship.education_level,

                "application_deadline":
                scholarship.application_deadline

            })

        return JsonResponse({
            "scholarships": data
        }, status=200)

    return JsonResponse({
        "error": "Invalid request method"
    }, status=400)

@csrf_exempt
def reports_analytics(request):

    if request.method == "GET":

        total_students = RegisterUser.objects.count()

        total_providers = ScholarshipProvider.objects.count()

        total_scholarships = Scholarship.objects.filter(
            is_deleted=False
        ).count()

        total_applications = ScholarshipApplication.objects.count()

        approved_applications = ScholarshipApplication.objects.filter(
            application_status="Approved"
        ).count()

        rejected_applications = ScholarshipApplication.objects.filter(
            application_status="Rejected"
        ).count()

        pending_applications = ScholarshipApplication.objects.filter(
            application_status="Pending"
        ).count()

        return JsonResponse({

            "total_students": total_students,

            "total_providers": total_providers,

            "total_scholarships": total_scholarships,

            "total_applications": total_applications,

            "approved_applications": approved_applications,

            "rejected_applications": rejected_applications,

            "pending_applications": pending_applications

        }, status=200)

    return JsonResponse({
        "error": "Invalid request method"
    }, status=400)

@csrf_exempt
def create_notification(request):

    if request.method == "POST":

        data = json.loads(request.body)

        notification = Notification.objects.create(

            title=data.get("title"),

            message=data.get("message")

        )

        return JsonResponse({

            "message":
            "Notification created successfully",

            "notification_id":
            notification.notification_id

        }, status=201)

    return JsonResponse({
        "error": "Invalid request method"
    }, status=400)

@csrf_exempt
def get_notifications(request):

    if request.method == "GET":

        notifications = Notification.objects.all().order_by(
            "-created_at"
        )

        data = []

        for notification in notifications:

            data.append({

                "notification_id":
                notification.notification_id,

                "title":
                notification.title,

                "message":
                notification.message,

                "created_at":
                notification.created_at

            })

        return JsonResponse({
            "notifications": data
        }, status=200)

    return JsonResponse({
        "error": "Invalid request method"
    }, status=400)

@csrf_exempt
def create_activity_log(request):

    if request.method == "POST":

        data = json.loads(request.body)

        log = ActivityLog.objects.create(
            activity=data.get("activity")
        )

        return JsonResponse({
            "message": "Activity log created",
            "log_id": log.log_id
        }, status=201)

    return JsonResponse({
        "error": "Invalid request method"
    }, status=400)

@csrf_exempt
def get_activity_logs(request):

    if request.method == "GET":

        logs = ActivityLog.objects.all().order_by(
            "-created_at"
        )

        data = []

        for log in logs:

            data.append({

                "log_id": log.log_id,

                "activity": log.activity,

                "created_at": log.created_at

            })

        return JsonResponse({
            "activity_logs": data
        }, status=200)

    return JsonResponse({
        "error": "Invalid request method"
    }, status=400)

#  SELECT ALL

def get_all_scholarships(request):
    data = Scholarship.objects.all().values(
        "scholarship_id",
        "scholarship_name",
        "amount"
    )
    return JsonResponse({"data": list(data)})



#  FILTER

def filter_scholarships(request):
    data = Scholarship.objects.filter(state="Maharashtra").values()
    return JsonResponse({"data": list(data)})



#  VALUES

def values_demo(request):
    data = Scholarship.objects.values("scholarship_name", "amount")
    return JsonResponse({"data": list(data)})


#  VALUES_LIST

def values_list_demo(request):
    data = Scholarship.objects.values_list("scholarship_name", "amount")
    return JsonResponse({"data": list(data)})



#  VALUES_LIST FLAT

def values_list_flat_demo(request):
    data = Scholarship.objects.values_list("scholarship_name", flat=True)
    return JsonResponse({"data": list(data)})



#  COUNT

def count_demo(request):
    total = Scholarship.objects.count()
    return JsonResponse({"total_scholarships": total})

#  UPDATE

@csrf_exempt
def update_demo(request):
    if request.method == "PUT":
        data = json.loads(request.body)

        Scholarship.objects.filter(
            scholarship_id=data.get("id")
        ).update(amount=data.get("amount"))

        return JsonResponse({"message": "Updated successfully"})

    return JsonResponse({"error": "Invalid method"})

#  SAVE

@csrf_exempt
def save_demo(request):
    if request.method == "PUT":
        data = json.loads(request.body)

        obj = Scholarship.objects.get(
            scholarship_id=data.get("id")
        )
        obj.amount = data.get("amount")
        obj.save()

        return JsonResponse({"message": "Saved successfully"})

    return JsonResponse({"error": "Invalid method"})

#  MAX / MIN / AVG

def aggregate_demo(request):
    data = Scholarship.objects.aggregate(
        max_amount=Max("amount"),
        min_amount=Min("amount"),
        avg_amount=Avg("amount")
    )
    return JsonResponse(data)