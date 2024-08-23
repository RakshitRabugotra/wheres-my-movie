export default function MoviePage({ params }: { params: { movieId: string } }) {
  console.log(params.movieId)

  return <div>{params.movieId}</div>
}
