<template>
  <div class="page_container">
    <div>
      <div class="nav">
        <nuxt-link to="/" class="button--grey">Retour à l'index</nuxt-link>
        <nuxt-link to="/videos" class="button--grey">Retour à la Liste des video</nuxt-link>
      </div>
      <h2 class="subtitle">Video information : {{ video.name }}</h2>
      <div>
        <ul>
          <p>id: {{ video.id }}</p>
          <p>name: {{ video.name }}</p>
          <p>source: {{ video.source }}</p>
          <p>created: {{ video.created_at }}</p>
          <p>view: {{ video.view }}</p>
        </ul>
        <hr>
        <video width="50%" controls style="margin: 25px">
          <source :src="require('~/assets/videos/SampleVideo_1280x720_30mb.mp4')" type="video/mp4">
        </video>
      </div>
    </div>
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
      const { data } = await axios.get(`http://localhost:5000/video/${+params.id}`)
      return { video:data.data }
    } catch (e) {
      error({ message: 'Video not found', statusCode: 404 })
    }
  }
};
</script>

<style>

</style>