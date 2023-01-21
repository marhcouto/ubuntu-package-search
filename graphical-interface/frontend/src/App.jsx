import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import Homepage from './pages/Homepage';
import ResultsPage from './pages/ResultsPage';
import { searchPackages } from './documentFetcher';

function App() {
  const router = createBrowserRouter([
    {
      path: '/',
      element: <Homepage />
    },
    {
      path: 'search',
      element: <ResultsPage />,
      loader: async (params) => {
        const url = new URL(params.request.url);
        const searchTerms = url.searchParams.get('q');
        const weights = {
          description: url.searchParams.get('desc-weight'),
          package: url.searchParams.get('pack-weight'),
          section: url.searchParams.get('sec-weight'),
          exactMatches: url.searchParams.get('exact-matches')
        };
        const filterFields = Array.from(url.searchParams.entries()).filter((entry) =>
          /field-\d/.test(entry[0])
        );
        const filterKeywords = Array.from(url.searchParams.entries()).filter((entry) =>
          /keyword-\d/.test(entry[0])
        );
        const filterModes = Array.from(url.searchParams.entries()).filter((entry) =>
          /mode-\d/.test(entry[0])
        );

        const filters = filterFields.map((entry) => {
          let n = entry[0].slice(-1);
          const keyword = filterKeywords[n - 1][1];
          const mode = filterModes[n - 1][1];
          return [keyword, entry[1], mode];
        });

        const relevantDocuments = url.searchParams.get('rd');
        return {
          queryString: searchTerms,
          weights,
          filters,
          docs: await searchPackages(searchTerms, relevantDocuments, weights, filters)
        };
      }
    }
  ]);

  return <RouterProvider router={router} />;
}

export default App;
