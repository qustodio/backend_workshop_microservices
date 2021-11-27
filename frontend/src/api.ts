export const fetchBooks = () =>
  fetch(`${process.env.REACT_APP_API_BASE_URL}/catalog/books`)
    .then(res => res.json())

export const fetchAuthors = () =>
  fetch(`${process.env.REACT_APP_API_BASE_URL}/catalog/authors`)
    .then(res => res.json())

export const fetchGenres = () =>
  fetch(`${process.env.REACT_APP_API_BASE_URL}/catalog/genres`)
    .then(res => res.json())

export const fetchLanguages = () =>
  fetch(`${process.env.REACT_APP_API_BASE_URL}/catalog/languages`)
    .then(res => res.json())

export const fetchBook = (bookId: string|undefined) =>
  fetch(`${process.env.REACT_APP_API_BASE_URL}/catalog/books/${bookId}`)
    .then(res => res.json())

export const fetchAuthor = (authorId: number) =>
  fetch(`${process.env.REACT_APP_API_BASE_URL}/catalog/authors/${authorId}`)
    .then(res => res.json())
