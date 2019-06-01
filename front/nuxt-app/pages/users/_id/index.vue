<template>
    <div>
      <h1>{{ $route.params.id }}</h1>
      <h1>all users</h1>      
      <ul>
        User information<hr/><br/>
        <p>id: {{ user.id }}</p> 
        <p>pseudo: {{ user.pseudo }}</p>
        <p>username: {{ user.username }}</p>
        <p>created: {{ user.created_at }}</p>
        <p v-if="user.email">{{ user.email }}</p>
      </ul>
    <hr>
    Data Complet :
    <pre>{{ user }}</pre>
    </div>
</template>

<script>
import axios from 'axios';
import { Route } from "vue-router"

export default {
  validate({ params }) {
    return !isNaN(+params.id)
  },

  async asyncData ({params, error}) {
    try {
      const { data } = await axios.get(`http://172.16.0.10:5000/user/${+params.id}`)
      return { user:data.data }
    } catch (e) {
      error({ message: 'User not found', statusCode: 404 })
    }
  }
}
</script>

<style>

</style>
