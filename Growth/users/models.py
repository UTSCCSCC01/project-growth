from django.db import models
from django.contrib.auth.models import AbstractUser
from company_page.models import Company


class User(AbstractUser):
    
    nickname = models.CharField(max_length=50, blank=True)
    
    ROLE_CHOICES = (
        ('Partner','Partner'),('Student','Student'),('Instructor','Instructor'),
    )
    role = models.CharField(max_length=20, default='---Select Role---', choices= ROLE_CHOICES)

    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)

    company_role = models.CharField( # Role in a company
        choices=[
            ("admin", "admin"),
            ("member", "member"),
            ("pending_member", "pending_member") # Requested to be an member but have not been approved
        ],
        max_length=100,
        default="member"
    )

    class Meta(AbstractUser.Meta):
        pass


    
