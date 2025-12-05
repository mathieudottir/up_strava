const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const api = {
  async get(endpoint: string) {
    const response = await fetch(`${API_URL}${endpoint}`)
    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`)
    }
    return response.json()
  },

  async post(endpoint: string, data?: any) {
    const response = await fetch(`${API_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: data ? JSON.stringify(data) : undefined,
    })
    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`)
    }
    return response.json()
  },
}

export async function fetchUserProfile(userId: string) {
  return api.get(`/api/v1/users/${userId}`)
}

export async function fetchUserActivities(userId: string, skip = 0, limit = 20) {
  return api.get(`/api/v1/activities/?user_id=${userId}&skip=${skip}&limit=${limit}`)
}

export async function syncActivities(userId: string) {
  return api.post(`/api/v1/activities/sync?user_id=${userId}`)
}

export async function fetchBadges(userId?: string) {
  const query = userId ? `?user_id=${userId}` : ''
  return api.get(`/api/v1/badges/${query}`)
}

export async function fetchLeaderboards() {
  return api.get('/api/v1/leaderboards/')
}

export async function fetchChallenges(userId?: string) {
  const query = userId ? `?user_id=${userId}` : ''
  return api.get(`/api/v1/challenges/${query}`)
}
