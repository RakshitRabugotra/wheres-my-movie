export interface GenreProps {
  title: string
  image: string
  color: string
}

export const GENRES: GenreProps[] = [
  {
    title: "Action",
    image: "/genre-images/action.webp",
    color: "#7F00FF",
  },
  {
    title: "Thriller",
    image: "/genre-images/thriller.jpg",
    color: "#4b0082",
  },
  {
    title: "Sci-Fi",
    image: "/genre-images/scifi.webp",
    color: "#0000FF",
  },
  {
    title: "Romance",
    image: "/genre-images/romance.webp",
    color: "#00FF00",
  },
  {
    title: "Crime",
    image: "/genre-images/crime.webp",
    color: "#008080",
  },
  {
    title: "Comedy",
    image: "/genre-images/comedy.webp",
    color: "#00FFFF",
  },
  {
    title: "Horror",
    image: "/genre-images/horror.webp",
    color: "#FFC0CB",
  },
  {
    title: "Comics",
    image: "/genre-images/comics.webp",
    color: "#FF0000",
  },
]
