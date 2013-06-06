# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Comment'
        db.create_table('webapp_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('ts', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 3, 30, 0, 0), auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('webapp', ['Comment'])

        # Adding M2M table for field idea on 'Comment'
        db.create_table('webapp_comment_idea', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('comment', models.ForeignKey(orm['webapp.comment'], null=False)),
            ('idea', models.ForeignKey(orm['webapp.idea'], null=False))
        ))
        db.create_unique('webapp_comment_idea', ['comment_id', 'idea_id'])

        # Adding field 'Idea.ts'
        db.add_column('webapp_idea', 'ts',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 3, 30, 0, 0), auto_now=True, blank=True),
                      keep_default=False)

        # Adding field 'Suggestion.ts'
        db.add_column('webapp_suggestion', 'ts',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 3, 30, 0, 0), auto_now=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Comment'
        db.delete_table('webapp_comment')

        # Removing M2M table for field idea on 'Comment'
        db.delete_table('webapp_comment_idea')

        # Deleting field 'Idea.ts'
        db.delete_column('webapp_idea', 'ts')

        # Deleting field 'Suggestion.ts'
        db.delete_column('webapp_suggestion', 'ts')


    models = {
        'webapp.comment': {
            'Meta': {'object_name': 'Comment'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idea': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['webapp.Idea']", 'symmetrical': 'False'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'ts': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 3, 30, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'})
        },
        'webapp.idea': {
            'Meta': {'object_name': 'Idea'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'ts': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 3, 30, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'upvotes': ('django.db.models.fields.IntegerField', [], {})
        },
        'webapp.suggestion': {
            'Meta': {'object_name': 'Suggestion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idea': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['webapp.Idea']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'ts': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 3, 30, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'upvotes': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['webapp']