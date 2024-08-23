interface User {
  id: string
  email: string
  username: string
  created: string
}

// The movies model
interface Movie {
  movieId: number
  title: string
  genres: string[]
  tags: string[]
  rating: number
  image?: string | null
  imdbId: number | null
  tmdbId: number | null
}
