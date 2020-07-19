import Vue from 'vue'
import Element from 'element-ui';
Vue.use(Element, { size: 'small', zIndex: 3000 });
import 'element-ui/lib/theme-chalk/index.css';
import App from './App.vue'
import VueRouter from 'vue-router'
Vue.use(VueRouter)
Vue.config.productionTip = false
import axios from 'axios'
Vue.prototype.$axios=axios


//配置路由
// 1. 定义 (路由) 组件。
import ProfileMnage from './components/ProfileManage.vue'
import Article from './components/Article.vue'
import Admin from './components/Admin'
import VideoTool from './components/VideoTool'
// 2. 定义路由
const routes = [
    { path: '/article', component: Article },
    {
        path: '/admin', component: Admin,
        children: [
            {
                path: '/admin/profile',
                component: ProfileMnage,
                meta:{
                    title:'Profile'
                }
            },
            {
                path: '/admin/article',
                component: Article,
                meta:{
                    title:'Article'
                }
            },
            {
                path:'/admin/videotool',
                component:VideoTool,
                meta:{
                    title:'VideoTool'
                }
            }
        ]
    },
    // { path: '/admin/createProfile', component: ProfileMnage, meta: { title: '配置管理', icon: 'el-icon-setting' } },
    // { path: '/admin/article', component: Article, meta: { title: '文章列表', icon: 'el-icon-document' } },
    // { path: '/page/article', component: Article, meta: { title: '文章列表', icon: 'el-icon-document' } }
]
// 3. 创建 router 实例，然后传 `routes` 配置
const router = new VueRouter({
    routes // (缩写) 相当于 routes: routes
})


new Vue({
    router,
    data: {
        routes: routes
    },
    render: h => h(App),
    methods: {

    }
}).$mount('#app')