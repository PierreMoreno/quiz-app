<template>
  <h1>Home page</h1>
  <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
    {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
  </div>
  <router-link to="/start-new-quiz-page">Démarrer le quiz !</router-link>
</template>

<script>
import quizApiService from "@/services/QuizApiService";

var registeredScores = []

export default {
  name: "HomePage",
  registeredScores,
  data() {
    return { registeredScores
    };
  },
  async created() {
		console.log("Composant Home page 'created'");
    var quizInfo = await quizApiService.getQuizInfo()
    registeredScores = quizInfo.data.scores;
    console.log(registeredScores);
  }
};
</script>
