<template>
    <div class="form">
        
        <div class="form-control">
            Company
            <input type="text" maxlength=30 v-model="info.company" :placeholder=user_info.company />
        </div>
        <div class="form-control">
            Place
            <input type="text" maxlength=30 v-model="info.place" :placeholder=user_info.place />
        </div>
        <div class="form-control">
            Email
            <div class="wrong-message">{{wrong_message.email}}</div>
            <input type="email" maxlength=30 v-model="info.email" :placeholder=user_info.email />
        </div>
        <div class="form-control">
            Phone
            <div class="wrong-message">{{wrong_message.phone}}</div>
            <input type="text" maxlength=30 v-model="info.phone" :placeholder=user_info.phone />
        </div>

        <div class='buttonarea'>
            <Button @btn-click="submit"  text='Submit' background='#202f5c' color='#fff' />
            <Button @btn-click="cancel"  text='Cancel' background='#202f5c' color='#fff' />
        </div>

    </div>
</template>

<script>
import Button from "./Button.vue"
export default {
    name: 'UnserForm',
	components: {
		Button,
	},
    props: {
        user_info: Object
    },
    data() {
        return {
            info: {
                company: '',
                place: '',
                email: '',
                phone: '',
            },
            wrong_message: {
                email: '',
                phone: '',
            },
        }
    },
    methods: {
        submit() {
            const phone_re = /^09\d{2}(-|\s)?\d{6}$/
            const email_re = /\S+@\S+\.\S+/

            const phone_ok = this.info.phone!=='' ? phone_re.exec(this.info.phone) : true;
            const email_ok = this.info.email!=='' ? email_re.exec(this.info.email) : true;

            this.wrong_message.phone = !phone_ok ? "Not a valid phone number with area code!" : ''
            this.wrong_message.email = !email_ok ? "Not a valid email!" : ''

            if (phone_ok && email_ok) { this.$emit('submit', this.info)}
        },
        cancel() {
            this.info.company = '';
            this.info.place = '';
            this.info.email = '';
            this.info.phone = '';
            this.$emit('cancel')
        }
    },
}
</script>

<style scoped>
.form {
  height: 60vh;
  width: 80%;
  border: 2px solid black;
  background: #cfd6df;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.form-control {
    width: 80%;
	margin: 5px 0px;
	font-size: 25px;
	background: #cfd6df;
	color: black;
	display: flex;
    flex-direction: column;
	justify-content: center;
    align-items: stretch;
}

.wrong-message {
    background: #cfd6df;
    padding: 0px 5px;
    font-size: 20px;
    color: red;
}

.buttonarea {
	background: #cfd6df;
    width: 80%;
	margin: 0px 20px;
	padding: 20px 40px;
	display: flex;
	align-items: center;
	justify-content: center;
}

button {
	cursor: pointer;
	margin: 30px 20px;
	width: 40%;
	padding: 10px 0px;
	font-size: 20px;
	border-radius: 10px;
	border: 0;
	background: #cfd6df;
	color: #0523c9;
}

input {
    margin: 5px 0px;
    padding: 7px 10px;
    width: 93%;
    font-size: 20px;
    border-radius: 5px;
    background: #fff;

}
</style>