import { Router } from 'express'
import {
  stockCurrentPriceController,
  stockDataController,
  stockPredictionsController,
  stockNewsController,
} from '../controllers/stockController'
import { authenticateUser } from '../middlewares/authMiddelware'

const router = Router()

router.get('/predictions', authenticateUser, stockPredictionsController)
router.get('/stock-data', authenticateUser, stockDataController)
router.get('/current-price', authenticateUser, stockCurrentPriceController)
router.get('/stock-news', authenticateUser, stockNewsController)

export default router
