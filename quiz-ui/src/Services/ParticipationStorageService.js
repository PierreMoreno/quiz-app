export default {
    clear() {
        window.localStorage.setItem("playerName", "");
        window.localStorage.setItem("score", 0);
    },
    savePlayerName(playerName) {
          window.localStorage.setItem("playerName", playerName);
    },
    getPlayerName() {		
          return window.localStorage.getItem("playerName");
    },
    saveParticipationScore(participationScore) {
        window.localStorage.setItem("score", participationScore);
    },
    getParticipationScore() {
          return window.localStorage.getItem("score");
    }
};