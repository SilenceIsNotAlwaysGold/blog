import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import { useUserStore } from '@/stores/user'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: DefaultLayout,
    children: [
      {
        path: '',
        name: 'home',
        component: () => import('@/pages/home/Index.vue'),
        meta: { title: 'Home' }
      },
      {
        path: 'tech',
        name: 'tech',
        component: () => import('@/pages/tech/List.vue'),
        meta: { title: 'Tech Board' }
      },
      {
        path: 'tech/:id',
        name: 'tech-detail',
        component: () => import('@/pages/tech/Detail.vue'),
        meta: { title: 'Article Detail' }
      },
      {
        path: 'life',
        name: 'life',
        component: () => import('@/pages/life/List.vue'),
        meta: { title: 'Life Board', requiresAuth: true }
      },
      {
        path: 'life/:id',
        name: 'life-detail',
        component: () => import('@/pages/life/Detail.vue'),
        meta: { title: 'Article Detail', requiresAuth: true }
      },
      {
        path: 'about',
        name: 'about',
        component: () => import('@/pages/about/Index.vue'),
        meta: { title: 'About Me' }
      }
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/pages/auth/Login.vue'),
    meta: { title: 'Login' }
  },
  {
    path: '/admin',
    name: 'admin',
    component: () => import('@/pages/admin/Dashboard.vue'),
    meta: { title: 'Dashboard', requiresAuth: true, requiresAdmin: true }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Navigation guard
router.beforeEach((to, _from, next) => {
  const userStore = useUserStore()

  // Set page title
  document.title = (to.meta.title as string) || 'Personal Blog'

  // Check authentication
  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    // Redirect to login if not authenticated
    next({
      name: 'login',
      query: { redirect: to.fullPath }
    })
    return
  }

  // Check admin permission
  if (to.meta.requiresAdmin && !userStore.isAdmin) {
    // Redirect to home if not admin
    next({ name: 'home' })
    return
  }

  // If already logged in and trying to access login page, redirect to admin
  if (to.name === 'login' && userStore.isAuthenticated) {
    next({ name: 'admin' })
    return
  }

  next()
})

export default router
