from django.db import models
from django.contrib.auth.hashers import make_password, check_password


# ---------------------------------------------------
# USER ROLE MODEL
# ---------------------------------------------------
class UserRole(models.Model):
    user_role_id = models.AutoField(primary_key=True)
    user_role_name = models.CharField(max_length=100)
    user_role_description = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_role_name


# ---------------------------------------------------
# USER MODEL
# ---------------------------------------------------
class User(models.Model):
    user_id = models.AutoField(primary_key=True)

    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)

    password = models.CharField(max_length=255)
    confirm_password = models.CharField(max_length=255)  # ✅ sir requirement

    email_otp = models.CharField(max_length=6, blank=True, null=True)
    mobile_otp = models.CharField(max_length=6, blank=True, null=True)

    is_email_verified = models.BooleanField(default=False)

    user_role = models.ForeignKey(UserRole, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ---------------------------------------------------
    # PASSWORD HASHING
    # ---------------------------------------------------
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    # ---------------------------------------------------
    # PASSWORD CHECK
    # ---------------------------------------------------
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    # ---------------------------------------------------
    # STRING REPRESENTATION
    # ---------------------------------------------------
    def __str__(self):
        return self.full_name


# from django.db import models

class RegisterUser(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, unique=True)
    state = models.CharField(max_length=100)
    education_level = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    annual_family_income = models.DecimalField(max_digits=10, decimal_places=2)
    password = models.CharField(max_length=255)
    reset_otp = models.CharField(max_length=6, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    

class Scholarship(models.Model):

    scholarship_id = models.AutoField(primary_key=True)

    scholarship_name = models.CharField(max_length=255)

    provider_name = models.CharField(max_length=255)

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    category = models.CharField(max_length=100)

    state = models.CharField(max_length=100)

    education_level = models.CharField(max_length=100)

    eligibility = models.TextField()

    description = models.TextField()

    application_deadline = models.DateField()

    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.scholarship_name
    
class SavedScholarship(models.Model):

    saved_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        RegisterUser,
        on_delete=models.CASCADE
    )

    scholarship = models.ForeignKey(
        Scholarship,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.full_name} - {self.scholarship.scholarship_name}"
    
class ScholarshipApplication(models.Model):

    application_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        RegisterUser,
        on_delete=models.CASCADE
    )

    scholarship = models.ForeignKey(
        Scholarship,
        on_delete=models.CASCADE
    )

    application_status = models.CharField(
        max_length=50,
        default="Pending"
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.full_name} - {self.scholarship.scholarship_name}"
    

class ScholarshipProvider(models.Model):

    provider_id = models.AutoField(primary_key=True)

    organization_name = models.CharField(max_length=255)

    contact_person = models.CharField(max_length=255)

    email = models.EmailField(unique=True)

    mobile_number = models.CharField(max_length=15)

    address = models.TextField()

    is_approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.organization_name
    
class Notification(models.Model):

    notification_id = models.AutoField(primary_key=True)

    title = models.CharField(max_length=255)

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class ActivityLog(models.Model):

    log_id = models.AutoField(primary_key=True)

    activity = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.activity