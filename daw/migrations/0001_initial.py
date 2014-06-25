# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'State'
        db.create_table('daw_state', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_updated_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('last_updated_by', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=5000)),
        ))
        db.send_create_signal('daw', ['State'])

        # Adding model 'Transition'
        db.create_table('daw_transition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_updated_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('last_updated_by', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('source_state', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transitions_as_source', to=orm['daw.State'])),
            ('destination_state', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transitions_as_destination', to=orm['daw.State'])),
        ))
        db.send_create_signal('daw', ['Transition'])

        # Adding model 'TransitionApproveDefinition'
        db.create_table('daw_transition_approve_definition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_updated_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('last_updated_by', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('transition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['daw.Transition'])),
            ('permission', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Permission'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('daw', ['TransitionApproveDefinition'])

        # Adding unique constraint on 'TransitionApproveDefinition', fields ['transition', 'permission']
        db.create_unique('daw_transition_approve_definition', ['transition_id', 'permission_id'])

        # Adding unique constraint on 'TransitionApproveDefinition', fields ['transition', 'permission', 'order']
        db.create_unique('daw_transition_approve_definition', ['transition_id', 'permission_id', 'order'])

        # Adding model 'TransitionApprovement'
        db.create_table('daw_transition_approvement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_updated_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('last_updated_by', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_pk', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('approve_definition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['daw.TransitionApproveDefinition'])),
            ('transactioner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('transaction_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='0', max_length=20)),
            ('skip', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('daw', ['TransitionApprovement'])


    def backwards(self, orm):
        # Removing unique constraint on 'TransitionApproveDefinition', fields ['transition', 'permission', 'order']
        db.delete_unique('daw_transition_approve_definition', ['transition_id', 'permission_id', 'order'])

        # Removing unique constraint on 'TransitionApproveDefinition', fields ['transition', 'permission']
        db.delete_unique('daw_transition_approve_definition', ['transition_id', 'permission_id'])

        # Deleting model 'State'
        db.delete_table('daw_state')

        # Deleting model 'Transition'
        db.delete_table('daw_transition')

        # Deleting model 'TransitionApproveDefinition'
        db.delete_table('daw_transition_approve_definition')

        # Deleting model 'TransitionApprovement'
        db.delete_table('daw_transition_approvement')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'daw.state': {
            'Meta': {'object_name': 'State'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '5000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'last_updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_updated_by': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'daw.transition': {
            'Meta': {'object_name': 'Transition'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'destination_state': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transitions_as_destination'", 'to': "orm['daw.State']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_updated_by': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'source_state': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transitions_as_source'", 'to': "orm['daw.State']"})
        },
        'daw.transitionapprovedefinition': {
            'Meta': {'unique_together': "[('transition', 'permission'), ('transition', 'permission', 'order')]", 'object_name': 'TransitionApproveDefinition', 'db_table': "'daw_transition_approve_definition'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_updated_by': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Permission']"}),
            'transition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['daw.Transition']"})
        },
        'daw.transitionapprovement': {
            'Meta': {'object_name': 'TransitionApprovement', 'db_table': "'daw_transition_approvement'"},
            'approve_definition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['daw.TransitionApproveDefinition']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_updated_by': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'object_pk': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'skip': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '20'}),
            'transaction_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'transactioner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['daw']