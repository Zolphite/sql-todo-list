module.exports = {
    // configureWebpack: { output: { filename: '[name].[hash].bundle.js' } },
    // configureWebpack: { output: { filename: '[name].bundle.js' } },
    assetsDir: 'static',
    filenameHashing: true,
    devServer: {
        host: '127.0.0.1',
        port: 8080,
        proxy: {
            '/api/': {
                target: 'http://127.0.0.1:5000',
                changeOrigin: true,
            },
            '/static/': {
                target: 'http://127.0.0.1:5000',
                changeOrigin: true,
            },
        }
    },
}
