import axios from 'axios'
import { Request, Response } from 'express'

export const stockPredictionsController = async (req: Request, res: Response) => {
  try {
    const predictions = await axios.get('http://localhost:8000/predictions')
    res.status(200).json(predictions.data.predictions)
  } catch (error) {
    if (error instanceof Error) {
      res.status(400).json({ error: error.message })
    } else {
      res.status(400).json({ error: 'An unknown error occurred' })
    }
  }
}

export const stockDataController = async (req: Request, res: Response) => {
  try {
    const { ticker, days } = req.query
    const stockData = await axios.get('http://localhost:8000/stock-data', {
      params: {
        ticker,
        days,
      },
    })
    res.status(200).json(stockData.data.stockData)
  } catch (error) {
    if (error instanceof Error) {
      res.status(400).json({ error: error.message })
    } else {
      res.status(400).json({ error: 'An unknown error occurred' })
    }
  }
}
