
const routes = [
  {
    path: '/',
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') }
    ]
  },
  {
    path: '/login/',
    children: [
      { path: '', component: () => import('pages/LoginPage.vue') }
    ]
  },
  {
    path: '/create/',
    children: [
      { path: '', component: () => import('pages/CreateUserPage.vue') }
    ]
  },
  {
    path: '/home/',
    children: [
      { path: '', component: () => import('pages/HomePage.vue') }
    ]
  },

  {
    path: '/garden/new/',
    children: [
      { path: '', component: () => import('pages/NewGardenPage.vue') }
    ]
  },

  {
    path: '/harvest/new/',
    children: [
      { path: '', component: () => import('pages/HarvestPage.vue') }
    ]
  },
  {
    path: '/plant/new/',
    children: [
      { path: '', component: () => import('pages/NewPlantPage.vue') }
    ]
  },
  {
    path: '/variety/new/',
    children: [
      { path: '', component: () => import('pages/NewVarietyPage.vue') }
    ]
  },
  {
    path: '/userplant/new/',
    children: [
      { path: '', component: () => import('pages/NewUserPlantPage.vue') }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
