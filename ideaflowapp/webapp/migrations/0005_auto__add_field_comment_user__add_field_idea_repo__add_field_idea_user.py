# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Comment.user'
        db.add_column('webapp_comment', 'user',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=256),
                      keep_default=False)

        # Adding field 'Idea.repo'
        db.add_column('webapp_idea', 'repo',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=200),
                      keep_default=False)

        # Adding field 'Idea.user'
        db.add_column('webapp_idea', 'user',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=256),
                      keep_default=False)

        # Adding field 'Suggestion.user'
        db.add_column('webapp_suggestion', 'user',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=256),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Comment.user'
        db.delete_column('webapp_comment', 'user')

        # Deleting field 'Idea.repo'
        db.delete_column('webapp_idea', 'repo')

        # Deleting field 'Idea.user'
        db.delete_column('webapp_idea', 'user')

        # Deleting field 'Suggestion.user'
        db.delete_column('webapp_suggestion', 'user')


    models = {
        'webapp.comment': {
            'Meta': {'object_name': 'Comment'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idea': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['webapp.Idea']", 'symmetrical': 'False'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'ts': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 3, 30, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'})
        },
        'webapp.idea': {
            'Meta': {'object_name': 'Idea'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repo': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'ts': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 3, 30, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'upvotes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'})
        },
        'webapp.suggestion': {
            'Meta': {'object_name': 'Suggestion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idea': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webapp.Idea']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'ts': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 3, 30, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'upvotes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'})
        }
    }

    complete_apps = ['webapp']