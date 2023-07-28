<template>
	<div class="search-container">	
		<div class="search-bar" >
			<input type="text" v-model="text" placeholder="Search" 
				:style="this.$route.path.includes('/board') ? 'padding-left: 150px' : 'padding-left: 50px'"/>
		</div>
		<div class="search-icon" >
			<i @click="$emit('search', text)" class="fas fa-search"></i>
			<select v-model="selected" v-show="this.$route.path.includes('/board')">
				<option value="Title">By Title</option>
				<option value="Author">By Author</option>
				<option value="Like">By Like</option>
			</select>
		</div>
	</div>
</template>

<script>

export default {
	name: 'SearchBar',
	data() {
		return {
			text: "",
			selected: "Title",
		}
	},
	watch: {
		text: "SearchStringHandler",
		selected: "SelectedHandler",
	},
	methods: {
		SearchStringHandler(text) {
			this.$emit("search", this.selected, text);
		},
		SelectedHandler(selected) {
			this.$emit("search", selected, this.text);
		},
	},
}
</script>

<style scoped>
input[type="text"] {
	background:#fff; 
	width: 100%;
	height: 30px;
	margin: 0px 15px;
	font-size: 15px;
	border-radius: 5px;
	border: 1px solid #a5a5a5;
}

select {
	cursor: pointer;
	background:#fff; 
	margin-top: -35px; 
	margin-left: 20px;
}
option{
	background:#fff;
}

.fas.fa-search{
	cursor: pointer;
	background:#fff;
	margin-top: -35px; 
	margin-left: 30px;
}

.search-container{
	padding: 15px 0px;
	display: flex;
	flex-direction: column;
	justify-content: start;
	align-items: flex-start;
	background: #fff;
}

.search-bar{
	margin: 0px 1%;
	width: 98%;
	display: flex;
	flex-direction: row;
	justify-content: flex-end;
	align-items: center;
	background: #fff;
}

.search-icon{
	margin: 0px 1%;
	width: 98%;
	display: flex;
	flex-direction: row;
	justify-content: flex-start;
	align-items: center;
	background: #fff;
}
</style>

