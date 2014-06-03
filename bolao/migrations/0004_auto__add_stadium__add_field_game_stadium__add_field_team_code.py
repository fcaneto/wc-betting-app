# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Stadium'
        db.create_table(u'bolao_stadium', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('city', self.gf('django.db.models.fields.CharField')(default='', max_length=20)),
        ))
        db.send_create_signal(u'bolao', ['Stadium'])

        # Adding field 'Game.stadium'
        db.add_column(u'bolao_game', 'stadium',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolao.Stadium'], null=True),
                      keep_default=False)

        # Adding field 'Team.code'
        db.add_column(u'bolao_team', 'code',
                      self.gf('django.db.models.fields.CharField')(default='XXX', max_length=4),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Stadium'
        db.delete_table(u'bolao_stadium')

        # Deleting field 'Game.stadium'
        db.delete_column(u'bolao_game', 'stadium_id')

        # Deleting field 'Team.code'
        db.delete_column(u'bolao_team', 'code')


    models = {
        u'bolao.game': {
            'Meta': {'object_name': 'Game'},
            'away_goals_extra_time': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'away_goals_normal_time': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'away_goals_penalties': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'away_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'away_games'", 'to': u"orm['bolao.Team']"}),
            'changed_timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {}),
            'had_extra_time': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'home_goals_extra_time': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'home_goals_normal_time': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'home_goals_penalties': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'home_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'home_games'", 'to': u"orm['bolao.Team']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stadium': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bolao.Stadium']", 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'NS'", 'max_length': '2'})
        },
        u'bolao.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1'}),
            'teams': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['bolao.Team']", 'through': u"orm['bolao.GroupTeamRelationship']", 'symmetrical': 'False'})
        },
        u'bolao.groupteamrelationship': {
            'Meta': {'object_name': 'GroupTeamRelationship'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bolao.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bolao.Team']"})
        },
        u'bolao.player': {
            'Meta': {'object_name': 'Player'},
            'email': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'bolao.playerresults': {
            'Meta': {'object_name': 'PlayerResults'},
            'away_goals_normal_time': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'changed_timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bolao.Game']"}),
            'home_goals_normal_time': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bolao.Player']"})
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'})
        }
    }

    complete_apps = ['bolao']