"use client"

import { GenreProps, GENRES } from "@/lib/constants"
import { Card, CardHeader, CardBody, CardFooter } from "@nextui-org/card"
import { Image } from "@nextui-org/image"
import React from "react"

export const MovieCards = () => {
  return (
    <div className="w-full gap-4 grid grid-cols-2 sm:grid-cols-4">
      {GENRES.map((genre, index) => (
        <MovieCard key={index + genre.title} {...genre} />
      ))}
    </div>
  )
}

const MovieCard: React.FC<GenreProps> = ({ title, image, color }) => {
  return (
    <Card shadow="sm" isPressable onPress={() => console.log("item pressed")}>
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
    </Card>
  )
}
