// The authentication actions
type AuthAction = {
  signIn: FormAction
  signUp: FormAction
  // Logout the current user
  signOut: BaseAction
  // Get the current user
  getUser: FruitAction<User | null>
}

export const auth = {
  signIn: async e => {
    // TODO: Logic for sign-in here
  },
  signUp: async e => {
    // TODO: Logic for sign-up here
  },
  signOut: async () => {
    // TODO: Logic for sign-out here
  },
  getUser: async () => {
    // TODO: Logic for current-user here
    return null
  },
} as AuthAction

// The movies actions
type MovieAction = {
  search: FruitFormAction<Movie[] | null>
  recommend: FruitFormAction<Movie[] | null>
}

export const movie = {
  search: async e => null,
  recommend: async e => null,
} as MovieAction
