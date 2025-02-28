import * as React from 'react';
import { Link } from 'react-router-dom';

const NavBar = ({ user, handleSignout }) => {
  return (
    <>
      { user ? (
        <nav>
            <div><button onClick={handleSignout}>Sign Out</button></div>
        </nav>
      ) : (
        <nav>
          <div>
            <Link to="/signin">Sign In</Link>
            <Link to="/signup">Sign Up</Link>
          </div>
        </nav>
      )}
    </>
  )
}

export default NavBar;