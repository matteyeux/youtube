<template>
  <div class="page_container">
    <div>
      <div class="nav">
        <nuxt-link to="/" class="button--grey">Retour à l'index</nuxt-link>
        <nuxt-link to="/users" class="button--grey">Liste des utilisateurs</nuxt-link>
      </div>
      <h2 class="subtitle">List Vidéos</h2>
      <div>
        <ul>
          <li v-for="video in videos.data" class="item">
            <div class="row">
              <nuxt-link v-bind:to="'/videos/' + video.id" style="margin-top: 50px">{{ video.id }} - {{ video.name}}</nuxt-link>
              <video :src="require('~/assets/video/SampleVideo_1280x720_30mb.mp4')" width="160" height="120" style="margin-left: 20px">
              </video>
            </div>
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
      const {data} = await axios.get('http://localhost:5000/videos')
      return {videos:data}
    }
  };
</script>

<style>

</style>