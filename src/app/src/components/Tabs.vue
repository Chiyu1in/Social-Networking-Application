<template>
	<div>
		<div v-show="$route.path==='/'" class='tabs'>
			<div class='tabs-control'>
				<div :key='index' v-for="(tab, index) in tabs" class='tabs-control'>
					<Tab @onClick="$emit('selectTab', tab.name)" :tab=tab />
				</div>
			</div>
			<router-link @click='logout' to='/login'>Logout</router-link>
		</div>
		
		<div v-show="$route.path==='/board'" class='tabs'>
			<i @click="$emit('go_back')" class="fas fa-arrow-circle-left"></i>
			<h1>{{title}}</h1>
			<i @click="$emit('post_artical')" class="far fa-edit"></i>
		</div>

		<div v-show="$route.path.includes('article')" class='tabs' style='justify-content: flex-start'>
			<i @click="$emit('go_back')" class="fas fa-arrow-circle-left"></i>
			<h1>{{title}}</h1>
		</div>

		<div v-show="$route.path==='/post'" class='tabs' style='justify-content: flex-end'>
			<h2>{{title}}</h2>
		</div>
	</div>
		
</template>

<script>
import Tab from './Tab.vue'

export default {
	name: 'Tabs',
	components: {
		Tab
	},
	props: {
		tabs: Array,
		title: String
	},
	methods: {
		logout() {
			localStorage.removeItem("tokenInfo")
		}
	},
}
</script>

<style scoped>
.tabs {
	height: 60px;
	display: flex;
	align-items: center;
	justify-content: space-between;
	background: #cfd6df;
}

.tabs-control {
	margin-left: 5px;
	display: flex;
	justify-content: flex-start;
	background: #cfd6df;
}

.fas.fa-arrow-circle-left{
	cursor: pointer;
	background: #cfd6df;
	font-size: 30px;
	padding: 0px 50px;
}

.far.fa-edit {
	cursor: pointer;
	background: #cfd6df;
	font-size: 25px;
	padding: 0px 50px;
}

a {
	text-align: center;
	padding: 10px 20px;
	font-size: 20px;
	color: #0523c9;
	text-decoration: none;
	background: #cfd6df;
}

h1 {
	background: #cfd6df;
	margin: 0px;
	color: #0523c9;
}

h2 {
	background: #cfd6df;
	margin: 30px;
	color: #505050;;
}
</style>