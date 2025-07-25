import { Router } from 'express'
import {
  stockCurrentPriceController,
  stockDataController,
  stockPredictionsController,
} from '../controllers/stockController'
import { authenticateUser } from '../middlewares/authMiddelware'

const router = Router()

router.get('/predictions', authenticateUser, stockPredictionsController)
router.get('/stock-data', authenticateUser, stockDataController)
router.get('/current-price', authenticateUser, stockCurrentPriceController)

export default router
