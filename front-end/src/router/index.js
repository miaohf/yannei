import Vue from 'vue'
import Router from 'vue-router'

/* Router Modules */

import dashboardsRouter from './modules/dashboards'
import pagesRouter from './modules/pages'
Vue.use(Router)

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  // {
  //   path: '/',
  //   component: () => import('@/views/base/Index'),
  //   children: [
  //     // Dashboard
  //     {
  //       name: 'Dashboard',
  //       path: '',
  //       component: () => import('@/views/dashboard/Dashboard'),
  //     },
  //   ],
  // },
  dashboardsRouter,
  pagesRouter,
]

/**
 * asyncRoutes
 * the routes that need to be dynamically loaded based on user roles
 */
export const asyncRoutes = [
  /** when your routing map is too long, you can split it into small modules **/
]

const createRouter = () =>
  new Router({
    // mode: 'history', // require service support
    scrollBehavior: () => ({ y: 0 }),
    routes: constantRoutes,
  })

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
