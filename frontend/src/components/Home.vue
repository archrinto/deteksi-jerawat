<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        <v-img
          :src="require('../assets/logo.png')"
          class="my-6"
          contain
          height="150"
        />
      </v-col>

      <v-col class="mb-4">
        <h1 class="display-1 mb-3">
          Skin Analyzer
        </h1>

        <p class="subheading font-weight-regular blue-grey--text">
          Aplikasi web analisis kulit pada wajah menggunakan algoritma <i>deep learning</i> dengan TensorFlow
        </p>
        <v-btn class="mt-4" color="primary" @click="$emit('openDialogAsesmen')">
          <v-icon left>mdi-camera</v-icon>
          Asesmen
        </v-btn>
      </v-col>

    </v-row>
  </v-container>
</template>
<script>
export default {
  name: 'Home'
}
</script>