import { Router } from 'express'
import { getUserMoney } from '../controllers/userController'

const router = Router()

router.get('/money', getUserMoney)

export default router
