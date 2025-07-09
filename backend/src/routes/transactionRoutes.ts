import Router from 'express'
import { newTransactionController } from '../controllers/transactionsController'
import { authenticateUser } from '../middlewares/authMiddelware'

const router = Router()

router.post('/new', authenticateUser, newTransactionController)

export default router
