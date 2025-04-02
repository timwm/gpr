from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    AbstractUser,
    #BaseUserManager,
    UserManager,
    Permission,
    Group,
)
from django.utils.translation import gettext_lazy as _  # Updated import
from django.db import models
from django.core.exceptions import ValidationError

from .department import Department  # Ensure this import is correct


class UserManager(UserManager):
    def create_user(self, username, email, password=None, **kwargs):
        """Create and return a `User` with an email, username and password."""
        if username is None:
            raise TypeError("Users must have a username.")
        if email is None:
            raise TypeError("Users must have an email.")

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError("Superusers must have a password.")
        if email is None:
            raise TypeError("Superusers must have an email.")
        if username is None:
            raise TypeError("Superusers must have an username.")

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class Role(models.Model):
    """
    Example: Admin <- Lecturer <- Student

    Lecturer.base_role = Student
    Admin.base_role = Lecturer
    """
    ROLE_STUDENT = 'Student'
    ROLE_LECTURER = 'Lecturer'
    ROLE_REGISTRAR = 'Registrar'
    ROLE_ADMINISTRATOR = 'Administrator'

    name = models.CharField(unique=True, max_length=64)
    permissions = models.ManyToManyField(Permission, blank=True)
    description = models.CharField(max_length=256, blank=False, default='')
    # base_role = models.ForeignKey('self', # unique=True, # editable=False,
    #     null=True, blank=True, related_name='derived_roles', on_delete=models.SET_NULL
    # )

    # def get_permissions(self):
    #     """Recursively get all permissions, including from parent roles."""
    #     permissions = self.permissions.all()
    #     base_role = self.base_role
    #     while base_role:
    #         permissions.union(base_role.permissions.all())
    #         base_role = base_role.base_role

    #     return permissions

    def save(self, *args, **kwargs):
        if self.base_role and self.derived_roles.filter(pk=self.base_role.pk).exists():
            raise ValidationError("Can not create a backward relationship if a forward relationship exists")
        super().save(*args, **kwargs)

    def __str__(self):
        return "%s" % (self.name)


#class User(AbstractBaseUser, PermissionsMixin):
#    username = models.CharField(db_index=True, max_length=255, unique=True)
#    email = models.EmailField(db_index=True, unique=True)
#    is_active = models.BooleanField(default=True)
#    is_staff = models.BooleanField(default=False)
#    date = models.DateTimeField(auto_now_add=True)
#
#    USERNAME_FIELD = "email"
#    REQUIRED_FIELDS = ["username"]
#
#    objects = UserManager()
#
#    def __str__(self):
#        return f"{self.email}"


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    email = models.EmailField(_("email address"), db_index=True, unique=True)
    roles = models.ManyToManyField(Role,
        blank=True,
        related_name="users",
        # verbose_name=_("roles"),
    )
    updated_at = models.DateTimeField(null=True)
    
    objects = UserManager()

    def __str__(self):
        return "@%s" % self.username or self.email


class Student(User):
    """
    The student table
    """
    # user = models.OneToOneField(
    #     User,
    #     primary_key=True,
    #     related_name="%(class)s_details",
    #     on_delete=models.CASCADE,
    # )
    student_no = models.CharField(max_length=32, blank=False)

    # def __str__(self):
    #     return "Student Table"



class Staff(User):
    """
    The staff table
    """
    # user = models.OneToOneField(
    #     User,
    #     primary_key=True,
    #     related_name="%(class)s_details",
    #     on_delete=models.CASCADE,
    # )
    departments = models.ManyToManyField(Department,
        related_name='staff'
    )


    # def __str__(self):
    #     return "Staff Table"
