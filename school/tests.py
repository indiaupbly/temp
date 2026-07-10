from django.test import TestCase
from accounts.models import User, UserRole
from school.constants import BoardChoices, SchoolTypeChoices
from school.models import School

class SchoolModelTests(TestCase):
    def test_school_code_is_generated(self):
        admin = User.objects.create_user(email="admin@example.com", password="pass12345", name="Admin", role=UserRole.SCHOOL_ADMIN)
        school = School.objects.create(school_name="Test School", email="school@example.com", phone_number="1234567890", address="Addr", city="City", district="Dist", state="State", pincode="123456", board=BoardChoices.CBSE, school_type=SchoolTypeChoices.PRIVATE, principal_name="P", principal_phone="1234567890", principal_email="p@example.com", admin=admin)
        self.assertEqual(school.school_code, "SCH0001")
