<template>
	<div class="container">
		<Tabs @selectTab="selectTab" :tabs=tabs />
		<SearchBar @search="search" v-show="$route.hash!=='#user-info'" />
		<Bar v-show="$route.hash!=='#user-info'" bar_type="boards" />

		<Guides 
			@clickGuide="clickBoard"
			@clickBookmark="clickBookmark" 
			@clickTrash="clickTrash"
			v-show="$route.hash!=='#user-info'"
			:guides="selected_boards"
			guide_type = "boards"
		/>

		<UnserInfo @editProfile="editProfile" :user_info="user_info" />

	</div>
</template>

<script>
import Tabs from "../components/Tabs.vue"
import SearchBar from "../components/SearchBar.vue"
import Bar from "../components/Bar.vue"
import Guides from "../components/Guides.vue"
import UnserInfo from "../components/UserInfo.vue"
import { getData, patchData, putData } from "../utils/fetch_data"

export default {
	name: 'Home',
	components: {
		Tabs,
		SearchBar,
		Bar,
		Guides,
		UnserInfo
	},
	data() {
		return {
			tabs: [
				{id: 1, name: 'My Favorite'},
				{id: 2, name: 'All Boards'},
				{id: 3, name: 'User Info'},
			],
			titles: ['Board Name', 'Last Post'],
			selected_boards: [],
			boards: [],
			// id, board_name, is_latest_read, is_favorite, last_post
			user_info: {},
			// username, email, company, place, phone
			server_url: 'https://ptt-server-stage.azurewebsites.net'
		}
	},
	created: function(){
		const token_info = localStorage.getItem("tokenInfo")

		if (!token_info) {
			this.$router.push('/login')
			return
		}
		
		putData(`${this.server_url}/update_boards/`)
		.then(getData(`${this.server_url}/boards/`)
		.then(response => this.boards = response)
		.then(response => this.selected_boards = response));

		getData(`${this.server_url}/user/`)
		.then(response => this.user_info = response)

	},
	methods: {
		selectTab(tab_name) {
			tab_name = tab_name.replace(' ', '-').toLowerCase()
			this.$router.push({
				hash: `#${tab_name}`,
			})
		},
		clickBoard(id) {
			this.$router.push({
				path: "/board",
				query: {
					id: id,
				},
			})
		},
		clickBookmark(id) {
			this.boards = this.boards.map((board) =>
				board.id === id ? { ...board, is_favorite: !board.is_favorite } : board
			)
			this.selected_boards = this.boards;

			patchData(`${this.server_url}/board/${id}/update_favorite/`);
		},
		clickTrash(id) {
			const board = this.boards.find(board => board.id === id)

			if (board.is_favorite==true) {
				board.is_favorite=false;
				this.selected_boards = this.boards;
				patchData(`${this.server_url}/board/${id}/delete_favorite/`)
			}
		},
		editProfile(info) {
			this.user_info.company = info.company==='' ? this.user_info.company : info.company
			this.user_info.place = info.place==='' ? this.user_info.place : info.place
			this.user_info.email = info.email==='' ? this.user_info.email : info.email
			this.user_info.phone = info.phone==='' ? this.user_info.phone : info.phone

			info.company = '';
            info.place = '';
            info.email = '';
            info.phone = '';

			patchData(`${this.server_url}/user/`, this.user_info)	
		},
		changeImg() {
			// TODO
			alert('edit')
		},
		search(selected, text) {

			// if search_string === "", condition is all true
			this.selected_boards = this.boards.filter((board) =>
				board.board_name.toLowerCase().includes(text.toLowerCase())
				? board
				: ""
			)
			if (text==='') {
				this.selected_boards = this.boards;
			}

		},
	},
}
</script>
	

<style>

.text {
	background: #fff;
	padding-left: 10px;
}

.far{
	background: #fff;
}

.fas{
	background: #fff;
}


</style>

