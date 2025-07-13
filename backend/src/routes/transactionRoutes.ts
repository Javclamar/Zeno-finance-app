import Router from 'express'
import {
  getDashboardTransactionsController,
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
export default router
