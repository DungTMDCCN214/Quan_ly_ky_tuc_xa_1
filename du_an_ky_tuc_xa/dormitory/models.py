# dormitory/models.py
from django.db import models
from accounts.models import CustomUser

class Building(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    total_floors = models.IntegerField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class RoomType(models.Model):
    name = models.CharField(max_length=100)  # Phòng đơn, đôi, tập thể
    capacity = models.IntegerField()
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.capacity} người"

class Room(models.Model):
    room_number = models.CharField(max_length=10)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    floor = models.IntegerField()
    status_choices = (
        ('available', 'Còn trống'),
        ('occupied', 'Đã thuê'),
        ('maintenance', 'Bảo trì'),
    )
    status = models.CharField(max_length=20, choices=status_choices, default='available')
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['building', 'room_number']
    
    def __str__(self):
        return f"{self.building.name} - Phòng {self.room_number}"

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    university = models.CharField(max_length=200)
    faculty = models.CharField(max_length=100)
    course = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    def __str__(self):
        return f"{self.student_id} - {self.user.get_full_name()}"

class Contract(models.Model):
    contract_number = models.CharField(max_length=20, unique=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    status_choices = (
        ('active', 'Đang hoạt động'),
        ('expired', 'Đã hết hạn'),
        ('terminated', 'Đã chấm dứt'),
    )
    status = models.CharField(max_length=20, choices=status_choices, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.contract_number} - {self.student}"