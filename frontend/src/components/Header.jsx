import React from 'react'
import { Link } from 'react-router-dom'

export default function Header() {
  return (
    <div  style={{
        backgroundColor: 'black',
        color: 'white',
        padding: '10px',
        textAlign: 'center'
    }}>
      <Link to="/" style={{color: 'white', marginRight: '10px'}}>Home</Link>
      <Link to="/about" style={{color: 'white', marginRight: '10px'}}>About</Link>
      <Link to="/contact" style={{color: 'white', marginRight: '10px'}}>Contact</Link>
      <Link to="/colleges" style={{color: 'white', marginRight: '10px'}}>Colleges</Link>
      <Link to="/issue" style={{color: 'white', marginRight: '10px'}}>Issue</Link>
    </div>
  )
}
