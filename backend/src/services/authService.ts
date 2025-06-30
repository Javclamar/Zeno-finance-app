import { PrismaClient, User } from '@prisma/client'
import axios from 'axios'
import bcrypt from 'bcryptjs'
import jwt from 'jsonwebtoken'

const prisma = new PrismaClient()

export const registerUserService = async (
  name: string,
  email: string,
  password: string,
  repeatPassword: string,
) => {
  if (password !== repeatPassword) {
    throw new Error('Passwords do not match')
  }

  const existingUser = await prisma.user.findUnique({
    where: { email },
  })

  if (existingUser) {
    throw new Error('User already exists')
  }

  const hashedPassword = await bcrypt.hash(password, 10)

  const user = await prisma.user.create({
    data: {
      name,
      email,
      password: hashedPassword,
    },
  })

  return user
}

export const loginUserService = async (email: string, password: string) => {
  const user = await prisma.user.findUnique({
    where: { email },
  })

  if (!user) {
    throw new Error('User not found')
  }

  if (!user.password) {
    throw new Error('User does not have a password set')
  }
  const isPasswordValid = await bcrypt.compare(password, user.password)

  if (!isPasswordValid) {
    throw new Error('Invalid password')
  }

  const token = jwt.sign({ id: user.id, email: user.email, name: user.name }, 'clave-secreta', {
    expiresIn: '1h',
  })

  return token
}

export const exchangeGoogleCodeForToken = async (code: string) => {
  interface GoogleTokenResponse {
    sub: string
    email: string
    name: string
    picture?: string
    email_verified?: boolean
  }

  const res = await axios.post('https://oauth2.googleapis.com/token', {
    code,
    client_id: process.env.CLIENT_ID,
    client_secret: process.env.CLIENT_SECRET,
    redirect_uri: process.env.REDIRECT_URI,
    grant_type: 'authorization_code',
  })

  const idToken: string = res.data.id_token
  const decoded = jwt.decode(idToken) as GoogleTokenResponse | null

  if (!decoded || !decoded.email || !decoded.sub) {
    throw new Error('Failed to decode Google ID token')
  }

  let user: User | null = await prisma.user.findUnique({
    where: { googleId: decoded.sub },
  })
  if (!user) {
    user = await prisma.user.findUnique({
      where: { email: decoded.email },
    })
    if (user) {
      user = await prisma.user.update({
        where: { id: user.id },
        data: {
          googleId: decoded.sub,
          provider: 'google',
          name: decoded.name,
        },
      })
    } else {
      user = await prisma.user.create({
        data: {
          email: decoded.email,
          name: decoded.name,
          googleId: decoded.sub,
          provider: 'google',
        },
      })
    }
  } else {
    user = await prisma.user.update({
      where: { id: user.id },
      data: {
        email: decoded.email,
        name: decoded.name,
      },
    })
  }

  const token = jwt.sign({ id: user.id, email: user.email, name: user.name }, 'clave-secreta', {
    expiresIn: '1h',
  })

  return token
}
