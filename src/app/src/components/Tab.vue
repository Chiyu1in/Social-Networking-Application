<template>

  <div 
    @click="$emit('onClick', tab.name)"
    :class="[`#${tab.name}`.replace(' ', '-').toLowerCase() === $route.hash ? 'is_active' : '', 'tab']" 
  > 
    {{ tab.name }}
  </div>

  
</template>

<script>
export default {
  name: 'Tab',
  props: {
    tab: Object,
  },
}
</script>

<style scope>
.tab {
  background: #f4f4f4;
  margin-top: 12px;
  width: 80px;
  padding: 15px 20px;
  cursor: pointer;
  color: #0523c9;
  text-align: center;
}

.tab.is_active {
	background: #fff;
}
</style>
