import { Link } from "react-router-dom"
import "../App.css"


export default function Navbar() {
    return (
        <div className="navbar">
            <div className="nav-logo"><img src="Nav Logo.svg"/></div>
            <ul className="nav-btn-container">
                <li><Link to="/" className="nav-btn">Home</Link></li>
                <li><Link to="/about" className="nav-btn">About</Link></li>
            </ul>
        </div>
    )
}