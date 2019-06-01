<template>
    <div>

      <h1>all users</h1>      
      <ul>
        ID - Pseudo - Username<hr/><br/>
        <div v-for="user in users" class="users" :key="user">
          <nuxt-link v-bind:to="'/users/' + user.id" >{{ user.id }} - {{ user.pseudo}} - {{ user.pseudo }</nuxt-link>
        </div>
      </ul>

    <hr>
    Data Complet :
        <pre>{{ users }}</pre>
   </div>
</template>

<script>
import axios from 'axios';

export default {
  async asyncData ({ app, params }) {

    const { data } = await app.$axios.get('http://172.16.0.10:5000/users')
    console.log('data arrived')
    
    return { users:data.data }

//    try {
//      const { data } = await app.$axios.get('http://172.16.0.10:5000/users')
//      console.log('data arrived')
//      return { user: data.data }
//    } catch (e) {
//      console.log(e)
//    }
  },
}
</script>

<style>

</style>
