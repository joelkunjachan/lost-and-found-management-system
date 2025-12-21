# Generated manually to add request fields to item_match
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('lostandfound', '0005_item_match'),
    ]

    operations = [
        migrations.AddField(
            model_name='item_match',
            name='request_status',
            field=models.CharField(choices=[('none', 'None'), ('requested', 'Requested'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='none', max_length=20),
        ),
        migrations.AddField(
            model_name='item_match',
            name='requested_by',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
