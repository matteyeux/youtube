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
          <form>
          <div class="form-group">
            <label for="InputUsername">Username</label>
            <input type="text" v-model="form.username" class="form-control" id="InputUsername" placeholder="Enter your username" required>
            <small id="usernameHelp" class="form-text text-muted">Your username must be unique</small>
          </div>
          <div class="form-group">
            <label for="InputPseudo">Pseudo</label>
            <input type="text" v-model="form.pseudo" class="form-control" id="InputPseudo" placeholder="Enter your pseudo" required>
            <small id="pseudonameHelp" class="form-text text-muted">
              Your username does not have to be unique
            </small>
          </div>
          <div class="form-group">
            <label for="InputEmail">Email address</label>
            <input type="email" v-model="form.email" class="form-control" id="InputEmail" placeholder="Enter your email" required>
          </div>
          <div class="form-group">
            <label for="InputPassword">Password</label>
            <input type="password" v-model="form.password" class="form-control" placeholder="Enter your password" required>
          </div>
          <button type="submit" v-on:click="formSubmit" class="btn btn-primary">Submit</button>
          </form>
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
      form : {
        username: null,
        pseudo: null,
        email: null,
        password: null
      }
    };
  },
  methods: {
    formSubmit(e) {
      e.preventDefault();
      let currentObj = this;
      axios.post('http://localhost:5000/user', this.form)
      .then(() => this.$router.push(this.$route.query.redirect || '/'))
      .catch(function (error) {
        currentObj.output = error;
      });
    }
  }
};
</script>

<style>

</style>