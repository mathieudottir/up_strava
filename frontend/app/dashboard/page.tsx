'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useQuery } from '@tanstack/react-query'

interface UserProfile {
  id: number
  username: string | null
  firstname: string | null
  lastname: string | null
  total_points: number
  level: number
  activity_count: number
  total_distance: number
  total_elevation: number
}

export default function Dashboard() {
  const router = useRouter()
  const [userId, setUserId] = useState<string | null>(null)
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

  useEffect(() => {
    const token = localStorage.getItem('auth_token')
    const storedUserId = localStorage.getItem('user_id')

    if (!token || !storedUserId) {
      router.push('/')
      return
    }

    setUserId(storedUserId)
  }, [router])

  const { data: profile, isLoading } = useQuery<UserProfile>({
    queryKey: ['profile', userId],
    queryFn: async () => {
      const response = await fetch(`${API_URL}/api/v1/users/${userId}`)
      if (!response.ok) throw new Error('Failed to fetch profile')
      return response.json()
    },
    enabled: !!userId,
  })

  const handleSync = async () => {
    if (!userId) return

    try {
      const response = await fetch(
        `${API_URL}/api/v1/activities/sync?user_id=${userId}`,
        { method: 'POST' }
      )

      if (response.ok) {
        window.location.reload()
      }
    } catch (error) {
      console.error('Sync failed:', error)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user_id')
    router.push('/')
  }

  if (isLoading || !profile) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-orange-500 mx-auto mb-4"></div>
          <p className="text-xl">Loading...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-strava-orange">Strava Gamification</h1>
          <div className="flex items-center gap-4">
            <button
              onClick={handleSync}
              className="bg-strava-orange text-white px-4 py-2 rounded-lg hover:bg-strava-dark-orange transition-colors"
            >
              Sync Activities
            </button>
            <button
              onClick={handleLogout}
              className="text-gray-600 hover:text-gray-900"
            >
              Logout
            </button>
          </div>
        </div>
      </nav>

      <div className="container mx-auto px-4 py-8">
        <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
          <div className="flex items-center gap-6">
            <div className="w-24 h-24 bg-gradient-to-br from-orange-500 to-pink-500 rounded-full flex items-center justify-center text-white text-3xl font-bold">
              {profile.firstname?.[0] || 'U'}
            </div>
            <div>
              <h2 className="text-3xl font-bold">
                {profile.firstname} {profile.lastname}
              </h2>
              <p className="text-gray-600">@{profile.username || 'athlete'}</p>
            </div>
          </div>
        </div>

        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="text-4xl mb-2">⭐</div>
            <div className="text-3xl font-bold text-strava-orange">{profile.total_points}</div>
            <div className="text-gray-600">Total Points</div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="text-4xl mb-2">🎯</div>
            <div className="text-3xl font-bold text-blue-600">{profile.level}</div>
            <div className="text-gray-600">Level</div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="text-4xl mb-2">🏃</div>
            <div className="text-3xl font-bold text-green-600">{profile.activity_count}</div>
            <div className="text-gray-600">Activities</div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="text-4xl mb-2">📏</div>
            <div className="text-3xl font-bold text-purple-600">{profile.total_distance.toFixed(1)} km</div>
            <div className="text-gray-600">Total Distance</div>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-xl font-bold mb-4">Recent Activities</h3>
            <p className="text-gray-500">Sync your Strava activities to see them here</p>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-xl font-bold mb-4">Badges</h3>
            <p className="text-gray-500">Earn badges by completing challenges</p>
          </div>
        </div>
      </div>
    </div>
  )
}
