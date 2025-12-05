'use client'

import { Suspense, useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'

function AuthCallbackContent() {
  const router = useRouter()
  const searchParams = useSearchParams()

  useEffect(() => {
    const handleCallback = async () => {
      const code = searchParams.get('code')
      const error = searchParams.get('error')

      if (error) {
        console.error('Strava auth error:', error)
        router.push('/?error=auth_failed')
        return
      }

      if (!code) {
        router.push('/?error=no_code')
        return
      }

      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

      try {
        const response = await fetch(
          `${API_URL}/api/v1/auth/strava/callback?code=${code}`
        )

        if (!response.ok) {
          throw new Error('Authentication failed')
        }

        const data = await response.json()

        // Store auth token and user ID
        localStorage.setItem('auth_token', data.access_token)
        localStorage.setItem('user_id', data.user_id.toString())

        // Redirect to dashboard
        router.push('/dashboard')
      } catch (error) {
        console.error('Failed to complete authentication:', error)
        router.push('/?error=auth_failed')
      }
    }

    handleCallback()
  }, [router, searchParams])

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-orange-500 via-red-500 to-pink-500">
      <div className="text-center text-white">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-white mx-auto mb-4"></div>
        <p className="text-xl font-semibold">Authenticating with Strava...</p>
      </div>
    </div>
  )
}

export default function AuthCallback() {
  return (
    <Suspense fallback={
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-orange-500 via-red-500 to-pink-500">
        <div className="text-center text-white">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-white mx-auto mb-4"></div>
          <p className="text-xl font-semibold">Loading...</p>
        </div>
      </div>
    }>
      <AuthCallbackContent />
    </Suspense>
  )
}
