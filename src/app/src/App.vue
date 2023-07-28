<template>
  <router-view></router-view>
</template>

<script>

export default {
  name: 'App',
}
</script>

<style scope>

* {
  background-color: #202f5c; 
}

#app {
  height: 95vh;
  padding: 15px;
  /* background: #00c3ff; */
  display: flex;
  justify-content: center;
  align-items: center;
}

.container {
  height: 95vh;
  width: 100%;
  border: 0;
  background: #fff; 
  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  align-items: stretch;
}
</style>
