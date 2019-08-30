// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store/'


import 'element-ui/lib/theme-chalk/index.css';
import element from './element/index'
Vue.use(element)


// import ElementUI from 'element-ui';
import QS from 'qs';
import axios from 'axios';;

Vue.prototype.$axios = axios;
Vue.prototype.qs = QS;
Vue.config.productionTip = false
Vue.config.devtools = true;


router.beforeEach((to, from, next) => {
  /* 路由发生变化修改页面title */
  if (to.meta.title) {
    document.title = to.meta.title
  }
  next()
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
