<template>
  <div class="page_container">
    <div>
      <div class="nav">
        <nuxt-link to="/" class="button--grey">Retour à l'index</nuxt-link>
        <nuxt-link to="/videos" class="button--grey">Liste des vidéos</nuxt-link>
      </div>
      <h2 class="subtitle">List Users</h2>
      <div>
        <ul>
          <li v-for="user in users.data" class="item">
              <p>Pseudo : {{ user.pseudo }} (date de création : {{ user.created_at }})</p>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  async asyncData () {
    const {data} = await axios.get('http://localhost:5000/users')
    return {users:data}
  }
};
</script>

<style>

</style>