import { Button, TextField, Typography } from '@mui/material';
import { Box } from '@mui/system';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Layout from '../components/Layout/Layout';
import { useAuth } from '../lib/auth';

const Login = () => {
  let navigate = useNavigate();
  const { login } = useAuth();
  const [error, setError] = useState(false);

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    // eslint-disable-next-line no-console
    console.log({
      username: data.get('username'),
      password: data.get('password'),
    });
    // login(data)
    //   .then(() => {
    //     setError(false);
    //     return navigate('/');
    //   })
    //   .catch(() => setError(true));
  };

  return (
    <Layout>
      <>
        <h1>Login</h1>
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'left',
            maxWidth: '300px'
          }}
        >
          <Box component="form" onSubmit={handleSubmit} noValidate>
            <TextField
              margin="normal"
              required
              fullWidth
              id="username"
              label="Username"
              name="username"
              autoComplete="username"
              autoFocus
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Sign In
            </Button>
            {error && (
              <Typography sx={{color: '#ff0000'}} variant="caption" display="block" gutterBottom>
                Something is wrong, try again in a few minutes
              </Typography>
            )}
          </Box>
        </Box>
      </>
    </Layout>
  )
}

export default Login;
