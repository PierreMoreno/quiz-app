<template>
  <div class = "homeDiv" v-if="isCreated">
    <h1>Home page</h1>
    <div class = "scoresListDiv" v-for="(scoreEntry, index) in registeredScores" v-bind:key="scoreEntry.date">
      <p v-if="scoreEntry.score != null && index <= 10"> {{ scoreEntry.playerName }} - {{ scoreEntry.score }} </p>
    </div>
    <nav>
      <RouterLink to="/start-new-quiz-page">Start the quiz !</RouterLink>
    </nav>
  </div>
</template>

<style>

.homeDiv{
  text-align: center;
}

.homeDiv h1{
  margin-top: 60px;
  margin-bottom: 40px;
}

.homeDiv nav{
  margin-top: 60px;
  font-size: 24px;
}

.scoresListDiv{
  font-size: 20px;
  margin-bottom: 0px;
}

</style>



<script>

import quizApiService from "@/services/QuizApiService.js";

export default {
  name: "HomePage",
  data() {
    return { 
      registeredScores: [],
      isCreated: false
    };
  },
  async created() {
    console.log("Composant Home page 'created'");
    var quizInfo = await quizApiService.getQuizInfo();
    this.registeredScores = quizInfo.data.scores;
    console.log(quizInfo.data);
    this.isCreated = true;
  }
};

</script>

