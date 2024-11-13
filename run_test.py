import os
import django

# Set up Django settings before importing your tests
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_manage.settings')
django.setup()

# Now import your test
from chinese.tests.test_models import PoemDataTest

if __name__ == "__main__":
    test = PoemDataTest()
    test.setUp()
    test.test_create_and_retrieve() 