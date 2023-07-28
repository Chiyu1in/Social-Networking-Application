<template>
    <div v-show="$route.hash==='#user-info'" class="info">
        <img
            @click="changeImg" 
            v-show="!show_form"
            src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" 
        />
        <Button @btn-click='editProfile' text='Edit Profile' v-show="!show_form" />
        <UserForm 
            @submit="submit" 
            @cancel="cancel" 
            v-show="show_form" 
            :user_info="user_info" 
        />

        <div v-show="!show_form" class="info-control">
            <i class="far fa-building"></i>
            <div class="text">{{user_info.company}}</div>
        </div>
        <div v-show="!show_form" class="info-control">
            <i class="fas fa-map-marker-alt"></i>
            <div class="text">{{user_info.place}}</div>
        </div>
        <div v-show="!show_form" class="info-control">
            <i class="far fa-envelope"></i>
            <div class="text">{{user_info.email}}</div>
        </div>
        <div v-show="!show_form" class="info-control">
            <i class="fas fa-phone"></i>
            <div class="text">{{user_info.phone}}</div>
        </div>
    </div>


</template>

<script>

import Button from "./Button.vue"
import UserForm from "./UserForm.vue"
// import { getData, patchData, putData } from "../utils/fetch_data"

export default {
	name: 'UnserInfo',
	components: {
		Button,
        UserForm
	},
    props: {
        user_info: Object,
    },
    data() {
        return {
            show_form: false,
        }
    },
    methods: {
        editProfile() {
            this.show_form = true
        },
        submit(info) {
            if (confirm('Confirm to edit profile?')) {
                this.show_form = false
                this.$emit('editProfile', info)
            }

        },
        cancel(){
            if (confirm('Cancel this change?')) {
                this.show_form = false
            }
        },
        changeImg() {
            console.log('edit img')
        }
    },
}
</script>

<style scoped>
.info {
  height: 95vh;
  width: 100%;
  border: 0;
  background: #fff;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

img {
	cursor: pointer;
	width: 40%;
	max-width: 400px;
	background: #fff;
	border-radius: 50%;
	border: 2px solid grey;
}

button {
	cursor: pointer;
	margin: 30px 0px;
	width: 50%;
	padding: 10px 0px;
	font-size: 20px;
	border-radius: 10px;
	border: 2px solid grey;
	background: #cfd6df;
	color: #0523c9;
}

.info-control {
	width: 50%;
	margin: 5px 0px;
	font-size: 20px;
	background: #fff;
	color: #505050;
	display: flex;
	justify-content: flex-start;
    align-items: center;
}
</style>