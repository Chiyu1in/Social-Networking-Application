<template>
  <div class="login">
    <LoginTask @btn-click="verifyAccount" />
  </div>
</template>

<script>
import LoginTask from "../components/LoginTask.vue"

export default {
  name: 'Login',
  components: {
    LoginTask
  },
  data() {
    return {
      server_url: 'https://ptt-server-stage.azurewebsites.net'
    }
  },
  methods: {
    async verifyAccount(task) {
      
      const data = new URLSearchParams({username: task.username, password: task.password})

      // let tokenInfo
      try{
        const response = await fetch(`${this.server_url}/login`, {
          method: 'POST',
          headers: {
            'content-type': 'application/x-www-form-urlencoded',
          },
          body: data
        });
        if (!response.ok) {
          alert('Invalid user name and password!');
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const tokenInfo = await response.json();
        localStorage.setItem("tokenInfo", JSON.stringify(tokenInfo));
        this.$router.push("/");
      } catch(error) {
        console.error('Error:', error);
      }
    },
    
  },
}
</script>

<style scoped>
.login {
  height: 400px;
  width: 400px;
  border: 1px solid steelblue;
  padding: 30px;
  background-color: #202f5c;
  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  justify-content: center;
  align-items: center;
}
</style>
