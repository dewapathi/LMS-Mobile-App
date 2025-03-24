from django.db import models

class CourseCategory(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        db_table = "course_categories"
        
    def __str__(self):
        return self.name