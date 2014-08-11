# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CodeTemplate'
        db.create_table(u'emacshaqiba_codetemplate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('gist_url', self.gf('django.db.models.fields.URLField')(max_length=70, null=True, blank=True)),
            ('code', self.gf('django.db.models.fields.TextField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('screenshot', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('download_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'emacshaqiba', ['CodeTemplate'])

        # Adding model 'Dependency'
        db.create_table(u'emacshaqiba_dependency', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('loadpath', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('require', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('tarFile', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('config', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('screenshot', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('download_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'emacshaqiba', ['Dependency'])

        # Adding model 'BundleTemplate'
        db.create_table(u'emacshaqiba_bundletemplate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('config', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('screenshot', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('download_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'emacshaqiba', ['BundleTemplate'])

        # Adding M2M table for field dep on 'BundleTemplate'
        m2m_table_name = db.shorten_name(u'emacshaqiba_bundletemplate_dep')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bundletemplate', models.ForeignKey(orm[u'emacshaqiba.bundletemplate'], null=False)),
            ('dependency', models.ForeignKey(orm[u'emacshaqiba.dependency'], null=False))
        ))
        db.create_unique(m2m_table_name, ['bundletemplate_id', 'dependency_id'])

        # Adding model 'UserProfile'
        db.create_table(u'emacshaqiba_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'emacshaqiba', ['UserProfile'])


    def backwards(self, orm):
        # Deleting model 'CodeTemplate'
        db.delete_table(u'emacshaqiba_codetemplate')

        # Deleting model 'Dependency'
        db.delete_table(u'emacshaqiba_dependency')

        # Deleting model 'BundleTemplate'
        db.delete_table(u'emacshaqiba_bundletemplate')

        # Removing M2M table for field dep on 'BundleTemplate'
        db.delete_table(db.shorten_name(u'emacshaqiba_bundletemplate_dep'))

        # Deleting model 'UserProfile'
        db.delete_table(u'emacshaqiba_userprofile')


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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'emacshaqiba.bundletemplate': {
            'Meta': {'object_name': 'BundleTemplate'},
            'config': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'dep': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['emacshaqiba.Dependency']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'download_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'screenshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'emacshaqiba.codetemplate': {
            'Meta': {'object_name': 'CodeTemplate'},
            'code': ('django.db.models.fields.TextField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'download_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'gist_url': ('django.db.models.fields.URLField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'screenshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'emacshaqiba.dependency': {
            'Meta': {'object_name': 'Dependency'},
            'config': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'download_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loadpath': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'require': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'screenshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'tarFile': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'emacshaqiba.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['emacshaqiba']