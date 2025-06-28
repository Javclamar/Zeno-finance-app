import { Router } from 'express'
import {
  getUserMoney,
  getUserTransactions,
  searchUserTransactions,
} from '../controllers/userController'

const router = Router()

router.get('/transactions', getUserTransactions)
router.get('/money', getUserMoney)
router.get('/transactions/search', searchUserTransactions)

export default router
