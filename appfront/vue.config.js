module.exports = {
    //axios域代理，解决axios跨域问题
    baseUrl: '/',
    devServer: {
        proxy: {
            '': {
                target: 'http://172.16.97.221:8001',
                changeOrigin: true,
                ws: true,
                pathRewrite: {

                }
            }
        }
    }
}