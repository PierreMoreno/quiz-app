import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import NewQuizPage from '../views/NewQuizPage.vue'
import QuestionManager from '../views/QuestionManager.vue'
import AdminPage from '../views/AdminView.vue'
import ScoreRecap from '../views/ScoreRecapView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "HomePage",
      component: HomePage,
    },
    {
      path: "/start-new-quiz-page",
      name: "NewQuizPage",
      component: NewQuizPage,
    },
    {
      path: "/questions",
      name: "QuestionManager",
      component: QuestionManager,
    },
    {
      path: "/score-recap",
      name: "ScoreRecap",
      component: ScoreRecap,
    },
    {
      path: "/admin",
      name: "Admin",
      component: AdminPage,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    }
   
  ]
})

export default router
