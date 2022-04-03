<template>
    <div style=' display: flex;'>
        <Home :class="{'first': !extraPerson}" :smaller="true" v-on:new="addPerson()" />
        <Home v-if='extraPerson' :smaller="extraPerson" />
    </div>
</template>

<script>
import Home from './Home.vue'

export default {
  components: {
      Home
  },
  data(){
      return {
          extraPerson: false,
      }
  },
  methods : {
      addPerson(){
          this.extraPerson = true
      }
  }
}
</script>

<style scoped lang='sass'>
.first
    position: absolute
    left: 60%
    transform: translateX(-50%)
</style>
