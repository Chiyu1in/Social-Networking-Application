<template>
  <button @click="$emit('btn-click')" :style="{ background: background, color: color}" class="btn">
    {{ text }} {{img_unicode}}
  </button>
</template>

<script>
export default {
  name: 'Button',
  props: {
    text: String,
    background: String,
    color: String,
    img_unicode: String,
  },
}
</script>
