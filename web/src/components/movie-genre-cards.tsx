"use client"

import { GenreProps, GENRES } from "@/lib/constants"
import { Card, CardBody, CardFooter } from "@nextui-org/card"
import { Image } from "@nextui-org/image"
import { Skeleton } from "@nextui-org/skeleton"
import React, { useEffect } from "react"

export const GenreCards = () => {
  return (
    <div className="w-full gap-4 grid grid-cols-2 sm:grid-cols-4">
      {GENRES.map((genre, index) => (
        <GenreCard key={index + genre.title} {...genre} />
      ))}
    </div>
  )
}

const GenreCard: React.FC<GenreProps> = ({ title, image, color }) => {
  const [isLoaded, setLoaded] = React.useState(false)

  useEffect(() => {
    setLoaded(true)
  }, [])

  return (
    <Card
      shadow="sm"
      isPressable
      onPress={() => console.log("item pressed")}
      className="shadow-lg shadow-primary-300/25 w-full"
    >
      <Skeleton isLoaded={isLoaded} className="w-full rounded-lg">
        <CardBody className="overflow-visible p-0">
          <Image
            shadow="sm"
            radius="lg"
            width="100%"
            alt={title}
            className="w-full object-cover h-[100px] object-top"
            src={image}
          />
        </CardBody>
        <CardFooter className="text-small justify-between">
          <b>{title}</b>
          <p
            className="text-default-500 w-2 h-2 rounded-full"
            style={{ backgroundColor: color }}
          ></p>
        </CardFooter>
      </Skeleton>
    </Card>
  )
}
