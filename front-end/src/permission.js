import router from './router'
import store from './store'

import NProgress from 'nprogress' // progress bar
// import 'nprogress/nprogress.css' // progress bar style
import { getToken } from '@/utils/auth' // get token from cookie
import getPageTitle from '@/utils/get-page-title'

NProgress.configure({ showSpinner: false }) // NProgress Configuration

const whiteList = [
  '/pages/login',
  '/pages/register',
  '/auth-redirect',
  '/mp/mp/1',
  '/mp/mp/2',
  '/mp/mp/3',
  '/mp/mp/4',
  '/mp/mp/5',
  '/mp/mp/6',
  '/mp/mp/7',
  '/mp/mp/8',
  '/mp/mp/9',
  '/mp/mp/10',
  '/mp/mp/11',
  '/mp/mp/12',
  '/mp/mp/13',
  '/mp/mp/15',
  '/mp/mp/16',
] // no redirect whitelist

router.beforeEach(async (to, from, next) => {
  // start progress bar
  NProgress.start()

  // set page title
  document.title = getPageTitle(to.meta.title)

  // determine whether the user has logged in
  const hasToken = getToken()

  if (hasToken) {
    if (to.path === '/pages/login') {
      // if is logged in, redirect to the home page
      next({ path: '/' })
      NProgress.done()
    } else {
      // determine whether the user has obtained his permission roles through getInfo
      const role = store.getters.role
      if (role.permissions !== 0) {
        next()
      } else {
        try {
          // get user info
          const { role } = await store.dispatch('user/getInfo')

          // generate accessible routes map based on role
          const accessRoutes = await store.dispatch(
            'permission/generateRoutes',
            role
          )

          // dynamically add accessible routes
          router.addRoutes(accessRoutes)

          // hack method to ensure that addRoutes is complete
          // set the replace: true, so the navigation will not leave a history record
          next({ ...to, replace: true })
        } catch (error) {
          // remove token and go to login page to re-login
          await store.dispatch('user/resetToken')
          next(`/pages/login?redirect=${to.path}`)
          NProgress.done()
        }
      }
    }
  } else {
    /* has no token */

    if (whiteList.indexOf(to.path) !== -1) {
      // in the free login whitelist, go directly
      next()
    } else {
      // other pages that do not have permission to access are redirected to the login page.
      next(`/pages/login?redirect=${to.path}`)
      NProgress.done()
    }
  }
})

router.afterEach(() => {
  // finish progress bar
  NProgress.done()
})
