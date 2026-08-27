from django.core.management.base import BaseCommand
from dataentry.models import Student

# proposed command = py manage.py insertdata

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        help = 'Insert values to the database'
        
        dataset = [
            {'roll_no': 1000, 'name': 'luffy', 'age': 19},
            {'roll_no': 1003, 'name': 'usoop', 'age': 19},
            {'roll_no': 1002, 'name': 'nami', 'age': 20}
        ]
        
        for data in dataset:
            roll_no = data['roll_no']
            exists_data = Student.objects.filter(roll_no=roll_no).exists()
            
            if not exists_data:
                Student.objects.create(roll_no=data['roll_no'], name=data['name'], age=data['age'])
            else:
                self.stdout.write(self.style.WARNING(f'Student with roll no {roll_no} already exists!'))
        self.stdout.write(self.style.SUCCESS("Successfully inserted the vaulues"))