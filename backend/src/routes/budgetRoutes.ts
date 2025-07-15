import { Router } from 'express'
import {
  createBudgetController,
  deleteBudgetController,
  getActiveBudgetsController,
} from '../controllers/budgetController'
import { authenticateUser } from '../middlewares/authMiddelware'

const router = Router()

router.get('/active', authenticateUser, getActiveBudgetsController)
router.post('/new', authenticateUser, createBudgetController)
router.delete('/delete', authenticateUser, deleteBudgetController)

export default router
