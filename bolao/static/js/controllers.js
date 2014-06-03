(function () {

  var app = angular.module('bolaoApp', ['ngCookies']);

  app.controller('LeagueController', ['$scope', '$http', '$cookies', function ($scope, $http, $cookies) {
    this.groups = groups;
    this.roundOf16 = roundOf16;
    this.quarterFinals = quarterFinals;
    this.semiFinals = semiFinals;
    this.finals = finals;

    var cup = this;

    $scope.refreshStandings = function (group) {
      group.refreshStandings();

      for (var match in cup.roundOf16) {
        cup.roundOf16[match].refresh();
      }
    };

    $scope.refreshFinals = function () {
      var match;
      for (match in cup.quarterFinals)
        cup.quarterFinals[match].refresh();

      for (match in cup.semiFinals)
        cup.semiFinals[match].refresh();
      for (match in cup.finals)
        cup.finals[match].refresh();
    };

    $scope.setTiedMatchWinner = function (match, team) {
      match.setTiedMatchWinner(team);
      this.refreshFinals();
    };

    $scope.submit = function () {
      if (confirm("Está certo disso? Olha lá hein!")) {

        var data = [];
        var key = null;
        var match = null;

        for (key in cup.groups) {
          var group = cup.groups[key];
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

        addMatches(cup.roundOf16, data);
        addMatches(cup.quarterFinals, data);
        addMatches(cup.semiFinals, data);
        addMatches(cup.finals, data);

        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
        $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;
        $http.defaults.headers.common['X-Access-Token'] = $cookies.token;

        $http.post(
            '/bet/',
            data).
          success(function (data, status) {
            console.log(status);
            console.log(data);
          }).
          error(function (data, status) {
            console.log('FAIL');
            console.log(status);
            console.log(data);
          });
      }
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
    match49: new SecondRoundMatch(49, groups.A, getFirst, groups.B, getSecond),
    match50: new SecondRoundMatch(50, groups.A, getSecond, groups.B, getFirst),
    match51: new SecondRoundMatch(51, groups.C, getFirst, groups.D, getSecond),
    match52: new SecondRoundMatch(52, groups.C, getSecond, groups.D, getFirst),
    match53: new SecondRoundMatch(53, groups.E, getFirst, groups.F, getSecond),
    match54: new SecondRoundMatch(54, groups.E, getSecond, groups.F, getFirst),
    match55: new SecondRoundMatch(55, groups.G, getFirst, groups.H, getSecond),
    match56: new SecondRoundMatch(56, groups.G, getSecond, groups.H, getFirst)
  };

  var getWinner = roundOf16.match49.getWinner;
  var getLoser = roundOf16.match49.getLoser;

  var quarterFinals = {
    match57: new SecondRoundMatch(57, roundOf16.match49, getWinner, roundOf16.match50, getWinner),
    match58: new SecondRoundMatch(58, roundOf16.match51, getWinner, roundOf16.match52, getWinner),
    match59: new SecondRoundMatch(59, roundOf16.match53, getWinner, roundOf16.match54, getWinner),
    match60: new SecondRoundMatch(60, roundOf16.match55, getWinner, roundOf16.match56, getWinner)
  };

  var semiFinals = {
    match61: new SecondRoundMatch(61, quarterFinals.match57, getWinner, quarterFinals.match58, getWinner),
    match62: new SecondRoundMatch(62, quarterFinals.match59, getWinner, quarterFinals.match60, getWinner)
  };

  var finals = {
    match63: new SecondRoundMatch(63, semiFinals.match61, getLoser, semiFinals.match62, getLoser),
    match64: new SecondRoundMatch(64, semiFinals.match61, getWinner, semiFinals.match62, getWinner)
  };

})();