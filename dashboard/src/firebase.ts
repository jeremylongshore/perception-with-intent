import { initializeApp } from 'firebase/app'
import { getAuth } from 'firebase/auth'
import { getFirestore } from 'firebase/firestore'

// Firebase configuration from environment variables
// For local development, create a .env.local file with these values
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || "AIzaSyBhVVxPp7g7vXv1XZ7pZ2L0q7YxPxUgXqM",
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || "perception-with-intent.firebaseapp.com",
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || "perception-with-intent",
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || "perception-with-intent.firebasestorage.app",
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || "755584869357",
  appId: import.meta.env.VITE_FIREBASE_APP_ID || "1:755584869357:web:d5f7c3b8b4e6f9a8c4d5e6"
}

// Initialize Firebase
const app = initializeApp(firebaseConfig)

// Initialize services
export const auth = getAuth(app)
export const db = getFirestore(app)

export default app
