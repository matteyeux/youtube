<template>
  <div class="container">
    <div>
      <div class="row">
        <nuxt-link to="/createUser" class="button--grey">Registration</nuxt-link>
        <nuxt-link to="/auth/login" class="button--grey">Login</nuxt-link>
      </div>
      <div class="row">
        <nuxt-link to="/users" class="button--grey">Liste des utilisateurs</nuxt-link>
        <nuxt-link to="/videos" class="button--grey">Liste des vidéos</nuxt-link>
      </div>
      <logo />
      <h1 class="title">
        My Youtube
      </h1>
      <h2 class="subtitle">
        Broadcast together
      </h2>
      <div class="links">
        <a href="https://nuxtjs.org/" target="_blank" class="button--green">Documentation</a>
        <a href="https://github.com/nuxt/nuxt.js" target="_blank" class="button--grey">GitHub</a>
      </div>
    </div>
  </div>
</template>

<script>
import Logo from '~/components/Logo.vue'

export default {
  components: {
    Logo
  }
};
</script>

<style>
.container {
  margin: 0 auto;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.title {
  font-family: 'Quicksand', 'Source Sans Pro', -apple-system, BlinkMacSystemFont,
    'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  display: block;
  font-weight: 300;
  font-size: 100px;
  color: #35495e;
  letter-spacing: 1px;
}

.subtitle {
  font-weight: 300;
  font-size: 42px;
  color: #526488;
  word-spacing: 5px;
  padding-bottom: 15px;
}

.links {
  padding-top: 15px;
}

.row {
  margin: 25px auto;
}

.page_container {
  margin: 0px 50px;
}

.nav {
  margin: 25px 0px;
}
</style>
