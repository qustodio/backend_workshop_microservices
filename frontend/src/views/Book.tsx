import { Chip, Grid } from '@mui/material';
import { useQuery } from 'react-query';
import { useParams } from 'react-router';
import { fetchAuthor, fetchBook, fetchGenres, fetchLanguages } from '../api';
import Layout from '../components/Layout/Layout';

const Book = () => {
  let { id } = useParams();
  return (
    <Layout>
      <>
        <h1>Book details</h1>
        <BookDetails bookId={id}/>
      </>
    </Layout>
  );
}

const BookDetails = ({bookId}: {bookId: string|undefined}) => {
  const query = useQuery(['book', bookId], () => fetchBook(bookId));

  const genres = useQuery(
    'genres', fetchGenres,
    {
      enabled: query.isSuccess,
    }
  )

  const languages = useQuery(
    'languages', fetchLanguages,
    {
      enabled: query.isSuccess,
    }
  )

  const authorId = query.data?.id
  const author = useQuery(
    ['author', authorId] , () => fetchAuthor(authorId),
    {
      enabled: !!authorId,
    }
  )

  const getGenreName = (genreId: number) => {
    let genreName = '';
    console.log(genres.data);
    genres.data.forEach((genre: any) => {
      if (genreId == genre.id) genreName = genre.name;
    });
    return genreName;
  }
  const renderGenres = () => (
    query.data.genre.map((genreId: number) => (
      <Chip sx={{ marginRight: '8px' }} label={getGenreName(genreId).toUpperCase()} />
    ))
  )

  const renderLanguage = () => {
    let languageName = '';
    languages.data.forEach((language: any) => {
      if (query.data.language == language.id) languageName = language.name;
    });
    return languageName;
  }

  return (
    <>
      {query.isSuccess && (
        <Grid container justifyContent="left" alignItems="stretch" spacing={2}>
          <Grid item xs={6}>
            <p>Title: {query.data.title}</p>
            <p>ISBN: {query.data.isbn}</p>
            <p>Author: {author.isSuccess && `${author.data.first_name} ${author.data.last_name}`}</p>
            <p>Genre: {genres.isSuccess && renderGenres()}</p>
            <p>Language: {languages.isSuccess && renderLanguage()}</p>
          </Grid>
          <Grid item xs={6}>
            <img
              src={query.data.image ? `data:image/png;base64, ${query.data.image}` : 'https://fakeimg.pl/400x600/?text=No%20Cover&font=bebas'}
              alt={query.data.title}
              loading="lazy"
              height={500}
            />
          </Grid>
        </Grid>
      )}
    </>
  )
}

export default Book;
