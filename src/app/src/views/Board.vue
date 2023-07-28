<template>
	<div class="container">
		<Tabs @go_back='go_back' @post_artical='post_artical' :title=board_name />
		<SearchBar @search="search" />
		<Bar bar_type="posts" />

		<Guides 
			@clickGuide="clickPost"
			:guides="showPost" 
			guide_type = "posts"
		/>
		<!-- selected_posts.length -->
		<PageSelect @changePage="changePage" :max_page="maxPages" />
	</div>
	
</template>

<script>
import Tabs from "../components/Tabs.vue"
import SearchBar from "../components/SearchBar.vue"
import Bar from "../components/Bar.vue"
import Guides from "../components/Guides.vue"
import PageSelect from "../components/PageSelect.vue"
import { getData, postData, patchData } from "../utils/fetch_data"

export default {
	name: 'Board',
	components: {
		Tabs,
		SearchBar,
		Bar,
		Guides,
		PageSelect
	},
	data() {
		return {
			board_name: '',
			selected_posts: [],
			max_show: 10,
			posts: [],
			// id, title, is_read, author, like, post_date
			last_post: {},
			// author, board, post_datetime, title, article
			server_url: 'https://ptt-server-stage.azurewebsites.net'
		}
	},
	created: function(){
		const token_info = localStorage.getItem("tokenInfo")

		if (!token_info) {
			this.$router.push('/login')
			return
		}

		getData(`${this.server_url}/posts/?board_id=${this.$route.query.id}`)
		.then(response => this.posts = response)
		.then(response => this.selected_posts = response);
		
		getData(`${this.server_url}/board/${this.$route.query.id}/`)
		.then(response => this.board_name=response.board_name)
		.then(response => postData(`${this.server_url}/read_latest_post/`, {board: response}))
		.then(response => this.last_post=response)
		
	},
	computed: {
		showPost: function() {
			let cur_page = Number(this.$route.hash.slice(1))
			cur_page = Math.max(cur_page, 1)
			
			return this.selected_posts.slice((cur_page-1)*this.max_show, cur_page*this.max_show)
		},
		maxPages: function() {
			return Math.ceil(this.selected_posts.length/this.max_show)
		}
	},
	methods: {
		go_back() {
			this.$router.push("/")
		},
		post_artical() {
			this.$router.push({
				path: '/post',
				query: {
					board_id: this.$route.query.id
				},
			})
		},
		clickPost(id) {
			if (this.last_post.post_id === id) {
				patchData(`${this.server_url}/board/${this.$route.query.id}/read_latest_post/`)
			}
			this.$router.push({
				path: `/article/${id}`,
				query: {
					board_id: this.$route.query.id,
				},
			})
		},
		search(selected, text) {
			selected === 'Title' ?
			this.selected_posts = this.posts.filter((post) =>
				post.title.toLowerCase().includes(text.toLowerCase())
				? post
				: ""
			): selected === 'Author' ?
			this.selected_posts = this.posts.filter((post) =>
				post.author.toLowerCase().includes(text.toLowerCase())
				? post
				: ""
			): 
			this.selected_posts = this.posts.filter((post) =>
				post.like >= parseInt(text, 10)
				? post
				: ""
			)

			if (text==='') {this.selected_posts = this.posts;}
		},
		changePage(page) {
			this.$router.push({
				hash: `#${page}`,
				query: {
					id: this.$route.query.id
				},
			})
		}
	},
}
</script>

<style scoped>
</style>

