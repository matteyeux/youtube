<template>
  <header class="header">
    <h1 class="title">My YT</h1>
    <ul>
      <li>
        <a href="/">Home</a>
      </li>
      <li>
        <a href="/users/">Users</a>
      </li>
      <li>
        <nuxt-link to="users">Bad users</nuxt-link>
      </li>
      <li>
        <a href="/about">About</a>
      </li>
    </ul>
  </header>
</template>

<script>
export default {
  name: "AppHeader"
};
</script>

<style>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px dotted #ccc;
}

.header .title {
  font-size: 3rem;
  color: #526488;
}

.header ul {
  display: flex;
}

.header a {
  display: inline-block;
  background: #333;
  color: #fff;
  padding: 0.3rem 1rem;
  margin-right: 0.5rem;
}
</style>
