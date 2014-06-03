# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Game.home_team'
        db.alter_column(u'bolao_game', 'home_team_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['bolao.Team']))

        # Changing field 'Game.away_team'
        db.alter_column(u'bolao_game', 'away_team_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['bolao.Team']))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Game.home_team'
        raise RuntimeError("Cannot reverse this migration. 'Game.home_team' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Game.home_team'
        db.alter_column(u'bolao_game', 'home_team_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolao.Team']))

        # User chose to not deal with backwards NULL issues for 'Game.away_team'
        raise RuntimeError("Cannot reverse this migration. 'Game.away_team' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Game.away_team'
        db.alter_column(u'bolao_game', 'away_team_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolao.Team']))

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
        u'bolao.bet': {
            'Meta': {'object_name': 'Bet'},
            'away_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'changed_timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bolao.Game']"}),
            'home_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'bolao.game': {
            'Meta': {'object_name': 'Game'},
            'away_goals_extra_time': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'away_goals_normal_time': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'away_goals_penalties': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'away_team': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'away_games'", 'null': 'True', 'to': u"orm['bolao.Team']"}),
            'changed_timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'had_extra_time': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'home_goals_extra_time': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'home_goals_normal_time': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'home_goals_penalties': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'home_team': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'home_games'", 'null': 'True', 'to': u"orm['bolao.Team']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'NS'", 'max_length': '2'})
        },
        u'bolao.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1'})
        },
        u'bolao.stadium': {
            'Meta': {'object_name': 'Stadium'},
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'})
        },
        u'bolao.team': {
            'Meta': {'object_name': 'Team'},
            'code': ('django.db.models.fields.CharField', [], {'default': "'XXX'", 'max_length': '4'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bolao.Group']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['bolao']