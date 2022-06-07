<template>
  <div class="QuizUsernameDiv">
      <h1>Start a new Quiz !</h1>
      <p> Please type your username:</p>
      <input type="text" v-model="username">
      <button class="favorite styled" type="button" @click="launchNewQuiz"> Go ! </button>
  </div>
</template>

<style>
@import '@/assets/base.css';

.QuizUsernameDiv{
  text-align: center;
}

.QuizUsernameDiv h1{
  margin-top: 60px;
  margin-bottom: 40px;
}

.QuizUsernameDiv input{
  background-color : #424242; 
  color: #ffffff;
  padding-left: 10px;
  margin-right: 10px;
}

.QuizUsernameDiv button{
  background-color : #424242; 
  color: #ffffff;
}

</style>

<script>
import participationStorageService from "@/Services/ParticipationStorageService.js";

export default {
    
    name: "NewQuizPage",

    data() {
        return { 
            username : ""
        };
    },

    created() {
        console.log("Composant New Quiz Page 'created'");
        this.username = participationStorageService.getPlayerName();
    },

    methods :{
        launchNewQuiz(){
            if(this.username != ""){
                console.log("Launch new quiz with", this.username);
                participationStorageService.clear();
                participationStorageService.savePlayerName(this.username);           
                this.$router.push('/questions');
            }       
        },
    }

};

</script>
