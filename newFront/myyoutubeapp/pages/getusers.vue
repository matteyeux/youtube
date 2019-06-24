<template>
  <article>
    <section>
      <h1>GET API Result List Users</h1>
      <div>
        <ul>
          <li v-for="user in users.data" class="item">
          	<p>Pseudo : {{ user.pseudo }} (date de création : {{ user.created_at }})</p>
            <!-- <nuxt-link :to="'/user/' + user.id">{{ user.pseudo }}</nuxt-link> -->
          </li>
        </ul>
      </div>
    </section>
  </article>
</template>

<script>
  import axios from 'axios'

  export default {
    async asyncData () {
      const {data} = await axios.get('http://localhost:5000/users')
      return {users:data}
    }
  }

</script>

<style>
</style>