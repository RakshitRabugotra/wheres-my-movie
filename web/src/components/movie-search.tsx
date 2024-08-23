"use client"

import React, { useEffect, useState } from "react"
import { Autocomplete, AutocompleteItem } from "@nextui-org/autocomplete"
import { useAsyncList } from "@react-stately/data"
import { MovieClientJSON, moviesClient } from "@/lib/fetch-client"
import { MovieCamera } from "./icons"
import Link from "next/link"

export const MovieSearchAutocomplete = () => {
  const [filterText, setFilterText] = useState<string>(
    "The silence of the lambs"
  )

  const list = useAsyncList({
    async load({ filterText: ft, signal }) {
      const response = {
        items: [],
      }
      if (typeof ft === "undefined") return response
      if (ft.length === 0) return response

      let res = await moviesClient(`/search?q=${ft}`, {
        signal,
      })
      let json = (await res.json()) as MovieClientJSON

      if (json.payload) response.items = json.payload as never[]
      return response
    },
  })

  // Debounce the filterText state
  useEffect(() => {
    const handler = setTimeout(() => {
      list.setFilterText(filterText)
    }, 300) // Adjust the delay as needed
    return () => {
      clearTimeout(handler)
    }
  }, [filterText])

  return (
    <Autocomplete
      className="select-none max-w-md"
      inputValue={filterText}
      color="primary"
      isLoading={list.isLoading}
      items={list.items as Movie[]}
      label="Select a movie"
      labelPlacement="outside"
      placeholder="Type to search..."
      selectorIcon={null}
      endContent={null}
      startContent={<MovieCamera />}
      onInputChange={setFilterText}
    >
      {item => (
        <AutocompleteItem
          key={item.movieId}
          className="capitalize"
          textValue={item.title}
        >
          <Link href={"movie/" + item.movieId}>{item.title}</Link>
        </AutocompleteItem>
      )}
    </Autocomplete>
  )
}
