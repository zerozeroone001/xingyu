/**
 * Vue CLI 配置文件
 * 用于配置 UniApp 项目的构建选项
 */
module.exports = {
  transpileDependencies: ['@dcloudio/uni-ui'],

  // 配置 SCSS 全局变量和 mixins
  css: {
    loaderOptions: {
      scss: {
        // 全局导入 SCSS 变量文件
        // 注意：这里的路径是相对于项目根目录
        additionalData: `@import "@/styles/variables.scss";`
      }
    }
  },

  // 开发服务器配置
  devServer: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false
      }
    }
  }
}
