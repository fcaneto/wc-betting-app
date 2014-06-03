# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Player'
        db.create_table(u'bolao_player', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('email', self.gf('django.db.models.fields.CharField')(default='', max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal(u'bolao', ['Player'])

        # Adding model 'PlayerResults'
        db.create_table(u'bolao_playerresults', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('changed_timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')()),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolao.Player'])),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolao.Game'])),
            ('home_goals_normal_time', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('away_goals_normal_time', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'bolao', ['PlayerResults'])

        # Adding model 'Team'
        db.create_table(u'bolao_team', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'bolao', ['Team'])

        # Adding model 'Game'
        db.create_table(u'bolao_game', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('changed_timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')()),
            ('home_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='home_games', to=orm['bolao.Team'])),
            ('away_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='away_games', to=orm['bolao.Team'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='NS', max_length=2)),
            ('home_goals_normal_time', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('away_goals_normal_time', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('home_goals_extra_time', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('away_goals_extra_time', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('had_extra_time', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('home_goals_penalties', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('away_goals_penalties', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
        ))
        db.send_create_signal(u'bolao', ['Game'])


    def backwards(self, orm):
        # Deleting model 'Player'
        db.delete_table(u'bolao_player')

        # Deleting model 'PlayerResults'
        db.delete_table(u'bolao_playerresults')

        # Deleting model 'Team'
        db.delete_table(u'bolao_team')

        # Deleting model 'Game'
        db.delete_table(u'bolao_game')


    models = {
        u'bolao.game': {
            'Meta': {'object_name': 'Game'},
            'away_goals_extra_time': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'away_goals_normal_time': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'away_goals_penalties': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'away_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'away_games'", 'to': u"orm['bolao.Team']"}),
            'changed_timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {}),
            'had_extra_time': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'home_goals_extra_time': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'home_goals_normal_time': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'home_goals_penalties': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'home_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'home_games'", 'to': u"orm['bolao.Team']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'NS'", 'max_length': '2'})
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