/**
 * To create different base url clients for the requests
 */
export const apiUrl = process.env.NEXT_PUBLIC_API_URL!

/**
 *
 * @param baseUrl The base url, e.g, http://localhost:5000
 * @returns another function to make requests to an API endpoint with a given base URL
 */
function createFetchClientWithBaseUrl(
  baseUrl: string,
  baseOptions?: RequestInit
) {
  return async function (endpoint: string, options?: RequestInit) {
    const url = baseUrl + endpoint
    return await fetch(url, {
      ...baseOptions,
      ...options,
    })
  }
}

/**
 * The base client handling the route '/api'
 */
export const baseClient = createFetchClientWithBaseUrl(apiUrl, {
  headers: {
    "Content-Type": "application/json",
  },
})

/**
 * The auth client handling the route '/auth'
 */
export const authClient = createFetchClientWithBaseUrl(apiUrl + "/movies")

/**
 * The movies client handling the route '/movies'
 */
export const moviesClient = createFetchClientWithBaseUrl(apiUrl + "/movies")

/**
 * JSON Response types from the clients
 */

// The base client response from the server
export interface BaseClientJSON {
  msg: string
  code: number
  payload: any | null
  raw_msg: string
}

// The responses for the auth client
export interface AuthClientJSON extends BaseClientJSON {
  payload: User | null
}

// The responses for the movie client
export interface MovieClientJSON extends BaseClientJSON {
  payload: Movie[] | null
}
