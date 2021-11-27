import { QueryClient, QueryClientProvider } from 'react-query';
import Router from './routes';
import { AuthProvider } from './lib/auth';

const queryClient = new QueryClient();

const App = () =>
  <QueryClientProvider client={queryClient}>
    <AuthProvider>
      <Router />
    </AuthProvider>
  </QueryClientProvider>
;

export default App;
