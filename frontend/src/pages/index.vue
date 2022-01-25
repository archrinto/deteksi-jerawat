<template>
  <div class="home">
   <home @openDialogAsesmen="$emit('openDialogAsesmen')"></home>
  </div>
</template>

<script>
import Home from '../components/Home.vue'
// @ is an alias to /src
export default {
  components: { Home },
  layout: 'profile',
  props: {
    isDialogAsesmen: Boolean
  }
}
</script>
