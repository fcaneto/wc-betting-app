(function () {

  var app = angular.module('bolaoApp', ['ngCookies', 'ngAnimate']);

  app.controller('LeagueController', ['$scope', '$http', '$cookies', '$timeout',
    function ($scope, $http, $cookies, $timeout) {
    this.groups = groups;
    this.roundOf16 = roundOf16;
    this.quarterFinals = quarterFinals;
    this.semiFinals = semiFinals;
    this.finals = finals;

    $scope.isSaving = false;
    $scope.showSuccessMsg = false;
    $scope.showErrorMsg = false;

    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;
    $http.defaults.headers.common['X-Access-Token'] = $cookies.token;

    var controller = this;

    $scope.disableSaveData = function() {
      return controller.finals[63].getWinner() === null
          || controller.finals[64].getWinner() === null;
    }

    // TODO: refactor this mess.
    this.getTeamByCode = function (code) {
      var team = null;
      for (var group in controller.groups) {
        var teams = controller.groups[group].teams;

        for (var i = 0; i < teams.length; i++) {
          if (teams[i].code === code)
            team = teams[i];
        }
      }

      if (!team)
        console.log('LeagueController > getTeamByCode : team ' + code + ' not found!')
      return team;
    };

    this.updateSecondRoundMatchFromServer = function (matchId, stage, homeScore, awayScore, winnerCode) {
      console.log('Atualizando jogo ' + matchId);
      var match = stage[matchId];
      var team = controller.getTeamByCode(winnerCode);
      match.setTiedMatchWinner(team);
      match.homeScore = homeScore;
      match.awayScore = awayScore;
    }

    var retrieveBets = function () {
      $http.get(
          '/bet/').
        success(function (data, status) {
          console.log(status);
          console.log(data);

          var groupFromServer;
          var matchFromServer;
          var group;
          var matchId;

          for (var groupId in data.groups) {
            console.log('Atualizando ' + groupId);
            group = controller.groups[groupId];
            groupFromServer = data.groups[groupId];

            for (matchId in groupFromServer) {
              matchFromServer = groupFromServer[matchId];
              group.setMatchResults(matchId,
                matchFromServer.homeScore,
                matchFromServer.awayScore);
            }
            controller.refreshStandings(group);
          }

          console.log('Atualizando Oitavas.');
          for (matchId in data.roundOf16) {
            matchFromServer = data.roundOf16[matchId];
            controller.updateSecondRoundMatchFromServer(matchId,
              controller.roundOf16,
              matchFromServer.homeScore,
              matchFromServer.awayScore,
              matchFromServer.winnerCode);
          }
          controller.refreshFinals();

          console.log('Atualizando Quartas.');
          for (matchId in data.quarterFinals) {
            matchFromServer = data.quarterFinals[matchId];
            controller.updateSecondRoundMatchFromServer(matchId,
              controller.quarterFinals,
              matchFromServer.homeScore,
              matchFromServer.awayScore,
              matchFromServer.winnerCode);
          }
          controller.refreshFinals();

          console.log('Atualizando Semi-finais.');
          for (matchId in data.semiFinals) {
            matchFromServer = data.semiFinals[matchId];
            controller.updateSecondRoundMatchFromServer(matchId,
              controller.semiFinals,
              matchFromServer.homeScore,
              matchFromServer.awayScore,
              matchFromServer.winnerCode);
          }
          controller.refreshFinals();

          console.log('Atualizando finais.');
          for (matchId in data.finals) {
            matchFromServer = data.finals[matchId];
            controller.updateSecondRoundMatchFromServer(matchId,
              controller.finals,
              matchFromServer.homeScore,
              matchFromServer.awayScore,
              matchFromServer.winnerCode);
          }
          controller.refreshFinals();
        }).
        error(function (data, status) {
          console.log('FAIL');
          console.log(status);
          console.log(data);
        });
    }
    retrieveBets();

    this.refreshStandings = function (group) {
      group.refreshStandings();

      for (var match in controller.roundOf16) {
        controller.roundOf16[match].refresh();
      }
    };
    $scope.refreshStandings = this.refreshStandings;

    this.refreshFinals = function () {
      var match;
      for (match in controller.quarterFinals)
        controller.quarterFinals[match].refresh();

      for (match in controller.semiFinals)
        controller.semiFinals[match].refresh();
      for (match in controller.finals)
        controller.finals[match].refresh();
    };
    $scope.refreshFinals = this.refreshFinals;

    $scope.setTiedMatchWinner = function (match, team) {
      match.setTiedMatchWinner(team);
      this.refreshFinals();
    };

    $scope.submit = function () {
      var data = [];
      var key = null;
      var match = null;

      for (key in controller.groups) {
        var group = controller.groups[key];
        for (var i = 0; i < group.matches.length; i++) {
          match = group.matches[i];

          // TODO: Zerando gols nulos para facilitar teste. Apague isso depois.
          if (match.homeScore === null)
            match.homeScore = 0;
          if (match.awayScore === null)
            match.awayScore = 0;

          match.homeTeamName = group.teams[match.homeTeam].name;
          match.homeTeamCode = group.teams[match.homeTeam].code;
          match.awayTeamName = group.teams[match.awayTeam].name;
          match.awayTeamCode = group.teams[match.awayTeam].code;

          data.push(match);
        }
      }

      var addMatches = function (round, list) {
        for (key in round) {
          match = round[key];
          match.homeTeamName = match.homeTeam.name;
          match.homeTeamCode = match.homeTeam.code;
          match.awayTeamName = match.awayTeam.name;
          match.awayTeamCode = match.awayTeam.code;
          match.winnerCode = match.getWinner().code;
          list.push(match);
        }
      };

      addMatches(controller.roundOf16, data);
      addMatches(controller.quarterFinals, data);
      addMatches(controller.semiFinals, data);
      addMatches(controller.finals, data);



      $scope.isSaving = true;
      $http.post(
          '/bet/',
          data).
        success(function (data, status) {
          console.log(status);
          console.log(data);
          $scope.isSaving = false;
          $scope.showSuccessMsg = true;
          $timeout(function() {$scope.showSuccessMsg = false;}, 2000);
        }).
        error(function (data, status) {
          console.log('FAIL');
          console.log(status);
          console.log(data);
          $scope.isSaving = false;
          $scope.showErrorMsg = true;
          $timeout(function() {$scope.showErrorMsg = false;}, 2000);
        });
    }
  }]);

  var groups = {
    A: new Group(
      'A',
      [
        {name: 'Brasil', code: 'bra'},
        {name: 'Croácia', code: 'cro'},
        {name: 'México', code: 'mex'},
        {name: 'Camarões', code: 'cam'}
      ],
      [
        {id: 1, homeTeam: 0, awayTeam: 1, homeScore: null, awayScore: null},
        {id: 2, homeTeam: 2, awayTeam: 3, homeScore: null, awayScore: null},
        {id: 17, homeTeam: 0, awayTeam: 2, homeScore: null, awayScore: null},
        {id: 18, homeTeam: 3, awayTeam: 1, homeScore: null, awayScore: null},
        {id: 33, homeTeam: 3, awayTeam: 0, homeScore: null, awayScore: null},
        {id: 34, homeTeam: 1, awayTeam: 2, homeScore: null, awayScore: null}
      ]).init(),

    B: new Group(
      'B',
      [
        {name: 'Espanha', code: 'esp'},
        {name: 'Holanda', code: 'hol'},
        {name: 'Chile', code: 'chi'},
        {name: 'Austrália', code: 'aus'}
      ],
      [
        {id: 3, homeTeam: 0, awayTeam: 1, homeScore: null, awayScore: null},
        {id: 4, homeTeam: 2, awayTeam: 3, homeScore: null, awayScore: null},
        {id: 19, homeTeam: 0, awayTeam: 2, homeScore: null, awayScore: null},
        {id: 20, homeTeam: 3, awayTeam: 1, homeScore: null, awayScore: null},
        {id: 35, homeTeam: 3, awayTeam: 0, homeScore: null, awayScore: null},
        {id: 36, homeTeam: 1, awayTeam: 2, homeScore: null, awayScore: null}
      ]).init(),

    C: new Group(
      'C',
      [
        {name: 'Colômbia', code: 'col'},
        {name: 'Grécia', code: 'gre'},
        {name: 'Costa do Marfim', code: 'cdm'},
        {name: 'Japão', code: 'jap'}
      ],
      [
        {id: 5, homeTeam: 0, awayTeam: 1, homeScore: null, awayScore: null},
        {id: 6, homeTeam: 2, awayTeam: 3, homeScore: null, awayScore: null},
        {id: 21, homeTeam: 0, awayTeam: 2, homeScore: null, awayScore: null},
        {id: 22, homeTeam: 3, awayTeam: 1, homeScore: null, awayScore: null},
        {id: 37, homeTeam: 3, awayTeam: 0, homeScore: null, awayScore: null},
        {id: 38, homeTeam: 1, awayTeam: 2, homeScore: null, awayScore: null}
      ]).init(),

    D: new Group(
      'D',
      [
        {name: 'Uruguai', code: 'uru'},
        {name: 'Costa Rica', code: 'cos'},
        {name: 'Inglaterra', code: 'ing'},
        {name: 'Itália', code: 'ita'}
      ],
      [
        {id: 7, homeTeam: 0, awayTeam: 1, homeScore: null, awayScore: null},
        {id: 8, homeTeam: 2, awayTeam: 3, homeScore: null, awayScore: null},
        {id: 23, homeTeam: 0, awayTeam: 2, homeScore: null, awayScore: null},
        {id: 24, homeTeam: 3, awayTeam: 1, homeScore: null, awayScore: null},
        {id: 39, homeTeam: 3, awayTeam: 0, homeScore: null, awayScore: null},
        {id: 40, homeTeam: 1, awayTeam: 2, homeScore: null, awayScore: null}
      ]).init(),

    E: new Group(
      'E',
      [
        {name: 'Suíça', code: 'sui'},
        {name: 'Equador', code: 'equ'},
        {name: 'França', code: 'fra'},
        {name: 'Honduras', code: 'hon'}
      ],
      [
        {id: 9, homeTeam: 0, awayTeam: 1, homeScore: null, awayScore: null},
        {id: 10, homeTeam: 2, awayTeam: 3, homeScore: null, awayScore: null},
        {id: 25, homeTeam: 0, awayTeam: 2, homeScore: null, awayScore: null},
        {id: 26, homeTeam: 3, awayTeam: 1, homeScore: null, awayScore: null},
        {id: 41, homeTeam: 3, awayTeam: 0, homeScore: null, awayScore: null},
        {id: 42, homeTeam: 1, awayTeam: 2, homeScore: null, awayScore: null}
      ]).init(),

    F: new Group(
      'F',
      [
        {name: 'Argentina', code: 'arg'},
        {name: 'Bósnia', code: 'bos'},
        {name: 'Irã', code: 'ira'},
        {name: 'Nigéria', code: 'nga'}
      ],
      [
        {id: 11, homeTeam: 0, awayTeam: 1, homeScore: null, awayScore: null},
        {id: 12, homeTeam: 2, awayTeam: 3, homeScore: null, awayScore: null},
        {id: 27, homeTeam: 0, awayTeam: 2, homeScore: null, awayScore: null},
        {id: 28, homeTeam: 3, awayTeam: 1, homeScore: null, awayScore: null},
        {id: 43, homeTeam: 3, awayTeam: 0, homeScore: null, awayScore: null},
        {id: 44, homeTeam: 1, awayTeam: 2, homeScore: null, awayScore: null},

      ]).init(),

    G: new Group(
      'G',
      [
        {name: 'Alemanha', code: 'ale'},
        {name: 'Portugal', code: 'por'},
        {name: 'Gana', code: 'gan'},
        {name: 'EUA', code: 'eua'}
      ],
      [
        {id: 13, homeTeam: 0, awayTeam: 1, homeScore: null, awayScore: null},
        {id: 14, homeTeam: 2, awayTeam: 3, homeScore: null, awayScore: null},
        {id: 29, homeTeam: 0, awayTeam: 2, homeScore: null, awayScore: null},
        {id: 30, homeTeam: 3, awayTeam: 1, homeScore: null, awayScore: null},
        {id: 45, homeTeam: 3, awayTeam: 0, homeScore: null, awayScore: null},
        {id: 46, homeTeam: 1, awayTeam: 2, homeScore: null, awayScore: null},

      ]).init(),

    H: new Group(
      'H',
      [
        {name: 'Bélgica', code: 'bel'},
        {name: 'Argélia', code: 'agl'},
        {name: 'Rússia', code: 'rus'},
        {name: 'Coréia do Sul', code: 'cor'}
      ],
      [
        {id: 15, homeTeam: 0, awayTeam: 1, homeScore: null, awayScore: null},
        {id: 16, homeTeam: 2, awayTeam: 3, homeScore: null, awayScore: null},
        {id: 31, homeTeam: 0, awayTeam: 2, homeScore: null, awayScore: null},
        {id: 32, homeTeam: 3, awayTeam: 1, homeScore: null, awayScore: null},
        {id: 47, homeTeam: 3, awayTeam: 0, homeScore: null, awayScore: null},
        {id: 48, homeTeam: 1, awayTeam: 2, homeScore: null, awayScore: null},

      ]).init()
  };

  var getFirst = groups.A.first;
  var getSecond = groups.A.second;

  var roundOf16 = {
    49: new SecondRoundMatch(49, groups.A, getFirst, groups.B, getSecond),
    50: new SecondRoundMatch(50, groups.A, getSecond, groups.B, getFirst),
    51: new SecondRoundMatch(51, groups.C, getFirst, groups.D, getSecond),
    52: new SecondRoundMatch(52, groups.C, getSecond, groups.D, getFirst),
    53: new SecondRoundMatch(53, groups.E, getFirst, groups.F, getSecond),
    54: new SecondRoundMatch(54, groups.E, getSecond, groups.F, getFirst),
    55: new SecondRoundMatch(55, groups.G, getFirst, groups.H, getSecond),
    56: new SecondRoundMatch(56, groups.G, getSecond, groups.H, getFirst)
  };

  var getWinner = roundOf16[49].getWinner;
  var getLoser = roundOf16[49].getLoser;

  var quarterFinals = {
    57: new SecondRoundMatch(57, roundOf16[49], getWinner, roundOf16[50], getWinner),
    58: new SecondRoundMatch(58, roundOf16[51], getWinner, roundOf16[52], getWinner),
    59: new SecondRoundMatch(59, roundOf16[53], getWinner, roundOf16[54], getWinner),
    60: new SecondRoundMatch(60, roundOf16[55], getWinner, roundOf16[56], getWinner)
  };

  var semiFinals = {
    61: new SecondRoundMatch(61, quarterFinals[57], getWinner, quarterFinals[58], getWinner),
    62: new SecondRoundMatch(62, quarterFinals[59], getWinner, quarterFinals[60], getWinner)
  };

  var finals = {
    63: new SecondRoundMatch(63, semiFinals[61], getLoser, semiFinals[62], getLoser),
    64: new SecondRoundMatch(64, semiFinals[61], getWinner, semiFinals[62], getWinner)
  };

})();