<template>

  <div class="questionDisplayDiv" v-if="question" :src="question">
    <h2>{{question.questionTitle}}</h2>
    <img v-bind:src="question.questionImage" />
    <p>{{question.questionText}}</p>
    <div class="answerListDiv green" v-for="(answer, index) in question.possibleAnswers">
      <a @click="$emit('answer-selected', index+1)">{{answer.text}}</a>
    </div>
  </div>

</template>

<style>

.questionDisplayDiv{
  text-align: center;
}

.questionDisplayDiv img{
  max-width:480px;
  max-height:270px;
}

.questionDisplayDiv p{
  margin-bottom: 60px;
  font-size: 20px;
}

.answerListDiv{
  margin-bottom: 40px;
}

.answerListDiv a{
  font-size: 20px;  
}

</style>

<script>

export default {

    name: "QuestionDisplay",

    props: {
        question: {
            type: Object
        }
    },

    emits: ["answer-selected"],

    created() {
      console.log("Composant Question Display 'created'");
      console.log(this.question.questionImage);
    }
};

</script>