"use client"

import { useEffect, useState } from "react"
// Components
import { Card, CardBody, CardFooter } from "@nextui-org/card"
import { Link } from "@nextui-org/link"
import EmblaCarousel from "./embla/carousel"

import { RECOMMENDED_MOVIES } from "@/lib/constants"
import { Skeleton } from "@nextui-org/skeleton"
import { Image } from "@nextui-org/image"
import { StarIcon } from "./icons"

export const RecommendedMovieCards = () => {
  return (
    <div className="ml-4 overflow-hidden mt-2">
      <EmblaCarousel
        slides={RECOMMENDED_MOVIES}
        renderItem={MovieCard}
        shrink
      />
    </div>
  )
}

const MovieCard: React.FC<Movie> = ({
  movieId,
  title,
  genres,
  tags,
  rating,
  image,
  imdbId,
  tmdbId,
}) => {
  const [isLoaded, setLoaded] = useState(false)

  useEffect(() => {
    setLoaded(true)
  }, [])

  return (
    <Card
      radius="lg"
      isPressable
      as={Link}
      href={"/movie/" + movieId}
      className="border-none z-30 shadow-large"
      classNames={{
        body: "p-0 max-w-full [&>div]:!max-w-full",
      }}
    >
      <Skeleton isLoaded={isLoaded} className="w-full rounded-lg">
        <CardBody>
          <Image
            alt={title}
            className="object-cover w-full"
            height={800 / 3}
            src={image || "/"}
            width={200}
            loading="eager"
          />
        </CardBody>
        <CardFooter className="justify-between flex-wrap p-2 gap-2 flex-row items-end overflow-hidden absolute bottom-1 w-[calc(100%_-_8px)]">
          <div className="flex flex-col gap-2">
            <p className="text-tiny bg-default-600 dark:bg-black w-fit text-white/80 before:bg-white/10 border-white/20 p-1 px-2 border-1 before:rounded-xl rounded-large shadow-small  ml-1 z-10">
              {title}
            </p>
            <p className="text-tiny inline-flex items-center justify-between bg-default-600 dark:bg-black w-fit text-white/80 before:bg-white/10 border-white/20 p-1 px-2 border-1 before:rounded-xl rounded-large shadow-small  ml-1 z-10">
              <StarIcon className="text-amber-300" />
              <span className="mx-2">{rating.toFixed(1)}</span>
            </p>
          </div>

          {/* {fav && (
            <button
              className="text-red-500 p-2 bg-white rounded-full z-10"
              onClick={handleLike}
            >
              <HeartFilledIcon size={16} />
            </button>
          )} */}
        </CardFooter>
      </Skeleton>
    </Card>
  )
}
