'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'

export default function Home() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  useEffect(() => {
    const token = localStorage.getItem('auth_token')
    setIsAuthenticated(!!token)
  }, [])

  const handleStravaLogin = async () => {
    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    try {
      const response = await fetch(`${API_URL}/api/v1/auth/strava/authorize`)
      const data = await response.json()
      window.location.href = data.authorization_url
    } catch (error) {
      console.error('Failed to initiate Strava login:', error)
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-orange-500 via-red-500 to-pink-500">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center text-white">
          <h1 className="text-6xl font-bold mb-6">
            Strava Gamification
          </h1>
          <p className="text-2xl mb-8 opacity-90">
            Transform your activities into an epic adventure with points, badges, and challenges
          </p>

          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 mb-12">
            <h2 className="text-3xl font-semibold mb-6">Features</h2>
            <div className="grid md:grid-cols-3 gap-6 text-left">
              <div className="bg-white/10 rounded-xl p-6">
                <div className="text-4xl mb-4">🏆</div>
                <h3 className="text-xl font-bold mb-2">Points System</h3>
                <p className="opacity-80">Earn points for every activity based on distance, elevation, and time</p>
              </div>
              <div className="bg-white/10 rounded-xl p-6">
                <div className="text-4xl mb-4">🎖️</div>
                <h3 className="text-xl font-bold mb-2">Badges & Achievements</h3>
                <p className="opacity-80">Unlock exclusive badges by reaching milestones and completing challenges</p>
              </div>
              <div className="bg-white/10 rounded-xl p-6">
                <div className="text-4xl mb-4">📊</div>
                <h3 className="text-xl font-bold mb-2">Leaderboards</h3>
                <p className="opacity-80">Compete with others on global and segment-specific leaderboards</p>
              </div>
            </div>
          </div>

          {isAuthenticated ? (
            <div className="space-x-4">
              <Link
                href="/dashboard"
                className="inline-block bg-white text-strava-orange font-bold text-xl px-8 py-4 rounded-full hover:bg-gray-100 transition-colors"
              >
                Go to Dashboard
              </Link>
            </div>
          ) : (
            <button
              onClick={handleStravaLogin}
              className="inline-flex items-center gap-3 bg-strava-orange text-white font-bold text-xl px-8 py-4 rounded-full hover:bg-strava-dark-orange transition-colors"
            >
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M15.387 17.944l-2.089-4.116h-3.065L15.387 24l5.15-10.172h-3.066m-7.008-5.599l2.836 5.598h4.172L10.463 0l-7 13.828h4.169"/>
              </svg>
              Connect with Strava
            </button>
          )}
        </div>
      </div>
    </main>
  )
}
