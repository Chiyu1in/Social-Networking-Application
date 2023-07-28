<template>
	<div style="background: #fff">
		<div class="bar" v-show="show_board">
			<p style="width:90%">Board Name</p> 
			<p style="width:9%">Last Post</p> 
		</div>

		<div class="bar" v-show="bar_type==='posts'">
			<p style="width:37%">Title</p> 
			<p style="width:27%">Author</p> 
			<p style="width:12%">Like</p> 
			<p style="width:9%">Post Date</p> 
		</div>

		<div class="bar" v-show="bar_type==='article'">
			<p style="width:60%">Author</p> 
			<p style="width:11%">Like</p> 
			<p style="width:9%">Post Date</p> 
		</div>
	</div>

    
</template>

<script>
export default {
	name: 'Bar',
	props: {
		bar_type: String,
	},
	computed: {
		show_board: function() {
			return this.bar_type === 'boards' 
				&& this.$route.hash !== '#user-info'
		},
	},
}
</script>

<style scoped>
.bar {
	background: #cfd6df;
	border-radius: 10px;
	padding: 5px 35px;
	margin: 5px 20px;

	display: flex;
	align-items: center;
	justify-content: space-between;
} 

.bar p {
	background: #cfd6df;
	margin: 0px;
	color: #0523c9;
	font-size: 20px;
}
</style>

