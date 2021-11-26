import { Card, CardActionArea, CardMedia, CardContent, Typography, Button, CardActions, Grid } from '@mui/material';
import { useQuery } from 'react-query';
import { Link } from 'react-router-dom';
import Layout from '../components/Layout/Layout';

const Books = () =>
  <Layout>
    <>
      <h1>All Books</h1>
      <ListBooks />
    </>
  </Layout>

const ListBooks = () => {
  const query = useQuery('books', () =>
    fetch(`${process.env.REACT_APP_API_BASE_URL}/catalogs/books`).then(res => res.json())
  );

  return (
    <Grid container justifyContent="left" alignItems="stretch" spacing={2}>
      {query.isSuccess && query.data.map((book: any) => (
        <Grid key={book.id} item xs={3}>
          <BookCard book={book} />
        </Grid>
      ))}
    </Grid>
  );
}

const BookCard = ({book}: {book: any}) => {
  return (
    <Card>
      <CardActionArea>
        <Link to={`/book/${book.id}`}>
          <CardMedia
            component="img"
            height="300"
            image={'https://fakeimg.pl/400x600/?text=No%20Cover&font=bebas'}
            alt={book.title}
          />
          <CardContent>
            <Typography gutterBottom variant="h5" component="div">
              {book.title}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {book.summary}
            </Typography>
          </CardContent>
        </Link>
      </CardActionArea>
      <CardActions>
        <Button size="small" color="primary">
          Borrow
        </Button>
      </CardActions>
    </Card>
  );
}

export default Books;
