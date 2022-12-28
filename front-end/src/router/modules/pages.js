/** When your routing table is too long, you can split it into small modules **/

// import Layout from '@/layout'

const pagesRouter = {
  path: '/pages',
  component: () => import('@/views/pages/Index'),
  children: [
    {
      name: 'Login',
      path: 'login',
      component: () => import('@/views/pages/Login'),
    },
    {
      name: 'Register',
      path: 'register',
      component: () => import('@/views/pages/Register'),
    },
  ],
}
export default pagesRouter
