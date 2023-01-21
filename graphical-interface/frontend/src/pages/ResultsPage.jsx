import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import { useLoaderData } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import SearchBar from '../components/SearchBar';
import SearchResultCard from '../components/SearchResultCard';
import ReplayIcon from '../assets/replay.png';
import Button from 'react-bootstrap/Button';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Modal from 'react-bootstrap/Modal';

export default function ResultsPage() {
  const searchResult = useLoaderData();
  const [relevantDocuments, setRelevantDocuments] = useState([]);
  const [selectedDocument, setSelectedDocument] = useState(null);
  const [showModal, setShowModal] = useState(false);

  const handleOpenModal = () => setShowModal(true);
  const handleCloseModal = () => setShowModal(false);

  const navigate = useNavigate();

  const doRelevancyQuery = () => {
    setRelevantDocuments([]);
    let query =
      '?q=' +
      searchResult.queryString +
      '&desc-weight=' +
      searchResult.weights.description +
      '&pack-weight=' +
      searchResult.weights.package +
      '&sec-weight=' +
      searchResult.weights.section +
      '&exact-matches=' +
      searchResult.weights.exactMatches +
      '&rd=' + relevantDocuments.join(',');

    for (let i = 0; i < searchResult.filters.length; i++) {
      query += `&field-${i + 1}=${searchResult.filters[i][1]}&mode-${i + 1}=${
        searchResult.filters[i][2]
      }&keyword-${i + 1}=${searchResult.filters[i][0]}`;
    }
    query = query.replace(/ /g, '+');

    navigate({
      pathname: '/search',
      search: query
    });
  };

  const relevantDocumentToggle = (id) => {
    if (relevantDocuments.includes(id)) {
      setRelevantDocuments(relevantDocuments.filter((docId) => docId !== id));
    } else {
      setRelevantDocuments([...relevantDocuments, id]);
    }
  };

  const seeMoreHandler = (document) => {
    setSelectedDocument(document);
    handleOpenModal();
  };

  return (
    <>
      <header>
        <Navbar />
      </header>
      <div id="search-result-body">
        <SearchBar
          onSubmit={() => setRelevantDocuments([])}
          query={searchResult.queryString}
          weights={searchResult.weights}
          filters={searchResult.filters}
          rd={relevantDocuments}
        />
        <div id="requery-container">
          <OverlayTrigger
            placement="left"
            delay={{ show: 150, hide: 400 }}
            overlay={<Tooltip id="button-tooltip">Redo query considering relevance</Tooltip>}>
            <Button id="requery-btn" className="btn-secondary" onClick={doRelevancyQuery}>
              <img className="fit-container" src={ReplayIcon} />
            </Button>
          </OverlayTrigger>
        </div>
        <div id="search-result-container">
          {searchResult.docs.map((doc) => (
            <SearchResultCard
              key={doc.id}
              id={doc.id}
              relevant={relevantDocuments.includes(doc.id)}
              relevantToggle={relevantDocumentToggle}
              document={doc}
              seeMoreCb={() => seeMoreHandler(doc)}
            />
          ))}
        </div>
        {selectedDocument && (
          <Modal show={showModal} onHide={handleCloseModal}>
            <Modal.Header closeButton>
              <Modal.Title>
                {selectedDocument.package} ({selectedDocument.version})
              </Modal.Title>
            </Modal.Header>
            <Modal.Body>
              <dl>
                {selectedDocument.origin && (
                  <div className="inline-def-container">
                    <dt>Origin</dt>
                    <dd>{selectedDocument.origin}</dd>
                  </div>
                )}
                {selectedDocument.origin && (
                  <div className="inline-def-container">
                    <dt>Section</dt>
                    <dd>{selectedDocument.section}</dd>
                  </div>
                )}
                {selectedDocument.depends && (
                  <div className="inline-def-container">
                    <dt>Depends</dt>
                    <dd>{selectedDocument.depends}</dd>
                  </div>
                )}
                {selectedDocument.suggests && (
                  <div className="inline-def-container">
                    <dt>Suggests</dt>
                    <dd>{selectedDocument.suggests}</dd>
                  </div>
                )}
                {selectedDocument.recommends && (
                  <div className="inline-def-container">
                    <dt>Recommends</dt>
                    <dd>{selectedDocument.recommends}</dd>
                  </div>
                )}
                {selectedDocument.breaks && (
                  <div className="inline-def-container">
                    <dt>Breaks</dt>
                    <dd>{selectedDocument.breaks}</dd>
                  </div>
                )}
                {selectedDocument.conflicts && (
                  <div className="inline-def-container">
                    <dt>Conflicts</dt>
                    <dd>{selectedDocument.conflicts}</dd>
                  </div>
                )}
                {selectedDocument.downloads != null && selectedDocument.downloads != undefined && (
                  <div className="inline-def-container">
                    <dt>Downloads</dt>
                    <dd>{selectedDocument.downloads}</dd>
                  </div>
                )}
                {selectedDocument.regularlyUsed != null &&
                  selectedDocument.regularlyUsed != undefined && (
                    <div className="inline-def-container">
                      <dt>Regularly used</dt>
                      <dd>{selectedDocument.regularlyUsed}</dd>
                    </div>
                  )}
                {selectedDocument.recentlyUpdated != null &&
                  selectedDocument.recentlyUpdated != undefined && (
                    <div className="inline-def-container">
                      <dt>Recently updated</dt>
                      <dd>{selectedDocument.recentlyUpdated}</dd>
                    </div>
                  )}
                {selectedDocument.description && (
                  <div>
                    <dt>Description</dt>
                    <dd className="text-justify">{selectedDocument.description}</dd>
                  </div>
                )}
              </dl>
            </Modal.Body>
          </Modal>
        )}
      </div>
    </>
  );
}
