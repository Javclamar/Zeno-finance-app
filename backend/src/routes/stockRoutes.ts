import axios from 'axios'
import express from 'express'

const router = express.Router()

router.get('/most-active', async (req, res) => {
  try {
    const response = await axios.get('https://finnhub.io/api/v1/stock/screener', {
      params: {
        token: 'd1ddh8pr01qn1ojmu4r0d1ddh8pr01qn1ojmu4rg',
        volume: 1000000,
        exchange: 'US',
      },
      headers: {
        Accept: 'application/json',
      },
    })
    console.log(response.data)
    res.json(response.data)
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.error(error.response?.data || error.message)
    } else {
      console.error((error as Error).message)
    }
    res.status(500).json({ error: 'Error fetching stocks' })
  }
})

export default router
