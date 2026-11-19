export function getMediaUrl(path) {
  if (!path) return '/no-image.svg'
  // If path is already absolute (starts with http), return as-is
  if (path.startsWith('http')) return path
  // Otherwise return as-is (same domain now)
  return path
}
