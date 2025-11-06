import { createRouter, createWebHistory } from 'vue-router';

// 导入页面组件
const Index = () => import('@/pages/index/index.vue');
const Login = () => import('@/pages/login/login.vue');
const Register = () => import('@/pages/register/register.vue');
const Square = () => import('@/pages/square/square.vue');
const Discover = () => import('@/pages/discover/discover.vue');
const Profile = () => import('@/pages/profile/profile.vue');
const PoetryDetail = () => import('@/pages/poetry-detail/poetry-detail.vue');
const PoetryList = () => import('@/pages/poetry-list/poetry-list.vue');
const Search = () => import('@/pages/search/search.vue');
const Setting = () => import('@/pages/setting/setting.vue');

const routes = [
  {
    path: '/',
    name: 'Index',
    component: Index,
    meta: { title: '首页' },
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { title: '登录' },
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { title: '注册' },
  },
  {
    path: '/square',
    name: 'Square',
    component: Square,
    meta: { title: '广场' },
  },
  {
    path: '/discover',
    name: 'Discover',
    component: Discover,
    meta: { title: '发现' },
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { title: '我的' },
  },
  {
    path: '/poetry-detail',
    name: 'PoetryDetail',
    component: PoetryDetail,
    meta: { title: '诗词详情' },
  },
  {
    path: '/poetry-list',
    name: 'PoetryList',
    component: PoetryList,
    meta: { title: '诗词列表' },
  },
  {
    path: '/search',
    name: 'Search',
    component: Search,
    meta: { title: '搜索' },
  },
  {
    path: '/setting',
    name: 'Setting',
    component: Setting,
    meta: { title: '设置' },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - 星语诗词`;
  }
  next();
});

export default router;
