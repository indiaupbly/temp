from datetime import date
from django.test import TestCase
from accounts.models import User, UserRole
from academic.models import AcademicYear, Holiday
from academic.constants import HolidayTypeChoices
from academic.services import calculate_working_days
from school.constants import BoardChoices, SchoolTypeChoices
from school.models import School

class AcademicServiceTests(TestCase):
    def test_working_days_excludes_holiday_records(self):
        admin = User.objects.create_user(email="admin2@example.com", password="pass12345", name="Admin", role=UserRole.SCHOOL_ADMIN)
        school = School.objects.create(school_name="Test School 2", email="school2@example.com", phone_number="1234567891", address="Addr", city="City", district="Dist", state="State", pincode="123456", board=BoardChoices.CBSE, school_type=SchoolTypeChoices.PRIVATE, principal_name="P", principal_phone="1234567890", principal_email="p2@example.com", admin=admin)
        year = AcademicYear.objects.create(school=school, name="2026-27", start_date=date(2026,1,1), end_date=date(2026,1,3), is_current=True)
        Holiday.objects.create(school=school, academic_year=year, date=date(2026,1,2), title="X", type=HolidayTypeChoices.HOLIDAY)
        self.assertEqual(calculate_working_days(school, year), 2)
