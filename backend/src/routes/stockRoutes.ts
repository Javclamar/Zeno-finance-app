import { Router } from 'express'
import { stockDataController, stockPredictionsController } from '../controllers/stockController'
import { authenticateUser } from '../middlewares/authMiddelware'

const router = Router()

router.get('/predictions', authenticateUser, stockPredictionsController)
router.get('/stock-data', authenticateUser, stockDataController)

export default router
