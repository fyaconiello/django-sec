# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-26 21:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('load', models.BooleanField(db_index=True, default=False, help_text='If checked, all values will be loaded for this attribute.')),
                ('total_values', models.PositiveIntegerField(blank=True, null=True)),
                ('total_values_fresh', models.BooleanField(default=False, verbose_name=b'fresh')),
            ],
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=6, max_digits=40)),
                ('start_date', models.DateField(db_index=True, help_text='If attribute implies a duration, this is the date\n            the duration begins. If the attribute implies an instance, this\n            is the exact date it applies to.')),
                ('end_date', models.DateField(blank=True, help_text='If this attribute implies a duration, this is the date\n            the duration ends.', null=True)),
                ('filing_date', models.DateField(help_text='The date this information became publically available.')),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='values', to='django_sec.Attribute')),
            ],
            options={
                'ordering': ('-attribute__total_values', '-start_date', 'attribute__name'),
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('cik', models.IntegerField(db_index=True, help_text='Central index key that uniquely identifies a filing entity.', primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, help_text='The name of the company.', max_length=100)),
                ('load', models.BooleanField(db_index=True, default=False, help_text='If checked, all values for load-enabled attributes will be loaded for this company.')),
                ('min_date', models.DateField(blank=True, db_index=True, editable=False, help_text='The oldest date of associated SEC Edgar filings\n            for this company.', null=True)),
                ('max_date', models.DateField(blank=True, db_index=True, editable=False, help_text='The most recent date of associated SEC Edgar filings\n            for this company.', null=True)),
            ],
            options={
                'verbose_name_plural': 'companies',
            },
        ),
        migrations.CreateModel(
            name='Index',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form', models.CharField(blank=True, db_index=True, help_text='The type of form the document is classified as.', max_length=10, verbose_name='form type')),
                ('date', models.DateField(db_index=True, help_text='The date the item was filed with the SEC.', verbose_name='date filed')),
                ('filename', models.CharField(db_index=True, help_text='The name of the associated financial filing.', max_length=100)),
                ('year', models.IntegerField(db_index=True)),
                ('quarter', models.IntegerField(db_index=True)),
                ('_ticker', models.CharField(blank=True, db_column=b'ticker', db_index=True, help_text='Caches the trading symbol if one is detected in the\n            filing during attribute load.', max_length=50, null=True, verbose_name='ticker')),
                ('attributes_loaded', models.BooleanField(db_index=True, default=False)),
                ('valid', models.BooleanField(db_index=True, default=True, help_text='If false, errors were encountered trying to parse the associated files.')),
                ('error', models.TextField(blank=True, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filings', to='django_sec.Company')),
            ],
            options={
                'ordering': ('-date', 'filename'),
                'verbose_name_plural': 'indexes',
            },
        ),
        migrations.CreateModel(
            name='IndexFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(db_index=True)),
                ('quarter', models.IntegerField(db_index=True)),
                ('filename', models.CharField(max_length=100)),
                ('total_rows', models.PositiveIntegerField(blank=True, null=True)),
                ('processed_rows', models.PositiveIntegerField(blank=True, null=True)),
                ('downloaded', models.DateTimeField(blank=True, null=True)),
                ('processed', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ('year', 'quarter'),
            },
        ),
        migrations.CreateModel(
            name='Namespace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, unique=True)),
                ('master', models.BooleanField(default=True, editable=False, help_text='If true, indicates this unit is the master referred to by duplicates.')),
                ('true_unit', models.ForeignKey(blank=True, help_text='Points the the unit record this record duplicates.\n            Points to itself if this is the master unit.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='django_sec.Unit')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AlterUniqueTogether(
            name='indexfile',
            unique_together=set([('year', 'quarter')]),
        ),
        migrations.AddField(
            model_name='attributevalue',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='django_sec.Company'),
        ),
        migrations.AddField(
            model_name='attributevalue',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_sec.Unit'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='namespace',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_sec.Namespace'),
        ),
        migrations.AlterUniqueTogether(
            name='index',
            unique_together=set([('company', 'form', 'date', 'filename', 'year', 'quarter')]),
        ),
        migrations.AlterIndexTogether(
            name='index',
            index_together=set([('company', 'date', 'filename'), ('year', 'quarter')]),
        ),
        migrations.AlterUniqueTogether(
            name='attributevalue',
            unique_together=set([('company', 'attribute', 'start_date', 'end_date')]),
        ),
        migrations.AlterIndexTogether(
            name='attributevalue',
            index_together=set([('company', 'attribute', 'start_date')]),
        ),
        migrations.AlterUniqueTogether(
            name='attribute',
            unique_together=set([('namespace', 'name')]),
        ),
        migrations.AlterIndexTogether(
            name='attribute',
            index_together=set([('namespace', 'name')]),
        ),
    ]
