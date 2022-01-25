<template>
  <v-app>

    <v-app-bar
      color="blue darken-1"
      flat
      app
    >
      <v-app-bar-nav-icon class="white--text"></v-app-bar-nav-icon>
    </v-app-bar>

    <v-main>
      <v-navigation-drawer  permanent>
        <v-toolbar flat color="blue darken-1">
          <v-toolbar-title class="white--text">Skin Analyzer</v-toolbar-title>
        </v-toolbar>
      </v-navigation-drawer>
      
      <v-container fluid>
        <router-view></router-view>
      </v-container>
      
      <v-footer>
        <!-- -->
      </v-footer>

    </v-main>

    
  </v-app>
</template>
