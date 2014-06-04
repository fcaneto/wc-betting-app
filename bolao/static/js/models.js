function Group(name, teams, matches) {
  this.name = name;
  this.teams = teams;
  this.matches = matches;

  this.qualifiedTeams = [];

  this.init = function () {
    this.refreshStandings();
    return this;
  }

  this.resetStandings = function () {
    for (var i = 0; i < this.teams.length; i++) {
      var team = this.teams[i];
      team.points = 0;
      team.goalsMade = 0;
      team.goalsTaken = 0;
    }
  }

  this.getTeamsByRank = function () {
    var group = this;
    return this.teams.slice().sort(function (team1, team2) {
      /*
       * CAIXCA.
       *
       * CritÃ©rios de desempate:
       * - pontos
       * - saldo de gols
       * - gols prÃ³
       *
       * Se dois ou mais times empatam nos critÃ©rios acima:
       * - confronto direto
       * - sorteio
       *
       * Se tieBreaker for:
       * - negativo: team1 Ã© melhor
       * - zero: empate
       * - positivo: team2 Ã© melhor
       *
       */
      var tieBreaker = -(team1.points - team2.points);

      if (tieBreaker == 0) {
        // Saldo de gols
        var team1GoalDiff = team1.goalsMade - team1.goalsTaken;
        var team2GoalDiff = team2.goalsMade - team2.goalsTaken;

        tieBreaker = -(team1GoalDiff - team2GoalDiff);
      }

      if (tieBreaker == 0) {
        // Gols prÃ³
        tieBreaker = -(team1.goalsMade - team2.goalsMade);
      }

      if (tieBreaker == 0) {
        // Confronto direto
        for (var i = 0; i < group.matches.length; i++) {
          var match = group.matches[i];

          if (group.teams[match.homeTeam] === team1 && group.teams[match.awayTeam] === team2) {
            tieBreaker = match.awayScore - match.homeScore;
            break;
          } else if (group.teams[match.homeTeam] === team2 && group.teams[match.awayTeam] === team1) {
            tieBreaker = match.homeScore - match.awayScore;
            break;
          }

          // TODO: Tratar cenÃ¡rios de sorteio
        }
      }

      return tieBreaker;
    });
  };

  this.refreshStandings = function () {
    this.resetStandings();

    var everyGameHasBeenPlayed = true;

    for (var i = 0; i < this.matches.length; i++) {
      var match = this.matches[i];

      if (match.homeScore !== null && match.awayScore !== null) {
        if (match.homeScore > match.awayScore)
          this.teams[match.homeTeam].points += 3;
        if (match.homeScore === match.awayScore) {
          this.teams[match.homeTeam].points += 1;
          this.teams[match.awayTeam].points += 1;
        }
        if (match.homeScore < match.awayScore)
          this.teams[match.awayTeam].points += 3;

        // input don't have type=number (cause of chrome/safari spinner bug), so conversion is needed
        var homeScore = Number(match.homeScore);
        var awayScore = Number(match.awayScore);

        this.teams[match.homeTeam].goalsMade += homeScore;
        this.teams[match.awayTeam].goalsTaken += homeScore;

        this.teams[match.homeTeam].goalsTaken += awayScore;
        this.teams[match.awayTeam].goalsMade += awayScore;
      } else {
        everyGameHasBeenPlayed = false;
      }
    }

    // Only fill qualified teams list if every game has been played
    if (everyGameHasBeenPlayed) {
      console.log(this.getTeamsByRank());
      this.qualifiedTeams = this.getTeamsByRank().slice(0, 2);
      console.log(this.qualifiedTeams);
    } else {
      this.qualifiedTeams = [];
    }
  }

  this.first = function () {
    if (this.qualifiedTeams.length == 2)
      return this.qualifiedTeams[0];
    else
      return null;
  }

  this.second = function () {
    if (this.qualifiedTeams.length == 2)
      return this.qualifiedTeams[1];
    else
      return null;
  }

  this.setMatchResults = function(id, homeScore, awayScore) {
    var match;
    var found = false;

    for (var i = 0; i < this.matches.length; i++) {
      match = this.matches[i];

      if (match.id === Number(id)) {
        found = true;
        match.homeScore = homeScore;
        match.awayScore = awayScore;
      }
    }

    if (!found)
        console.log('Group > setMatchResults : id ' + id + ' not found.');
  }

};

function SecondRoundMatch(id, homeTeamTarget, homeTeamFunction, awayTeamTarget, awayTeamFunction) {
  // TODO: dependency of targets
  // TODO: need to call refresh

  this.homeTeamFunction = homeTeamFunction;
  this.homeTeamTarget = homeTeamTarget;
  this.awayTeamFunction = awayTeamFunction;
  this.awayTeamTarget = awayTeamTarget;

  this.id = id;
  this.homeTeam = null;
  this.awayTeam = null;
  this.homeScore = null;
  this.awayScore = null;
  this.tiedMatchWinner = null;

  this.refresh = function () {
    this.homeTeam = this.homeTeamFunction.call(this.homeTeamTarget);
    this.awayTeam = this.awayTeamFunction.call(this.awayTeamTarget);
    return this;
  }

  this.getWinner = function () {
    if (this.homeScore === null || this.awayScore === null)
      return null;

    // input don't have type=number (cause of chrome/safari spinner bug), so conversion is needed
    var homeScore = Number(this.homeScore);
    var awayScore = Number(this.awayScore);

    var winner = this.homeTeam;
    if (homeScore < awayScore) {
      winner = this.awayTeam;
    }
    if (homeScore === awayScore) {
      winner = this.tiedMatchWinner;
    }
    return winner;
  }

  this.homeTeamWon = function () {
    return this.getWinner() === this.homeTeam;
  }

  this.awayTeamWon = function () {
    return this.getWinner() === this.awayTeam;
  }

  this.isNotTied = function () {
    return this.homeScore !== this.awayScore
      || this.homeScore === null
      || this.homeScore === ''
      || this.awayScore === null
      || this.awayScore === '';
  }

  this.getLoser = function () {
    if (this.getWinner())
      return this.getWinner() === this.homeTeam ? this.awayTeam : this.homeTeam;
    else
      return null;
  }

  this.setTiedMatchWinner = function (team) {
    this.tiedMatchWinner = team;
  }
}

