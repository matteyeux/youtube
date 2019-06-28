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
<!--         <div class="md-6">
          <h2 class="subtitle">Commentaire vidéo</h2>
          <ul>
            <li v-for="comment in comments" class="item">
              <div class="card w-75">
                <div class="card-body">
                  <h5 class="card-title">Commentaire de {{ comment.user_id }}</h5>
                  <p class="card-text">With supporting text below as a natural lead-in to additional content.</p>
                </div>
              </div>
            </li>
          </ul>
        </div> -->
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
      const {data} = await axios.get(`http://localhost:5000/video/${+params.id}`)
      return { video:data.data }
    } catch (e) {
      error({ message: 'Video not found', statusCode: 404 })
    }
  },
};

//   async asyncData2 ({params, error}) {
//     try {
//       const {data} = await axios.get(`http://localhost:5000/video/${+params.id}/comments`)
//       return { comments:data.data }
//     } catch (e) {
//       error({ message: 'Comments not found', statusCode: 404 })
//     }
//   }

// const { dataVideo } = await axios.get(`http://localhost:5000/video/${+params.id}`)
// const { dataComment } = await axios.get(`http://localhost:5000/video/${+params.id}/comments`)
// return { video:dataVideo.data,  comment:dataComment.data}

// async componentDidMount() {
//   const firstRequest = await axios.get(URL1);
//   const secondRequest = await axios.get(URL2);
//   const thirdRequest = await axios.get(URL3);

//   this.setState({
//     p1Location: firstRequest.data,
//     p2Location: SecondRequest.data,
//     p3Location: thirdRequest.data,
//   });

</script>

<style>

</style>