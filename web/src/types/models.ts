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
  imdbId: number | null
  tmdbId: number | null
}
