import { storage } from './lib/storage';

export interface AuthResponse {
  jwt: string;
}

export interface User {
  id: string;
  username?: string;
}

export const fetchRecommendations = async (userId: any) => {
  return await fetch(`${process.env.REACT_APP_API_BASE_URL}/recommendations/${userId}`, {
    headers: {
      Authorization: `Bearer ${storage.getToken()}`
    }
  }).then(res => res.json());
}

export const postLoan = async (data: any) => {
  return await fetch(`${process.env.REACT_APP_API_BASE_URL}/catalog/loan`, {
    method: "POST",
    body: JSON.stringify(data),
    headers: {
      Authorization: `Bearer ${storage.getToken()}`
    }
  }).then(res => res.json());
}

export const postLogin = async (data: any): Promise<AuthResponse> => {
  return window
    .fetch(`${process.env.REACT_APP_API_BASE_URL}/auth`, {
      method: "POST",
      body: JSON.stringify(data)
    })
    .then(res => res.json())
    .catch(err => console.error(err));
}

export const fetchUser = () =>
  fetch(`${process.env.REACT_APP_API_BASE_URL}/users/me`,{
    headers: {
      Authorization: `Bearer ${storage.getToken()}`
    }
  }).then(res => res.json())

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
