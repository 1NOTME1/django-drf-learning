from .models import UserProfile

def get_user_or_none(user_id):
    try:
        return UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        return None
