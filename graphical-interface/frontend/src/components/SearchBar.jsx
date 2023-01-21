import InputGroup from 'react-bootstrap/InputGroup';
import { Form as RouterForm } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import RangeSlider from 'react-bootstrap-range-slider';
import React, { useState } from 'react';
import magnifyingGlass from '../assets/magnifying-glass.png';
import settings from '../assets/settings.png';

export default function SearchBar(props) {
  const [Description, setDescription] = useState(props.weights ? props.weights.description : 1);
  const [Package, setPackage] = useState(props.weights ? props.weights.package : 4);
  const [Section, setSection] = useState(props.weights ? props.weights.section : 2);
  const [options, setOptions] = useState(false);
  const [exactMatches, setExactMatches] = useState(
    props.weights ? props.weights.exactMatches : true
  );
  const [filters, setFilters] = useState(props.filters ? props.filters : []);

  const addFilter = (filters) => {
    if (filters.length < 5) {
      const newFilters = filters.concat([['', 'Depends', 'Does Not Contain']]);
      setFilters(newFilters);
    }
  };

  const removeFilter = (filters) => {
    if (filters.length > 0) setFilters(filters.slice(0, -1));
  };

  const drawFilters = (filters) => {
    let filterList = [];
    for (let i = 0; i < filters.length; i++) {
      filterList.push(
        <div className="row" style={{ margin: '0px 0px 10px 0px' }}>
          <div className="col">
            <Form.Select
              name={`field-${i + 1}`}
              defaultValue={filters[i][1]}
              title="Field to filter on">
              <option>Depends</option>
              <option>Breaks</option>
              <option>Suggests</option>
              <option>Recommends</option>
            </Form.Select>
          </div>
          <div className="col">
            <Form.Select name={`mode-${i + 1}`} defaultValue={filters[i][2]}>
              <option>Contains</option>
              <option>Does Not Contain</option>
            </Form.Select>
          </div>
          <div className="col">
            <Form.Control
              placeholder="keyword"
              name={`keyword-${i + 1}`}
              defaultValue={filters[i][0]}
              title="Exact word to filter by"
            />
          </div>
        </div>
      );
    }
    return filterList;
  };

  const fields = [
    { name: 'Description', id: 'desc-weight', value: Description, onChange: setDescription },
    { name: 'Package Name', id: 'pack-weight', value: Package, onChange: setPackage },
    { name: 'Section', id: 'sec-weight', value: Section, onChange: setSection }
  ];

  return (
    <RouterForm id="search-form" method="get" action="/search">
      <InputGroup>
        <InputGroup.Text
          id="search-icon"
          title="Advanced Options"
          onClick={() => {
            setOptions(!options);
          }}>
          <img className="fit-container" src={settings} />
        </InputGroup.Text>
        <Form.Control
          id="search-bar"
          name="q"
          placeholder="Search for some package..."
          aria-label="Search for some package..."
          defaultValue={props.query ? props.query : ''}
        />
        <Button
          id="search-button"
          type="submit"
          onClick={props.onSubmit ? props.onSubmit : () => {}}>
          Search
        </Button>
      </InputGroup>
      <div
        id="advanced-options"
        style={{ display: !options ? 'none' : 'flex', transition: 'display 10000ms' }}>
        <div className="sliders" title="Define the importance of each field for the search">
          {fields.map((i) => (
            <div
              className="slider-search"
              title="0 -> field not used; 1 -> normal weight; >1 -> more importance">
              <h3 style={{ textAlign: 'center' }}>{i.name}</h3>
              <RangeSlider
                name={i.id}
                value={i.value}
                onChange={(changeEvent) => i.onChange(changeEvent.target.value)}
                min={0}
                max={5}
                tooltipPlacement="top"
                variant="light"
              />
            </div>
          ))}
          <div
            title="Enhance exact matches on fields"
            className="slider-search"
            style={{ textAlign: 'center' }}>
            <h3>Exact Matches</h3>
            <Form.Check
              name="exact-matches"
              type="switch"
              id="exact-switch"
              defaultChecked={exactMatches}
              onClick={setExactMatches}
            />
          </div>
        </div>
        <div className="filters" title="Apply filters">
          <div className="row">
            <div className="col-md-3">
              <div className="row" style={{ margin: '0px 0px 10px 0px' }}>
                <Button
                  id="add-filter-button"
                  className="btn btn-primary btn-sm"
                  onClick={() => addFilter(filters)}>
                  Add Filter
                </Button>
              </div>
              <div className="row" style={{ margin: '0px 0px 10px 0px' }}>
                <Button
                  id="remove-filter-button"
                  className="btn btn-primary btn-sm"
                  onClick={() => removeFilter(filters)}>
                  Remove Filter
                </Button>
              </div>
            </div>
            <div className="col">{drawFilters(filters)}</div>
          </div>
        </div>
      </div>
    </RouterForm>
  );
}
