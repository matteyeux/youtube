<template>
    <div>
    upload here
        <input type="file" @change="onFileSelected">
        <button @click="onUpload">AAA</button>
    </div>
</template>

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
            fd.append('name', 'AlexProfond');
            axios.post(`http://localhost:5000/video`, fd, config)
            .then(res => {
                console.log()
            });
        }
    }
}
</script>