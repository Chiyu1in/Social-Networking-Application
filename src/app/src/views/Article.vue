<template>
	<div class="container">
		<Tabs @go_back='go_back' :title="article.title" />
		<Bar bar_type="article"/>
		<Guide :guide="article" guide_type='article' />

		<textarea 
			v-model="article.article"
			maxlength=1000
			readonly=true
		>
		</textarea>

		<div class=buttonarea>
			<Button @btn-click='hate' text='Hate It' img_unicode='&#128545;'
				:background="article.favor==='hate' ? '#202f5c' : '#9eacd1'"
				:color="article.favor==='hate' ? '#cfd6df' : '#fff'" />
			<Button @btn-click='like' text='Like It' img_unicode='&#128516;'
				:background="article.favor==='like' ? '#202f5c' : '#9eacd1'" 
				:color="article.favor==='like' ? '#cfd6df' : '#fff'" />
		</div>

	</div>
	
</template>

<script>
import Tabs from "../components/Tabs.vue"
import Bar from "../components/Bar.vue"
import Guide from "../components/Guide.vue"
import Button from "../components/Button.vue"
import { patchData, getData, putData } from "../utils/fetch_data"

export default {
	name: 'Article',
	components: {
		Tabs,
		Bar,
		Guide,
		Button,
	},
	data() {
		return {
			article: {},
			// author, board_name, title, article, like, post_date, favor, 
			server_url: 'https://ptt-server-stage.azurewebsites.net'
		}
	},
	created: function(){
		const token_info = localStorage.getItem("tokenInfo")

		if (!token_info) {
			this.$router.push('/login')
			return
		}

		getData(`${this.server_url}/post/${this.$route.params.id}/`)
			.then(response => this.article = response);
		putData(`${this.server_url}/post/${this.$route.params.id}/read/`);	
	},
	methods: {
		go_back(){
			this.$router.push({
				path: '/board',
				query: {
					id: this.$route.query.board_id,
				},
			})
		},
		like(){
			if (this.article.favor === 'hate') {
				this.article.favor = 'like';
				this.article.like += 2;
				patchData(`${this.server_url}/post/${this.$route.params.id}/like/`)
				patchData(`${this.server_url}/post/${this.$route.params.id}/unhate/`)
			} else if (this.article.favor === 'like') {
				this.article.favor = undefined;
				this.article.like -= 1;
				patchData(`${this.server_url}/post/${this.$route.params.id}/unlike/`)
			} else {
				this.article.favor = 'like';
				this.article.like += 1;
				patchData(`${this.server_url}/post/${this.$route.params.id}/like/`)
			}
		},
		hate(){
			if (this.article.favor === 'like') {
				this.article.favor = 'hate';
				this.article.like -= 2;
				patchData(`${this.server_url}/post/${this.$route.params.id}/hate/`)
				patchData(`${this.server_url}/post/${this.$route.params.id}/unlike/`)
			} else if (this.article.favor === 'hate') {
				this.article.favor = undefined;
				this.article.like += 1;
				patchData(`${this.server_url}/post/${this.$route.params.id}/unhate/`)
			} else {
				this.article.favor = 'hate';
				this.article.like -= 1;
				patchData(`${this.server_url}/post/${this.$route.params.id}/hate/`)
			}
		},
	},
}
</script>

<style scoped>
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
	padding: 10px 15%;
	font-size: 120%;
	white-space:nowrap;
	border-radius: 10px;
	border: 0;
	background: #9eacd1;
	color: white;
}
</style>