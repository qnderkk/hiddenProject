import pytest
from pydantic import ValidationError
from app.schemas.contact import ContactForm

"""
Тестирование схемы формы обратной связи (ContactForm):
- Проверка обязательных полей: имя, email, тема и сообщение.
- Валидация длины полей: проверка того, что слишком короткие имена (менее 2 символов) не проходят валидацию.
"""

def test_contact_form_valid():
    data = {
        "name": "Ivan",
        "email": "ivan@test.com",
        "subject": "Question",
        "message": "How to buy?"
    }
    form = ContactForm(**data)
    assert form.subject == "Question"

def test_contact_form_short_name():
    """Имя должно быть не менее 2 символов"""
    data = {"name": "I", "email": "i@test.com", "subject": "Subj", "message": "Text"}
    with pytest.raises(ValidationError):
        ContactForm(**data)