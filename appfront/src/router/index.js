import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'

import mainPage from '@/gmpage/mainPage'
import submitForm from '@/gmpage/submitForm'
import subForm from '@/gmpage/subForm'
import certInfo from '@/gmpage/certInfo'
import downCert from '@/gmpage/downCert'

Vue.use(Router)

export default new Router({
  mode: 'history',  //去掉url中的#
  routes: [
    {
      path: '/',
      name: 'mainPage',
      component: mainPage,
      meta:{
        title:"GMCert"
      }
    },{
      path: '/mainPage',
      name: 'mainPage',
      component: mainPage,
      meta:{
        title:"GMCert"
      }
    },{
      path: '/submitForm',
      name: 'submitForm',
      component: submitForm,
      meta:{
        title:"CSR证书签发"
      }
    },{
      path: '/subForm',
      name: 'subForm',
      component: subForm,
      meta:{
        title:"线上证书签发"
      }
    },{
      path: '/certInfo',
      name: 'certInfo',
      component: certInfo,
      meta:{
        title:"证书签发"
      }
    },{
      path: '/downCert',
      name: 'downCert',
      component: downCert,
      meta:{
        title:"下载证书"
      }
    }
  ]
})
