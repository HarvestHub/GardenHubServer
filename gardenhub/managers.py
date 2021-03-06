import uuid
from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.template.loader import render_to_string
from gardenhub.utils import today


class OrderQuerySet(models.QuerySet):
    """
    Custom QuerySet for advanced filtering of orders.
    """
    def open(self):
        """ Orders that have not finished but also may not have begun. """
        return self.filter(end_date__gt=today()).exclude(canceled=True)

    def closed(self):
        """ Orders that have finished or were canceled. """
        completed = self.filter(end_date__lt=today())
        canceled = self.filter(canceled=True)
        return completed.union(canceled).distinct()

    def upcoming(self):
        """ Orders that have not yet begun but are scheduled to happen. """
        return self.filter(start_date__gt=today()).exclude(canceled=True)

    def active(self):
        """ Orders that are happening right now. """
        return self.filter(
            Q(end_date__gte=today()) &
            Q(start_date__lte=today())
        ).exclude(canceled=True)

    def inactive(self):
        """ All orders that aren't happening right now. """
        return self.filter(
            Q(end_date__lt=today()) |
            Q(start_date__gt=today()) |
            Q(canceled=True)
        )

    def picked_today(self):
        """ Orders that have at least one Pick from today. """
        return self.filter(plot__picks__timestamp__gte=today())

    def unpicked_today(self):
        """ Orders that have no Picks from today. """
        return self.exclude(plot__picks__timestamp__gte=today())


class UserManager(BaseUserManager):
    """
    Custom User manager because the custom User model only does auth by email.
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def get_or_invite_users(self, emails, request):
        """
        Gets or creates users from the list of emails. When a user is created
        they are sent an invitation email.
        """
        users = []

        # Loop through the list of emails
        for email in emails:
            # Get or create a user from the email
            user, created = get_user_model().objects.get_or_create(email=email)
            # If the user was just newly created...
            if created:
                # Generate a random token for account activation
                user.activation_token = str(uuid.uuid4())
                user.save()
                # Send the user an invitation email with their activation token
                inviter = request.user
                activate_url = request.build_absolute_uri(
                    '/activate/{}/'.format(user.activation_token)
                )
                email_data = {
                    'inviter': inviter,
                    'activate_url': activate_url
                }
                user.email_user(
                    subject="{} invited you to join GardenHub".format(
                        inviter.get_full_name()),
                    message=render_to_string(
                        'gardenhub/email_invitation.txt', email_data
                    ),
                    html_message=render_to_string(
                        'gardenhub/email_invitation.html', email_data
                    )
                )

            users.append(user)

        return users
