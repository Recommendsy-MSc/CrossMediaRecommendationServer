from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, **extrafields):
        if not username:
            raise ValueError("Username Must be Set!")
        user = self.model(username=username, **extrafields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password, **extrafields):
        extrafields.setdefault('is_superuser', True)
        extrafields.setdefault('is_staff', True)
        return self.create_user(username, password, **extrafields)
