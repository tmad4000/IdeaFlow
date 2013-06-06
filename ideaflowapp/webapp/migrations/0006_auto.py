# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field idea on 'Comment'
        db.delete_table('webapp_comment_idea')

        # Adding M2M table for field comments on 'Idea'
        db.create_table('webapp_idea_comments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('idea', models.ForeignKey(orm['webapp.idea'], null=False)),
            ('comment', models.ForeignKey(orm['webapp.comment'], null=False))
        ))
        db.create_unique('webapp_idea_comments', ['idea_id', 'comment_id'])

        # Adding M2M table for field comments on 'Suggestion'
        db.create_table('webapp_suggestion_comments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('suggestion', models.ForeignKey(orm['webapp.suggestion'], null=False)),
            ('comment', models.ForeignKey(orm['webapp.comment'], null=False))
        ))
        db.create_unique('webapp_suggestion_comments', ['suggestion_id', 'comment_id'])


    def backwards(self, orm):
        # Adding M2M table for field idea on 'Comment'
        db.create_table('webapp_comment_idea', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('comment', models.ForeignKey(orm['webapp.comment'], null=False)),
            ('idea', models.ForeignKey(orm['webapp.idea'], null=False))
        ))
        db.create_unique('webapp_comment_idea', ['comment_id', 'idea_id'])

        # Removing M2M table for field comments on 'Idea'
        db.delete_table('webapp_idea_comments')

        # Removing M2M table for field comments on 'Suggestion'
        db.delete_table('webapp_suggestion_comments')


    models = {
        'webapp.comment': {
            'Meta': {'object_name': 'Comment'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'ts': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 3, 30, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'default': "'anon'", 'max_length': '256'})
        },
        'webapp.idea': {
            'Meta': {'object_name': 'Idea'},
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['webapp.Comment']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repo': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'ts': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 3, 30, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'upvotes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.CharField', [], {'default': "'anon'", 'max_length': '256'})
        },
        'webapp.suggestion': {
            'Meta': {'object_name': 'Suggestion'},
            'comments': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['webapp.Comment']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idea': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webapp.Idea']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'ts': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 3, 30, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'upvotes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.CharField', [], {'default': "'anon'", 'max_length': '256'})
        }
    }

    complete_apps = ['webapp']