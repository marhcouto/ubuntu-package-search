import axios from 'axios';

const filterDocuments = (filters, documents) => {
  if (filters.length === 0) return documents;
  const finalDocs = [];
  for (let [keyword, field, mode] of filters) {
    for (let document of documents) {
      if (mode == 'Contains' && document[field] && keyword in document[field].split(' '))
        finalDocs.push(document);
      else if (
        mode == 'Does Not Contain' &&
        document[field] &&
        !(keyword in document[field].split(' '))
      )
        finalDocs.push(document);
    }
  }
  return finalDocs;
};

const createBasisURL = (nRows) => {
  const realURL = new URL('http://localhost:8983/solr/pri_solr_final/select');
  realURL.searchParams.append('indent', 'true');
  realURL.searchParams.append('q.op', 'AND');
  realURL.searchParams.append('defType', 'edismax');
  realURL.searchParams.append('tv.tf', 'true');
  if (nRows) {
    realURL.searchParams.append('rows', nRows);
  } else {
    realURL.searchParams.append('rows', 40);
  }

  return realURL;
};

const parseQueryTerms = (field, parsedQueryStr) => {
  const queryTerms = new Map();

  let fieldStartIdx = parsedQueryStr.search(`${field}:`);
  while (fieldStartIdx !== -1) {
    parsedQueryStr = parsedQueryStr.slice(fieldStartIdx + field.length + 1, -1);
    const sepIdx = parsedQueryStr.search(/[\s\)]/);
    const term = parsedQueryStr.slice(0, sepIdx);
    if (queryTerms.has(term)) {
      queryTerms.set(term, queryTerms.get(term) + 1);
    } else {
      queryTerms.set(term, 1);
    }
    fieldStartIdx = parsedQueryStr.search(`${field}:`);
  }
  return queryTerms;
};

const parseDocumentsTerms = (termVector, validFieldsArr) => {
  const documents = new Map();
  for (let docIdx = 0; docIdx < termVector.length; docIdx += 2) {
    const documentData = termVector[docIdx + 1];
    const documentFields = new Map();
    for (let fieldIdx = 2; fieldIdx < documentData.length; fieldIdx += 2) {
      const fieldName = documentData[fieldIdx];
      if (validFieldsArr.includes(fieldName)) {
        const fieldTerms = new Map();
        for (let termIdx = 0; termIdx < documentData[fieldIdx + 1].length; termIdx += 2) {
          const term = documentData[fieldIdx + 1][termIdx];
          const termFrequency = documentData[fieldIdx + 1][termIdx + 1][1];
          fieldTerms.set(term, termFrequency);
        }
        documentFields.set(fieldName, fieldTerms);
      }
    }
    documents.set(termVector[docIdx], documentFields);
  }
  return documents;
};

const computeRocchio = (
  queryTerms,
  documentTerms,
  relevantDocuments,
  retrievedDocuments,
  field
) => {
  const relatedDocumentsWeight = 0.75 / relevantDocuments.length;
  const nonRelevantDocumentsWeight = 0.15 / (retrievedDocuments - relevantDocuments.length);
  const rocchioQuery = new Map(queryTerms.entries());
  for (const [docId, docFields] of documentTerms.entries()) {
    const docFieldTerms = docFields.get(field);
    for (const [term, termFrequency] of docFieldTerms.entries()) {
      if (relevantDocuments.includes(docId)) {
        if (rocchioQuery.has(term)) {
          rocchioQuery.set(term, rocchioQuery.get(term) + termFrequency * relatedDocumentsWeight);
        } else {
          rocchioQuery.set(term, termFrequency * relatedDocumentsWeight);
        }
      } else {
        if (rocchioQuery.has(term)) {
          rocchioQuery.set(term, rocchioQuery.get(term) - termFrequency * nonRelevantDocumentsWeight);
        } else {
          rocchioQuery.set(term, - termFrequency * nonRelevantDocumentsWeight);
        }
      }
    }
  }

  for(const [term, termFrequency] of rocchioQuery.entries()) {
    if(termFrequency < 0) {
      rocchioQuery.delete(term);
    }
  }
  return rocchioQuery;
};

const computeRocchioVector = (queryResponse, relevantDocuments) => {
  const queryTerms = parseQueryTerms('Description', queryResponse.debug.parsedquery);
  const documentTerms = parseDocumentsTerms(queryResponse.termVectors, ['Description']);
  return computeRocchio(
    queryTerms,
    documentTerms,
    relevantDocuments,
    queryResponse.response.numFound,
    'Description'
  );
};

export const fetchDocuments = async (query) => {
  const realURL = createBasisURL(query.rows);

  realURL.searchParams.append('q', query.q);

  let weights = JSON.parse(query.weights);
  let qfString = ':';

  if (weights.exactMatches === 'on') {
    weights = {
      ...weights,
      packageExact: Math.max(Math.min(Math.round(weights.package * 1.25), 6), 0),
      descriptionFull: Math.max(Math.min(Math.round(weights.description * 2.5), 5), 0)
    };
    qfString = `Package^${weights.package} PackageExact^${weights.packageExact} Description^${weights.description} Section^${weights.section} DescriptionFull^${weights.descriptionFull}`;
  } else {
    qfString = `Package^${weights.package} Description^${weights.description} Section^${weights.section}`;
  }

  realURL.searchParams.append('qf', qfString);
  realURL.searchParams.append('debugQuery', 'true');

  const response = await axios.get(realURL.href);
  const filteredDocuments = filterDocuments(JSON.parse(query.filters), response.data.response.docs);
  response.data.response.docs = filteredDocuments;
  return response.data;
};

export const fetchDocumentsWithRelevance = async (query) => {
  const relevantDocuments = query.rd.split(',');
  const originalResponse = await fetchDocuments(query);

  const realURL = createBasisURL(query.rows);
  const rocchioVector = computeRocchioVector(originalResponse, relevantDocuments);
  let weigthedTerms = [];
  for (const [term, weight] of rocchioVector.entries()) {
    weigthedTerms.push([term, weight]);
  }
  weigthedTerms.sort((a, b) => b[1] - a[1]);
  weigthedTerms = weigthedTerms.slice(0, 101);
  weigthedTerms = weigthedTerms.map((pair) => `(DescriptionNoParse:${pair[0]})^=${pair[1]}`);

  query.q = `(${query.q}) OR (${weigthedTerms.join(' OR ')})`;

  realURL.searchParams.append('q', query.q);
  realURL.searchParams.append('qf', 'Package^4 PackageExact^5 Section^2');

  const response = await axios.get(realURL.href);
  return response.data;
};
