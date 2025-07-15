import Router from 'express'
import {
  getDashboardTransactionsController,
  getMonthlyIncomeByUserController,
  getMonthlySpendingByUserController,
  getMonthlyTransactionsController,
  getPaginatedUserTransactionsController,
  newTransactionController,
  searchTransactionsController,
} from '../controllers/transactionsController'
import { authenticateUser } from '../middlewares/authMiddelware'

const router = Router()

router.post('/new', authenticateUser, newTransactionController)
router.get('/dashboard', authenticateUser, getDashboardTransactionsController)
router.get('/monthly', authenticateUser, getMonthlyTransactionsController)
router.get('/search', authenticateUser, searchTransactionsController)
router.get('/user', authenticateUser, getPaginatedUserTransactionsController)
router.get('/monthly-income', authenticateUser, getMonthlyIncomeByUserController)
router.get('/monthly-spending', authenticateUser, getMonthlySpendingByUserController)
export default router
