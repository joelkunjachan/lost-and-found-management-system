from django.db import models

class registerr(models.Model):
    name=models.CharField(max_length=150)
    email=models.CharField(max_length=150)
    phone=models.CharField(max_length=150)
    password=models.CharField(max_length=150)
    student_id=models.FileField(max_length=150)
    status=models.FileField(max_length=150)
    




class lost_table(models.Model):
    user_id=models.CharField(max_length=150) 
    itemname=models.CharField(max_length=150)
    category_id=models.CharField(max_length=150)
    title=models.CharField(max_length=150)
    description=models.CharField(max_length=150)
    item_type=models.CharField(max_length=150)
    location=models.CharField(max_length=150)
    date=models.CharField(max_length=150)
    status=models.CharField(max_length=150)
    item_image=models.FileField(max_length=150)
    image_features = models.BinaryField(null=True, blank=True)

class found_table(models.Model):
    user_id=models.CharField(max_length=150)
    itemname=models.CharField(max_length=150)
    category_id=models.CharField(max_length=150)
    title=models.CharField(max_length=150)
    description=models.CharField(max_length=150)
    item_type=models.CharField(max_length=150)
    location=models.CharField(max_length=150)
    date=models.CharField(max_length=150)
    status=models.CharField(max_length=150)
    item_image=models.FileField(max_length=150)
    image_features = models.BinaryField(null=True, blank=True)

class cat_tbl(models.Model):
    category_name=models.CharField(max_length=150)

class item_match(models.Model):
    lost_item = models.ForeignKey(
        'lost_table',
        on_delete=models.CASCADE,
        related_name='lost_matches'
    )
    found_item = models.ForeignKey(
        'found_table',
        on_delete=models.CASCADE,
        related_name='found_matches'
    )
    similarity_score = models.FloatField()
    matched_on = models.DateTimeField(auto_now_add=True)
    # Request workflow fields
    request_status = models.CharField(
        max_length=20,
        choices=(
            ('none', 'None'),
            ('requested', 'Requested'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
        ),
        default='none'
    )
    requested_by = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        unique_together = ('lost_item', 'found_item')
  
