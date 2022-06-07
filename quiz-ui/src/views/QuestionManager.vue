<template>

  <div class="questionManagerDiv" v-if="isCreated">
    <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</h1>
    <QuestionDisplay :question="currentQuestion" @answer-selected="answerClickedHandler" />
    <p>Your score: {{playerScore}} </p>
  </div>

</template>

<style>

.questionManagerDiv h1{
    text-align: center;
    margin-top: 60px;
    margin-bottom: 40px;
}

.questionManagerDiv p{
    text-align: center;
    
}

</style>

<script>

import QuestionDisplay from "../views/QuestionDisplay.vue";
import quizApiService from "@/services/QuizApiService.js";
import participationStorageService from "@/Services/ParticipationStorageService.js";

export default {

    name: "QuestionManager",

    data() {
        return { 

            currentQuestion: {
                questionImage : "",
                possibleAnswers : [],
                questionText: "",
                questionTitle : ""
            },

            currentQuestionPosition : 1,
            totalNumberOfQuestion : '',
            playerScore : 0,

            playerAnswers: [],

            isCreated: false
        };
    },

    components : {

        QuestionDisplay

    },

    async created() {
        console.log("Composant Question Manager 'created'");
        var quizInfo = await quizApiService.getQuizInfo();
        this.totalNumberOfQuestion = quizInfo.data.size;
        this.currentQuestion = await this.loadQuestionByPosition();
        console.log(this.currentQuestion);
        this.isCreated = true;
    },

    methods :{

        async loadQuestionByPosition(){
            var currentQuestionRequest = await quizApiService.getQuestion(this.currentQuestionPosition);
            var currentQuestionData = currentQuestionRequest.data;

            this.currentQuestion.questionImage = currentQuestionData.image;
            this.currentQuestion.possibleAnswers = currentQuestionData.possibleAnswers;
            this.currentQuestion.questionText = currentQuestionData.text;
            this.currentQuestion.questionTitle = currentQuestionData.title;

            console.log(this.currentQuestion);

            return this.currentQuestion;
        },

        async answerClickedHandler(answerIndex){
            console.log("Answer clicked");
            
            this.playerAnswers.push(answerIndex);
            console.log(this.playerAnswers);

            if(this.currentQuestion.possibleAnswers[answerIndex-1].isCorrect)
                this.playerScore++;

            if(this.currentQuestionPosition+1 <= this.totalNumberOfQuestion){
                this.currentQuestionPosition++;
                this.loadQuestionByPosition();
            }
                
            else
                this.endQuiz();
        },

        async endQuiz(){
            participationStorageService.saveParticipationScore(this.playerScore);

            var participation= {
                "playerName": participationStorageService.getPlayerName(),
                "answers": this.playerAnswers
            }
            quizApiService.postParticipation(participation);
            this.$router.push('/score-recap');
        }

    }
};

</script>