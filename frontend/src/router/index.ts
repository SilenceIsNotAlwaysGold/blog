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
        path: 'about',
        name: 'about',
        component: () => import('@/pages/about/Index.vue'),
        meta: { title: 'About Me' }
      },
      {
        path: 'skills',
        name: 'skills',
        component: () => import('@/pages/skills/Index.vue'),
        meta: { title: 'Skills' }
      },
      {
        path: 'projects',
        name: 'projects',
        component: () => import('@/pages/projects/Index.vue'),
        meta: { title: '项目展示' }
      },
      {
        path: 'tags',
        name: 'tags',
        component: () => import('@/pages/tags/Index.vue'),
        meta: { title: '标签云' }
      },
      {
        path: 'archives',
        name: 'archives',
        component: () => import('@/pages/archives/Index.vue'),
        meta: { title: '文章归档' }
      }
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/pages/auth/Login.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/admin',
    component: DefaultLayout,
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: 'dashboard',
        name: 'admin-dashboard',
        component: () => import('@/pages/admin/Dashboard.vue'),
        meta: { title: '管理中心' }
      },
      {
        path: 'article/new',
        name: 'article-new',
        component: () => import('@/pages/admin/ArticleEditor.vue'),
        meta: { title: '新建文章' }
      },
      {
        path: 'article/edit/:id',
        name: 'article-edit',
        component: () => import('@/pages/admin/ArticleEditor.vue'),
        meta: { title: '编辑文章' }
      },
      {
        path: 'project/new',
        name: 'project-new',
        component: () => import('@/pages/admin/ProjectEditor.vue'),
        meta: { title: '新建项目' }
      },
      {
        path: 'project/edit/:id',
        name: 'project-edit',
        component: () => import('@/pages/admin/ProjectEditor.vue'),
        meta: { title: '编辑项目' }
      },
      {
        path: 'skill/new',
        name: 'skill-new',
        component: () => import('@/pages/admin/SkillEditor.vue'),
        meta: { title: '新建技能' }
      },
      {
        path: 'skill/edit/:id',
        name: 'skill-edit',
        component: () => import('@/pages/admin/SkillEditor.vue'),
        meta: { title: '编辑技能' }
      },
      {
        path: 'about/edit',
        name: 'about-edit',
        component: () => import('@/pages/admin/AboutEditor.vue'),
        meta: { title: '编辑关于' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(_to, _from, savedPosition) {
    if (savedPosition) return savedPosition
    return { top: 0, behavior: 'smooth' }
  }
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

  // If already logged in and trying to access login page, redirect to home
  if (to.name === 'login' && userStore.isAuthenticated) {
    next({ name: 'home' })
    return
  }

  next()
})

export default router
