# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GroupTeamRelationship'
        db.create_table(u'bolao_groupteamrelationship', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolao.Team'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolao.Group'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'bolao', ['GroupTeamRelationship'])

        # Removing M2M table for field teams on 'Group'
        db.delete_table(db.shorten_name(u'bolao_group_teams'))


    def backwards(self, orm):
        # Deleting model 'GroupTeamRelationship'
        db.delete_table(u'bolao_groupteamrelationship')

        # Adding M2M table for field teams on 'Group'
        m2m_table_name = db.shorten_name(u'bolao_group_teams')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('group', models.ForeignKey(orm[u'bolao.group'], null=False)),
            ('team', models.ForeignKey(orm[u'bolao.team'], null=False))
        ))
        db.create_unique(m2m_table_name, ['group_id', 'team_id'])


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
        u'bolao.team': {
            'Meta': {'object_name': 'Team'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['bolao']