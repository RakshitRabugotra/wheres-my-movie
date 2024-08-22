"use client"

// Carousel hooks
import useEmblaCarousel from "embla-carousel-react"

// Internal Components for carousel
import { PrevButton, NextButton, usePrevNextButtons } from "./carousel-button"
import { DotButton, useDotButton } from "./carousel-dots"

// Type definitions
import { EmblaOptionsType } from "embla-carousel"
import { useEffect, useState } from "react"
import clsx from "clsx"

type PropType<T> = {
  slides: T[]
  renderItem: React.FC<T>
  shrink?: boolean
  options?: EmblaOptionsType
}
// The default options for the carousel
const OPTIONS: EmblaOptionsType = { align: "start", loop: false }

function EmblaCarousel<T>({
  slides,
  renderItem,
  shrink = false,
  options = OPTIONS,
}: PropType<T>) {
  const [emblaRef, emblaApi] = useEmblaCarousel(options)
  // To get the selected index element
  const [selectedIndex, setSelectedIndex] = useState(0)

  const onSelect = () => {
    if (!emblaApi) return
    setSelectedIndex(emblaApi.selectedScrollSnap())
  }

  useEffect(() => {
    if (!emblaApi) return
    emblaApi.on("select", onSelect)
    onSelect()
  }, [emblaApi])

  const { scrollSnaps, onDotButtonClick } = useDotButton(emblaApi)

  const {
    prevBtnDisabled,
    nextBtnDisabled,
    onPrevButtonClick,
    onNextButtonClick,
  } = usePrevNextButtons(emblaApi)

  return (
    <section className="embla">
      <div className="embla__viewport" ref={emblaRef}>
        <div className="embla__container">
          {slides.map((props, index) => (
            <div
              className={clsx(
                "embla__slide",
                index === selectedIndex ? (shrink ? "is-selected" : "") : ""
              )}
              key={index}
            >
              {renderItem(props)}
            </div>
          ))}
        </div>
      </div>

      <div className="embla__controls">
        <div className="embla__buttons">
          <PrevButton onClick={onPrevButtonClick} disabled={prevBtnDisabled} />
          <NextButton onClick={onNextButtonClick} disabled={nextBtnDisabled} />
        </div>

        <div className="embla__dots">
          {scrollSnaps.map((_, index) => (
            <DotButton
              key={index}
              onClick={() => onDotButtonClick(index)}
              className={"embla__dot".concat(
                index === selectedIndex ? " embla__dot--selected" : ""
              )}
            />
          ))}
        </div>
      </div>
    </section>
  )
}

export default EmblaCarousel
