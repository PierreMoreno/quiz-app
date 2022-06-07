<template>
  <div class="scoreRecapDiv" v-if="isCreated">
    <h1>Your Score :</h1>

    <p> {{playerScore}} / {{numTotalQuestions}} </p>

  </div>
</template>

<style>

.scoreRecapDiv h1{
  text-align: center;
  margin-top: 200px;
  margin-bottom: 40px;
}

.scoreRecapDiv p{
  text-align: center;
  font-size: 26px;
}

</style>

<script>
import quizApiService from "@/services/QuizApiService.js";
import participationStorageService from "@/Services/ParticipationStorageService.js";

export default {
  name: "HomePage",
  data() {
    return { 
      isCreated: false,
      numTotalQuestions: 0,
      playerScore: 0
    };
  },

  async created() {
    console.log("Composant ScoreRecap created'");
    var quizInfo = await quizApiService.getQuizInfo();
    console.log(quizInfo);
    this.numTotalQuestions = quizInfo.data.size;
    this.playerScore = participationStorageService.getParticipationScore();
    console.log(quizInfo.data);
    this.isCreated = true;
  }

};

</script>