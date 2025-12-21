from django.db import models
from django.db.models.functions import Length
from django.contrib.auth.models import BaseUserManager
from django.db.models import Count, Max, Min, Case, When, Value, CharField


class CustomManagerProxy(models.Manager):
    
    def get_queryset(self):
        return super().get_queryset().filter(post__isnull=True)
    
    
class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields):
        
        if not email:
            raise ValueError(('The Email must be set'))
        
        email = self.normalize_email(email)
        
        if 'username' not in extra_fields:
            extra_fields['username'] = email.split('@')[0]
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)
    
    def users_in_emails(self, email_list):
        return self.filter(email__in=email_list)
    
    def users_with_domain(self, domain):
        return self.filter(email__icontains=domain) # LIKE '%domain'
    
    def users_without_first_name(self):
        return self.filter(first_name__isnull=True)
    
    def users_created_before(self, date):
        return self.filter(created_at__lte=date)
    
    def users_created_after(self, date):
        return self.filter(created_at__gte=date)
    
    def email_exists(self, email):
        return self.filter(email=email).exists()
    
    def count_by_group(self, group):
        return self.filter(groups=group).count()
    
    def exclude_group(self, group):
        return self.exclude(groups=group) # not in
    
    def user_statistics(self):
        return self.aggregate(
            total_users=Count('id'),
            latest_creation=Max('created_at'),
            earliest_creation=Min('created_at'),
        )
    
    def users_with_email_length(self):
        return self.annotate(email_length=Length('email'))
    
    def users_with_group_display(self): 
        return self.annotate(
            group_display=Case(
                When(groups='A', then=Value('Admin')),
                When(groups='B', then=Value('Basic User')),
                When(groups='C', then=Value('Premium User')),
                default=Value('Unknown'),
                output_field=CharField()
            )
        )

    def users_with_profile(self):
        return self.all() 
    
    def users_with_profile_optimized(self):
        return self.select_related('profile')
    
    def users_with_groups_prefetched(self):
        return self.prefetch_related('groups')