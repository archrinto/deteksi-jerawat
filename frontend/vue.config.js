module.exports = {
  transpileDependencies: [
    'vuetify'
  ],

  pluginOptions: {
    autoRouting: {
      chunkNamePrefix: 'page-'
    }
  },

  devServer: {
    proxy: {
      '^/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        pathRewrite: {
          '^/api': ''
        },
        logLevel: "debug"
      },
    }
  }
}
