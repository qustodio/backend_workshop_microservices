import { QueryClient, QueryClientProvider } from 'react-query';
import Router from './routes';

const queryClient = new QueryClient();

const App = () =>
  <QueryClientProvider client={queryClient}>
    <Router />
  </QueryClientProvider>
;

export default App;
