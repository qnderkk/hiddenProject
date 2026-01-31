const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
    transpileDependencies: true,
    publicPath: '/',
    assetsDir: 'assets',
    devServer: {
        port: 8080 // Явно указываем порт
    }
})