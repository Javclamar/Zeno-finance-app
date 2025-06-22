import cors from 'cors';
import express from 'express';
import authRoutes from './routes/authRoutes';

const app = express();

app.use(cors({
    origin: 'http://localhost:5173',
    credentials: true
  }));
app.use(express.json());

app.use('/api/auth', authRoutes);

export default app;