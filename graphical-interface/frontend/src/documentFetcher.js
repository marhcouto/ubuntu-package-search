export const searchPackages = async (queryTerms, relevantDocuments, weights, filters) => {
  const url = new URL('http://localhost:5000/select');
  url.searchParams.append('q', queryTerms);
  url.searchParams.append('weights', JSON.stringify(weights));
  url.searchParams.append('filters', JSON.stringify(filters));
  if (relevantDocuments) {
    url.searchParams.append('rd', relevantDocuments);
  }
  const response = await fetch(url);
  return await response.json();
};
