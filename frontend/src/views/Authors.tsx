import Layout from '../components/Layout/Layout';
import { useQuery } from 'react-query';
import { Card, CardContent, Grid, Typography } from '@mui/material';
import { fetchAuthors } from '../api';

const Authors = () =>
  <Layout>
    <>
      <h1>All Authors</h1>
      <ListAuthors />
    </>
  </Layout>

const ListAuthors = () => {
  const query = useQuery('authors', fetchAuthors);

  return (
    <Grid container justifyContent="left" alignItems="stretch" spacing={2}>
      {query.isSuccess && query.data.map((author: any) => (
        <Grid key={author.id} item xs={3}>
          <AuthorCard author={author} />
        </Grid>
      ))}
    </Grid>
  );
}

const AuthorCard = ({author}: {author: any}) => {
  return (
    <Card>
      <CardContent>
        <Typography variant="h5" component="div">
          {author.first_name} {author.last_name}
        </Typography>
        <Typography sx={{ mb: 1.5 }} color="text.secondary">
        {author.date_of_birth} - {author.date_of_death}
        </Typography>
      </CardContent>
    </Card>
  );
}

export default Authors;
