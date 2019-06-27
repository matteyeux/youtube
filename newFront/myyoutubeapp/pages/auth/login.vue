<template>
  <div class="page_container">
    <div>
      <div class="nav">
        <nuxt-link to="/" class="button--grey">Back to Index</nuxt-link>
        <nuxt-link to="/users" class="button--grey">List of Users</nuxt-link>
        <nuxt-link to="/videos" class="button--grey">List of Videos</nuxt-link>
      </div>
      <h2 class="subtitle">Registration</h2>
      <div>
        <div class="col-md-4">
          <form @submit.prevent="formSubmit">
          <div class="form-group">
            <label for="InputUsername">Username</label>
            <input type="text" v-model="username" class="form-control" id="InputUsername" placeholder="Enter your username" required>
            <small id="usernameHelp" class="form-text text-muted">Your username must be unique</small>
          </div>
          <div class="form-group">
            <label for="InputPassword">Password</label>
            <input type="password" v-model="password" class="form-control" placeholder="Enter your password" required>
          </div>
          <button type="submit" class="btn btn-primary">Submit</button>
          </form>
          Token : {{ token }}
          <br/>{{ $store.state.token }}<br/>
          <button @click="$store.commit('updateToken', 'ahah')">aa {{ $store.state.counter }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      username: '',
      output: '',
      token: 'vide'
    };
  },
  methods: {
    formSubmit(e) {
      const {data} = axios
      .post('http://localhost:5000/auth', {
        username: this.username,
        password: this.password
      })
      .then((result) => {
        console.log(result.data.data.token);
        this.token = result.data.data.token;
        
        //set cookie token
        this.$cookies.set('token', result.data.data.token, {
          path: '/',
          maxAge: 60 * 60 * 24 * 7
        })
        
        this.$store.commit('updateToken', result.data.data.token)
      })  
    }
  }
};

</script>

<style>

</style>