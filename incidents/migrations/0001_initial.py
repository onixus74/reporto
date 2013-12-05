# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'incidents_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100, null=True, blank=True)),
            ('definition', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal(u'incidents', ['Category'])

        # Adding model 'Feature'
        db.create_table(u'incidents_feature', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['incidents.Feature'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=200, null=True, blank=True)),
            ('definition', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('selectable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'incidents', ['Feature'])

        # Adding model 'Media'
        db.create_table(u'incidents_media', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=300)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'incidents', ['Media'])

        # Adding model 'Victim'
        db.create_table(u'incidents_victim', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.CharField')(default='C', max_length=1, null=True, blank=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(default='M', max_length=1, null=True, blank=True)),
            ('birthdate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('birthplace', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('identity_card_number', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('marital_status', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('have_children', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('social_class', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('profession', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('education', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'], null=True, blank=True)),
        ))
        db.send_create_signal(u'incidents', ['Victim'])

        # Adding model 'Comment'
        db.create_table(u'incidents_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='U', max_length=1)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'incidents', ['Comment'])

        # Adding model 'Report'
        db.create_table(u'incidents_report', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('location_text', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['incidents.Category'])),
            ('victim', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['incidents.Victim'])),
            ('aggressor', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('aggressor_category', self.gf('django.db.models.fields.CharField')(default='COP', max_length=3, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sources', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('is_verified', self.gf('django.db.models.fields.BooleanField')()),
            ('is_closed', self.gf('django.db.models.fields.BooleanField')()),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'incidents', ['Report'])

        # Adding M2M table for field media on 'Report'
        m2m_table_name = db.shorten_name(u'incidents_report_media')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('report', models.ForeignKey(orm[u'incidents.report'], null=False)),
            ('media', models.ForeignKey(orm[u'incidents.media'], null=False))
        ))
        db.create_unique(m2m_table_name, ['report_id', 'media_id'])

        # Adding M2M table for field features on 'Report'
        m2m_table_name = db.shorten_name(u'incidents_report_features')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('report', models.ForeignKey(orm[u'incidents.report'], null=False)),
            ('feature', models.ForeignKey(orm[u'incidents.feature'], null=False))
        ))
        db.create_unique(m2m_table_name, ['report_id', 'feature_id'])

        # Adding M2M table for field comments on 'Report'
        m2m_table_name = db.shorten_name(u'incidents_report_comments')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('report', models.ForeignKey(orm[u'incidents.report'], null=False)),
            ('comment', models.ForeignKey(orm[u'incidents.comment'], null=False))
        ))
        db.create_unique(m2m_table_name, ['report_id', 'comment_id'])

        # Adding model 'ThankCategory'
        db.create_table(u'incidents_thankcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100, null=True, blank=True)),
            ('definition', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal(u'incidents', ['ThankCategory'])

        # Adding model 'ThankReport'
        db.create_table(u'incidents_thankreport', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('location_text', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['incidents.ThankCategory'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'incidents', ['ThankReport'])

        # Adding M2M table for field media on 'ThankReport'
        m2m_table_name = db.shorten_name(u'incidents_thankreport_media')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('thankreport', models.ForeignKey(orm[u'incidents.thankreport'], null=False)),
            ('media', models.ForeignKey(orm[u'incidents.media'], null=False))
        ))
        db.create_unique(m2m_table_name, ['thankreport_id', 'media_id'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'incidents_category')

        # Deleting model 'Feature'
        db.delete_table(u'incidents_feature')

        # Deleting model 'Media'
        db.delete_table(u'incidents_media')

        # Deleting model 'Victim'
        db.delete_table(u'incidents_victim')

        # Deleting model 'Comment'
        db.delete_table(u'incidents_comment')

        # Deleting model 'Report'
        db.delete_table(u'incidents_report')

        # Removing M2M table for field media on 'Report'
        db.delete_table(db.shorten_name(u'incidents_report_media'))

        # Removing M2M table for field features on 'Report'
        db.delete_table(db.shorten_name(u'incidents_report_features'))

        # Removing M2M table for field comments on 'Report'
        db.delete_table(db.shorten_name(u'incidents_report_comments'))

        # Deleting model 'ThankCategory'
        db.delete_table(u'incidents_thankcategory')

        # Deleting model 'ThankReport'
        db.delete_table(u'incidents_thankreport')

        # Removing M2M table for field media on 'ThankReport'
        db.delete_table(db.shorten_name(u'incidents_thankreport_media'))


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
        u'incidents.category': {
            'Meta': {'object_name': 'Category'},
            'definition': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'incidents.comment': {
            'Meta': {'ordering': "['created_at']", 'object_name': 'Comment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'U'", 'max_length': '1'})
        },
        u'incidents.feature': {
            'Meta': {'object_name': 'Feature'},
            'definition': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['incidents.Feature']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'selectable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'incidents.media': {
            'Meta': {'object_name': 'Media'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '300'})
        },
        u'incidents.report': {
            'Meta': {'ordering': "['-datetime']", 'object_name': 'Report'},
            'aggressor': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'aggressor_category': ('django.db.models.fields.CharField', [], {'default': "'COP'", 'max_length': '3', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['incidents.Category']"}),
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['incidents.Comment']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'features': ('mptt.fields.TreeManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['incidents.Feature']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_closed': ('django.db.models.fields.BooleanField', [], {}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'location_text': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'media': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['incidents.Media']", 'null': 'True', 'blank': 'True'}),
            'sources': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'victim': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['incidents.Victim']"})
        },
        u'incidents.thankcategory': {
            'Meta': {'object_name': 'ThankCategory'},
            'definition': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'incidents.thankreport': {
            'Meta': {'ordering': "['-datetime']", 'object_name': 'ThankReport'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['incidents.ThankCategory']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'location_text': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'media': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['incidents.Media']", 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'incidents.victim': {
            'Meta': {'object_name': 'Victim'},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'birthdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'birthplace': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'default': "'C'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'education': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'M'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'have_children': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity_card_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'marital_status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'profession': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'social_class': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']", 'null': 'True', 'blank': 'True'})
        },
        u'users.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'R'", 'max_length': '1'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['incidents']