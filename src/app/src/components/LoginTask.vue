<template>
  <form @submit="onSubmit">
    <div class="form-control">
      <label>User Name</label>
      <input type="text" v-model="username" />
    </div>
    <div class="form-control">
      <label>Password</label>
      <input :type="password_type" v-model="password" />
      <i :class="eye_visible" @click='onClick'></i>
      
    </div>
    <div class="form-control">
      <input type="submit" value="LOG IN" />
    </div>
  </form>

</template>

<script>
export default {
  name: 'LoginTask',
  data() {
    return {
      username: '',
      password: '',
      eye_visible: "far fa-eye",
    }
  },
  computed: {
		password_type: function() {
			return (this.eye_visible === "far fa-eye") ? 'password': 'text'
		},
	},
  methods: {
    onSubmit(e) {
      e.preventDefault()

      if (!this.username) {
        alert('Enter user name and password')
        return
      }

      const newTask = {
        // id: Math.floor(Math.random() * 100000),
        username: this.username,
        password: this.password,
      }

      this.$emit('btn-click', newTask)

      this.username = ''
      this.password = ''
    },
    onClick() {
      this.eye_visible = (this.eye_visible === "far fa-eye") 
      ? "far fa-eye-slash": "far fa-eye"
    },
  },
}
</script>

<style scoped>

.form-control {
  margin: 5px 0;
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
}

.form-control label {
  width: 100%;
  color: #fff;
  font-size: 15px;
}

.form-control input {
  background:#4c5374; 
  width: 300px;
  height: 30px;
	margin: 5px;
  padding: 3px 7px;
  font-size: 15px;
  border:0;
  border-radius: 5px;
}

.form-control input[type="submit"] { 
  background: #fff;
  color: #202f5c;
	width: 300px;
	height: 35px;
  margin-top: 70px;
  border: 0;
  border-radius: 5px;
  cursor: pointer;
  font-size: 15px;
}

i {
  color: white;
  margin-right: 20px;
  margin-top: -30px;
  cursor: pointer;
  align-self: flex-end;
  background:#4c5374;
}
</style>
