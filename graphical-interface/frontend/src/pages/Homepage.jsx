import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import SearchBar from '../components/SearchBar';

export default function Homepage() {
  return (
    <>
      <header>
        <Navbar />
      </header>
      <div id="main">
        <SearchBar />
      </div>
    </>
  );
}
