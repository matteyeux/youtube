In this folder, run :

# Build the image
docker build --no-cache -t yt_nuxt .

# Run the container
docker container prune -f && docker run -it --name yt_nuxt -p 3000:3000 -v $(pwd)/my_app:/usr/src/nuxt-app yt_nuxt