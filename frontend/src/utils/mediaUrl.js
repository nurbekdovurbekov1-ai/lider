const BACKEND_URL = import.meta.env.VITE_API_URL || ''

export function getMediaUrl(path) {
  if (!path) return '/no-image.svg'
  // If path is already absolute (starts with http), return as-is
  if (path.startsWith('http')) return path
  // If path starts with /media/, prepend backend URL
  if (path.startsWith('/media/')) {
    return BACKEND_URL ? `${BACKEND_URL}${path}` : path
  }
  // Otherwise return as-is (for local assets like /no-image.svg)
  return path
}
