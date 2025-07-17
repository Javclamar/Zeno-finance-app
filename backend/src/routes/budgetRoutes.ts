import { Router } from 'express'
import {
  createBudgetController,
  deleteBudgetController,
  getActiveBudgetsController,
  updateBudgetController,
} from '../controllers/budgetController'
import { authenticateUser } from '../middlewares/authMiddelware'

const router = Router()

router.get('/active', authenticateUser, getActiveBudgetsController)
router.post('/new', authenticateUser, createBudgetController)
router.delete('/delete', authenticateUser, deleteBudgetController)
router.put('/update', authenticateUser, updateBudgetController)

export default router
