import { Link } from 'react-router-dom';
import Layout from '../components/Layout/Layout';

const Home = () =>
  <Layout>
    <>
      <h1>Home</h1>
      <p>Welcome to PyDay 2021, take a look at our <Link style={{color: 'blue', textDecoration: 'underline'}} to='/books'>library</Link></p>
    </>
  </Layout>

export default Home;
