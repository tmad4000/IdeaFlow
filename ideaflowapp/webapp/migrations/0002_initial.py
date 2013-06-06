# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Idea'
        db.create_table('webapp_idea', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('upvotes', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('webapp', ['Idea'])

        # Adding model 'Suggestion'
        db.create_table('webapp_suggestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('idea', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['webapp.Idea'])),
            ('upvotes', self.gf('django.db.models.fields.IntegerField')()),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('webapp', ['Suggestion'])


    def backwards(self, orm):
        # Deleting model 'Idea'
        db.delete_table('webapp_idea')

        # Deleting model 'Suggestion'
        db.delete_table('webapp_suggestion')


    models = {
        'webapp.idea': {
            'Meta': {'object_name': 'Idea'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'upvotes': ('django.db.models.fields.IntegerField', [], {})
        },
        'webapp.suggestion': {
            'Meta': {'object_name': 'Suggestion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idea': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webapp.Idea']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'upvotes': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['webapp']