import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home'
import Login from '../views/Login'
import Board from '../views/Board'
import Post from '../views/Post'
import Article from '../views/Article'

const routes = [
  { path: '/', name: 'Home', component: Home }, 
  { path: '/login', name: 'Login', component: Login }, 
  { path: '/board', name: 'Board', component: Board },
  { path: '/post', name: 'Post', component: Post },
  { path: '/article/:id', name: 'Article', component: Article}
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
