export const fetchBooks = () =>
  fetch(`${process.env.REACT_APP_API_BASE_URL}/catalogs/books`)
    .then(res => res.json())

export const fetchAuthors = () =>
  fetch(`${process.env.REACT_APP_API_BASE_URL}/catalogs/authors`)
    .then(res => res.json())

export const fetchGenres = () =>
  fetch(`${process.env.REACT_APP_API_BASE_URL}/catalogs/genres`)
    .then(res => res.json())

export const fetchLanguages = () =>
  fetch(`${process.env.REACT_APP_API_BASE_URL}/catalogs/languages`)
    .then(res => res.json())

export const fetchBook = (bookId: string|undefined) =>
  fetch(`${process.env.REACT_APP_API_BASE_URL}/catalogs/books/${bookId}`)
    .then(res => res.json())

export const fetchAuthor = (authorId: number) =>
  fetch(`${process.env.REACT_APP_API_BASE_URL}/catalogs/authors/${authorId}`)
    .then(res => res.json())
