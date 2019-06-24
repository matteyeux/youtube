<template>
  <article>
    <section>
      <h1>GET API Result List Users</h1>
      <div>
        <ul>
          <li v-for="video in videos.data" class="item">
          	<p>{{ video.format }}</p>
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
      const {data} = await axios.get('http://localhost:5000/videos')
      return {videos:data}
    }
  }

</script>

<style>
</style>