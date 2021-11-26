import { Grid } from '@mui/material';
import { useQuery } from 'react-query';
import { useParams } from 'react-router';
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
  const query = useQuery(`book-${bookId}`, () =>
    fetch(`${process.env.REACT_APP_API_BASE_URL}/catalogs/books/${bookId}`).then(res => res.json())
  );

  return (
    <>
      {query.isSuccess && (
        <Grid container justifyContent="left" alignItems="stretch" spacing={2}>
          <Grid item xs={6}>
            <p>Title: {query.data.title}</p>
            <p>ISBN: {query.data.isbn}</p>
            <p>Author: {query.data.author}</p>
            <p>Genre: {query.data.genre}</p>
            <p>Language: {query.data.language}</p>
          </Grid>
          <Grid item xs={6}>
            <img
              src={'https://fakeimg.pl/400x600/?text=No%20Cover&font=bebas'}
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
