import jwt from 'jsonwebtoken'

import { NextFunction, Request, Response } from 'express'

import { JwtPayload } from 'jsonwebtoken'

interface UserPayload extends JwtPayload {
  id: string
  email: string
  name: string
}

declare module 'express-serve-static-core' {
  interface Request {
    user?: UserPayload
  }
}

export function authenticateUser(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    res.status(401).json({ message: 'No token provided' })
    return
  }
  const token = authHeader.split(' ')[1]
  try {
    if (!process.env.JWT_SECRET) {
      throw new Error('JWT_SECRET is not defined in environment variables')
    }
    const decoded = jwt.verify(token, process.env.JWT_SECRET as string)
    if (typeof decoded === 'object' && decoded !== null && 'id' in decoded && 'email' in decoded) {
      req.user = decoded as UserPayload
      next()
    } else {
      res.status(401).json({ message: 'Invalid token payload' })
    }
  } catch (err) {
    res.status(401).json({ message: `Invalid token: ${err}` })
  }
}
