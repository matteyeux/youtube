<template>
  <div class="page_container">
    <div>
      <div class="nav">
        <nuxt-link to="/" class="button--grey">Retour à l'index</nuxt-link>
        <nuxt-link to="/videos" class="button--grey">Retour à la Liste des video</nuxt-link>
      </div>
      <h2 class="subtitle">Uploader une video</h2>
      <div>
        <input type="file" @change="onFileSelected">
        <label for="namevideo">Nome de la video</label>
        <input v-model="namevideo" class="form-control" placeholder="Nom de la vidéo" required>
        <button @click="onUpload">Envoyer</button>
      </div>
    </div>
  </div>
</template>



<!-- <template>
    <div>
    Uploader une video
        <input type="file" @change="onFileSelected">
        <button @click="onUpload">Envoyer</button>
    </div>
</template> -->

<script>
import axios from 'axios'

export default {
    data () {
        return {
            selectedFile: null
        }
    },
    methods: {
        onFileSelected(event) {
           this.selectedFile = event.target.files[0]
        },
        onUpload() {
            const config = { headers: { 'content-type': 'multipart/form-data', 'Authorization': this.$store.state.token } }
            const fd = new FormData();
            fd.append('source', this.selectedFile);
            fd.append('name', this.namevideo);
            axios.post(`http://localhost:5000/video`, fd, config)
            .then(() => this.$router.push(this.$route.query.redirect || '/videos'));
        }
    }
};
</script>