import { GenreCards } from "@/components/movie-genre-cards"
import { RecommendedMovieCards } from "@/components/movie-recommended"
import { MovieSearchAutocomplete } from "@/components/movie-search"
import { subtitle, title } from "@/components/primitives"
import { ThemeSwitch } from "@/components/theme-switch"

export default function Home() {
  const user: User = {
    id: "123",
    email: "rakshit.rabugotra360@gmail.com",
    username: "Rakshit Rabugotra",
    created: "2024-08-20",
  }

  return (
    <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
      {/* Heading */}
      <section className="px-4 w-full flex flex-row justify-between ">
        <div className="grow">
          <h2 className={subtitle({ class: "m-0" })}>Welcome</h2>
          <h1
            className={title({
              class: "font-semibold m-0 text-left w-full leading-none",
            })}
          >
            {user.username.split(" ")[0]}
          </h1>
        </div>
        <ThemeSwitch />
      </section>

      {/* The search section */}
      <section className="mt-8 w-full px-4">
        <MovieSearchAutocomplete />
      </section>

      {/* The section with the cards */}
      <section className="p-6 w-full">
        <GenreCards />
      </section>

      {/* The section for recommended movies */}
      <section className="w-full mt-5">
        <h3
          className={subtitle({
            class: "px-6 text-2xl font-medium leading-snug",
          })}
        >
          For you!
        </h3>
        <RecommendedMovieCards />
      </section>
    </section>
  )
}
