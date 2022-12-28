/** When your routing table is too long, you can split it into small modules **/

// import Layout from '@/layout'

const dashboardsRouter = {
  path: '/',
  component: () => import('@/views/dashboard/Index'),
  children: [
    // Dashboard
    {
      name: 'Dashboard',
      path: '',
      component: () => import('@/views/dashboard/Dashboard'),
    },
    {
      name: 'User',
      path: 'settings/users',
      component: () => import('@/views/dashboard/settings/users'),
    },

    {
      name: 'Customer',
      path: 'customers',
      component: () => import('@/views/dashboard/customers/List'),
    },
    {
      name: 'CustomerDetails',
      path: 'customers/detail/:id',
      component: () => import('@/views/dashboard/customers/Details'),
    },
    {
      name: 'Visit',
      path: 'visits',
      component: () => import('@/views/dashboard/visits/List'),
    },
    {
      name: 'VisitDetails',
      path: 'visits/detail/:id',
      component: () => import('@/views/dashboard/visits/Details'),
    },
    {
      name: 'Order',
      path: 'orders',
      component: () => import('@/views/dashboard/orders/List'),
    },
    {
      name: 'OrderDetails',
      path: 'orders/detail/:id',
      component: () => import('@/views/dashboard/orders/Details'),
    },
  ],
}

export default dashboardsRouter
