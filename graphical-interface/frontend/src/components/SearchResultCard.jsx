import React from 'react';
import Card from 'react-bootstrap/Card';
import OverlayTrigger from 'react-bootstrap/esm/OverlayTrigger';
import checkFull from '../assets/check-full.png';
import checkOutlined from '../assets/check-outline.png';
import Tooltip from 'react-bootstrap/Tooltip';
import Button from 'react-bootstrap/Button';


export default function SearchResultCard({ id, relevantToggle, document, relevant, seeMoreCb }) {  
  return (
    <Card className="result-card">
      <Card.Header>
        {document.package} ({document.version})
      </Card.Header>
      <Card.Body>
        <div className="search-result-card-body-container">
          <p className="search-result-card-description">{document.description}</p>
          <OverlayTrigger
            placement="right"
            delay={{ show: 50, hide: 200 }}
            overlay={<Tooltip>Mark as relevant</Tooltip>}
          >
            <button className="relevant-toggle" onClick={(_) => relevantToggle(id)}>
              {relevant ? <img src={checkFull} /> : <img src={checkOutlined} />}
            </button>
          </OverlayTrigger>
        </div>
        <Button className="btn-secondary search-result-card-see-more" onClick={seeMoreCb}>See More</Button>
      </Card.Body>
    </Card>
  );
}
