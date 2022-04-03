<template>
  <div>
    <!-- <div id="nav"> -->
      <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="#" style="margin-left: 15px">Paper Trails</a>
        <div class="" id="navbarSupportedContent">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item">
              <a class="nav-link" href="/" style="padding-right: 25px">Home</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="https://github.com/JosephShepin/PaperTrails" style="padding-right: 25px">Github</a>
            </li>
          </ul>
        </div>
      </nav>
      <!-- <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link> -->
    <!-- </div> -->
    <router-view />
  </div>
</template>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

#nav {
  padding: 30px;
  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
