<template>
	<div class="container">
		<div :key="guide.id" v-for="guide in guides">
			<Guide 
				@clickGuide="$emit('clickGuide', guide.id)"
				@clickBookmark="$emit('clickBookmark', guide.id)" 
				@clickTrash="$emit('clickTrash', guide.id)"
				:guide="guide"
				:guide_type=guide_type
			/>
		</div>
	</div>
</template>

<script>
import Guide from "./Guide.vue"

export default {
	name: 'Guides',
	components: {
		Guide,
	},
	props: {
		guides: Array,
		guide_type: String,
	},
}
</script>

<style scoped>
</style>