<template>
  <div class="aboutDiv">
    <h1>About Us</h1>
    <h2> 
      This web application was developped by 3 ESIEE Students :
    </H2>
    <p> Brunet Thomas </p>
    <p> Bureau Dimitri </p>
    <p> Moreno Pierre </p>
  </div>
  <span class="imageSpan">
    <img src= "../assets/ImageAbout/ImageThomas.jpg"/>
    <img src= "../assets/ImageAbout/ImageDimitri.jpg"/>
    <img src= "../assets/ImageAbout/ImagePierre.jpg"/>
  </span>
</template>

<style>

.aboutDiv h1{
  text-align: center;
  margin-top: 60px;
  margin-bottom: 40px;
}

.aboutDiv h2{
  text-align: center;
  font-size: 24px;
  margin-bottom: 60px;
}

.aboutDiv p{
  text-align: center;
  font-size: 20px;
}

.aboutDiv ul{
  text-align: center;
  list-style-type: none;
}

.imageSpan{
  
  margin-left: 190px;
  margin-right: 220px;
}

.imageSpan img{
  margin-top: 80px;
  margin-left: 60px;
}

</style>
