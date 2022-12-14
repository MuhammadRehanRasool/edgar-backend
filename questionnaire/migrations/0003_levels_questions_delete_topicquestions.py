# Generated by Django 4.0.4 on 2022-10-26 04:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0002_topicquestions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Levels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1028)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=1028)),
                ('optionA', models.CharField(max_length=1028)),
                ('optionB', models.CharField(max_length=1028)),
                ('optionC', models.CharField(max_length=1028)),
                ('optionD', models.CharField(max_length=1028)),
                ('answer', models.CharField(max_length=1028)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire.levels')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire.topic')),
            ],
        ),
        migrations.DeleteModel(
            name='TopicQuestions',
        ),
    ]
