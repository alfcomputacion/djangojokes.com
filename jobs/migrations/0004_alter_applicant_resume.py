# Generated by Django 4.1.3 on 2023-02-08 19:19

from django.db import migrations
import jobs.models
import private_storage.fields
import private_storage.storage.files


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_alter_applicant_resume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='resume',
            field=private_storage.fields.PrivateFileField(blank=True, help_text='PDFs only', storage=private_storage.storage.files.PrivateFileSystemStorage(), upload_to='resumes', validators=[jobs.models.validate_pdf]),
        ),
    ]