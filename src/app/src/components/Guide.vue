<template>
	<div>
		<div v-show="show_board" class="guide">
			<div @click="$emit('clickGuide')" style="font-size:25px" class="title">
				{{guide.board_name}}
				<i :class="guide.is_latest_read? 'fas fa-circle-null' : 'fas fa-circle'"></i>
			</div>
			<i @click="$emit('clickBookmark')" :class='bookmark'></i>
			<i @click="$emit('clickTrash')" class="far fa-trash-alt"></i>
			<div class="date">{{guide.last_post}}</div>
		</div>

		<div v-show="guide_type==='posts'" class="guide">
			<div @click="$emit('clickGuide')" style="font-size:20px" class="title">
				{{guide.title}}
				<i :class="guide.is_read? 'fas fa-circle-null' : 'fas fa-circle'"></i>
			</div>
			<div style="font-size:20px" class="author">{{guide.author}}</div>
			<div style="font-size:20px" :class="guide.like>=0 ? 'like' : 'ilike' ">
				{{guide.like>=0 ? '+' : ''}}{{guide.like}}
			</div>
			<div style="font-size:20px" class="date">{{guide.post_date}}</div>
		</div>

		<div v-show="guide_type==='article'" style='border-bottom: 0px solid #a5a5a5;' class="guide">
			<div class="author">{{guide.author}}</div>
			<div class="null"></div>
			<div :class="guide.like>=0 ? 'like' : 'ilike' ">
				{{guide.like>=0 ? '+' : ''}}{{guide.like}}
			</div>
			<div class="date">{{guide.post_date}}</div>
		</div>
	</div>
	
</template>

<script>
export default {
	name: 'Guide',
	props: {
		guide: Object,
		guide_type: String,
	},
	computed: {
		bookmark: function() {
			return this.$route.hash!=='#all-boards' ? ''
				: this.guide.is_favorite ? 'fas fa-bookmark' : 'far fa-bookmark'
		},
		show_board: function() {
			return this.guide_type === 'boards' 
				&& (this.guide.is_favorite === true
				|| this.$route.hash === '#all-boards')
		},
	},
}
</script>

<style scoped>
.guide {
	background: white;
	border-bottom: 1px solid #a5a5a5;
	padding: 20px 40px;
	display: flex;
	align-items: center;
	justify-content: space-between;
} 

.guide-control {
	background: #0523c9;
	display: flex;
	align-items: center;
	justify-content: flex-start;
}

.guide .date{
	background: #fff;
	color: #505050;
	font-size: 20px;
	width: 10%;
}

.guide .title{
	cursor: pointer;
	background: #fff;
	color: #0523c9;
	font-size: 20px;
	width: 35%;
}

.guide .author{
	background: #fff;
	color: #0523c9;
	font-size: 25px;
	margin-left: 0;
	width: 25%;
}

.guide .null{
	background: #fff;
	color: #0523c9;
	font-size: 25px;
	margin-left: 50px;
	width: 20%;
}

.guide .like{
	background: #fff;
	color: #0523c9;
	font-size: 25px;
	width: 10%;
}

.guide .ilike{
	background: #fff;
	color: red;
	font-size: 25px;
	width: 10%;
}

.far.fa-trash-alt{
	cursor: pointer;
	background: #fff;
	color: #e47870;
	padding-right: 20px;
	width: 10%;
	text-align: right;
}

.far.fa-bookmark{
	cursor: pointer;
	background: #fff;
	color: #14a4cf;
	font-size: 20px;
	width: 35%;
	text-align: center;
}

.fas.fa-bookmark{
	cursor: pointer;
	background: #fff;
	color: #14a4cf;
	font-size: 20px;
	width: 35%;
	text-align: center;
}

.fas.fa-circle{
	background: #fff;
	color: #f3c21f;
	font-size: 13px;
	margin: 0px 20px;
	width: 3%;
}
.fas.fa-circle-null{
	background: #fff;
	font-size: 13px;
	margin: 0;
	width: 3%;
}
</style>
