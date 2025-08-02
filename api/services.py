from api.models import Note

def find_my_notes(user_id: int) -> list[Note]:
    return Note.objects.filter(user_id=user_id).order_by('-created_at')
