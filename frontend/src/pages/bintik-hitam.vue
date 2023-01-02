<template>
  <div>
    <div v-if="results.length > 0">
      <v-slide-group
        class="pa-2"
        center-active
        show-arrows
      >
        <v-spacer></v-spacer>

        <v-slide-item
          v-for="(result, n) in results"
          :key="n"
        >
          <v-card
            :color="selectedImageIndex == n ? 'primary' : 'grey lighten-1'"
            class="ma-4"
            height="100"
            width="100"
            @click="selectedImageIndex = n"
          >
            <v-img :src="'/api'+result.image.url" max-height="100%"></v-img>
          </v-card>
        </v-slide-item>

        <v-spacer></v-spacer>
      </v-slide-group>
      <div class="text-center pa-2">
        <v-row justify="center">
          <v-col md="4" align-self="center">
            <canvas ref="display" width="100%"></canvas>
            <v-img max-width="100%" v-if="currentResult != null" :src="currentResult.image.url"></v-img>
          </v-col>
        </v-row>
      </div>
    </div>
    <home v-else @openDialogAsesmen="$emit('openDialogAsesmen')"></home>
  </div>
</template>
<script>
import Home from '../components/Home.vue'

export default {
  layout: 'bintik-hitam',
  components: { Home },
  props: {
    images: Array,
    clientId: String,
    results: Array
  },
  watch: {
    selectedImageIndex: function(val) {
      if (val != null) {
        this.changeImage()
      }
    }
  },
  mounted() {
    console.log(this.$refs.display)
    this.changeImage()
  },
  data() {
    return {
      selectedImageIndex: 0,
      currentResult: null
    }
  },
  methods: {
    async changeImage() {
      if (this.results.length == 0) {
        return
      }

      const result = this.results[this.selectedImageIndex]
      this.currentResult = result

      const image = new Image()
      image.src = '/api' + result.image.url

      const canvas = this.$refs.display
      const context = canvas.getContext('2d')
      const items = result.result.acne

      context.clearRect(0, 0, canvas.width, canvas.height);

      image.onload = function() {
        console.log('loaded')

        canvas.style.width = '100%'

        let { width, height } = canvas.getBoundingClientRect();
        
        height = (width / result.image.width) * result.image.height

        canvas.width = width
        canvas.height = height

        context.drawImage(image, 0, 0, width, height)
        
        items.forEach(item => {
          const ymin = item.box[0], xmin = item.box[1], ymax = item.box[2], xmax = item.box[3]
          const left = xmin * width
          const right = xmax * width
          const top = ymin * height
          const bottom = ymax * height
          const box_h = bottom-top, box_w = right-left
          let radius = Math.sqrt((box_h) ** 2 + (box_w) ** 2) / 2
          
          context.strokeStyle = "yellow"

          context.beginPath();
          // context.strokeRect(left, top, right-left, bottom-top);
          context.arc(left + box_w / 2, top + box_h / 2, radius, 0, 2 * Math.PI);
          context.stroke();
        });
       
      }
    }
  }
}
</script>
