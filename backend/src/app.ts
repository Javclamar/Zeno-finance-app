import cors from 'cors';
import express from 'express';
import userRoutes from './routes/userRoutes';

const app = express();

app.use(cors());
app.use(express.json());

app.use('/users', userRoutes);

export default app;