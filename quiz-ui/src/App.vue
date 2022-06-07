<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <div class="headerDiv">
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
        <RouterLink to="/admin">Admin</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style>
@import '@/assets/base.css';

#app {
  max-width: 1280px;
  max-height: 900px;
  margin: 0 auto;
  padding: 2rem;
  font-weight: normal;
}

header {
  border: 2px solid var(--color-border);
  font-size: 20px;
  text-align: center;
  margin-left: 286px;
  margin-right: 286px;
  padding : 5px;
}

a,
.green {
  text-decoration: none;
  color: hsla(160, 100%, 37%, 1);
  transition: 0.4s;
}

@media (hover: hover) {
  a:hover {
    background-color: hsla(160, 100%, 37%, 0.2);
  }
}

.headerDiv nav a.router-link-exact-active {
  color: var(--color-text);
}

.headerDiv  nav a.router-link-exact-active:hover {
  background-color: transparent;
}

.headerDiv  nav a {
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

.headerDiv  nav a:first-of-type {
  border: 0;
}

</style>