/**********************************************************************
 * Testes unitÃ¡rios para critÃ©rios de classificaÃ§Ã£o na fase de grupos
 **********************************************************************/
var testGetTeamsByRank = function () {

  var assertRanking = function (caller, ranking, expected) {
    for (var i = 0; i < expected.length; i++)
      if (ranking[i].name !== expected[i])
        alert('FAIL (' + caller.name + ') > [' + i + ']: ' + ranking[i].name + ' - expected: ' + expected[i]);
  }

  var setUpGroup = function (matches) {
    return new Group(
      'A',
      [
        {name: 'A'},
        {name: 'B'},
        {name: 'C'},
        {name: 'D'}
      ],
      matches).init();
  }

  function testTwoTeamsByGoalDiff() {
    /*
     * A empata com B nos pontos mas ganha no saldo de gols
     *
     * A: 0 x 0 :B
     * C: 0 x 0 :D
     * A: 0 x 0 :C
     * B: 0 x 0 :C
     * A: 2 x 0 :D
     * B: 1 x 0 :D
     */
    var matches = [
      {homeTeam: 0, awayTeam: 1, homeScore: 0, awayScore: 0},
      {homeTeam: 2, awayTeam: 3, homeScore: 0, awayScore: 0},
      {homeTeam: 0, awayTeam: 2, homeScore: 0, awayScore: 0},
      {homeTeam: 1, awayTeam: 2, homeScore: 0, awayScore: 0},
      {homeTeam: 0, awayTeam: 3, homeScore: 2, awayScore: 0}, // <--| jogos que desempatam
      {homeTeam: 1, awayTeam: 3, homeScore: 1, awayScore: 0}  // <--|
    ];

    var group = setUpGroup(matches);
    var ranking = group.getTeamsByRank();
    var expected = ['A', 'B', 'C', 'D'];

    assertRanking(testTwoTeamsByGoalDiff, ranking, expected);
  }

  function testTwoTeamsByGoalMade() {
    /*
     * A empata com B nos pontos e saldo de gols mas ganha nos gols prÃ³
     *
     * A: 0 x 0 :B
     * C: 0 x 0 :D
     * A: 0 x 0 :C
     * B: 0 x 0 :C
     * A: 2 x 1 :D
     * B: 1 x 0 :D
     */
    var matches = [
      {homeTeam: 0, awayTeam: 1, homeScore: 0, awayScore: 0},
      {homeTeam: 2, awayTeam: 3, homeScore: 0, awayScore: 0},
      {homeTeam: 0, awayTeam: 2, homeScore: 0, awayScore: 0},
      {homeTeam: 1, awayTeam: 2, homeScore: 0, awayScore: 0},
      {homeTeam: 0, awayTeam: 3, homeScore: 2, awayScore: 1}, // <--| jogos que desempatam
      {homeTeam: 1, awayTeam: 3, homeScore: 1, awayScore: 0}  // <--|
    ];

    var group = setUpGroup(matches);
    var ranking = group.getTeamsByRank();
    var expected = ['A', 'B', 'C', 'D'];

    assertRanking(testTwoTeamsByGoalMade, ranking, expected);
  }

  function testTwoTeamsByMatchResult() {
    /*
     * A = P: 4, SG: 0, GP: 1
     * B = P: 4, SG: 0, GP: 1
     * C = P: 3, SG: 0, GP: 2
     * D = P: 4, SG: 0, GP: 3
     *
     * A: 0 x 1 :B
     * C: 2 x 2 :D
     * A: 0 x 0 :C
     * B: 0 x 0 :C
     * A: 1 x 0 :D
     * B: 0 x 1 :D
     */
    var matches = [
      {homeTeam: 0, awayTeam: 1, homeScore: 0, awayScore: 1}, // <-- confronto direto que coloca B na frente de A
      {homeTeam: 2, awayTeam: 3, homeScore: 2, awayScore: 2}, // <-- coloca D na frente por gol prÃ³
      {homeTeam: 0, awayTeam: 2, homeScore: 0, awayScore: 0},
      {homeTeam: 1, awayTeam: 2, homeScore: 0, awayScore: 0},
      {homeTeam: 0, awayTeam: 3, homeScore: 1, awayScore: 0},
      {homeTeam: 1, awayTeam: 3, homeScore: 0, awayScore: 1}
    ];

    var group = setUpGroup(matches);
    var ranking = group.getTeamsByRank();
    var expected = ['D', 'B', 'A', 'C'];

    assertRanking(testTwoTeamsByMatchResult, ranking, expected);
  }

  // Run all test cases
  testTwoTeamsByGoalDiff();
  testTwoTeamsByGoalMade();
  testTwoTeamsByMatchResult();
}
