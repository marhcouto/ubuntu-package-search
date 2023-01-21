import express from 'express';
import bodyParser from 'body-parser';
import cors from 'cors';
import { parse } from 'csv-parse/sync';
import fs from 'fs';
import { fetchDocuments, fetchDocumentsWithRelevance } from './documentFetcher.mjs';

const queryResultToModel = (originalDocuments, documents) => {
  return documents.map((document) => {
    const originalDocument = originalDocuments.get(document.Package);
    return {
      id: document.id,
      package: originalDocument.Package,
      version: originalDocument.Version,
      section: originalDocument.Section,
      description: originalDocument.Description,
      depends: originalDocument.Depends,
      recommends: originalDocument.Recommends,
      suggests: originalDocument.Suggests,
      conflicts: originalDocument.Conflicts,
      replaces: originalDocument.Replaces,
      origin: originalDocument.Origin,
      downloads: document.Downloads,
      regularlyUsed: document.Regularly_Used,
      recentlyUpdated: document.Recently_Updated
    };
  });
};

const main = () => {
  const app = express();
  app.use(cors());
  app.use(bodyParser.json());

  const originalDocuments = new Map();
  const documentsFromCSV = parse(fs.readFileSync('../../pipeline/out/csv_data/clean/final.csv'), {
    columns: true,
    skip_empty_lines: true
  });
  for (const document of documentsFromCSV) {
    document.Description = document.Description.replace(/\\n/g, '\n');
    originalDocuments.set(document.Package, document);
  }

  app.get('/select', async (req, rep) => {
    console.log('Received Request. Request Query:\n', req.query);
    let documents;
    if (!req.query.rd) {
      documents = await fetchDocuments(req.query);
    } else {
      documents = await fetchDocumentsWithRelevance(req.query);
    }
    rep.status(200).json(queryResultToModel(originalDocuments, documents.response.docs)).end();
  });

  app.listen(5000, () => {
    console.log('Listening on port 5000');
  });
};

main();
