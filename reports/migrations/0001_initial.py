# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'reports_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100, null=True, blank=True)),
            ('definition', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal(u'reports', ['Category'])

        # Adding model 'Feature'
        db.create_table(u'reports_feature', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=200, null=True, blank=True)),
            ('definition', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal(u'reports', ['Feature'])

        # Adding model 'Media'
        db.create_table(u'reports_media', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=300)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'reports', ['Media'])

        # Adding model 'Victim'
        db.create_table(u'reports_victim', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.CharField')(default='CIT', max_length=3)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('gender', self.gf('django.db.models.fields.CharField')(default='M', max_length=1)),
            ('age', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('education', self.gf('django.db.models.fields.CharField')(default='?', max_length=2)),
            ('social_class', self.gf('django.db.models.fields.CharField')(default='?', max_length=2)),
            ('profession', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'], null=True, blank=True)),
        ))
        db.send_create_signal(u'reports', ['Victim'])

        # Adding model 'Comment'
        db.create_table(u'reports_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='U', max_length=1)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'reports', ['Comment'])

        # Adding model 'Report'
        db.create_table(u'reports_report', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('location_text', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reports.Category'])),
            ('victim', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reports.Victim'])),
            ('aggressor', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('aggressor_category', self.gf('django.db.models.fields.CharField')(default='COP', max_length=3, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('sources', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('is_verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_closed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'reports', ['Report'])

        # Adding M2M table for field media on 'Report'
        m2m_table_name = db.shorten_name(u'reports_report_media')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('report', models.ForeignKey(orm[u'reports.report'], null=False)),
            ('media', models.ForeignKey(orm[u'reports.media'], null=False))
        ))
        db.create_unique(m2m_table_name, ['report_id', 'media_id'])

        # Adding M2M table for field features on 'Report'
        m2m_table_name = db.shorten_name(u'reports_report_features')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('report', models.ForeignKey(orm[u'reports.report'], null=False)),
            ('feature', models.ForeignKey(orm[u'reports.feature'], null=False))
        ))
        db.create_unique(m2m_table_name, ['report_id', 'feature_id'])

        # Adding M2M table for field comments on 'Report'
        m2m_table_name = db.shorten_name(u'reports_report_comments')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('report', models.ForeignKey(orm[u'reports.report'], null=False)),
            ('comment', models.ForeignKey(orm[u'reports.comment'], null=False))
        ))
        db.create_unique(m2m_table_name, ['report_id', 'comment_id'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'reports_category')

        # Deleting model 'Feature'
        db.delete_table(u'reports_feature')

        # Deleting model 'Media'
        db.delete_table(u'reports_media')

        # Deleting model 'Victim'
        db.delete_table(u'reports_victim')

        # Deleting model 'Comment'
        db.delete_table(u'reports_comment')

        # Deleting model 'Report'
        db.delete_table(u'reports_report')

        # Removing M2M table for field media on 'Report'
        db.delete_table(db.shorten_name(u'reports_report_media'))

        # Removing M2M table for field features on 'Report'
        db.delete_table(db.shorten_name(u'reports_report_features'))

        # Removing M2M table for field comments on 'Report'
        db.delete_table(db.shorten_name(u'reports_report_comments'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'reports.category': {
            'Meta': {'object_name': 'Category'},
            'definition': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'reports.comment': {
            'Meta': {'ordering': "['created_at']", 'object_name': 'Comment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'U'", 'max_length': '1'})
        },
        u'reports.feature': {
            'Meta': {'object_name': 'Feature'},
            'definition': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'reports.media': {
            'Meta': {'object_name': 'Media'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '300'})
        },
        u'reports.report': {
            'Meta': {'ordering': "['-datetime']", 'object_name': 'Report'},
            'aggressor': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'aggressor_category': ('django.db.models.fields.CharField', [], {'default': "'COP'", 'max_length': '3', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reports.Category']"}),
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['reports.Comment']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'features': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['reports.Feature']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'location_text': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'media': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['reports.Media']", 'null': 'True', 'blank': 'True'}),
            'sources': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'victim': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reports.Victim']"})
        },
        u'reports.victim': {
            'Meta': {'object_name': 'Victim'},
            'age': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'default': "'CIT'", 'max_length': '3'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'education': ('django.db.models.fields.CharField', [], {'default': "'?'", 'max_length': '2'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'M'", 'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'profession': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'social_class': ('django.db.models.fields.CharField', [], {'default': "'?'", 'max_length': '2'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']", 'null': 'True', 'blank': 'True'})
        },
        u'users.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'R'", 'max_length': '1'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['reports']