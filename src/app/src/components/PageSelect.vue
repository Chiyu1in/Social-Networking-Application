<template>
	<div class="select-bar">

        <div @click="selectPage(1-basic_page)" 
            :class="isSelected(1-basic_page)"
            v-show="basic_page>1"
        >
            {{1}}
        </div>
        <div class="unselect-page" v-show="basic_page>2">...</div>

        <div :key='index' v-for="(page_index, index) in Array(Math.min(max_show, max_page)).keys()" 
            @click="selectPage(page_index)"
            :class="isSelected(page_index)"
        >
            {{this.basic_page+page_index}}
        </div>

        <div class="unselect-page" v-show="max_page>basic_page+max_show">...</div>
        <div @click="selectPage(max_page-basic_page)" 
            :class="isSelected(max_page-basic_page)"
            v-show="max_page+1>basic_page+max_show"
        >
            {{max_page}}
        </div>
	</div>
	
</template>

<script>
export default {
	name: 'PageSelect',
    props: {
        max_page: Number,
    },
    data() {
        return {
            max_show: 15,
            basic_page: 1,
            moving_page_index: 10,
        }
    },
    watch: {
        max_page: 'changeMaxPages'
    },
    methods: {
        isSelected(page_index) {
            return this.basic_page+page_index===Math.max(Number(this.$route.hash.slice(1)), 1) ?
            'select-page' : 'unselect-page'
        },
        selectPage(page_index) {

            this.$emit('changePage', this.basic_page+page_index);

            this.basic_page = 
            this.basic_page+page_index < this.moving_page_index ? 1
            : this.basic_page+page_index > this.max_page-this.max_show+this.moving_page_index-1 ? Math.max(this.max_page-this.max_show+1, 1)
            : this.basic_page+page_index-this.moving_page_index+2

        },
        changeMaxPages() {
            this.$router.push({
                path: 'board',
				query: {
					id: this.$route.query.id
				},
			})
            this.basic_page = 1
        }
    },
}
</script>

<style scoped>
.select-bar {
    width: 100%;
    border: 0;
    padding: 10px 0px;
    font-size: 20px;
    background: #cfd6df;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
}

.select-page{
    cursor: pointer;
    border: 0;
    margin: 10px 5px;
    font-size: 20px;
    font-weight: bold;
    color: #0523c9;
    background: #cfd6df;
}

.unselect-page{
    cursor: pointer;
    border: 0;
    margin: 10px 5px;
    font-size: 20px;
    font-weight: bold;
    color: black;
    background: #cfd6df;
}
</style>

