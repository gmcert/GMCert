const path = require('path')
const webpack = require('webpack')
module.exports = {
  entry: {
    //填写需要提取出来的依赖包
    //如果有些依赖包在index.html页面引入了cdn了就无需再引入了，否则会打包进js文件中，在页面重复引入代码。
    vendor: ['vue','vue-router']
  },
  output: {
    path: path.join(__dirname, '../static'),
    filename: 'dll.[name].js',
    library: '[name]'
  },
  plugins: [
    new webpack.DllPlugin({
      path: path.join(__dirname, '../', '[name]-manifest.json'),
      name: '[name]'
    })
  ]
}