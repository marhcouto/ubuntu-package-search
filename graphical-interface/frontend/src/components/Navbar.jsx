import logo from '../assets/logo.png';
import { Form as RouterForm, Link } from 'react-router-dom';
import { Button } from 'bootstrap';

export default function Navbar() {
  return (
    <>
      <Link to="/" className="text-decoration-none" title="Home Page">
        <div id="header-content" type="submit">
          <img id="logo" src={logo} />
          <h1>Ubuntu Package Search</h1>
        </div>
      </Link>
    </>
  );
}
