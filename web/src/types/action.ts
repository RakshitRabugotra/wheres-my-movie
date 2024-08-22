// The base action for the application
type BaseAction = () => Promise<void>

// The base action which returns a certain generic type
type FruitAction<T> = () => Promise<T>

// The action taking in form-data from client
type FormAction = (e: FormData) => Promise<void>

type FruitFormAction<T> = (e: FormData) => Promise<T>
