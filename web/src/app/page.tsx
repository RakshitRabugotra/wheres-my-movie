import { MovieSearchAutocomplete } from "@/components/movie-search"
import { Link } from "@nextui-org/link"
import { button as buttonStyles } from "@nextui-org/theme"

export default function Home() {
  return (
    <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
      <MovieSearchAutocomplete />
    </section>
  )
}
