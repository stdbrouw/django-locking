# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Lock'
        db.create_table('locking_lock', (
            ('app', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('_hard_lock', self.gf('django.db.models.fields.BooleanField')(default=False, db_column='hard_lock', blank=True)),
            ('entry_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('_locked_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='working_on_lock', null=True, db_column='locked_by', to=orm['account.User'])),
            ('_locked_at', self.gf('django.db.models.fields.DateTimeField')(null=True, db_column='locked_at')),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('locking', ['Lock'])

        # Adding unique constraint on 'Lock', fields ['app', 'model', 'entry_id']
        db.create_unique('locking_lock', ['app', 'model', 'entry_id'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Lock'
        db.delete_table('locking_lock')

        # Removing unique constraint on 'Lock', fields ['app', 'model', 'entry_id']
        db.delete_unique('locking_lock', ['app', 'model', 'entry_id'])
    
    
    models = {
        'account.user': {
            'Meta': {'object_name': 'User', '_ormbases': ['auth.User']},
            'bio': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'reviewer': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'locking.lock': {
            'Meta': {'unique_together': "(('app', 'model', 'entry_id'),)", 'object_name': 'Lock'},
            '_hard_lock': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_column': "'hard_lock'", 'blank': 'True'}),
            '_locked_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_column': "'locked_at'"}),
            '_locked_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'working_on_lock'", 'null': 'True', 'db_column': "'locked_by'", 'to': "orm['account.User']"}),
            'app': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'entry_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'})
        }
    }
    
    complete_apps = ['locking']
