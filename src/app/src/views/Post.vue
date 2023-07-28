<template>
	<div class="container">
		<Tabs :title="new Date().toISOString().slice(0,10).replaceAll('-', '/')" />

		<input type='text' maxlength=50 v-model="title" placeholder='TitleOfYourPost' />

		<textarea 
			v-model="content"
			maxlength=1000
			placeholder="Content you want to post"
		></textarea>

		<div class=buttonarea>
			<Button @btn-click='cancel' text='Cancel' background='#202f5c' color='#cfd6df' />
			<Button @btn-click='post_art' text='Post' background='#202f5c' color='#cfd6df' />
		</div>

	</div>
	
</template>

<script>
import Tabs from "../components/Tabs.vue"
import Button from "../components/Button.vue"
import { postData } from "../utils/fetch_data"

export default {
	name: 'Post',
	components: {
		Tabs,
		Button,
	},
	data() {
		return {
			title: '',
			content: '',
			post: {},
			post_result: '',
			server_url: 'https://ptt-server-stage.azurewebsites.net'
		}
	},
	created: function() {
		const token_info = localStorage.getItem("tokenInfo")

		if (!token_info) {
			this.$router.push('/login')
			return
		}
	},
	watch: {
		post_result: 'backToBoard',
	},
	methods: {
		post_art() {
			if(confirm('Are you sure you want to publish this post?')){
				const data = {
				board_id: this.$route.query.board_id,
				title: this.title,
				content: this.content,
				};

				postData(`${this.server_url}/write_post/`, data)
				.then( response => this.post_result = response);
				
			}
		},
		backToBoard(post_result) {
			if ( post_result==='OK') {
				this.$router.push({
					path: '/board',
					query: {
						id: this.$route.query.board_id,
					},
				}) 
			} 
			post_result = ''
		},
		cancel() {
			if(confirm('Cancel this publishment?')) {
				this.$router.push({
					path: '/board',
					query: {
						id: this.$route.query.board_id,
					},
				})
			}
		},
	},
}
</script>

<style scoped>
input[type='text'] {
	background: #fff;
	border: 2px solid black;
	margin: 20px 20px;
	padding: 3px 20px;
	font-size: 30px;
}

textarea{
	background: #fff;
	border: 2px solid black;
	margin: 0px 20px;
	padding: 20px 20px;
	font-size: 20px;
	resize: none;
	height: 70%;
}

.buttonarea {
	background: #fff;
	margin: 0px 20px;
	padding: 20px 40px;
	display: flex;
	align-items: center;
	justify-content: center;
}

button {
	cursor: pointer;
	margin: 0px 40px;
	padding: 10px 100px;
	font-size: 20px;
	border-radius: 10px;
	border: 0;
}
</style>