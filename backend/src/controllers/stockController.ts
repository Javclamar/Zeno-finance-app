import axios from 'axios'
import { Request, Response } from 'express'
import { searchStocksService } from '../services/stockService'

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
    const response = await axios.get('http://localhost:8000/stock-data', {
      params: {
        ticker,
        days,
      },
    })
    res.status(200).json(response.data.stockData)
  } catch (error) {
    if (error instanceof Error) {
      res.status(400).json({ error: error.message })
    } else {
      res.status(400).json({ error: 'An unknown error occurred' })
    }
  }
}

export const stockCurrentPriceController = async (req: Request, res: Response) => {
  try {
    const { ticker } = req.query
    const response = await axios.get('http://localhost:8000/current-price', {
      params: {
        ticker,
      },
    })
    res.status(200).json(response.data)
  } catch (error) {
    if (error instanceof Error) {
      res.status(400).json({ error: error.message })
    } else {
      res.status(400).json({ error: 'An unknown error occurred' })
    }
  }
}

export const stockNewsController = async (req: Request, res: Response) => {
  try {
    const { ticker } = req.query
    const response = await axios.get('http://localhost:8000/stock-news', {
      params: { ticker },
    })
    res.status(200).json(response.data)
  } catch (error) {
    if (error instanceof Error) {
      res.status(400).json({ error: error.message })
    } else {
      res.status(400).json({ error: 'An unknown error occurred' })
    }
  }
}

export const seacrhStockController = async (req: Request, res: Response) => {
  try {
    const searchTerm = req.query.search as string
    const stocks = await searchStocksService(searchTerm)
    res.status(200).json(stocks)
  } catch (error) {
    if (error instanceof Error) {
      res.status(400).json({ error: error.message })
    } else {
      res.status(400).json({ error: 'An unknown error occurred' })
    }
  }
}
