<template>
  <div class="home">
    <div class="container shadow p-3 mb-5 bg-white rounded">
      <h1>Welcome to Lorem Ipsum</h1>
      <br>
      <input class="form-control address-input" placeholder="Enter Candidate Name">
      <br>
      <button class="btn btn-primary">Search</button>
    </div>
  </div>
</template>

<script>
// import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'Home',
  components: {
  }
}
</script>

<style lang="sass" scoped>
.container
  display: flex
  flex-direction: column
  align-items: center
  max-width: 750px !important

.address-input
  width: 100%
  max-width: 600px
  text-align: center
</style>